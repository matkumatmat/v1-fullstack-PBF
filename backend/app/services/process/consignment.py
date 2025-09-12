# file: app/services/consignment_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from sqlalchemy.orm import selectinload, joinedload

from app.models.product import Allocation
from app.models.process import ConsignmentAgreement, Consignment, ConsignmentItem
from app.schemas.process.consignment import ConsignmentReallocationPayload
from app.core.exceptions import NotFoundException, UnprocessableEntityException, BadRequestException

async def reallocate_stock_for_consignment(db: AsyncSession, payload: ConsignmentReallocationPayload) -> Consignment:
    """
    Mengorkestrasi proses re-alokasi stok dari reguler ke konsinyasi.
    """
    agreement = await db.get(ConsignmentAgreement, payload.consignment_agreement_id)
    if not agreement:
        raise NotFoundException(f"Consignment Agreement with id {payload.consignment_agreement_id} not found.")

    # --- Langkah 1: Buat master Consignment ---
    new_consignment = Consignment(
        consignment_number=payload.consignment_number,
        agreement_id=agreement.id,
        consignment_date=date.today(),
        status='PENDING' # Status awal sebelum dikirim
    )
    db.add(new_consignment)
    await db.flush()

    # --- Langkah 2: Proses setiap item dalam payload ---
    for item_payload in payload.items:
        source_allocation = await db.get(Allocation, item_payload.source_allocation_id, options=[selectinload(Allocation.batch)])
        if not source_allocation:
            raise NotFoundException(f"Source Allocation with id {item_payload.source_allocation_id} not found.")

        # Validasi (mirip dengan tender)
        if source_allocation.allocation_type_id != 1: # REGULAR_STOCK
            raise BadRequestException(f"Allocation {source_allocation.id} is not REGULAR_STOCK.")
        
        available_quantity = source_allocation.allocated_quantity - source_allocation.reserved_quantity - source_allocation.shipped_quantity
        if item_payload.quantity > available_quantity:
            raise UnprocessableEntityException(f"Requested quantity for batch {source_allocation.batch.lot_number} exceeds available quantity.")

        # --- Langkah 3: Lakukan Re-alokasi per item ---
        
        # 3a. Kurangi alokasi sumber
        source_allocation.allocated_quantity -= item_payload.quantity
        db.add(source_allocation)

        # 3b. Buat alokasi baru untuk konsinyasi
        # Asumsikan ID 5 = CONSIGNMENT_STOCK
        consignment_alloc = Allocation(
            batch_id=source_allocation.batch_id,
            allocation_type_id=5,
            allocated_quantity=item_payload.quantity,
            allocation_date=date.today(),
            status='RESERVED', # Dicadangkan untuk pengiriman konsinyasi
            customer_id=agreement.customer_id
        )
        db.add(consignment_alloc)
        await db.flush() # Dapatkan ID untuk consignment_alloc

        # 3c. Buat ConsignmentItem
        consignment_item = ConsignmentItem(
            consignment_id=new_consignment.id,
            product_id=source_allocation.batch.product_id,
            batch_id=source_allocation.batch_id,
            quantity_shipped=item_payload.quantity, # Awalnya shipped = requested
            selling_price=item_payload.selling_price,
            status='PENDING_SHIPMENT'
        )
        db.add(consignment_item)
        
        # ### KUNCI LOGIKA ###
        # Tautkan Consignment utama ke alokasi konsinyasi yang baru dibuat
        # Ini bisa dilakukan dengan menambahkan relasi di model Consignment
        new_consignment.allocation_id = consignment_alloc.id # Jika relasi 1-to-1
        # Jika 1-to-many, Anda perlu append ke list.

    await db.flush()
    await db.refresh(new_consignment, ["items.product", "items.batch"])
    return new_consignment
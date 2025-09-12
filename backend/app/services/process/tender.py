# file: app/services/tender_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.models import Allocation, TenderContract, ContractReservation, AllocationStatusEnum
from app.schemas.process.tender import TenderReallocationPayload
from app.schemas.product import AllocationCreate
from app.core.exceptions import NotFoundException, UnprocessableEntityException, BadRequestException
from ..product_service import create_allocation as create_allocation
async def reallocate_stock_for_tender(db: AsyncSession, payload: TenderReallocationPayload) -> Allocation:
    """
    Mengorkestrasi proses re-alokasi stok dari reguler ke tender.
    Ini adalah satu unit kerja transaksional.

    """
    tender_contract = await db.get(TenderContract, payload.tender_contract_id)
    if not tender_contract:
        raise NotFoundException(...)

    # --- Langkah 1: Ambil dan Validasi Entitas Sumber ---
    source_allocation = await db.get(Allocation, payload.source_allocation_id)
    if not source_allocation:
        raise NotFoundException(f"Source Allocation with id {payload.source_allocation_id} not found.")

    tender_contract = await db.get(TenderContract, payload.tender_contract_id)
    if not tender_contract:
        raise NotFoundException(f"Tender Contract with id {payload.tender_contract_id} not found.")

    # --- Langkah 2: Validasi Bisnis ---
    # Asumsikan ID 1 = REGULAR_STOCK, ID 2 = TENDER_STOCK
    if source_allocation.allocation_type_id != 1:
        raise BadRequestException("Source allocation must be of type REGULAR_STOCK.")
    
    available_quantity = source_allocation.allocated_quantity - source_allocation.reserved_quantity - source_allocation.shipped_quantity
    if payload.quantity > available_quantity:
        raise UnprocessableEntityException(f"Requested quantity ({payload.quantity}) exceeds available quantity ({available_quantity}) in source allocation.")

    # --- Langkah 3: Lakukan Re-alokasi (dalam satu transaksi) ---
    
    # 3a. Kurangi kuantitas dari alokasi sumber
    source_allocation.allocated_quantity -= payload.quantity
    db.add(source_allocation)

    # 3b. Buat alokasi baru untuk tender
    tender_allocation_schema = AllocationCreate(
        batch_id=source_allocation.batch_id,
        allocation_type_id=2, # TENDER_STOCK
        allocated_quantity=payload.quantity,
        allocation_date=date.today(),
        status=AllocationStatusEnum.RESERVED, # Status khusus untuk stok yang sudah terikat kontrak
        customer_id=source_allocation.customer_id # Bisa di-override jika perlu
    )
    tender_allocation = await create_allocation(db, allocation_in=tender_allocation_schema)
    await db.flush()

    # 3c. Buat catatan reservasi kontrak
    reservation = ContractReservation(
        contract_id=tender_contract.id,          # Menunjuk ke master kontrak
        product_id=source_allocation.batch.product_id, # Info produk
        batch_id=source_allocation.batch_id,         # Info batch
        allocation_id=tender_allocation.id,      # Menunjuk ke Allocation TENDER yang baru
        reserved_quantity=payload.quantity,      # Jumlah yang dicadangkan
        remaining_quantity=payload.quantity      # Awalnya, sisa = yang dicadangkan
    )
    db.add(reservation) # Simpan bukti transaksi ini
    await db.flush()
    
    await db.refresh(tender_allocation)
    return tender_allocation
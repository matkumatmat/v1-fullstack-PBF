
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product, Batch, Allocation, StockPlacement, AllocationStatusEnum
from app.schemas.process.inbound import InboundPayload
from app.schemas.product import BatchCreate, AllocationCreate
from app.schemas.warehouse import StockPlacementCreate

from app.services import product_service, warehouse_service
from app.core.exceptions import NotFoundException, UnprocessableEntityException

async def process_full_inbound(db: AsyncSession, payload: InboundPayload) -> StockPlacement:
    """
    Mengorkestrasi seluruh proses inbound, membuat alokasi dengan status QUARANTINE.
    """
    if payload.product_id:
        product = await db.get(Product, payload.product_id)
        if not product:
            raise NotFoundException(f"Product with id {payload.product_id} not found.")
        product_id_to_use = product.id
    else:
        new_product = await product_service.create_product(db, product_in=payload.new_product_data)
        await db.flush()
        product_id_to_use = new_product.id

    # --- Langkah 2: Buat Batch ---
    batch_data_dict = payload.batch_data.model_dump()
    batch_create_schema = BatchCreate(**batch_data_dict, product_id=product_id_to_use)
    new_batch = await product_service.create_batch(db, batch_in=batch_create_schema)
    await db.flush()

    # --- Langkah 3: Buat Alokasi (dengan status Karantina) ---
    allocation_data_dict = payload.allocation_data.model_dump()
    
    ### KUNCI LOGIKA BARU ###
    # 1. Atur status default ke QUARANTINE.
    # 2. Asumsikan allocation_type_id untuk REGULAR_STOCK adalah 1 (bisa diambil dari payload jika UI mengizinkan).
    allocation_create_schema = AllocationCreate(
        **allocation_data_dict,
        batch_id=new_batch.id,
        status=AllocationStatusEnum.QUARANTINE,
        allocation_type_id=1 # Default ke REGULAR_STOCK
    )
    
    if allocation_create_schema.allocated_quantity > new_batch.received_quantity:
        raise UnprocessableEntityException("Allocation quantity cannot exceed batch received quantity.")
    
    new_allocation = await product_service.create_allocation(db, allocation_in=allocation_create_schema)
    await db.flush()

    # --- Langkah 4: Tempatkan Stok di Rak ---
    if payload.placement_quantity > new_allocation.allocated_quantity:
        raise UnprocessableEntityException("Placement quantity cannot exceed allocated quantity.")
        
    placement_schema = StockPlacementCreate(
        rack_id=payload.rack_id,
        allocation_id=new_allocation.id,
        quantity=payload.placement_quantity
    )
    final_placement = await warehouse_service.place_stock_in_rack(db, placement_in=placement_schema)
    
    # --- Finalisasi: Muat relasi untuk respons ---
    # (Logika refresh tetap sama)
    await db.refresh(final_placement, ["rack", "allocation.batch.product"])
    
    return final_placement
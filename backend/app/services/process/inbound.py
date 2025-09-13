# file: app/services/process/inbound.py (FINAL & COMPLETE)

from typing import List
from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Impor model yang relevan
from app.models import (
    Product, Batch, Allocation, StockPlacement, Rack, AllocationType,
    ProductType, PackageType, TemperatureType, AllocationStatusEnum
)
# Impor skema yang relevan
from app.schemas.process.inbound import InboundPayload, InboundFormData
# Impor exception kustom
from app.core.exceptions import NotFoundException, UnprocessableEntityException, BadRequestException

# --- Service untuk Persiapan Form ---

async def get_inbound_form_data(db: AsyncSession) -> InboundFormData:
    """Mengambil semua data lookup yang dibutuhkan untuk form inbound."""
    async with db.begin_nested():
        allocation_types = (await db.execute(select(AllocationType))).scalars().all()
        product_types = (await db.execute(select(ProductType))).scalars().all()
        package_types = (await db.execute(select(PackageType))).scalars().all()
        temperature_types = (await db.execute(select(TemperatureType))).scalars().all()
    
    return InboundFormData(
        allocation_types=allocation_types,
        product_types=product_types,
        package_types=package_types,
        temperature_types=temperature_types
    )

async def search_products_for_inbound(db: AsyncSession, query: str) -> List[Product]:
    """Mencari produk berdasarkan kode atau nama."""
    search_term = f"%{query.lower()}%"
    stmt = (
        select(Product)
        .where(or_(
            Product.product_code.ilike(search_term),
            Product.name.ilike(search_term)
        ))
        .limit(20)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def search_racks_for_inbound(db: AsyncSession, query: str) -> List[Rack]:
    """Mencari rak yang tersedia berdasarkan kode rak atau kode warehouse."""
    search_term = f"%{query.lower()}%"
    stmt = (
        select(Rack)
        .join(Rack.warehouse)
        .where(or_(
            Rack.code.ilike(search_term),
            Rack.warehouse.has(code=query.upper())
        ))
        .filter(Rack.placement == None) # Hanya rak yang kosong
        .options(selectinload(Rack.warehouse))
        .limit(20)
    )
    result = await db.execute(stmt)
    return result.unique().scalars().all()

# --- Service untuk Proses Utama ---

async def process_full_inbound(db: AsyncSession, payload: InboundPayload) -> StockPlacement:
    """
    Mengeksekusi seluruh proses inbound dalam SATU transaksi atomik.
    """
    async with db.begin_nested(): # Memulai satu transaksi untuk seluruh proses
        # 1. Dapatkan atau Buat Produk
        product = None
        if payload.existing_product_id:
            product = await db.get(Product, payload.existing_product_id)
            if not product:
                raise NotFoundException(f"Product with id {payload.existing_product_id} not found.")
        elif payload.new_product_data:
            product = Product(**payload.new_product_data.model_dump())
            db.add(product)
            await db.flush()
        
        # 2. Validasi Rak dan Tipe Alokasi
        rack = await db.get(Rack, payload.placement_data.rack_id)
        if not rack:
            raise NotFoundException(f"Rack with id {payload.placement_data.rack_id} not found.")
        if rack.placement:
            raise BadRequestException(f"Rack {rack.code} is already occupied.")
        
        alloc_type = await db.get(AllocationType, payload.allocation_type_id)
        if not alloc_type:
            raise NotFoundException(f"AllocationType with id {payload.allocation_type_id} not found.")

        # 3. Buat Batch
        db_batch = Batch(**payload.batch_data.model_dump(), product_id=product.id)
        
        # 4. Buat Alokasi dengan Status Karantina
        db_allocation = Allocation(
            batch=db_batch,
            allocation_type=alloc_type,
            allocated_quantity=db_batch.received_quantity,
            status=AllocationStatusEnum.QUARANTINE,
            allocation_date=db_batch.receipt_date
        )
        
        # 5. Buat Penempatan Stok
        if payload.placement_data.quantity > db_allocation.allocated_quantity:
            raise UnprocessableEntityException("Placement quantity cannot exceed received quantity.")
            
        db_placement = StockPlacement(
            rack=rack,
            allocation=db_allocation,
            quantity=payload.placement_data.quantity
        )
        
        db.add_all([db_batch, db_allocation, db_placement])
        await db.flush()

        # 6. Muat Ulang dengan Eager Loading untuk Respons yang Lengkap
        # Ini adalah cara yang BENAR untuk memuat relasi yang dalam sebelum sesi ditutup.
        result = await db.get(
            StockPlacement, 
            db_placement.id, 
            options=[
                selectinload(StockPlacement.rack).selectinload(Rack.warehouse),
                selectinload(StockPlacement.allocation).selectinload(Allocation.batch).selectinload(Batch.product),
                selectinload(StockPlacement.allocation).selectinload(Allocation.allocation_type),
                selectinload(StockPlacement.allocation).selectinload(Allocation.customer)
            ]
        )
        if not result:
            raise UnprocessableEntityException("Failed to retrieve placement after creation.")
            
        return result
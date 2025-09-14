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
        .filter(Rack.placement.is_(None)) # Hanya rak yang kosong
        .options(selectinload(Rack.warehouse))
        .limit(20)
    )
    result = await db.execute(stmt)
    return result.unique().scalars().all()

# --- Service untuk Proses Utama ---

# file: app/services/process/inbound.py (SERVICE YANG DISESUAIKAN)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
import uuid

from app.models import (
    Product, Batch, Allocation, StockPlacement, Rack, AllocationType,
    AllocationStatusEnum
)
from app.schemas.process.inbound import InboundPayload, InboundResponse
from app.core.exceptions import NotFoundException, UnprocessableEntityException

async def process_full_inbound(db: AsyncSession, payload: InboundPayload) -> InboundResponse:
    """
    Mengeksekusi seluruh proses inbound dalam satu transaksi atomik,
    menggunakan skema yang disederhanakan.
    """
    async with db.begin_nested():
        # --- 1. Dapatkan atau Buat Produk ---
        product = None
        if payload.existing_product_public_id:
            product_query = select(Product).where(Product.public_id == payload.existing_product_public_id)
            product = (await db.execute(product_query)).scalar_one_or_none()
            if not product:
                raise NotFoundException(f"Product with public_id {payload.existing_product_public_id} not found.")
        elif payload.new_product_data:
            product = Product(**payload.new_product_data.model_dump())
            db.add(product)
            await db.flush()
        
        # --- 2. Validasi Rak dan Tipe Alokasi ---
        rack_query = select(Rack).where(Rack.public_id == payload.rack_public_id)
        rack = (await db.execute(rack_query)).scalar_one_or_none()
        if not rack:
            raise NotFoundException(f"Rack with public_id {payload.rack_public_id} not found.")
        
        alloc_type_query = select(AllocationType).where(AllocationType.public_id == payload.allocation_type_public_id)
        alloc_type = (await db.execute(alloc_type_query)).scalar_one_or_none()
        if not alloc_type:
            raise NotFoundException(f"AllocationType with public_id {payload.allocation_type_public_id} not found.")

        # --- 3. Buat Batch dari data payload yang datar ---
        db_batch = Batch(
            product_id=product.id,
            lot_number=payload.lot_number,
            expiry_date=payload.expiry_date,
            NIE=payload.NIE,
            received_quantity=payload.received_quantity,
            receipt_document=payload.receipt_document,
            receipt_date=payload.receipt_date,
            length=payload.length,
            width=payload.width,
            height=payload.height,
            weight=payload.weight
        )
        
        # --- 4. Buat Alokasi ---
        db_allocation = Allocation(
            batch=db_batch,
            allocation_type_id=alloc_type.id,
            allocated_quantity=db_batch.received_quantity,
            status=AllocationStatusEnum.QUARANTINE,
            allocation_date=db_batch.receipt_date
        )
            
        # --- 5. Buat Penempatan Stok ---
        db_placement = StockPlacement(
            rack_id=rack.id,
            allocation=db_allocation,
            quantity=payload.placement_quantity
        )
        
        db.add_all([db_batch, db_allocation, db_placement])
        await db.flush() # Kirim ke DB untuk mendapatkan ID dan public_id

        # --- 6. Bangun Respons Ringkas Secara Manual ---
        return InboundResponse(
            product_public_id=product.public_id,
            batch_public_id=db_batch.public_id,
            allocation_public_id=db_allocation.public_id,
            stock_placement_public_id=db_placement.public_id
        )
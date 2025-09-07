# file: app/services/product_service.py

from typing import List, Optional
from sqlalchemy import exc, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Impor model yang relevan untuk service ini
from app.models.product import Product, Batch, Allocation

# Impor skema yang dibutuhkan oleh fungsi-fungsi di file ini
from app.schemas.product.product import ProductCreate, ProductUpdate
from app.schemas.product.batch import BatchCreate, BatchUpdate
from app.schemas.product.allocation import AllocationCreate, AllocationUpdate

# Impor exception kustom untuk penanganan error yang bersih dan eksplisit
from app.core.exceptions import NotFoundException, BadRequestException, UnprocessableEntityException

# --- Product Services ---

async def get_product_by_id(db: AsyncSession, product_id: int) -> Optional[Product]:
    """
    Mengambil satu produk berdasarkan ID internalnya.

    Secara proaktif memuat (eager load) relasi-relasi umum untuk mencegah
    query N+1 di layer router atau response. Ini adalah praktik optimasi performa.
    """
    query = (
        select(Product)
        .where(Product.id == product_id)
        .options(
            selectinload(Product.product_type),
            selectinload(Product.package_type),
            selectinload(Product.temperature_type),
            selectinload(Product.batches)
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_products(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Product]:
    """
    Mengambil daftar semua produk dengan paginasi.
    """
    query = select(Product).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:
    """
    Membuat entitas produk baru di database.
    """
    # TODO: Validasi proaktif untuk foreign keys (product_type_id, dll.) dapat ditambahkan di sini
    # untuk memberikan pesan error yang lebih spesifik sebelum mencoba commit.
    
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    try:
        await db.commit()
    except exc.IntegrityError as e:
        await db.rollback()
        # Menganalisis constraint violation untuk memberikan feedback yang lebih baik ke klien.
        if "uq_products_product_code" in str(e.orig):
            raise BadRequestException(f"Product with code '{product_in.product_code}' already exists.")
        if "fk_products" in str(e.orig):
             raise BadRequestException("One of the provided type IDs (product, package, temperature) is invalid.")
        # Fallback untuk error integritas lainnya.
        raise BadRequestException("Failed to create product due to a data conflict.")

    await db.refresh(db_product)
    return db_product

async def update_product(db: AsyncSession, product_id: int, product_in: ProductUpdate) -> Product:
    """
    Memperbarui data produk yang sudah ada.
    """
    db_product = await get_product_by_id(db, product_id)
    if not db_product:
        raise NotFoundException(f"Product with id {product_id} not found.")
    
    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
        
    db.add(db_product)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException("Update failed. A product with the provided code may already exist.")
        
    await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, product_id: int) -> Product:
    """
    Menghapus produk dari database.
    """
    db_product = await get_product_by_id(db, product_id)
    if not db_product:
        raise NotFoundException(f"Product with id {product_id} not found.")
    
    # Validasi aturan bisnis: Mencegah penghapusan produk yang sudah memiliki data transaksional (batch).
    if db_product.batches:
        raise BadRequestException(f"Cannot delete product '{db_product.name}'. It has associated batches and historical data.")
        
    await db.delete(db_product)
    await db.commit()
    return db_product

# --- Batch Services ---

async def get_batch_by_id(db: AsyncSession, batch_id: int) -> Optional[Batch]:
    """
    Mengambil satu batch berdasarkan ID, dengan eager loading untuk relasi penting.
    """
    query = (
        select(Batch)
        .where(Batch.id == batch_id)
        .options(
            selectinload(Batch.product),
            selectinload(Batch.allocations)
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_batches(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Batch]:
    """
    Mengambil daftar semua batch dengan paginasi.
    """
    query = select(Batch).offset(skip).limit(limit).options(selectinload(Batch.product))
    result = await db.execute(query)
    return result.scalars().all()

async def create_batch(db: AsyncSession, batch_in: BatchCreate) -> Batch:
    """
    Mencatat penerimaan batch baru untuk sebuah produk yang sudah ada.
    """
    # Validasi aturan bisnis: Pastikan produk induknya ada sebelum membuat batch.
    product = await get_product_by_id(db, batch_in.product_id)
    if not product:
        raise NotFoundException(f"Cannot create batch. Product with id {batch_in.product_id} not found.")

    db_batch = Batch(**batch_in.model_dump())
    db.add(db_batch)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException(f"Failed to create batch. A unique constraint might have been violated (e.g., duplicate lot number for this product).")
        
    await db.refresh(db_batch)
    return db_batch

async def update_batch(db: AsyncSession, batch_id: int, batch_in: BatchUpdate) -> Batch:
    """
    Memperbarui data batch yang ada.
    """
    db_batch = await get_batch_by_id(db, batch_id)
    if not db_batch:
        raise NotFoundException(f"Batch with id {batch_id} not found.")
        
    update_data = batch_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_batch, key, value)
        
    db.add(db_batch)
    await db.commit()
    await db.refresh(db_batch)
    return db_batch

async def delete_batch(db: AsyncSession, batch_id: int) -> Batch:
    """
    Menghapus batch.
    """
    db_batch = await get_batch_by_id(db, batch_id)
    if not db_batch:
        raise NotFoundException(f"Batch with id {batch_id} not found.")
        
    # Validasi aturan bisnis: Mencegah penghapusan batch yang sudah dialokasikan.
    if db_batch.allocations:
        raise BadRequestException(f"Cannot delete batch with lot number '{db_batch.lot_number}'. It has associated allocations.")
        
    await db.delete(db_batch)
    await db.commit()
    return db_batch

# --- Allocation Services ---

async def get_allocation_by_id(db: AsyncSession, allocation_id: int) -> Optional[Allocation]:
    """
    Mengambil satu alokasi berdasarkan ID, dengan eager loading.
    """
    query = (
        select(Allocation)
        .where(Allocation.id == allocation_id)
        .options(
            selectinload(Allocation.allocation_type),
            selectinload(Allocation.placements) # Penting untuk kalkulasi stok
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_allocation(db: AsyncSession, allocation_in: AllocationCreate) -> Allocation:
    """
    Membuat alokasi baru dari sebuah batch yang ada.
    Fungsi ini kritis dan harus dijalankan dalam transaksi yang aman.
    """
    async with db.begin_nested():
        # Mengunci baris batch untuk mencegah race condition saat beberapa proses
        # mencoba membuat alokasi dari batch yang sama secara bersamaan.
        batch_query = select(Batch).where(Batch.id == allocation_in.batch_id).options(selectinload(Batch.allocations)).with_for_update()
        batch = (await db.execute(batch_query)).scalar_one_or_none()

        if not batch:
            raise NotFoundException(f"Batch with id {allocation_in.batch_id} not found.")

        # Validasi aturan bisnis: Memastikan kuantitas yang dialokasikan tidak melebihi stok yang tersedia di batch.
        total_already_allocated = sum(alloc.allocated_quantity for alloc in batch.allocations)
        available_for_allocation = batch.received_quantity - total_already_allocated

        if allocation_in.allocated_quantity > available_for_allocation:
            raise UnprocessableEntityException(
                f"Cannot allocate {allocation_in.allocated_quantity} units. "
                f"Only {available_for_allocation} units are available from batch {batch.lot_number}."
            )
        
        # TODO: Validasi bahwa allocation_type_id ada.

        db_allocation = Allocation(**allocation_in.model_dump())
        db.add(db_allocation)
        
        await db.flush()
        await db.refresh(db_allocation)
        
    return db_allocation

async def update_allocation(db: AsyncSession, allocation_id: int, allocation_in: AllocationUpdate) -> Allocation:
    """
    Memperbarui alokasi yang ada, dengan validasi yang cermat.
    """
    async with db.begin_nested():
        db_allocation = await get_allocation_by_id(db, allocation_id)
        if not db_allocation:
            raise NotFoundException(f"Allocation with id {allocation_id} not found.")
        
        update_data = allocation_in.model_dump(exclude_unset=True)
        
        # Validasi aturan bisnis: Mencegah update yang akan merusak integritas data.
        if "allocated_quantity" in update_data:
            new_quantity = update_data["allocated_quantity"]
            total_placed = sum(p.quantity for p in db_allocation.placements)
            
            if new_quantity < db_allocation.shipped_quantity:
                raise BadRequestException(f"Cannot set allocated quantity to {new_quantity}. {db_allocation.shipped_quantity} units have already been shipped.")
            if new_quantity < total_placed:
                raise BadRequestException(f"Cannot set allocated quantity to {new_quantity}. {total_placed} units have already been placed in racks.")

        for key, value in update_data.items():
            setattr(db_allocation, key, value)
            
        db.add(db_allocation)
        await db.flush()
        await db.refresh(db_allocation)
        
    return db_allocation

async def delete_allocation(db: AsyncSession, allocation_id: int) -> Allocation:
    """
    Menghapus alokasi.
    """
    db_allocation = await get_allocation_by_id(db, allocation_id)
    if not db_allocation:
        raise NotFoundException(f"Allocation with id {allocation_id} not found.")
        
    # Validasi aturan bisnis: Mencegah penghapusan alokasi yang sudah memiliki data transaksional.
    if db_allocation.placements:
        raise BadRequestException(f"Cannot delete allocation. It has stock placed in racks.")
    if db_allocation.shipped_quantity > 0:
        raise BadRequestException(f"Cannot delete allocation. It has items that have already been shipped.")
        
    await db.delete(db_allocation)
    await db.commit()
    return db_allocation
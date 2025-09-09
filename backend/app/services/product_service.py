# file: app/services/product_service.py (FINAL REFACTORED CODE v2 - FULL VERSION)

from typing import List, Optional
from sqlalchemy import exc
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

# ===================================================================
# 1. PRODUCT SERVICES
# ===================================================================

async def get_product_by_id(db: AsyncSession, product_id: int) -> Optional[Product]:
    """
    Mengambil satu produk berdasarkan ID dengan SEMUA relasi yang dibutuhkan
    oleh skema `schemas.Product` sudah di-eager load.
    """
    query = (
        select(Product)
        .where(Product.id == product_id)
        .options(
            selectinload(Product.product_type),
            selectinload(Product.package_type),
            selectinload(Product.temperature_type),
            selectinload(Product.prices),
            selectinload(Product.batches),
            selectinload(Product.sales_order_items)
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_products(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Product]:
    """
    Mengambil daftar semua produk dengan paginasi.
    ✅ DIPERBAIKI: Relasi sekarang di-eager load untuk mencegah error serialisasi.
    """
    query = (
        select(Product)
        .order_by(Product.id)
        .offset(skip)
        .limit(limit)
        .options(
            # Muat semua relasi yang sama seperti di get_product_by_id
            # agar konsisten dengan skema respons List[schemas.Product].
            selectinload(Product.product_type),
            selectinload(Product.package_type),
            selectinload(Product.temperature_type),
            selectinload(Product.prices),
            selectinload(Product.batches),
            selectinload(Product.sales_order_items)
        )
    )
    result = await db.execute(query)
    return result.scalars().all()

async def create_product(db: AsyncSession, product_in: ProductCreate) -> Product:
    """
    Membuat entitas produk baru dan mengembalikannya dengan semua relasi yang
    dibutuhkan oleh skema respons sudah di-load.
    """
    db_product = Product(**product_in.model_dump())
    db.add(db_product)
    try:
        await db.flush()
    except exc.IntegrityError as e:
        await db.rollback()
        if "uq_products_product_code" in str(e.orig):
            raise BadRequestException(f"Product with code '{product_in.product_code}' already exists.")
        if "fk_products" in str(e.orig):
             raise BadRequestException("One of the provided type IDs (product, package, temperature) is invalid.")
        raise BadRequestException("Failed to create product due to a data conflict.")

    complete_product = await get_product_by_id(db, db_product.id)
    if not complete_product:
        raise UnprocessableEntityException("Failed to retrieve product immediately after creation.")
        
    return complete_product

async def update_product(db: AsyncSession, product_id: int, product_in: ProductUpdate) -> Product:
    """
    Memperbarui data produk dan mengembalikannya dengan relasi yang sudah di-load.
    """
    db_product = await db.get(Product, product_id)
    if not db_product:
        raise NotFoundException(f"Product with id {product_id} not found.")
    
    update_data = product_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
        
    db.add(db_product)
    try:
        await db.flush()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException("Update failed. A product with the provided code may already exist.")
        
    return await get_product_by_id(db, product_id)

async def delete_product(db: AsyncSession, product_id: int) -> Product:
    """
    Menghapus produk dari database.
    """
    db_product = await get_product_by_id(db, product_id)
    if not db_product:
        raise NotFoundException(f"Product with id {product_id} not found.")
    
    if db_product.batches:
        raise BadRequestException(f"Cannot delete product '{db_product.name}'. It has associated batches.")
        
    await db.delete(db_product)
    return db_product

# ===================================================================
# 2. BATCH SERVICES (Lengkap dan sudah diperbaiki)
# ===================================================================

async def get_batch_by_id(db: AsyncSession, batch_id: int) -> Optional[Batch]:
    """
    Mengambil satu batch berdasarkan ID, dengan relasi yang aman untuk API.
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
    query = (
        select(Batch)
        .order_by(Batch.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Batch.product))
    )
    result = await db.execute(query)
    return result.scalars().all()

async def create_batch(db: AsyncSession, batch_in: BatchCreate) -> Batch:
    """
    Mencatat penerimaan batch baru dan mengembalikannya dengan relasi di-load.
    """
    product = await db.get(Product, batch_in.product_id)
    if not product:
        raise NotFoundException(f"Cannot create batch. Product with id {batch_in.product_id} not found.")

    db_batch = Batch(**batch_in.model_dump())
    db.add(db_batch)
    try:
        await db.flush()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException(f"Failed to create batch. A unique constraint might have been violated.")
        
    return await get_batch_by_id(db, db_batch.id)

async def update_batch(db: AsyncSession, batch_id: int, batch_in: BatchUpdate) -> Batch:
    """
    Memperbarui data batch yang ada dan mengembalikannya dengan relasi di-load.
    """
    db_batch = await db.get(Batch, batch_id)
    if not db_batch:
        raise NotFoundException(f"Batch with id {batch_id} not found.")
        
    update_data = batch_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_batch, key, value)
        
    db.add(db_batch)
    await db.flush()
    return await get_batch_by_id(db, batch_id)

async def delete_batch(db: AsyncSession, batch_id: int) -> Batch:
    """
    Menghapus batch. Menerapkan validasi bisnis sebelum menghapus.
    """
    db_batch = await get_batch_by_id(db, batch_id)
    if not db_batch:
        raise NotFoundException(f"Batch with id {batch_id} not found.")
        
    if db_batch.allocations:
        raise BadRequestException(f"Cannot delete batch with lot number '{db_batch.lot_number}'. It has associated allocations.")
        
    await db.delete(db_batch)
    return db_batch

# ===================================================================
# 3. ALLOCATION SERVICES (Lengkap dan sudah diperbaiki)
# ===================================================================

async def get_allocation_by_id(db: AsyncSession, allocation_id: int) -> Optional[Allocation]:
    """
    Mengambil satu alokasi berdasarkan ID, dengan relasi yang aman untuk API.
    """
    query = (
        select(Allocation)
        .where(Allocation.id == allocation_id)
        .options(
            selectinload(Allocation.allocation_type),
            selectinload(Allocation.batch).selectinload(Batch.product),
            selectinload(Allocation.placements),
            selectinload(Allocation.customer)
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_allocation(db: AsyncSession, allocation_in: AllocationCreate) -> Allocation:
    """
    Membuat alokasi baru dari sebuah batch dan mengembalikannya dengan relasi di-load.
    """
    new_allocation_id: Optional[int] = None
    async with db.begin_nested():
        batch_query = select(Batch).where(Batch.id == allocation_in.batch_id).options(selectinload(Batch.allocations)).with_for_update()
        batch = (await db.execute(batch_query)).scalar_one_or_none()

        if not batch:
            raise NotFoundException(f"Batch with id {allocation_in.batch_id} not found.")

        total_already_allocated = sum(alloc.allocated_quantity for alloc in batch.allocations)
        available_for_allocation = batch.received_quantity - total_already_allocated

        if allocation_in.allocated_quantity > available_for_allocation:
            raise UnprocessableEntityException(
                f"Cannot allocate {allocation_in.allocated_quantity} units. "
                f"Only {available_for_allocation} units are available from batch {batch.lot_number}."
            )
        
        db_allocation = Allocation(**allocation_in.model_dump())
        db.add(db_allocation)
        await db.flush()
        new_allocation_id = db_allocation.id
    
    if not new_allocation_id:
        raise UnprocessableEntityException("Failed to create allocation and get its ID.")

    return await get_allocation_by_id(db, new_allocation_id)

async def update_allocation(db: AsyncSession, allocation_id: int, allocation_in: AllocationUpdate) -> Allocation:
    """
    Memperbarui alokasi yang ada, dengan validasi yang cermat.
    """
    async with db.begin_nested():
        db_allocation = await get_allocation_by_id(db, allocation_id)
        if not db_allocation:
            raise NotFoundException(f"Allocation with id {allocation_id} not found.")
        
        update_data = allocation_in.model_dump(exclude_unset=True)
        
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
        
    return await get_allocation_by_id(db, allocation_id)

async def delete_allocation(db: AsyncSession, allocation_id: int) -> Allocation:
    """
    Menghapus alokasi. Menerapkan validasi bisnis sebelum menghapus.
    """
    db_allocation = await get_allocation_by_id(db, allocation_id)
    if not db_allocation:
        raise NotFoundException(f"Allocation with id {allocation_id} not found.")
        
    if db_allocation.placements:
        raise BadRequestException(f"Cannot delete allocation. It has stock placed in racks.")
    if db_allocation.shipped_quantity > 0:
        raise BadRequestException(f"Cannot delete allocation. It has items that have already been shipped.")
        
    await db.delete(db_allocation)
    return db_allocation
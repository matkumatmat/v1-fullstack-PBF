# file: app/services/customer_service.py (VERSI FINAL DAN DEFINITIF)

from typing import List, Optional
from sqlalchemy import exc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Impor model yang relevan
from app.models.customer import Customer, CustomerAddress

# Impor skema yang telah kita finalisasi
from app.schemas.customer.customer import (
    CustomerCreate, CustomerUpdate,
    CustomerAddressCreate, CustomerAddressUpdate
)

# Impor exception kustom
from app.core.exceptions import NotFoundException, BadRequestException

# --- Customer Services ---

async def get_customer_by_id(db: AsyncSession, customer_id: int) -> Optional[Customer]:
    """
    Mengambil satu pelanggan berdasarkan ID, dengan eager loading untuk alamat.
    """
    query = (select(Customer).where(Customer.id == customer_id).options(selectinload(Customer.addresses)))
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_customers(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Customer]:
    """
    Mengambil daftar semua pelanggan dengan paginasi dan eager loading alamat.
    """
    query = select(Customer).offset(skip).limit(limit).options(selectinload(Customer.addresses))
    result = await db.execute(query)
    return result.scalars().all()

async def create_customer(db: AsyncSession, customer_in: CustomerCreate) -> Customer:
    """
    Membuat pelanggan baru, termasuk alamat-alamat yang terkait dalam satu transaksi.
    Fungsi ini dirancang untuk bekerja dengan skema `CustomerCreate` yang mendukung pembuatan bersarang.
    """
    customer_data = customer_in.model_dump(exclude={'addresses'})
    db_customer = Customer(**customer_data)

    # Iterasi melalui data alamat yang diberikan dan menambahkannya ke sesi
    # SQLAlchemy akan secara otomatis menangani penetapan `customer_id` saat commit.
    for address_in in customer_in.addresses:
        db_address = CustomerAddress(**address_in.model_dump())
        db_customer.addresses.append(db_address)
        
    db.add(db_customer)
    try:
        await db.commit()
    except exc.IntegrityError as e:
        await db.rollback()
        if "uq_customers_code" in str(e.orig):
            raise BadRequestException(f"Customer with code '{customer_in.code}' already exists.")
        if "fk_customers" in str(e.orig):
            raise BadRequestException("One of the provided type IDs (customer, sector) is invalid.")
        raise BadRequestException("Failed to create customer due to a data conflict.")

    await db.refresh(db_customer)
    return db_customer

async def update_customer(db: AsyncSession, customer_id: int, customer_in: CustomerUpdate) -> Customer:
    """
    Memperbarui data inti pelanggan (tidak termasuk alamat).
    """
    db_customer = await get_customer_by_id(db, customer_id)
    if not db_customer:
        raise NotFoundException(f"Customer with id {customer_id} not found.")
    
    update_data = customer_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
        
    db.add(db_customer)
    try:
        await db.commit()
    except exc.IntegrityError:
        await db.rollback()
        raise BadRequestException("Update failed. A customer with the provided code may already exist.")
        
    await db.refresh(db_customer)
    return db_customer

async def delete_customer(db: AsyncSession, customer_id: int) -> Customer:
    """
    Menghapus pelanggan. Cascade delete akan menghapus alamat-alamat terkait.
    """
    db_customer = await get_customer_by_id(db, customer_id)
    if not db_customer:
        raise NotFoundException(f"Customer with id {customer_id} not found.")
    
    # TODO: Tambahkan validasi bisnis, misal: tidak bisa menghapus pelanggan
    # jika sudah memiliki sales order atau alokasi.
    
    await db.delete(db_customer)
    await db.commit()
    return db_customer

# --- Customer Address Services ---

async def get_address_by_id(db: AsyncSession, address_id: int) -> Optional[CustomerAddress]:
    """
    Mengambil satu alamat berdasarkan ID-nya.
    """
    result = await db.execute(select(CustomerAddress).where(CustomerAddress.id == address_id))
    return result.scalar_one_or_none()

async def add_address_to_customer(db: AsyncSession, customer_id: int, address_in: CustomerAddressCreate) -> CustomerAddress:
    """
    Menambahkan alamat baru ke pelanggan yang sudah ada.
    """
    db_customer = await get_customer_by_id(db, customer_id)
    if not db_customer:
        raise NotFoundException(f"Customer with id {customer_id} not found.")
        
    # Skema `CustomerAddressCreate` tidak memiliki `customer_id`, jadi kita tambahkan di sini.
    db_address = CustomerAddress(**address_in.model_dump(), customer_id=customer_id)
    db.add(db_address)
    await db.commit()
    await db.refresh(db_address)
    return db_address

async def update_customer_address(db: AsyncSession, address_id: int, address_in: CustomerAddressUpdate) -> CustomerAddress:
    """
    Memperbarui alamat yang sudah ada.
    """
    db_address = await get_address_by_id(db, address_id)
    if not db_address:
        raise NotFoundException(f"Address with id {address_id} not found.")
        
    update_data = address_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_address, key, value)
        
    db.add(db_address)
    await db.commit()
    await db.refresh(db_address)
    return db_address

async def delete_customer_address(db: AsyncSession, address_id: int) -> CustomerAddress:
    """
    Menghapus alamat dari seorang pelanggan.
    """
    db_address = await get_address_by_id(db, address_id)
    if not db_address:
        raise NotFoundException(f"Address with id {address_id} not found.")
        
    # TODO: Tambahkan validasi, misal: tidak bisa menghapus alamat default
    # atau alamat yang sedang digunakan di pengiriman aktif.
    
    await db.delete(db_address)
    await db.commit()
    return db_address
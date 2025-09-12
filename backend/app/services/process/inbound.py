from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, selectinload

# Impor model yang relevan
from app.models.product import Product
from app.models.warehouse import Rack, Warehouse
from app.models.users import Customer
from app.models.configuration import AllocationType
from app.schemas.process.inbound import InboundPayload, InboundResponse, InboundFormData
from app.schemas.warehouse.stock_placement import StockPlacementCreate
from app.schemas.product.batch import BatchCreate
from app.schemas.product.allocation import AllocationCreate

# Impor service lain
from app.services import product_service, warehouse_service, type_service
from app.core.exceptions import NotFoundException, BadRequestException, UnprocessableEntityException

# ===================================================================
# 1. FUNGSI UNTUK PERSIAPAN FORM (EFISIEN)
# ===================================================================


async def get_inbound_form_data(db: AsyncSession) -> InboundFormData:
    """
    Mengambil semua data lookup yang diperlukan untuk form inbound secara sekuensial.
    Ini adalah pola yang aman dan benar untuk satu AsyncSession.
    """
    ### DEVIL'S ADVOCATE NOTE ###
    # INI ADALAH PERBAIKAN KRITIS.
    # Kita tidak bisa menggunakan `asyncio.gather` pada satu objek `db: AsyncSession`
    # karena itu akan mencoba menjalankan query secara bersamaan pada koneksi yang sama,
    # yang menyebabkan error 'concurrent operations not permitted'.
    # Pola yang benar adalah menjalankan query satu per satu (sekuensial) seperti di bawah ini.
    # Untuk tabel lookup yang kecil, dampaknya pada performa dapat diabaikan.

    allocation_types_data = await type_service.allocation_type.get_multi(db, limit=200)
    product_types_data = await type_service.product_type.get_multi(db, limit=200)
    package_types_data = await type_service.package_type.get_multi(db, limit=200)
    temperature_types_data = await type_service.temperature_type.get_multi(db, limit=200)
    
    return InboundFormData(
        allocation_types=allocation_types_data,
        product_types=product_types_data,
        package_types=package_types_data,
        temperature_types=temperature_types_data
    )

async def search_products_for_inbound(db: AsyncSession, query: str) -> List[Product]:
    """
    Mencari produk dengan query ringan, hanya memuat kolom yang dibutuhkan UI.
    (Tidak ada perubahan di sini, kode ini sudah benar)
    """
    search_query = (
        select(Product)
        .filter((Product.product_code.ilike(f"%{query}%")) | (Product.name.ilike(f"%{query}%")))
        .options(load_only(Product.id, Product.product_code, Product.name))
        .limit(20)
    )
    result = await db.execute(search_query)
    return result.scalars().all()

async def search_racks_for_inbound(db: AsyncSession, query: str) -> List[Rack]:
    """
    Mencari rak berdasarkan kode, sambil memuat data warehouse terkait secara efisien.
    (Tidak ada perubahan di sini, kode ini sudah benar)
    """
    search_query = (
        select(Rack)
        .join(Rack.warehouse)
        .filter((Rack.code.ilike(f"%{query}%")) | (Warehouse.code.ilike(f"%{query}%")))
        .options(selectinload(Rack.warehouse))
        .limit(20)
    )
    result = await db.execute(search_query)
    return result.scalars().all()

# ===================================================================
# 2. FUNGSI ORKESTRASI PROSES (TRANSAKSIONAL)
# ===================================================================
async def process_full_inbound(db: AsyncSession, payload: InboundPayload) -> InboundResponse:
    """
    Mengorkestrasi seluruh proses inbound dengan validasi dan penanganan data yang aman.
    """
    # --- Langkah 1: Tentukan atau Buat Produk ---
    product_id_to_use: int
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
    ### DEVIL'S ADVOCATE NOTE: INI ADALAH PERBAIKAN KRITIS ###
    # 1. Ubah data Pydantic menjadi dictionary.
    batch_data_dict = payload.batch_data.model_dump()
    # 2. Hapus 'product_id' jika ada, untuk menghindari konflik. Ini adalah
    #    langkah defensif untuk mengabaikan nilai yang mungkin dikirim klien.
    batch_data_dict.pop('product_id', None)
    # 3. Buat skema Create yang lengkap dengan menggabungkan data yang sudah bersih
    #    dengan product_id yang benar dari server.
    batch_create_schema = BatchCreate(**batch_data_dict, product_id=product_id_to_use)
    
    new_batch = await product_service.create_batch(db, batch_in=batch_create_schema)
    await db.flush()

    # --- Langkah 3: Buat Alokasi (dengan validasi) ---
    allocation_data = payload.allocation_data
    
    alloc_type = await db.get(AllocationType, allocation_data.allocation_type_id)
    if not alloc_type:
        raise NotFoundException(f"AllocationType with id {allocation_data.allocation_type_id} not found.")

    if allocation_data.customer_id:
        customer = await db.get(Customer, allocation_data.customer_id)
        if not customer:
            raise NotFoundException(f"Customer with id {allocation_data.customer_id} not found.")

    # Lakukan hal yang sama untuk alokasi demi konsistensi dan keamanan
    allocation_data_dict = allocation_data.model_dump()
    allocation_data_dict.pop('batch_id', None)
    allocation_create_schema = AllocationCreate(**allocation_data_dict, batch_id=new_batch.id)
    
    if allocation_create_schema.allocated_quantity > new_batch.received_quantity:
        raise UnprocessableEntityException(f"Allocation quantity ({allocation_create_schema.allocated_quantity}) cannot exceed batch received quantity ({new_batch.received_quantity}).")
    
    new_allocation = await product_service.create_allocation(db, allocation_in=allocation_create_schema)
    await db.flush()

    # --- Langkah 4: Tempatkan Stok di Rak ---
    if payload.placement_quantity > new_allocation.allocated_quantity:
        raise UnprocessableEntityException(f"Placement quantity ({payload.placement_quantity}) cannot exceed allocated quantity ({new_allocation.allocated_quantity}).")
        
    placement_schema = StockPlacementCreate(
        rack_id=payload.rack_id,
        allocation_id=new_allocation.id,
        quantity=payload.placement_quantity
    )
    final_placement = await warehouse_service.place_stock_in_rack(db, placement_in=placement_schema)
    
    # --- Finalisasi: Muat relasi untuk respons ---
    await db.refresh(final_placement, attribute_names=["rack", "allocation"])
    if final_placement.allocation:
        await db.refresh(final_placement.allocation, attribute_names=["batch"])
        if final_placement.allocation.batch:
            await db.refresh(final_placement.allocation.batch, attribute_names=["product"])
    
    return final_placement
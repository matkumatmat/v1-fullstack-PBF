# file: app/services/customer_service.py

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, load_only
import uuid

# Impor model yang relevan
from app.models.users.customer import (
    Customer, 
    Branch, 
    Location, 
    CustomerDetails, 
    CustomerSpecification
)

# Impor skema yang sudah kita finalisasi
from app.schema.internal.user.customer import (
    CustomerOnboard,
    BranchCreateForExistingCustomer,
    LocationCreate,
    BranchNestedCreate
)

# Impor exception kustom
from app.core.exceptions import NotFoundException, BadRequestException

# =============================================================================
# FUNGSI HELPER (PRIVATE)
# =============================================================================

async def _get_customer_by_public_id(db: AsyncSession, public_id: uuid.UUID) -> Customer:
    """Helper untuk mengambil customer berdasarkan public_id, raise error jika tidak ada."""
    query = select(Customer).where(Customer.public_id == public_id)
    result = await db.execute(query)
    customer = result.scalar_one_or_none()
    if not customer:
        raise NotFoundException(f"Customer with public_id {public_id} not found.")
    return customer

async def _get_branch_by_public_id(db: AsyncSession, public_id: uuid.UUID) -> Branch:
    """Helper untuk mengambil branch berdasarkan public_id, raise error jika tidak ada."""
    query = select(Branch).where(Branch.public_id == public_id)
    result = await db.execute(query)
    branch = result.scalar_one_or_none()
    if not branch:
        raise NotFoundException(f"Branch with public_id {public_id} not found.")
    return branch

async def _get_location_by_public_id(db: AsyncSession, public_id: uuid.UUID) -> Location:
    """Helper untuk mengambil location berdasarkan public_id, raise error jika tidak ada."""
    query = select(Location).where(Location.public_id == public_id)
    result = await db.execute(query)
    location = result.scalar_one_or_none()
    if not location:
        raise NotFoundException(f"Location with public_id {public_id} not found.")
    return location    

async def _create_branch_hierarchy_recursive(
    db: AsyncSession, 
    branch_data_list: List[BranchNestedCreate], 
    customer: Customer, 
    parent_branch: Optional[Branch] = None
):
    """
    Fungsi rekursif privat untuk membuat seluruh pohon branch dan location.
    Ini adalah inti dari orkestrasi.
    """
    for branch_data in branch_data_list:
        # 1. Buat objek Branch
        new_branch = Branch(
            name=branch_data.name,
            customer_id=customer.id,
            parent_id=parent_branch.id if parent_branch else None
        )
        
        # 2. Buat semua Location untuk branch ini
        for loc_data in branch_data.locations:
            # Langsung unpack skema ke model karena namanya sudah konsisten
            new_loc = Location(**loc_data.model_dump())
            new_branch.locations.append(new_loc)
            
        db.add(new_branch)
        await db.flush() # Flush untuk mendapatkan ID branch baru

        # 3. Panggil fungsi ini lagi untuk semua anak cabang (rekursi)
        if branch_data.children:
            await _create_branch_hierarchy_recursive(
                db, 
                branch_data.children, 
                customer, 
                parent_branch=new_branch
            )

# =============================================================================
# FUNGSI SERVICE UTAMA (PUBLIK)
# =============================================================================

async def onboard_customer(db: AsyncSession, payload: CustomerOnboard) -> Customer:
    """
    SKENARIO 1: Orkestrasi Penuh.
    Membuat Customer, Details, Spec, dan seluruh hierarki Branch & Location.
    """
    # Cek apakah customer dengan nama atau NPWP yang sama sudah ada (opsional tapi bagus)
    # ... (tambahkan logika validasi duplikat jika perlu) ...

    # 1. Buat objek Customer utama beserta relasi 1-to-1 nya
    new_customer = Customer(
        name=payload.name,
        customer_type=payload.customer_type,
        details=CustomerDetails(**payload.details.model_dump()),
        specification=CustomerSpecification(**payload.specification.model_dump())
    )
    db.add(new_customer)
    await db.flush() # Penting untuk mendapatkan ID customer sebelum membuat branch

    # 2. Panggil helper rekursif untuk membuat seluruh struktur di bawahnya
    await _create_branch_hierarchy_recursive(
        db, 
        payload.branches, 
        customer=new_customer
    )
    
    # 3. Muat ulang (refresh) objek customer untuk mendapatkan semua relasi yang baru dibuat
    # Ini penting agar objek yang dikembalikan ke router berisi semua data.
    await db.refresh(new_customer, attribute_names=['branches'])
    
    # Eager load seluruh pohon untuk response (opsional, tapi bagus untuk performa)
    result = await db.execute(
        select(Customer).where(Customer.id == new_customer.id).options(
            selectinload(Customer.branches).selectinload(Branch.locations),
            selectinload(Customer.branches).selectinload(Branch.children) # Perlu cara lebih baik untuk deep load
        )
    )
    
    return result.scalar_one()

async def add_branch_to_customer(
    db: AsyncSession, 
    customer_public_id: uuid.UUID, 
    payload: BranchCreateForExistingCustomer
) -> Customer:
    """
    SKENARIO 2: Menambahkan hierarki Branch baru ke Customer yang sudah ada.
    """
    # 1. Cari customer yang dituju
    customer = await _get_customer_by_public_id(db, customer_public_id)
    
    # 2. Panggil helper rekursif untuk membuat struktur branch
    # Kita mengirimkan list berisi satu item karena payload-nya hanya satu branch_data
    await _create_branch_hierarchy_recursive(
        db, 
        [payload.branch_data], 
        customer=customer
    )
    
    # 3. Refresh dan kembalikan objek customer yang sudah ter-update
    await db.refresh(customer, attribute_names=['branches'])
    return customer

async def add_location_to_branch(
    db: AsyncSession, 
    branch_public_id: uuid.UUID, 
    payload: LocationCreate
) -> Location:
    """
    SKENARIO 3: Menambahkan satu Location baru ke Branch yang sudah ada.
    """
    # 1. Cari branch yang dituju
    branch = await _get_branch_by_public_id(db, branch_public_id)
    
    # 2. Buat objek Location baru
    new_location = Location(**payload.model_dump(), branch_id=branch.id)
    db.add(new_location)
    await db.flush()
    await db.refresh(new_location)
    
    return new_location

async def get_all_customers(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Customer]:
    """
    Mengambil daftar semua customer (data dasar, tanpa relasi berat).
    Bagus untuk halaman list/tabel utama.
    """
    query = select(Customer).offset(skip).limit(limit).order_by(Customer.name)
    result = await db.execute(query)
    return result.scalars().all()

async def get_customer_with_full_hierarchy(db: AsyncSession, customer_public_id: uuid.UUID) -> Optional[Customer]:
    """
    Mengambil SATU customer LENGKAP dengan seluruh hierarki branch dan location-nya.
    Ini adalah query yang berat, gunakan hanya untuk halaman detail.
    """
    customer = await _get_customer_by_public_id(db, customer_public_id)
    query = (
        select(Customer)
        .where(Customer.id == customer.id)
        .options(
            # Muat relasi 1-to-1
            selectinload(Customer.details),
            selectinload(Customer.specification),
            selectinload(Customer.branches)
            .selectinload(Branch.locations),
            selectinload(Customer.branches)
            .selectinload(Branch.children)
            .selectinload(Branch.locations), # Anak level 1
            selectinload(Customer.branches)
            .selectinload(Branch.children)
            .selectinload(Branch.children)
            .selectinload(Branch.locations) # Anak level 2
        )
    )
    
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_branch_with_locations(db: AsyncSession, branch_public_id: uuid.UUID) -> Optional[Branch]:
    """
    Mengambil SATU branch lengkap dengan daftar lokasinya DAN anak-anaknya.
    """
    branch = await _get_branch_by_public_id(db, branch_public_id)
    
    query = (
        select(Branch)
        .where(Branch.id == branch.id)
        .options(
            selectinload(Branch.locations),
            selectinload(Branch.parent),
            selectinload(Branch.customer),
            selectinload(Branch.children).selectinload(Branch.locations)
        )
    )
    
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_location_details(db: AsyncSession, location_public_id: uuid.UUID) -> Optional[Location]:
    """
    Mengambil detail SATU lokasi.
    """
    query = (
        select(Location)
        .where(Location.public_id == location_public_id)
        .options(
            selectinload(Location.branch).selectinload(Branch.customer) # Muat branch & customer-nya
        )
    )
    result = await db.execute(query)
    location = result.scalar_one_or_none()
    if not location:
        raise NotFoundException(f"Location with public_id {location_public_id} not found.")
    return location

async def get_all_customers_for_lookup(db: AsyncSession) -> List[Customer]:
    """
    Mengambil SEMUA customer beserta hierarki branch & location-nya,
    tapi HANYA field yang dibutuhkan untuk lookup (id, public_id, name, parent_id).
    Ini dioptimalkan untuk performa.
    """
    query = (
        select(Customer)
        .options(
            # Eager load relasi-relasi yang kita butuhkan
            selectinload(Customer.branches)
            .selectinload(Branch.locations),
            
            selectinload(Customer.branches)
            .selectinload(Branch.children)
            .selectinload(Branch.locations), # Level 2
            
            # OPTIMASI: Hanya muat kolom yang kita butuhkan dari database
            load_only(Customer.id, Customer.public_id, Customer.name),
            
            selectinload(Customer.branches).load_only(
                Branch.id, Branch.public_id, Branch.name, Branch.customer_id, Branch.parent_id
            ),
            selectinload(Customer.branches).selectinload(Branch.locations).load_only(
                Location.id, Location.public_id, Location.name, Location.branch_id, Location.location_type
            ),
            selectinload(Customer.branches).selectinload(Branch.children).load_only(
                Branch.id, Branch.public_id, Branch.name, Branch.customer_id, Branch.parent_id
            ),
            selectinload(Customer.branches).selectinload(Branch.children).selectinload(Branch.locations).load_only(
                Location.id, Location.public_id, Location.name, Location.branch_id
            )
        )
        .order_by(Customer.name)
    )
    
    result = await db.execute(query)
    return result.scalars().all()
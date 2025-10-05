# file: app/services/packing_service.py

import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.packing.manifest import PackingManifest, PackedBox, PackedItem
from app.schema.internal.packing.packing_manifest import PackingManifestCreate
from app.service.internal.user.customer import _get_location_by_public_id
from app.core.exceptions import BadRequestException, NotFoundException

# --- FUNGSI HELPER UNTUK GENERATOR ID ---

def _calculate_check_digit(number_string: str) -> int:
    """Menghitung check digit Modulo 10 dengan bobot 3-1-3-1..."""
    total = 0
    weights = [3, 1]
    for i, digit in enumerate(reversed(number_string)):
        total += int(digit) * weights[i % 2]
    
    check_digit = (10 - (total % 10)) % 10
    return check_digit

def _generate_sscc(box_id: int) -> str:
    """Generate SSCC-18 berdasarkan ID unik dari kotak."""
    extension_digit = "1"
    company_prefix = "8994957"
    # ID unik, 8 digit, padding dengan nol di depan
    serial_reference = str(box_id).zfill(8)
    
    # Gabungin 17 digit pertama
    sscc_17_digits = f"{extension_digit}{company_prefix}{serial_reference}"
    
    # Hitung check digit
    check_digit = _calculate_check_digit(sscc_17_digits)
    
    return f"{sscc_17_digits}{check_digit}"

def _generate_gtin8() -> str:
    """Generate GTIN-8 statis."""
    indicator_digit = "1"
    company_prefix = "8994957" # Ini 7 digit, aneh buat GTIN-8, tapi kita ikutin
    item_ref = "000001" # Statis
    
    # GTIN-8 harusnya 8 digit total. Company prefix lo 7 digit, ini aneh.
    # Kita potong aja biar jadi 7 digit total + 1 check digit.
    gtin_7_digits = f"{indicator_digit}{company_prefix[:6]}" # Ambil 6 digit dari prefix
    
    check_digit = _calculate_check_digit(gtin_7_digits)
    
    return f"{gtin_7_digits}{check_digit}"

# --- FUNGSI SERVICE UTAMA ---

async def create_packing_manifest(db: AsyncSession, payload: PackingManifestCreate) -> PackingManifest:
    location = await _get_location_by_public_id(db, payload.locations.location_public_id)
    
    new_manifest = PackingManifest(
        location_id=location.id,
        tujuan_kirim=payload.locations.tujuan_kirim,
        packing_slip=payload.content.packing_slip,
        total_boxes=payload.content.total_box,
        shipping_address_details=payload.locations.model_dump()
    )
    db.add(new_manifest)
    await db.flush() # Flush untuk mendapatkan manifest.id

    for box_data in payload.content.boxes:
        # Buat dulu objek box tanpa SSCC/GTIN
        new_box = PackedBox(
            manifest_id=new_manifest.id,
            box_number=box_data.box_number,
            petugas=box_data.petugas,
            berat=box_data.berat,
            sscc="", # Placeholder
            gtin=""  # Placeholder
        )
        db.add(new_box)
        await db.flush() # Flush untuk mendapatkan new_box.id yang unik

        # SEKARANG BARU GENERATE SSCC PAKE ID YANG UDAH PASTI UNIK
        new_box.sscc = _generate_sscc(new_box.id)
        new_box.gtin = _generate_gtin8()
        
        for item_data in box_data.items:
            new_item = PackedItem(
                box_id=new_box.id,
                **item_data.model_dump()
            )
            db.add(new_item)
            
    await db.flush()
    
    # Eager load semua relasi untuk response
    result = await db.execute(
        select(PackingManifest)
        .where(PackingManifest.id == new_manifest.id)
        .options(
            selectinload(PackingManifest.packed_boxes)
            .selectinload(PackedBox.packed_items)
        )
    )
    return result.scalar_one()

async def get_latest_manifests(db: AsyncSession, limit: int = 25) -> List[PackingManifest]:
    """
    Mengambil daftar manifest packing terbaru, lengkap dengan semua
    kotak dan item di dalamnya (nested).
    """
    query = (
        select(PackingManifest)
        .options(
            # Eager load semua relasi yang dibutuhkan untuk response
            selectinload(PackingManifest.location), # Kita butuh ini buat public_id
            selectinload(PackingManifest.packed_boxes)
            .selectinload(PackedBox.packed_items)
        )
        .order_by(PackingManifest.created_at.desc()) # Urutkan dari yang paling baru
        .limit(limit) # Batasi jumlahnya
    )
    
    result = await db.execute(query)
    return result.scalars().all()

async def get_manifest_by_public_id(db: AsyncSession, public_id: uuid.UUID) -> PackingManifest:
    """Mengambil satu manifest spesifik berdasarkan public_id-nya."""
    query = (
        select(PackingManifest)
        .where(PackingManifest.public_id == public_id)
        .options(
            selectinload(PackingManifest.location),
            selectinload(PackingManifest.packed_boxes)
            .selectinload(PackedBox.packed_items)
        )
    )
    result = await db.execute(query)
    manifest = result.scalar_one_or_none()
    if not manifest:
        raise NotFoundException(f"Packing Manifest with public_id {public_id} not found.")
    return manifest

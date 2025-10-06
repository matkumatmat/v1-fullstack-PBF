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
from app.schema.internal.packing.packing_manifest import LabelAddressData # Impor skema baru
from app.models.users.customer import Location


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
    serial_reference = str(box_id).zfill(9)
    
    sscc_17_digits = f"{extension_digit}{company_prefix}{serial_reference}"
    
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
        shipping_address_details=payload.locations.model_dump(mode='json')
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
            selectinload(PackingManifest.location),
            selectinload(PackingManifest.packed_boxes)
            .selectinload(PackedBox.packed_items)
        )
    )
    return result.scalar_one()

# file: app/services/packing_service.py

async def get_latest_manifests(db: AsyncSession, limit: int = 25) -> List[PackingManifest]:
    """
    Mengambil daftar manifest packing terbaru, lengkap dengan semua
    kotak dan item di dalamnya (nested).
    """
    print("\n--- [INTEROGASI SERVICE DIMULAI] ---")
    print(">>> Membangun query `get_latest_manifests`...")
    query = (
        select(PackingManifest)
        .options(
            selectinload(PackingManifest.location),
            selectinload(PackingManifest.packed_boxes)
            .selectinload(PackedBox.packed_items)
        )
        .order_by(PackingManifest.created_at.desc())
        .limit(limit)
    )
    print(">>> Query selesai dibangun. Mengeksekusi ke DB...")
    
    result = await db.execute(query)
    manifests = result.scalars().all()
    
    print(f"<<< Query selesai. Ditemukan {len(manifests)} manifest.")

    # --- BAGIAN INTEROGASI PALING PENTING ---
    if manifests:
        print("\n--- MENGINSPEKSI MANIFEST PERTAMA ---")
        first_manifest = manifests[0]
        print(f"--- Tipe objek: {type(first_manifest)}")
        print(f"--- ID Manifest: {first_manifest.id}")
        
        print("--- Mengecek `first_manifest.location`...")
        if first_manifest.location:
            print("✅ `location` ADA.")
            print(f"--- Tipe location: {type(first_manifest.location)}")
            print(f"--- ID Location: {first_manifest.location.id}")
            print(f"--- Public ID Location: {first_manifest.location.public_id}")
        else:
            print("❌❌❌ ANJING! `location` TERNYATA KOSONG (None)! INI BIANG KEROKNYA! ❌❌❌")
    else:
        print("--- Tidak ada manifest untuk diinspeksi.")
        
    print("--- [INTEROGASI SERVICE SELESAI] ---\n")
    
    return manifests

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

def _process_shipping_address_for_label(manifest: PackingManifest) -> LabelAddressData:
    """
    Mengambil objek PackingManifest dan mengolah data TUJUAN KIRIM
    menjadi format yang siap dicetak di label.
    """
    # 1. Ambil data alamat mentah dari kolom JSONB
    address_details = manifest.shipping_address_details
    if not address_details:
        # Fallback kalo data JSON-nya kosong, pake string tujuan_kirim aja
        full_address = manifest.tujuan_kirim
        province = "N/A"
        city = "N/A"
        pic = ""
        pic_contact = ""
    else:
        # Ekstrak data dari dictionary JSON
        line_1 = address_details.get("line_1", "")
        line_2 = address_details.get("line_2", "")
        line_3 = address_details.get("line_3", "")
        province = address_details.get("province", "N/A")
        city = manifest.tujuan_kirim # Sesuai payload, `tujuan_kirim` itu nama kota/tujuan
        pic = address_details.get("pic", "")
        pic_contact = "" # Di payload lo nggak ada pic_contact buat tujuan

        # Gabungin semua baris alamat jadi satu string panjang
        full_address = " ".join(filter(None, [line_1, line_2, line_3])).strip()

    # 2. Logika pemotongan string alamat (maks 52 karakter per baris) - INI TETAP SAMA
    lines = []
    # ... (kode looping buat motong-motong string `full_address` tetap sama persis kayak sebelumnya) ...
    # ... (gue copy-paste dari jawaban sebelumnya) ...
    current_line = ""
    words = full_address.split()
    for word in words:
        if len(current_line) + len(word) + 1 <= 52:
            current_line += f" {word}"
        else:
            lines.append(current_line.strip())
            current_line = word
    if current_line:
        lines.append(current_line.strip())
        
    # 3. Potong kalo lebih dari 3 baris dan tambahin tanda hubung - INI JUGA TETAP SAMA
    addr_line_1_processed = lines[0] if len(lines) > 0 else ""
    addr_line_2_processed = None
    addr_line_3_processed = None
    if len(lines) > 1:
        if len(lines) == 2:
            addr_line_2_processed = lines[1]
        else:
            addr_line_2_processed = lines[1][:51] + "-"
    if len(lines) > 2:
        remaining_text = " ".join(lines[2:])
        if len(remaining_text) > 52:
            addr_line_3_processed = remaining_text[:51] + "-"
        else:
            addr_line_3_processed = remaining_text
            
    # 4. Format PIC dan kontak (sekarang dari data tujuan)
    pic_info = pic # Cuma ada nama PIC dari payload
        
    # 5. Rakit jadi objek Pydantic
    return LabelAddressData(
        line_1=addr_line_1_processed,
        line_2=addr_line_2_processed,
        line_3=addr_line_3_processed,
        province=province,
        city=city,
        pic_contact=pic_info
    )

# --- FUNGSI SERVICE UTAMA (SEDIKIT PERUBAHAN) ---

async def get_data_for_label_printing(db: AsyncSession, manifest_public_id: uuid.UUID) -> dict:
    """
    Mengambil semua data manifest dan mengolahnya menjadi format
    yang siap dikirim sebagai JSON untuk dicetak.
    """
    manifest = await get_manifest_by_public_id(db=db, public_id=manifest_public_id)
    
    # ✅ PANGGIL HELPER YANG BARU
    shipping_address_data = _process_shipping_address_for_label(manifest)
    
    label_data = {
        "public_id": manifest.public_id,
        "created_at": manifest.created_at,
        "updated_at": manifest.updated_at,        
        "manifest_public_id": manifest.public_id,
        "packing_slip": manifest.packing_slip,
        "tujuan_kirim": manifest.tujuan_kirim,
        
        # ✅ GANTI NAMA FIELD INI
        "shipping_address": shipping_address_data,
        
        "packed_boxes": manifest.packed_boxes
    }
    
    return label_data
# file: app/services/labeling_service.py (buat file & folder baru)

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.log.label_print_log import LabelPrintLog
from app.schema.internal.log.label_print_log import LabelPrintCreate
from app.service.internal.user.customer import _get_location_by_public_id # Pake ulang helper
from app.core.exceptions import NotFoundException

async def create_print_log(db: AsyncSession, payload: LabelPrintCreate) -> LabelPrintLog:
    """Membuat log cetak label baru dan memproses SSCC."""
    
    # 1. Ambil entitas Location
    location = await _get_location_by_public_id(db, payload.location_public_id)
    
    # 2. Proses/Generate SSCC jika perlu
    # Frontend ngirim "sscc": "string". Kita bisa ganti itu dengan UUID beneran.
    processed_content = payload.content.copy() # Jangan modifikasi payload asli
    if 'items' in processed_content and isinstance(processed_content['items'], list):
        for item in processed_content['items']:
            # Ganti placeholder "string" dengan UUID baru yang unik
            item['sscc'] = str(uuid.uuid4())
            
    # 3. Buat objek log
    new_log = LabelPrintLog(
        location_id=location.id,
        tujuan_kirim=payload.tujuan_kirim,
        content=processed_content # Simpen konten yang udah diproses
    )
    
    db.add(new_log)
    await db.flush()
    await db.refresh(new_log)
    
    return new_log

async def get_print_log_by_public_id(db: AsyncSession, public_id: uuid.UUID) -> LabelPrintLog:
    """Mengambil satu log cetak untuk keperluan reprint."""
    query = select(LabelPrintLog).where(LabelPrintLog.public_id == public_id).options(selectinload(LabelPrintLog.location))
    result = await db.execute(query)
    log = result.scalar_one_or_none()
    if not log:
        raise NotFoundException(f"Print log with public_id {public_id} not found.")
    return log
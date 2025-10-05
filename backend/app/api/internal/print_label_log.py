# file: app/api/routers/labeling_router.py (buat file baru)

import uuid
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session
from app.schema.internal.log.label_print_log import LabelPrintCreate, LabelPrintResponse
from app.service.internal.log.print_label import labeling_service

router = APIRouter(prefix="/labels", tags=["Label Printing"])

@router.post(
    "/print-log",
    response_model=LabelPrintResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Buat Log Cetak Label Baru"
)
async def create_print_log_endpoint(
    payload: LabelPrintCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Menerima data cetak, men-generate SSCC untuk setiap item,
    dan menyimpan hasilnya sebagai satu log.
    """
    log = await labeling_service.create_print_log(db=db, payload=payload)
    
    # Transformasi ke response
    return LabelPrintResponse(
        public_id=log.public_id,
        created_at=log.created_at,
        updated_at=log.updated_at,
        location_public_id=log.location.public_id,
        tujuan_kirim=log.tujuan_kirim,
        content=log.content
    )

@router.get(
    "/print-log/{public_id}",
    response_model=LabelPrintResponse,
    summary="Ambil Data Log Cetak untuk Reprint"
)
async def get_print_log_endpoint(
    public_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil satu log cetak berdasarkan public_id-nya.
    Frontend bisa pake data 'content' dari sini untuk reprint.
    """
    log = await labeling_service.get_print_log_by_public_id(db=db, public_id=public_id)
    
    # Transformasi ke response
    return LabelPrintResponse(
        public_id=log.public_id,
        created_at=log.created_at,
        updated_at=log.updated_at,
        location_public_id=log.location.public_id,
        tujuan_kirim=log.tujuan_kirim,
        content=log.content
    )
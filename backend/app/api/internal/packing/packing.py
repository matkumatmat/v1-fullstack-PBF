# file: app/api/routers/packing_router.py

import uuid
from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.schema.internal.packing import packing_manifest as schemas
from app.service.internal.packing import packing as packing_service

# ✅ BENERIN PREFIX BIAR JELAS DAN RESTFUL
router = APIRouter(prefix="/manifests", tags=["Packing & Manifest"])

@router.post(
    "", # Path: POST /manifests
    response_model=schemas.PackingManifestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Buat Packing Manifest Baru"
)
async def create_manifest_endpoint(
    payload: schemas.PackingManifestCreate,
    db: AsyncSession = Depends(get_db_session)
):
    manifest = await packing_service.create_packing_manifest(db=db, payload=payload)
    
    # Konstruksi response secara eksplisit
    return schemas.PackingManifestResponse(
        public_id=manifest.public_id,
        created_at=manifest.created_at,
        updated_at=manifest.updated_at,
        location_public_id=manifest.location.public_id,
        tujuan_kirim=manifest.tujuan_kirim,
        packing_slip=manifest.packing_slip,
        total_boxes=manifest.total_boxes,
        packed_boxes=manifest.packed_boxes
    )

@router.get(
    "", # Path: GET /manifests
    response_model=List[schemas.PackingManifestResponse],
    summary="Dapatkan Daftar Manifest Packing Terbaru"
)
async def get_latest_manifests_endpoint(
    limit: int = Query(default=25, lte=100),
    db: AsyncSession = Depends(get_db_session)
):
    manifests = await packing_service.get_latest_manifests(db=db, limit=limit)
    
    # Konstruksi response secara eksplisit untuk setiap item dalam list
    response_list = []
    for manifest in manifests:
        response_list.append(
            schemas.PackingManifestResponse(
                public_id=manifest.public_id,
                created_at=manifest.created_at,
                updated_at=manifest.updated_at,
                location_public_id=manifest.location.public_id,
                tujuan_kirim=manifest.tujuan_kirim,
                packing_slip=manifest.packing_slip,
                total_boxes=manifest.total_boxes,
                packed_boxes=manifest.packed_boxes
            )
        )
    return response_list

@router.get(
    "/{public_id}", # Path: GET /manifests/{public_id}
    response_model=schemas.PackingManifestResponse,
    summary="Dapatkan Detail Satu Manifest Packing"
)
async def get_manifest_details_endpoint(
    public_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    manifest = await packing_service.get_manifest_by_public_id(db=db, public_id=public_id)
    
    # Konstruksi response secara eksplisit
    return schemas.PackingManifestResponse(
        public_id=manifest.public_id,
        created_at=manifest.created_at,
        updated_at=manifest.updated_at,
        location_public_id=manifest.location.public_id,
        tujuan_kirim=manifest.tujuan_kirim,
        packing_slip=manifest.packing_slip,
        total_boxes=manifest.total_boxes,
        packed_boxes=manifest.packed_boxes
    )

@router.get(
    "/{public_id}/print-data",
    response_model=schemas.LabelDataResponse,
    summary="Dapatkan Data Terformat untuk Cetak Label"
)
async def get_formatted_label_data_endpoint(
    public_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil data dari satu manifest, mengolah data alamat pengirim
    sesuai aturan pemotongan string, dan mengembalikan JSON lengkap
    yang siap digunakan untuk men-generate ZPL di frontend atau di mana pun.
    """
    # Panggil service yang udah kerja keras
    label_data_dict = await packing_service.get_data_for_label_printing(db=db, manifest_public_id=public_id)
    
    # Service ngasih dictionary, kita tinggal return.
    # FastAPI akan validasi pake `LabelDataResponse`.
    return label_data_dict
# file: app/api/routers/packing_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import List
from fastapi import APIRouter, Depends, status, Query

from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session
from app.schema.internal.packing import packing_manifest as schemas
from app.service.internal.packing import packing as packing_service

router = APIRouter(prefix="/packings", tags=["Packing & Manifest"])

@router.post(
    "/manifest",
    response_model=schemas.PackingManifestResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Buat Packing Manifest Baru"
)
async def create_manifest_endpoint(
    payload: schemas.PackingManifestCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Menerima data packing lengkap, men-generate SSCC-18 dan GTIN-8 secara internal,
    menyimpan ke database, dan mengembalikan hasil yang sudah diproses.
    """
    manifest = await packing_service.create_packing_manifest(db=db, payload=payload)
    
    # Kita perlu transformasi manual karena skema response butuh `location_public_id`
    # yang ada di objek `manifest.location`
    response = schemas.PackingManifestResponse.model_validate(manifest)
    response.location_public_id = manifest.location.public_id
    
    return response

@router.get(
    "/manifests",
    response_model=List[schemas.PackingManifestResponse],
    summary="Dapatkan Daftar Manifest Packing Terbaru"
)
async def get_latest_manifests_endpoint(
    limit: int = Query(default=25, lte=100), # Default 25, maks 100
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil daftar manifest packing terbaru, diurutkan dari yang paling baru dibuat.
    Data dikembalikan dalam format nested lengkap.
    """
    manifests = await packing_service.get_latest_manifests(db=db, limit=limit)
    
    # Transformasi manual karena kita butuh `location_public_id`
    response_list = []
    for manifest in manifests:
        response = schemas.PackingManifestResponse.model_validate(manifest)
        response.location_public_id = manifest.location.public_id
        response_list.append(response)
        
    return response_list

@router.get(
    "/manifest/{public_id}",
    response_model=schemas.PackingManifestResponse,
    summary="Dapatkan Detail Satu Manifest Packing"
)
async def get_manifest_details_endpoint(
    public_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Mengambil detail lengkap dari satu manifest packing berdasarkan public_id-nya.
    """
    manifest = await packing_service.get_manifest_by_public_id(db=db, public_id=public_id)
    
    response = schemas.PackingManifestResponse.model_validate(manifest)
    response.location_public_id = manifest.location.public_id
    
    return response
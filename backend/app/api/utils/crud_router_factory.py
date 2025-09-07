# file: app/api/utils/crud_router_factory.py (VERSI FINAL YANG BEKERJA)

from typing import Type, List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

# Impor dari proyek Anda
from app.services.base import CRUDBase, ModelType, CreateSchemaType, UpdateSchemaType
from app.api import deps

def create_crud_router(
    *,
    service: CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType],
    response_schema: Type[BaseModel],
    prefix: str,
    tags: List[str]
) -> APIRouter:
    """
    Pabrik fungsional yang secara otomatis menghasilkan endpoint CRUD.
    Versi ini secara eksplisit memberikan tipe skema ke FastAPI untuk memastikan fungsionalitas runtime.
    """
    router = APIRouter(prefix=prefix, tags=tags)

    # Ekstrak tipe skema yang konkret dari service.
    # Ini adalah langkah kunci untuk memberitahu FastAPI skema mana yang harus digunakan.
    ConcreteCreateSchema = service.get_create_schema_type()
    ConcreteUpdateSchema = service.get_update_schema_type()

    @router.post("/", response_model=response_schema, status_code=status.HTTP_201_CREATED)
    async def create(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        # Gunakan tipe skema yang konkret ini. FastAPI akan tahu cara menanganinya.
        obj_in: ConcreteCreateSchema = Body(...), #type:ignore
    ) -> ModelType:
        """
        Membuat item baru.
        """
        return await service.create(db=db, obj_in=obj_in)

    @router.get("/", response_model=List[response_schema])
    async def get_all(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """
        Mengambil daftar item.
        """
        return await service.get_multi(db=db, skip=skip, limit=limit)

    @router.get("/{id}", response_model=response_schema)
    async def get_by_id(*, db: AsyncSession = Depends(deps.get_db_session), id: int) -> ModelType:
        """
        Mengambil satu item berdasarkan ID.
        """
        obj = await service.get(db=db, id=id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{service.model.__name__} not found")
        return obj

    @router.put("/{id}", response_model=response_schema)
    async def update(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        id: int,
        # Lakukan hal yang sama untuk endpoint update.
        obj_in: ConcreteUpdateSchema = Body(...), #type:ignore
    ) -> ModelType:
        """
        Memperbarui item yang sudah ada.
        """
        db_obj = await service.get(db=db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{service.model.__name__} not found")
        return await service.update(db=db, db_obj=db_obj, obj_in=obj_in)

    @router.delete("/{id}", response_model=response_schema)
    async def delete(*, db: AsyncSession = Depends(deps.get_db_session), id: int) -> ModelType:
        """
        Menghapus item.
        """
        # Pastikan service Anda memiliki metode 'remove' atau 'delete'
        deleted_obj = await service.remove(db=db, id=id)
        if not deleted_obj:
            raise HTTPException(status_code=404, detail=f"{service.model.__name__} not found")
        return deleted_obj

    return router
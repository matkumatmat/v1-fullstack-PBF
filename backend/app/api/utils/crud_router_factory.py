# file: app/api/utils/crud_router_factory.py (SUDAH DIPERBAIKI)

from typing import Type, List
# ✅ LANGKAH 1: Impor 'Body' dari FastAPI
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
    """
    router = APIRouter(prefix=prefix, tags=tags)

    @router.post("/", response_model=response_schema, status_code=status.HTTP_201_CREATED)
    async def create(
        *,
        db: AsyncSession = Depends(deps.get_db_session),
        # ✅ LANGKAH 2: Tambahkan '= Body(...)' untuk menandai ini sebagai Request Body yang wajib diisi.
        obj_in: CreateSchemaType = Body(...),
    ) -> ModelType:
        """
        Create a new item.
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
        Retrieve a list of items.
        """
        return await service.get_multi(db=db, skip=skip, limit=limit)

    @router.get("/{id}", response_model=response_schema)
    async def get_by_id(*, db: AsyncSession = Depends(deps.get_db_session), id: int) -> ModelType:
        """
        Retrieve a single item by ID.
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
        # ✅ LANGKAH 2 (Bonus): Terapkan perbaikan yang sama pada endpoint update untuk konsistensi.
        obj_in: UpdateSchemaType = Body(...),
    ) -> ModelType:
        """
        Update an existing item.
        """
        db_obj = await service.get(db=db, id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{service.model.__name__} not found")
        return await service.update(db=db, db_obj=db_obj, obj_in=obj_in)

    @router.delete("/{id}", response_model=response_schema)
    async def delete(*, db: AsyncSession = Depends(deps.get_db_session), id: int) -> ModelType:
        """
        Delete an item.
        """
        deleted_obj = await service.remove(db=db, id=id)
        if not deleted_obj:
            raise HTTPException(status_code=404, detail=f"{service.model.__name__} not found")
        return deleted_obj

    return router
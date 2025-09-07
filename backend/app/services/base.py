# file: app/services/base.py

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete

from app.models.base import BaseModel as DBModel

# Definisikan tipe generik untuk model dan skema kita
ModelType = TypeVar("ModelType", bound=DBModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Kelas CRUD generik dengan metode async untuk Create, Read, Update, Delete.

    **PARAMETERS**
    * `model`: Kelas model SQLAlchemy
    * `schema`: Kelas skema Pydantic (untuk respons)
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Mendapatkan satu objek berdasarkan ID."""
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Mendapatkan banyak objek dengan paginasi."""
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Membuat objek baru."""
        ### DEVIL'S ADVOCATE NOTE ###
        # Menggunakan `model_dump()` (Pydantic V2) bukan `.dict()` (V1).
        # Ini adalah cara yang benar untuk mengubah skema menjadi dict.
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Memperbarui objek yang ada di database."""
        update_data = obj_in
        if isinstance(obj_in, BaseModel):
            # `exclude_unset=True` sangat penting untuk PATCH.
            # Hanya field yang dikirim oleh klien yang akan di-update.
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if not update_data:
            return db_obj # Tidak ada yang diupdate

        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """Menghapus objek berdasarkan ID."""
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj
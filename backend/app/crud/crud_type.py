from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import Base

# Define custom types for SQLAlchemy model, Pydantic create schema, and Pydantic update schema
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD base class with async methods.

    Parameters:
        - `model`: A SQLAlchemy model class
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Get a single object by ID."""
        result = await db.execute(select(self.model).filter(self.model.id == id))
        return result.scalars().first()

    async def get_by_code(self, db: AsyncSession, code: str) -> Optional[ModelType]:
        """Get a single object by code."""
        result = await db.execute(select(self.model).filter(self.model.code == code))
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple objects with pagination."""
        result = await db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new object."""
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
        """Update an existing object."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """Remove an object by ID."""
        result = await db.execute(select(self.model).filter(self.model.id == id))
        obj = result.scalars().first()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

# Import all the type models
from app.models import type as type_models

# Create a specific CRUD object for each type model
crud_product_type = CRUDBase(type_models.ProductType)
crud_package_type = CRUDBase(type_models.PackageType)
crud_temperature_type = CRUDBase(type_models.TemperatureType)
crud_allocation_type = CRUDBase(type_models.AllocationType)
crud_movement_type = CRUDBase(type_models.MovementType)
crud_sector_type = CRUDBase(type_models.SectorType)
crud_customer_type = CRUDBase(type_models.CustomerType)
crud_document_type = CRUDBase(type_models.DocumentType)
crud_status_type = CRUDBase(type_models.StatusType)
crud_location_type = CRUDBase(type_models.LocationType)
crud_packaging_material = CRUDBase(type_models.PackagingMaterial)
crud_packaging_box_type = CRUDBase(type_models.PackagingBoxType)
crud_priority_level = CRUDBase(type_models.PriorityLevel)
crud_notification_type = CRUDBase(type_models.NotificationType)
crud_delivery_type = CRUDBase(type_models.DeliveryType)

# A dictionary to easily access the correct CRUD object by name
# This will be very useful in the API layer.
type_crud_map = {
    "product_types": crud_product_type,
    "package_types": crud_package_type,
    "temperature_types": crud_temperature_type,
    "allocation_types": crud_allocation_type,
    "movement_types": crud_movement_type,
    "sector_types": crud_sector_type,
    "customer_types": crud_customer_type,
    "document_types": crud_document_type,
    "status_types": crud_status_type,
    "location_types": crud_location_type,
    "packaging_materials": crud_packaging_material,
    "packaging_box_types": crud_packaging_box_type,
    "priority_levels": crud_priority_level,
    "notification_types": crud_notification_type,
    "delivery_types": crud_delivery_type,
}

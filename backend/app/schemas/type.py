from pydantic import BaseModel, Field
from typing import Optional, List

# A generic base schema for all "Type" models
# It includes common fields that most type models will have.
class TypeBaseSchema(BaseModel):
    code: str = Field(..., max_length=50, description="Unique code for the type")
    name: str = Field(..., max_length=100, description="Display name for the type")
    description: Optional[str] = Field(None, description="Detailed description")

    class Config:
        # This allows the Pydantic model to be created from ORM instances
        # e.g., my_schema = MySchema.from_orm(my_sqlalchemy_object)
        from_attributes = True

# Schema for creating a new type. Inherits from the base.
class TypeCreateSchema(TypeBaseSchema):
    pass

# Schema for updating a type. All fields are optional.
class TypeUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)

# Schema for reading a type, includes the database ID.
class TypeInDBSchema(TypeBaseSchema):
    id: int

# It's good practice to have separate schemas for different use cases.
# For example, a public-facing API might not expose the database ID.
class TypePublicSchema(TypeBaseSchema):
    pass

# We can also create more specific schemas if a type has unique fields.
# For example, for StatusType which has an 'entity_type'
class StatusTypeCreateSchema(TypeCreateSchema):
    entity_type: str = Field(..., description="The entity this status belongs to (e.g., SO, SHIPMENT)")

class StatusTypeUpdateSchema(TypeUpdateSchema):
    entity_type: Optional[str] = None

class StatusTypeInDBSchema(TypeInDBSchema):
    entity_type: str

# You can define more specific schemas for other types as needed.
# For now, the generic ones cover the basic CRUD operations for most types.

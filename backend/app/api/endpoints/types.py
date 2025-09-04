from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any

from app.schemas.type import TypeInDBSchema, TypeCreateSchema, TypeUpdateSchema
from app.crud.crud_type import type_crud_map
from app.database import get_db_session

router = APIRouter()

# A helper dependency to get the correct CRUD object from the map
def get_crud_from_map(type_name: str = Path(..., description="The name of the type entity, e.g., 'product_types'")):
    crud = type_crud_map.get(type_name)
    if not crud:
        raise HTTPException(status_code=404, detail=f"Type entity '{type_name}' not found.")
    return crud

@router.post("/{type_name}", response_model=TypeInDBSchema)
async def create_type(
    *,
    db: AsyncSession = Depends(get_db_session),
    crud: Any = Depends(get_crud_from_map),
    type_in: TypeCreateSchema,
) -> Any:
    """
    Create a new generic type instance.
    """
    # Check if a type with the same code already exists
    existing_type = await crud.get_by_code(db, code=type_in.code)
    if existing_type:
        raise HTTPException(
            status_code=400,
            detail=f"A type with code '{type_in.code}' already exists in this entity.",
        )

    new_type = await crud.create(db=db, obj_in=type_in)
    return new_type

@router.get("/{type_name}", response_model=List[TypeInDBSchema])
async def read_types(
    *,
    db: AsyncSession = Depends(get_db_session),
    crud: Any = Depends(get_crud_from_map),
    skip: int = 0,
    limit: int = 100,
) -> List[Any]:
    """
    Retrieve a list of types for a given entity.
    """
    types = await crud.get_multi(db, skip=skip, limit=limit)
    return types

@router.get("/{type_name}/{id}", response_model=TypeInDBSchema)
async def read_type_by_id(
    *,
    db: AsyncSession = Depends(get_db_session),
    crud: Any = Depends(get_crud_from_map),
    id: int,
) -> Any:
    """
    Get a specific type by its ID.
    """
    item = await crud.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Type not found")
    return item

@router.put("/{type_name}/{id}", response_model=TypeInDBSchema)
async def update_type(
    *,
    db: AsyncSession = Depends(get_db_session),
    crud: Any = Depends(get_crud_from_map),
    id: int,
    type_in: TypeUpdateSchema,
) -> Any:
    """
    Update a type.
    """
    db_obj = await crud.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Type not found")

    updated_type = await crud.update(db=db, db_obj=db_obj, obj_in=type_in)
    return updated_type

@router.delete("/{type_name}/{id}", response_model=TypeInDBSchema)
async def delete_type(
    *,
    db: AsyncSession = Depends(get_db_session),
    crud: Any = Depends(get_crud_from_map),
    id: int,
) -> Any:
    """
    Delete a type.
    """
    deleted_type = await crud.remove(db=db, id=id)
    if not deleted_type:
        raise HTTPException(status_code=404, detail="Type not found")
    return deleted_type

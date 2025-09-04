from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any

from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import User as UserModel
from app.crud import crud_user
from app.database import get_db_session
from app.api.endpoints.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db_session),
    user_in: UserCreate,
) -> Any:
    """
    Create a new user.
    This is a public endpoint, but in a real application,
    you might want to restrict it to superusers.
    """
    user = await crud_user.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    user = await crud_user.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists.",
        )

    new_user = await crud_user.user.create(db=db, obj_in=user_in)
    return new_user

@router.get("/me", response_model=User)
async def read_user_me(
    current_user: UserModel = Depends(get_current_user)
) -> Any:
    """
    Get the profile for the current logged-in user.
    """
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db_session),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
) -> Any:
    """
    Update the current user's profile.
    """
    user = await crud_user.user.update(db=db, db_obj=current_user, obj_in=user_in)
    return user

# In a real app, you'd add more endpoints, for example, to get a user by ID
# or to get a list of all users, likely restricted to superusers.
# @router.get("/{user_id}", response_model=User)
# async def read_user_by_id(
#     user_id: int,
#     db: AsyncSession = Depends(get_db_session),
#     current_user: UserModel = Depends(get_current_user) # Add permission check here
# ) -> Any:
#     """
#     Get a specific user by ID.
#     """
#     if current_user.role != 'superadmin' and current_user.id != user_id:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     user = await crud_user.user.get(db, id=user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

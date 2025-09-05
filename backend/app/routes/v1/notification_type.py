from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.notification_type import NotificationType, NotificationTypeCreate, NotificationTypeUpdate
import app.services.notification_type as notification_type_service

router = APIRouter()

@router.post("/", response_model=NotificationType)
async def create_notification_type(
    notification_type: NotificationTypeCreate, db: AsyncSession = Depends(get_db_session)
):
    return await notification_type_service.create_notification_type(db=db, notification_type=notification_type)

@router.get("/", response_model=List[NotificationType])
async def read_notification_types(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
):
    notification_types = await notification_type_service.get_notification_types(db, skip=skip, limit=limit)
    return notification_types

@router.get("/{notification_type_id}", response_model=NotificationType)
async def read_notification_type(notification_type_id: int, db: AsyncSession = Depends(get_db_session)):
    db_notification_type = await notification_type_service.get_notification_type(db, notification_type_id=notification_type_id)
    if db_notification_type is None:
        raise HTTPException(status_code=404, detail="NotificationType not found")
    return db_notification_type

@router.put("/{notification_type_id}", response_model=NotificationType)
async def update_notification_type(
    notification_type_id: int,
    notification_type: NotificationTypeUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    db_notification_type = await notification_type_service.update_notification_type(
        db, notification_type_id=notification_type_id, notification_type=notification_type
    )
    if db_notification_type is None:
        raise HTTPException(status_code=404, detail="NotificationType not found")
    return db_notification_type

@router.delete("/{notification_type_id}", response_model=NotificationType)
async def delete_notification_type(
    notification_type_id: int, db: AsyncSession = Depends(get_db_session)
):
    db_notification_type = await notification_type_service.delete_notification_type(db, notification_type_id=notification_type_id)
    if db_notification_type is None:
        raise HTTPException(status_code=404, detail="NotificationType not found")
    return db_notification_type
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db_session
from app.schemas.notification_type import NotificationType, NotificationTypeCreate, NotificationTypeUpdate
from app.services.notification_type import (
    create_notification_type,
    delete_notification_type,
    get_notification_type,
    get_notification_types,
    update_notification_type,
)

router = APIRouter()

@router.post("/", response_model=NotificationType)
def create_new_notification_type(
    notification_type: NotificationTypeCreate, db: Session = Depends(get_db_session)
):
    return create_notification_type(db=db, notification_type=notification_type)

@router.get("/{notification_type_id}", response_model=NotificationType)
def read_notification_type(notification_type_id: int, db: Session = Depends(get_db_session)):
    db_notification_type = get_notification_type(db, notification_type_id=notification_type_id)
    if db_notification_type is None:
        raise HTTPException(status_code=404, detail="NotificationType not found")
    return db_notification_type

@router.get("/", response_model=List[NotificationType])
def read_notification_types(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
):
    notification_types = get_notification_types(db, skip=skip, limit=limit)
    return notification_types

@router.put("/{notification_type_id}", response_model=NotificationType)
def update_existing_notification_type(
    notification_type_id: int,
    notification_type: NotificationTypeUpdate,
    db: Session = Depends(get_db_session),
):
    db_notification_type = update_notification_type(
        db, notification_type_id=notification_type_id, notification_type=notification_type
    )
    if db_notification_type is None:
        raise HTTPException(status_code=404, detail="NotificationType not found")
    return db_notification_type

@router.delete("/{notification_type_id}", response_model=NotificationType)
def delete_existing_notification_type(
    notification_type_id: int, db: Session = Depends(get_db_session)
):
    db_notification_type = delete_notification_type(db, notification_type_id=notification_type_id)
    if db_notification_type is None:
        raise HTTPException(status_code=404, detail="NotificationType not found")
    return db_notification_type

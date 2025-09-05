from sqlalchemy.orm import Session
from app.models.type import NotificationType
from app.schemas.notification_type import NotificationTypeCreate, NotificationTypeUpdate

def get_notification_type(db: Session, notification_type_id: int):
    return db.query(NotificationType).filter(NotificationType.id == notification_type_id).first()

def get_notification_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(NotificationType).offset(skip).limit(limit).all()

def create_notification_type(db: Session, notification_type: NotificationTypeCreate):
    db_notification_type = NotificationType(**notification_type.dict())
    db.add(db_notification_type)
    db.commit()
    db.refresh(db_notification_type)
    return db_notification_type

def update_notification_type(db: Session, notification_type_id: int, notification_type: NotificationTypeUpdate):
    db_notification_type = db.query(NotificationType).filter(NotificationType.id == notification_type_id).first()
    if db_notification_type:
        update_data = notification_type.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_notification_type, key, value)
        db.commit()
        db.refresh(db_notification_type)
    return db_notification_type

def delete_notification_type(db: Session, notification_type_id: int):
    db_notification_type = db.query(NotificationType).filter(NotificationType.id == notification_type_id).first()
    if db_notification_type:
        db.delete(db_notification_type)
        db.commit()
    return db_notification_type

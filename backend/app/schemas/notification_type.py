from pydantic import BaseModel
from typing import Optional

class NotificationTypeBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True
    is_email_enabled: bool = True
    is_sms_enabled: bool = False
    is_push_enabled: bool = True
    is_system_notification: bool = True
    email_template: Optional[str] = None
    sms_template: Optional[str] = None
    push_template: Optional[str] = None
    retry_count: int = 3
    retry_interval_minutes: int = 5

class NotificationTypeCreate(NotificationTypeBase):
    pass

class NotificationTypeUpdate(NotificationTypeBase):
    pass

class NotificationTypeInDBBase(NotificationTypeBase):
    id: int

    class Config:
        from_attributes = True

class NotificationType(NotificationTypeInDBBase):
    pass

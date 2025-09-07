# file: app/schemas/type/notification_type.py

from typing import Optional
from pydantic import Field
from .base import TypeBase, TypeCreate, TypeUpdate, TypeInDBBase

class NotificationTypeBase(TypeBase):
    is_active: bool = Field(default=True)
    is_email_enabled: bool = Field(default=True)
    is_sms_enabled: bool = Field(default=False)
    is_push_enabled: bool = Field(default=True)
    is_system_notification: bool = Field(default=True)
    email_template: Optional[str] = Field(default=None, max_length=100)
    sms_template: Optional[str] = Field(default=None, max_length=100)
    push_template: Optional[str] = Field(default=None, max_length=100)
    retry_count: int = Field(default=3)
    retry_interval_minutes: int = Field(default=5)

class NotificationTypeCreate(TypeCreate, NotificationTypeBase):
    pass

class NotificationTypeUpdate(TypeUpdate):
    is_active: Optional[bool] = None
    is_email_enabled: Optional[bool] = None
    is_sms_enabled: Optional[bool] = None
    is_push_enabled: Optional[bool] = None
    is_system_notification: Optional[bool] = None
    email_template: Optional[str] = None
    sms_template: Optional[str] = None
    push_template: Optional[str] = None
    retry_count: Optional[int] = None
    retry_interval_minutes: Optional[int] = None

class NotificationType(TypeInDBBase, NotificationTypeBase):
    pass
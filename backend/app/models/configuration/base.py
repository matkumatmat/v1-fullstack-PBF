# file: app/models/configuration/base.py

import uuid
from datetime import datetime
from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.database.database import Base 

@declarative_mixin
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

@declarative_mixin
class PublicIDMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    public_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), server_default=func.gen_random_uuid(), unique=True, nullable=False, index=True)


class BaseModel(Base, PublicIDMixin, TimestampMixin):
    __abstract__ = True
    
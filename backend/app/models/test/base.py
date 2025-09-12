# file: app/models/base.py

import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

# Impor Base deklaratif dari konfigurasi database Anda
from app.database import Base 

@declarative_mixin
class TimestampMixin:
    """
    Mixin yang menambahkan kolom created_at dan updated_at yang dikelola oleh server.
    Decorator @declarative_mixin menandai kelas ini agar kolomnya dapat diwariskan.
    """
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

@declarative_mixin
class PublicIDMixin:
    """
    Mixin yang menambahkan primary key integer dan public_id UUID.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    public_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), server_default=func.gen_random_uuid(), unique=True, nullable=False, index=True)


class BaseModel(Base, PublicIDMixin, TimestampMixin):
    """
    Base model kustom yang menggabungkan semua mixin yang diperlukan melalui pewarisan berganda.
    Semua model tabel Anda akan mewarisi dari kelas ini.
    
    DEVIL'S ADVOCATE FIX:
    Kita sekarang mewarisi langsung dari `Base`, `PublicIDMixin`, dan `TimestampMixin`.
    SQLAlchemy akan secara otomatis menggabungkan semua kolom dari mixin-mixin ini
    ke dalam `BaseModel` dan semua kelas yang mewarisinya.
    """
    __abstract__ = True
    
    # Kita tidak perlu lagi mendefinisikan ulang kolom di sini karena sudah diwarisi.
    # id: int
    # public_id: uuid.UUID
    # created_at: DateTime
    # updated_at: DateTime

    # Baris-baris yang menyebabkan error telah dihapus.
    # BaseModel = declarative_mixin(PublicIDMixin)(BaseModel)  <-- DIHAPUS
    # BaseModel = declarative_mixin(TimestampMixin)(BaseModel) <-- DIHAPUS
# file: app/schemas/type/base.py

import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from datetime import date, datetime  # ✅ FIXED: Import specific classes, not module


### DEVIL'S ADVOCATE NOTE ###
# Ini adalah fondasi modern kita. Satu set skema generik untuk semua
# lookup table Anda. Ini menegakkan konsistensi, validasi, dan prinsip DRY.

class TypeBase(BaseModel):
    """
    Skema dasar untuk semua model 'Tipe'.
    Mencakup validasi yang kuat dan konsisten.
    """
    # `code` harus berupa string uppercase, underscore, atau angka. Mencegah spasi atau karakter aneh.
    code: Annotated[str, Field(
        ..., # ... berarti field ini wajib diisi
        max_length=20, 
        pattern=r'^[A-Z0-9_]+$',
        description="Unique, uppercase code for the type (e.g., 'HOSPITAL', 'REGULAR')."
    )]
    
    name: Annotated[str, Field(
        ..., 
        max_length=100,
        description="Human-readable name for the type."
    )]
    
    description: Optional[str] = Field(
        None, 
        description="Optional detailed description for the type."
    )

class TypeCreate(TypeBase):
    """Skema untuk membuat tipe baru. Saat ini sama dengan Base."""
    pass

class TypeUpdate(BaseModel):
    """
    Skema untuk memperbarui tipe. Semua field opsional.
    Tidak mewarisi dari TypeBase agar `code` yang unik bisa di-handle secara berbeda jika perlu.
    """
    code: Optional[Annotated[str, Field(
        max_length=20, 
        pattern=r'^[A-Z0-9_]+$'
    )]] = None
    
    name: Optional[Annotated[str, Field(max_length=100)]] = None
    description: Optional[str] = None

class TypeInDBBase(TypeBase):
    """
    Skema dasar untuk representasi tipe dari database.
    Mencakup semua field yang dibuat oleh server.
    """
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    # Pydantic V2 `model_config` menggantikan `class Config`.
    # `from_attributes = True` adalah kunci untuk membaca data dari model SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)

class Type(TypeInDBBase):
    """Skema publik untuk membaca data Tipe."""
    pass
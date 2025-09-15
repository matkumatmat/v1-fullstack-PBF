import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from typing_extensions import Annotated
from datetime import datetime

class _Base(BaseModel):
    pass

class _WithDbMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class _PublicIdentifierMixin(BaseModel):
    public_id: uuid.UUID

class _InternalIdentifierMixin(BaseModel):
    id: int

class _TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

class FeResBase(_WithDbMixin, _PublicIdentifierMixin, _TimestampMixin, _Base):
    """
    - public_id, created_at, updated_at
    - Kemampuan untuk membaca dari objek ORM
    """
    pass

class FeResLookup(_WithDbMixin, _PublicIdentifierMixin, _Base):
    """
    Fondasi skema lookup/dropdown.
    """
    name: str 

class FePlBase(_Base):
    pass

class FePlUpdate(_Base):
    """
    Fondasi untuk skema update.
    Secara default kosong, karena semua field harus opsional dan
    didefinisikan di skema turunan.
    """
    pass    

class DbBase(_WithDbMixin, _InternalIdentifierMixin, _PublicIdentifierMixin, _TimestampMixin, _Base):
    """
    SEMUANYA: id, public_id, timestamps, dan orm_mode.
    """
    pass

class TypeBase(_Base):
    code : str
    name : str
    description: str

class TypeUpdate(FePlUpdate):
    """Pola Update untuk skema berbasis TypeBase."""
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None    



# file: app/schemas/internal/labeling/print_log_schemas.py (buat file & folder baru)

import uuid
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from app.schema.base import FePlBase, FeResBase

# --- SKEMA INPUT (PAYLOAD) ---

class LabelPrintCreate(FePlBase):
    """Payload untuk membuat log cetak label baru."""
    location_public_id: uuid.UUID
    tujuan_kirim: str
    content: Dict[str, Any] # Kita terima JSON apa adanya

# --- SKEMA RESPONSE ---

class LabelPrintResponse(FeResBase):
    """Data yang dikembalikan setelah log dibuat."""
    location_public_id: uuid.UUID
    tujuan_kirim: str
    content: Dict[str, Any]
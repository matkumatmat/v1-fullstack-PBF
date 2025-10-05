# file: app/models/labeling/print_log.py (buat file & folder baru)

from sqlalchemy import (
    String, ForeignKey, Integer, JSON
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Dict, Any

from ..configuration import BaseModel
from ..users.customer import Location # Impor Location

class LabelPrintLog(BaseModel):
    """
    Merekam satu event pencetakan label.
    Satu request dari frontend = satu baris di tabel ini.
    """
    __tablename__ = 'label_print_logs'
    
    # Siapa yang punya log ini?
    location_id: Mapped[int] = mapped_column(ForeignKey('locations.id'), nullable=False)
    
    # Data tambahan yang dikirim frontend
    tujuan_kirim: Mapped[str] = mapped_column(String(255), comment="Hasil olahan string alamat dari frontend")
    
    # Inti dari log: konten yang dicetak, disimpan sebagai JSONB.
    # Strukturnya persis kayak JSON yang lo kasih.
    content: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False)
    
    # Relasi (opsional, tapi bagus buat query)
    location: Mapped[Location] = relationship()
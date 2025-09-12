# file: app/schemas/process/consignment.py
from pydantic import BaseModel, Field
from typing import List

class ConsignmentItemPayload(BaseModel):
    source_allocation_id: int = Field(..., description="ID dari Alokasi REGULAR_STOCK.")
    quantity: int = Field(..., gt=0, description="Jumlah yang akan dikonsinyasikan dari alokasi ini.")
    # Tambahkan field lain jika perlu, misal harga jual yang disepakati
    selling_price: float

class ConsignmentReallocationPayload(BaseModel):
    consignment_agreement_id: int = Field(..., description="ID dari perjanjian konsinyasi.")
    items: List[ConsignmentItemPayload] = Field(..., min_length=1)
    # Tambahkan field lain untuk master Consignment, misal nomor dokumen
    consignment_number: str
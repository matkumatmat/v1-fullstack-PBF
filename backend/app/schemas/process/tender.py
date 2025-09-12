
from pydantic import BaseModel, Field

class TenderReallocationPayload(BaseModel):
    source_allocation_id: int = Field(..., description="ID dari Alokasi REGULAR_STOCK yang akan diambil kuantitasnya.")
    tender_contract_id: int = Field(..., description="ID dari TenderContract yang relevan.")
    quantity: int = Field(..., gt=0, description="Jumlah yang akan dire-alokasi untuk tender.")
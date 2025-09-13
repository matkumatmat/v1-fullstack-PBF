import uuid
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict

# Gunakan TYPE_CHECKING untuk type hinting tanpa menyebabkan circular import
if TYPE_CHECKING:
    from ..product.allocation import Allocation
    from ..order_process.sales_order import SalesOrder

# ===================================================================
# SKEMA UNTUK PROSES (PAYLOAD)
# ===================================================================

class TenderReallocationPayload(BaseModel):
    source_allocation_id: int = Field(..., description="ID dari Alokasi REGULAR_STOCK yang akan diambil kuantitasnya.")
    tender_contract_id: int = Field(..., description="ID dari TenderContract yang relevan.")
    quantity: int = Field(..., gt=0, description="Jumlah yang akan dire-alokasi untuk tender.")

# ===================================================================
# SKEMA UNTUK DATA (READ & WRITE MODELS)
# ===================================================================

# --- Skema untuk ContractReservation ---

class ContractReservationBase(BaseModel):
    """Skema dasar untuk ContractReservation."""
    contract_id: int
    product_id: int
    batch_id: int
    allocation_id: int
    reserved_quantity: int
    remaining_quantity: int

class ContractReservationCreate(ContractReservationBase):
    """Skema untuk membuat ContractReservation (biasanya digunakan internal oleh service)."""
    pass

class ContractReservation(ContractReservationBase):
    """Skema read untuk ContractReservation."""
    id: int
    allocated_quantity: int
    created_at: datetime

    # Relasi bisa ditambahkan jika perlu, tapi seringkali tidak dibutuhkan di level ini
    # allocation: Optional['Allocation'] = None

    model_config = ConfigDict(from_attributes=True)

# --- Skema untuk TenderContract ---

class TenderContractBase(BaseModel):
    """Skema dasar untuk TenderContract."""
    contract_number: str = Field(..., max_length=50)
    contract_date: date
    contract_value: Optional[float] = None
    start_date: date
    end_date: date
    tender_reference: Optional[str] = Field(None, max_length=100)
    tender_winner: Optional[str] = Field(None, max_length=100)
    status: str = Field("ACTIVE", max_length=20)
    erp_contract_id: Optional[str] = Field(None, max_length=50)
    contract_document_url: Optional[str] = Field(None, max_length=255)

class TenderContractCreate(TenderContractBase):
    """Skema untuk membuat TenderContract baru."""
    pass

class TenderContractUpdate(BaseModel):
    """Skema untuk memperbarui TenderContract. Semua field opsional."""
    contract_number: Optional[str] = Field(None, max_length=50)
    contract_date: Optional[date] = None
    contract_value: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    tender_reference: Optional[str] = Field(None, max_length=100)
    tender_winner: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=20)
    erp_contract_id: Optional[str] = Field(None, max_length=50)
    contract_document_url: Optional[str] = Field(None, max_length=255)

class TenderContract(TenderContractBase):
    """Skema read untuk TenderContract, termasuk relasi."""
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    # Relasi
    contract_reservations: List[ContractReservation] = []
    sales_orders: List['SalesOrder'] = []

    model_config = ConfigDict(from_attributes=True)
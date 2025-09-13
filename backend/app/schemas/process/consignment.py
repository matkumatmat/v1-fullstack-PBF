import uuid
from datetime import date, datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, Field, ConfigDict

# Gunakan TYPE_CHECKING untuk type hinting tanpa menyebabkan circular import
if TYPE_CHECKING:
    from ..customer.customer import Customer
    from ..product.product import Product
    from ..product.batch import Batch
    # from ..order_process.shipment import Shipment # Jika skema Shipment ada

# ===================================================================
# SKEMA UNTUK PROSES (PAYLOAD)
# ===================================================================

class ConsignmentItemPayload(BaseModel):
    source_allocation_id: int = Field(..., description="ID dari Alokasi REGULAR_STOCK.")
    quantity: int = Field(..., gt=0, description="Jumlah yang akan dikonsinyasikan dari alokasi ini.")
    selling_price: float = Field(..., description="Harga jual per unit yang disepakati untuk konsinyasi.")

class ConsignmentReallocationPayload(BaseModel):
    consignment_agreement_id: int = Field(..., description="ID dari perjanjian konsinyasi.")
    items: List[ConsignmentItemPayload] = Field(..., min_length=1)
    consignment_number: str = Field(..., description="Nomor dokumen untuk pengiriman konsinyasi ini.")

# ===================================================================
# SKEMA UNTUK DATA (READ & WRITE MODELS)
# ===================================================================

# --- Skema untuk ConsignmentAgreement ---
class ConsignmentAgreementBase(BaseModel):
    agreement_number: str = Field(..., max_length=50)
    customer_id: int
    agreement_date: date
    start_date: date
    end_date: Optional[date] = None
    commission_rate: Optional[float] = None
    payment_terms_days: int = 30
    return_policy_days: int = 90
    status: str = Field("ACTIVE", max_length=20)

class ConsignmentAgreementCreate(ConsignmentAgreementBase):
    pass

class ConsignmentAgreementUpdate(BaseModel):
    agreement_number: Optional[str] = Field(None, max_length=50)
    # ... tambahkan field lain yang bisa diupdate
    status: Optional[str] = Field(None, max_length=20)

# --- Skema untuk ConsignmentSale ---
class ConsignmentSale(BaseModel):
    id: int
    sale_number: str
    sale_date: date
    quantity_sold: int
    total_value: float
    status: str
    model_config = ConfigDict(from_attributes=True)

# --- Skema untuk ConsignmentReturn ---
class ConsignmentReturn(BaseModel):
    id: int
    return_number: str
    return_date: date
    quantity_returned: int
    return_reason: Optional[str] = None
    status: str
    model_config = ConfigDict(from_attributes=True)

# --- Skema untuk ConsignmentItem ---
class ConsignmentItem(BaseModel):
    id: int
    product_id: int
    batch_id: int
    quantity_shipped: int
    quantity_sold: int
    quantity_returned: int
    status: str
    # product: Optional['Product'] = None # Bisa di-enable jika perlu
    # batch: Optional['Batch'] = None   # Bisa di-enable jika perlu
    model_config = ConfigDict(from_attributes=True)

# --- Skema untuk Consignment ---
class ConsignmentBase(BaseModel):
    consignment_number: str
    agreement_id: int
    consignment_date: date
    status: str

class Consignment(ConsignmentBase):
    id: int
    public_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    # Relasi
    items: List[ConsignmentItem] = []
    sales: List[ConsignmentSale] = []
    returns: List[ConsignmentReturn] = []
    # agreement: Optional['ConsignmentAgreement'] = None # Hindari relasi kembali ke parent
    
    model_config = ConfigDict(from_attributes=True)

# --- Skema untuk ConsignmentAgreement (Read Model Lengkap) ---
class ConsignmentAgreement(ConsignmentAgreementBase):
    id: int
    public_id: uuid.UUID
    
    # Relasi
    customer: Optional['Customer'] = None
    consignments: List[Consignment] = []

    model_config = ConfigDict(from_attributes=True)

# --- Skema untuk ConsignmentStatement ---
class ConsignmentStatement(BaseModel):
    id: int
    statement_number: str
    period_start: date
    period_end: date
    total_sold_value: Optional[float] = None
    total_commission: Optional[float] = None
    net_amount_due: Optional[float] = None
    payment_status: str
    status: str
    model_config = ConfigDict(from_attributes=True)
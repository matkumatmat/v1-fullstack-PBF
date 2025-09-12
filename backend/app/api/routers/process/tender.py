# file: app/api/v1/endpoints/tenders.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.services.process import tender
from app.schemas.product import Allocation as AllocationSchema
from app.schemas.process.tender import TenderReallocationPayload

router = APIRouter()

@router.post("/reallocate-stock", response_model=AllocationSchema)
async def reallocate_for_tender(
    payload: TenderReallocationPayload,
    db: AsyncSession = Depends(deps.get_db)
):
    """Endpoint untuk mere-alokasi stok dari reguler ke tender."""
    tender_allocation = await tender.reallocate_stock_for_tender(db, payload=payload)
    return tender_allocation
# file: app/api/v1/endpoints/consignments.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.services.process import consignment
from app.schemas import Consignment as ConsignmentSchema
from app.schemas.process.consignment import ConsignmentReallocationPayload

router = APIRouter()

@router.post("/reallocate-stock", response_model=ConsignmentSchema)
async def reallocate_for_consignment(
    payload: ConsignmentReallocationPayload,
    db: AsyncSession = Depends(deps.get_db)
):
    """Endpoint untuk mere-alokasi stok dari reguler ke konsinyasi."""
    new_consignment = await consignment.reallocate_stock_for_consignment(db, payload=payload)
    return new_consignment
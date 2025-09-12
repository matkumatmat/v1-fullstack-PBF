# file: app/api/v1/endpoints/allocations.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.services.product import allocation
from app.schemas.product import Allocation as AllocationSchema

router = APIRouter()

@router.put("/{allocation_id}/approve", response_model=AllocationSchema)
async def approve_allocation(
    allocation_id: int,
    db: AsyncSession = Depends(deps.get_db)
    # current_user: User = Depends(deps.get_current_active_user) # Tambahkan otorisasi
):
    """Endpoint untuk menyetujui alokasi yang dikarantina."""
    approved_allocation = await allocation.approve_quarantined_allocation(db, allocation_id=allocation_id)
    return approved_allocation
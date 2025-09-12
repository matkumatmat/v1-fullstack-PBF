# file: app/services/allocation_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Allocation, AllocationStatusEnum
from app.core.exceptions import NotFoundException, BadRequestException

async def approve_quarantined_allocation(db: AsyncSession, allocation_id: int) -> Allocation:
    """Mengubah status alokasi dari QUARANTINE menjadi ACTIVE."""
    allocation = await db.get(Allocation, allocation_id)
    if not allocation:
        raise NotFoundException(f"Allocation with id {allocation_id} not found.")
    
    if allocation.status != AllocationStatusEnum.QUARANTINE:
        raise BadRequestException(f"Allocation is not in QUARANTINE status. Current status: {allocation.status.name}")
        
    allocation.status = AllocationStatusEnum.ACTIVE
    db.add(allocation)
    await db.flush()
    await db.refresh(allocation)
    return allocation

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.warehouse.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate
import backend.app.services.warehouse_service as warehouse_service

router_warehouses = APIRouter(prefix="/warehouses", tags=["Warehouses"])

@router_warehouses.post("/", response_model=Warehouse, status_code=status.HTTP_201_CREATED)
async def create_warehouse_route(warehouse: WarehouseCreate, db: AsyncSession = Depends(get_db_session)):
    return await warehouse_service.create_warehouse(db=db, warehouse=warehouse)

@router_warehouses.get("/", response_model=List[Warehouse])
async def read_warehouses_route(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)):
    warehouses = await warehouse_service.get_warehouses(db, skip=skip, limit=limit)
    return warehouses

@router_warehouses.get("/{warehouse_id}", response_model=Warehouse)
async def read_warehouse_route(warehouse_id: int, db: AsyncSession = Depends(get_db_session)):
    db_warehouse = await warehouse_service.get_warehouse(db, warehouse_id=warehouse_id)
    if db_warehouse is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return db_warehouse

@router_warehouses.put("/{warehouse_id}", response_model=Warehouse)
async def update_warehouse_route(warehouse_id: int, warehouse: WarehouseUpdate, db: AsyncSession = Depends(get_db_session)):
    db_warehouse = await warehouse_service.update_warehouse(db, warehouse_id=warehouse_id, warehouse=warehouse)
    if db_warehouse is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return db_warehouse

@router_warehouses.delete("/{warehouse_id}", response_model=Warehouse)
async def delete_warehouse_route(warehouse_id: int, db: AsyncSession = Depends(get_db_session)):
    db_warehouse = await warehouse_service.delete_warehouse(db, warehouse_id=warehouse_id)
    if db_warehouse is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return db_warehouse

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.warehouse.warehouse import Rack, RackCreate, RackUpdate
import backend.app.services.warehouse_service as rack_service

router_racks = APIRouter(prefix="/racks", tags=["Racks"])

@router_racks.post("/", response_model=Rack, status_code=status.HTTP_201_CREATED)
async def create_rack_route(rack: RackCreate, db: AsyncSession = Depends(get_db_session)):
    return await rack_service.create_rack(db=db, rack=rack)

@router_racks.get("/", response_model=List[Rack])
async def read_racks_route(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)):
    racks = await rack_service.get_racks(db, skip=skip, limit=limit)
    return racks

@router_racks.get("/{rack_id}", response_model=Rack)
async def read_rack_route(rack_id: int, db: AsyncSession = Depends(get_db_session)):
    db_rack = await rack_service.get_rack(db, rack_id=rack_id)
    if db_rack is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rack not found")
    return db_rack

@router_racks.put("/{rack_id}", response_model=Rack)
async def update_rack_route(rack_id: int, rack: RackUpdate, db: AsyncSession = Depends(get_db_session)):
    db_rack = await rack_service.update_rack(db, rack_id=rack_id, rack=rack)
    if db_rack is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rack not found")
    return db_rack

@router_racks.delete("/{rack_id}", response_model=Rack)
async def delete_rack_route(rack_id: int, db: AsyncSession = Depends(get_db_session)):
    db_rack = await rack_service.delete_rack(db, rack_id=rack_id)
    if db_rack is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rack not found")
    return db_rack

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db_session
from app.schemas.warehouse.warehouse import RackAllocation, RackAllocationCreate, RackAllocationUpdate
import backend.app.services.warehouse_service as rack_allocation_service

router_rack_allocations = APIRouter(prefix="/rack_allocations", tags=["Rack Allocations"])

@router_rack_allocations.post("/", response_model=RackAllocation, status_code=status.HTTP_201_CREATED)
async def create_rack_allocation_route(rack_allocation: RackAllocationCreate, db: AsyncSession = Depends(get_db_session)):
    return await rack_allocation_service.create_rack_allocation(db=db, rack_allocation=rack_allocation)

@router_rack_allocations.get("/", response_model=List[RackAllocation])
async def read_rack_allocations_route(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)):
    rack_allocations = await rack_allocation_service.get_rack_allocations(db, skip=skip, limit=limit)
    return rack_allocations

@router_rack_allocations.get("/{rack_allocation_id}", response_model=RackAllocation)
async def read_rack_allocation_route(rack_allocation_id: int, db: AsyncSession = Depends(get_db_session)):
    db_rack_allocation = await rack_allocation_service.get_rack_allocation(db, rack_allocation_id=rack_allocation_id)
    if db_rack_allocation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RackAllocation not found")
    return db_rack_allocation

@router_rack_allocations.put("/{rack_allocation_id}", response_model=RackAllocation)
async def update_rack_allocation_route(rack_allocation_id: int, rack_allocation: RackAllocationUpdate, db: AsyncSession = Depends(get_db_session)):
    db_rack_allocation = await rack_allocation_service.update_rack_allocation(db, rack_allocation_id=rack_allocation_id, rack_allocation=rack_allocation)
    if db_rack_allocation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RackAllocation not found")
    return db_rack_allocation

@router_rack_allocations.delete("/{rack_allocation_id}", response_model=RackAllocation)
async def delete_rack_allocation_route(rack_allocation_id: int, db: AsyncSession = Depends(get_db_session)):
    db_rack_allocation = await rack_allocation_service.delete_rack_allocation(db, rack_allocation_id=rack_allocation_id)
    if db_rack_allocation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RackAllocation not found")
    return db_rack_allocation

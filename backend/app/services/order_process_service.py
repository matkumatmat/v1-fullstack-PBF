# file: app/services/order_process_service.py

from typing import List, Optional
from decimal import Decimal
from sqlalchemy import exc, func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.models.order_process import SalesOrder, SalesOrderItem, ShippingPlan, ShippingPlanItem
from app.models.users import Customer
from app.models.product import Product

from app.schemas.order_process.sales_order import SalesOrderCreate, SalesOrderUpdate
from app.schemas.order_process.shipping_plan import ShippingPlanCreate, ShippingPlanUpdate
from app.core.exceptions import NotFoundException, BadRequestException, UnprocessableEntityException
from app.models.configuration import SalesOrderStatusEnum, ShippingPlanStatusEnum


async def get_sales_order_by_id(db: AsyncSession, so_id: int) -> Optional[SalesOrder]:
    query = (
        select(SalesOrder)
        .where(SalesOrder.id == so_id)
        .options(
            selectinload(SalesOrder.items).selectinload(SalesOrderItem.product),
            selectinload(SalesOrder.customer)
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_sales_orders(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[SalesOrder]:
    query = select(SalesOrder).offset(skip).limit(limit).options(selectinload(SalesOrder.items))
    result = await db.execute(query)
    return result.scalars().all()

async def create_sales_order(db: AsyncSession, so_in: SalesOrderCreate) -> SalesOrder:
    async with db.begin_nested():
        customer_check = await db.get(Customer, so_in.customer_id)
        if not customer_check:
            raise NotFoundException(f"Customer with id {so_in.customer_id} not found.")

        so_data = so_in.model_dump(exclude={'items'})
        db_so = SalesOrder(**so_data)
        
        total_amount = Decimal("0.0")
        
        product_ids = {item.product_id for item in so_in.items}
        products_query = select(Product).where(Product.id.in_(product_ids))
        products_result = await db.execute(products_query)
        found_products = {p.id: p for p in products_result.scalars().all()}

        if len(found_products) != len(product_ids):
            missing_ids = product_ids - set(found_products.keys())
            raise NotFoundException(f"Products with following IDs not found: {missing_ids}")

        for item_in in so_in.items:
            item_total = Decimal(item_in.quantity_requested) * item_in.unit_price
            total_amount += item_total
            db_item = SalesOrderItem(**item_in.model_dump(), total_price=item_total)
            db_so.items.append(db_item)
            
        db_so.total_amount = total_amount
        
        db.add(db_so)
        await db.flush()
        await db.refresh(db_so)
        for item in db_so.items:
            await db.refresh(item)
        
    return db_so

async def update_sales_order(db: AsyncSession, so_id: int, so_in: SalesOrderUpdate) -> SalesOrder:
    db_so = await get_sales_order_by_id(db, so_id)
    if not db_so:
        raise NotFoundException(f"Sales Order with id {so_id} not found.")
        
    if so_in.status and db_so.status in [SalesOrderStatusEnum.SHIPPED, SalesOrderStatusEnum.CANCELLED]:
        raise BadRequestException(f"Cannot change status of an order that is already '{db_so.status.value}'.")

    update_data = so_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_so, key, value)
        
    await db.commit()
    await db.refresh(db_so)
    return db_so

async def delete_sales_order(db: AsyncSession, so_id: int) -> SalesOrder:
    db_so = await get_sales_order_by_id(db, so_id)
    if not db_so:
        raise NotFoundException(f"Sales Order with id {so_id} not found.")
        
    if db_so.status != SalesOrderStatusEnum.PENDING:
        raise BadRequestException(f"Cannot delete Sales Order. It is already being processed (status: '{db_so.status.value}').")
        
    await db.delete(db_so)
    await db.commit()
    return db_so

# --- ShippingPlan Services ---

async def get_shipping_plan_by_id(db: AsyncSession, plan_id: int) -> Optional[ShippingPlan]:
    query = (
        select(ShippingPlan)
        .where(ShippingPlan.id == plan_id)
        .options(
            selectinload(ShippingPlan.items),
            selectinload(ShippingPlan.sales_order)
        )
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_shipping_plans(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ShippingPlan]:
    """
    Mengambil daftar semua Shipping Plan dengan paginasi.
    """
    query = select(ShippingPlan).offset(skip).limit(limit).options(selectinload(ShippingPlan.items))
    result = await db.execute(query)
    return result.scalars().all()

async def create_shipping_plan(db: AsyncSession, plan_in: ShippingPlanCreate) -> ShippingPlan:
    async with db.begin_nested():
        so = await get_sales_order_by_id(db, plan_in.sales_order_id)
        if not so:
            raise NotFoundException(f"Sales Order with id {plan_in.sales_order_id} not found.")

        so_items_map = {item.id: item for item in so.items}
        
        planned_quantities_query = (
            select(
                ShippingPlanItem.sales_order_item_id,
                func.sum(ShippingPlanItem.quantity_to_fulfill).label("total_planned")
            )
            .join(ShippingPlan)
            .where(ShippingPlan.sales_order_id == plan_in.sales_order_id)
            .group_by(ShippingPlanItem.sales_order_item_id)
        )
        planned_quantities_result = await db.execute(planned_quantities_query)
        already_planned = {row.sales_order_item_id: row.total_planned for row in planned_quantities_result}

        for item_in in plan_in.items:
            so_item = so_items_map.get(item_in.sales_order_item_id)
            if not so_item:
                raise BadRequestException(f"Sales Order Item with id {item_in.sales_order_item_id} does not belong to Sales Order {so.id}.")
            
            previously_planned_qty = already_planned.get(item_in.sales_order_item_id, 0)
            remaining_to_plan = so_item.quantity_requested - previously_planned_qty
            
            if item_in.quantity_to_fulfill > remaining_to_plan:
                raise UnprocessableEntityException(
                    f"Cannot fulfill {item_in.quantity_to_fulfill} for SO Item {so_item.id}. "
                    f"Only {remaining_to_plan} remaining to be planned."
                )

        plan_data = plan_in.model_dump(exclude={'items'})
        db_plan = ShippingPlan(**plan_data)
        
        for item_in in plan_in.items:
            db_item = ShippingPlanItem(**item_in.model_dump())
            db_plan.items.append(db_item)
            
        db.add(db_plan)
        await db.flush()
        await db.refresh(db_plan)
        
    return db_plan

async def update_shipping_plan(db: AsyncSession, plan_id: int, plan_in: ShippingPlanUpdate) -> ShippingPlan:
    """
    Memperbarui Shipping Plan yang ada.
    """
    db_plan = await get_shipping_plan_by_id(db, plan_id)
    if not db_plan:
        raise NotFoundException(f"Shipping Plan with id {plan_id} not found.")
        
    # Validasi bisnis: Mencegah perubahan pada rencana yang sudah final.
    if db_plan.status in [ShippingPlanStatusEnum.IN_TRANSIT, ShippingPlanStatusEnum.DELIVERED]:
        raise BadRequestException(f"Cannot update a shipping plan that is already in transit or delivered.")

    update_data = plan_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_plan, key, value)
        
    await db.commit()
    await db.refresh(db_plan)
    return db_plan

async def delete_shipping_plan(db: AsyncSession, plan_id: int) -> ShippingPlan:
    """
    Menghapus Shipping Plan.
    """
    db_plan = await get_shipping_plan_by_id(db, plan_id)
    if not db_plan:
        raise NotFoundException(f"Shipping Plan with id {plan_id} not found.")
        
    # Validasi bisnis: Hanya rencana yang masih pending yang bisa dihapus.
    if db_plan.status != ShippingPlanStatusEnum.PENDING:
        raise BadRequestException(f"Cannot delete shipping plan. It is already being processed (status: '{db_plan.status.value}').")
        
    await db.delete(db_plan)
    await db.commit()
    return db_plan
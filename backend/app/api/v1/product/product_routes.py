"""
Product Routes
==============

CRUD routes untuk Product management
"""

from fastapi import APIRouter, Depends, status, Query
from typing import Dict, Any, List, Optional

from app.services import ServiceRegistry
from app.schemas import (
    ProductSchema, ProductCreateSchema, ProductUpdateSchema, BatchSchema, AllocationSchema
)
from app.dependencies import get_service_registry, get_current_user
from app.responses import APIResponse
from app.schemas.base import PaginationSchema

router = APIRouter()


@router.get("", response_model=APIResponse[List[ProductSchema]])
async def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    product_type_id: Optional[int] = Query(None),
    manufacturer: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(True),
    service_registry: ServiceRegistry = Depends(get_service_registry)
):
    """
    Get products dengan pagination dan filtering
    """
    filters = {}
    if product_type_id:
        filters['product_type_id'] = product_type_id
    if manufacturer:
        filters['manufacturer'] = manufacturer
    if is_active is not None:
        filters['is_active'] = is_active

    result = await service_registry.product.list(
        page=page,
        per_page=per_page,
        search=search,
        filters=filters
    )

    return APIResponse.paginated(
        data=result['items'],
        pagination=PaginationSchema(**result['pagination']),
        message="Products retrieved successfully"
    )


@router.post("", response_model=APIResponse[ProductSchema], status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreateSchema,
    service_registry: ServiceRegistry = Depends(get_service_registry),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create new product
    """
    product = await service_registry.product.create(
        product_data.model_dump(),
        username=current_user["username"]
    )
    return APIResponse.success(
        data=product,
        message="Product created successfully"
    )


@router.get("/{product_id}", response_model=APIResponse[ProductSchema])
async def get_product(
    product_id: int,
    service_registry: ServiceRegistry = Depends(get_service_registry)
):
    """
    Get product by ID
    """
    product = await service_registry.product.get_by_id(product_id)
    return APIResponse.success(
        data=product,
        message="Product retrieved successfully"
    )


@router.put("/{product_id}", response_model=APIResponse[ProductSchema])
async def update_product(
    product_id: int,
    product_data: ProductUpdateSchema,
    service_registry: ServiceRegistry = Depends(get_service_registry),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update product"""
    product = await service_registry.product.update(
        product_id,
        product_data.model_dump(exclude_unset=True),
        username=current_user["username"]
    )
    return APIResponse.success(
        data=product,
        message="Product updated successfully"
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    service_registry: ServiceRegistry = Depends(get_service_registry),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Soft delete product (deactivate)"""
    await service_registry.product.delete(product_id, username=current_user["username"])
    return APIResponse.success(message="Product deleted successfully")


@router.get("/code/{product_code}", response_model=APIResponse[ProductSchema])
async def get_product_by_code(
    product_code: str,
    service_registry: ServiceRegistry = Depends(get_service_registry)
):
    """Get product by product code"""
    product = await service_registry.product.get_by_code(product_code)
    return APIResponse.success(
        data=product,
        message="Product retrieved successfully"
    )


@router.get("/{product_id}/stock-summary", response_model=APIResponse[Dict[str, Any]])
async def get_product_stock_summary(
    product_id: int,
    service_registry: ServiceRegistry = Depends(get_service_registry)
):
    """Get comprehensive stock summary untuk product"""
    stock_summary = await service_registry.product.get_product_stock_summary(product_id)
    return APIResponse.success(
        data=stock_summary,
        message="Product stock summary retrieved successfully"
    )


@router.get("/{product_id}/batches", response_model=APIResponse[List[BatchSchema]])
async def get_product_batches(
    product_id: int,
    include_inactive: bool = Query(False),
    service_registry: ServiceRegistry = Depends(get_service_registry)
):
    """Get all batches untuk specific product"""
    batches = await service_registry.batch.get_batches_by_product(
        product_id,
        include_inactive=include_inactive
    )
    return APIResponse.success(
        data=batches,
        message="Product batches retrieved successfully"
    )


@router.get("/{product_id}/allocations", response_model=APIResponse[List[AllocationSchema]])
async def get_product_allocations(
    product_id: int,
    status: Optional[str] = Query(None),
    service_registry: ServiceRegistry = Depends(get_service_registry)
):
    """Get all allocations untuk specific product"""
    allocations = await service_registry.allocation.get_allocations_by_product(
        product_id,
        status=status
    )
    return APIResponse.success(
        data=allocations,
        message="Product allocations retrieved successfully"
    )


@router.post("/{product_id}/activate", response_model=APIResponse[ProductSchema])
async def activate_product(
    product_id: int,
    service_registry: ServiceRegistry = Depends(get_service_registry),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Activate product"""
    product = await service_registry.product.activate(product_id, username=current_user["username"])
    return APIResponse.success(
        data=product,
        message="Product activated successfully"
    )


@router.post("/{product_id}/deactivate", response_model=APIResponse[ProductSchema])
async def deactivate_product(
    product_id: int,
    reason: Dict[str, str],
    service_registry: ServiceRegistry = Depends(get_service_registry),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Deactivate product"""
    # Note: The 'delete' method in CRUDService handles deactivation.
    # We can pass a reason in the future if the service supports it.
    product = await service_registry.product.delete(
        product_id,
        username=current_user["username"]
    )
    return APIResponse.success(
        data=product,
        message="Product deactivated successfully"
    )
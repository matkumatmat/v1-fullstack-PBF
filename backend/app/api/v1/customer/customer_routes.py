from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional, Dict, Any

from app.dependencies import get_service_registry, get_current_user
from app.responses import APIResponse
from app.services import ServiceRegistry
from app.schemas.customer import CustomerSchema, CustomerCreateSchema, CustomerUpdateSchema
from app.schemas.base import PaginationSchema

customer_router = APIRouter()


@customer_router.post(
    "/",
    response_model=APIResponse[CustomerSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new customer"
)
async def create_customer(
    customer_data: CustomerCreateSchema,
    service_registry: ServiceRegistry = Depends(get_service_registry),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new customer in the system.
    """
    new_customer = await service_registry.customer.create(
        customer_data.model_dump(),
        username=current_user["username"]
    )
    return APIResponse.success(data=new_customer, message="Customer created successfully")


@customer_router.get(
    "/",
    response_model=APIResponse[List[CustomerSchema]],
    summary="Get a list of customers"
)
async def get_all_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    service_registry: ServiceRegistry = Depends(get_service_registry)
):
    """
    Get a paginated list of customers.
    Allows searching by name, code, legal name, or email.
    """
    result = await service_registry.customer.list(
        page=page,
        per_page=per_page,
        search=search
    )
    return APIResponse.paginated(
        data=result['items'],
        pagination=PaginationSchema(**result['pagination'])
    )


@customer_router.get(
    "/{customer_id}",
    response_model=APIResponse[CustomerSchema],
    summary="Get a single customer by ID"
)
async def get_customer_by_id(
    customer_id: int,
    service_registry: ServiceRegistry = Depends(get_service_registry)
):
    """
    Retrieve the details of a single customer by their ID.
    """
    customer = await service_registry.customer.get_by_id(customer_id)
    return APIResponse.success(data=customer)


@customer_router.put(
    "/{customer_id}",
    response_model=APIResponse[CustomerSchema],
    summary="Update a customer"
)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdateSchema,
    service_registry: ServiceRegistry = Depends(get_service_registry),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update an existing customer's details.
    """
    updated_customer = await service_registry.customer.update(
        entity_id=customer_id,
        data=customer_data.model_dump(exclude_unset=True),
        username=current_user["username"]
    )
    return APIResponse.success(data=updated_customer, message="Customer updated successfully")


@customer_router.get(
    "/search/",
    response_model=APIResponse[List[CustomerSchema]],
    summary="Search for customers"
)
async def search_customers(
    term: str = Query(..., min_length=2),
    service_registry: ServiceRegistry = Depends(get_service_registry)
):
    """
    Search for customers by name or code for autocomplete fields.
    """
    customers = await service_registry.customer.search_customers(search_term=term)
    return APIResponse.success(data=customers)

from fastapi import APIRouter

# This is the main router that will aggregate all the specific endpoint routers.
# For now, it's empty. We will add routers to it in the next steps.
api_router = APIRouter()

from .endpoints import types

# Include the generic types router
api_router.include_router(types.router, prefix="/types", tags=["Types"])

from .endpoints import users, auth

# Include the authentication router
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Include the user management router
api_router.include_router(users.router, prefix="/users", tags=["Users"])

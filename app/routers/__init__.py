from fastapi import APIRouter
from app.routers.user import user_router

v1_router = APIRouter(prefix="/v1")
# public routers
public_router = APIRouter(prefix="/public", tags=["public apis"])
public_router.include_router(user_router)

# private routers
private_router = APIRouter(prefix="/private")

# admin routers
admin_router = APIRouter(prefix="/admin")


v1_router.include_router(public_router)
v1_router.include_router(private_router)
v1_router.include_router(admin_router)


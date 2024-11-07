from fastapi import APIRouter

from src.app.api.routers.client_router import router as client_router
from src.app.core.security import router as security_router

main_router = APIRouter()

main_router.include_router(client_router, prefix="/clients", tags=["Clients"])
main_router.include_router(security_router, prefix="/security", tags=["Security"])

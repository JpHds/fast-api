from fastapi import APIRouter
from src.app.api.routers.client_router import router as client_router
from src.app.core.security import router as security_router

api_router = APIRouter()

api_router.include_router(client_router, prefix="/clients", tags=["Clients"])
api_router.include_router(security_router, prefix="/security", tags=["Security"])

from fastapi import APIRouter
from src.app.api.endpoints.clientes_router import router as cliente_router
from src.app.core.security import router as security_router

# Criando um roteador principal para a API
api_router = APIRouter()

# Incluindo as rotas dos módulos específicos
api_router.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])
api_router.include_router(security_router, prefix="/security", tags=["Security"])

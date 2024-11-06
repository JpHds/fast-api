import os
from shared import config
import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from clientes.cliente_router import router as cliente_router
from auth.auth_router import router as auth_router
from shared.database import engine, Base

if config.environment_type == 'development':
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(cliente_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

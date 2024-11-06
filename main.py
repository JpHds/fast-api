import os

import uvicorn
from fastapi import FastAPI

from clientes import cliente_router
from shared.database import engine, Base

if os.getenv('ENVIRONMENT_DEVELOP') == 'development':
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(cliente_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

import os

from src.app.api.api_router import api_router
from src.app.core import config
import uvicorn
from fastapi import FastAPI

from src.app.db.database import engine, Base

if config.environment_type == 'development':
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("APP_HOST"), port=int(os.getenv("APP_PORT")))

import os

from src.app.api.api_router import api_router
from src.app.core import config
import uvicorn
from fastapi import FastAPI

from src.app.core.dependencies import get_db
from src.app.db.database import engine, Base
from src.app.services.super_admin_service import create_super_admin

if config.ENVIRONMENT_TYPE == 'development':
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with next(get_db()) as db:
        create_super_admin(db)
app = FastAPI()
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("APP_HOST"), port=int(os.getenv("APP_PORT")))

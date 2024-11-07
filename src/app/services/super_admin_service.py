# src/app/services/admin_service.py

from sqlalchemy.orm import Session
from src.app.core.hashing import hash_password
from src.app.models.superadmin_model import SuperAdmin
import os
from dotenv import load_dotenv


load_dotenv()

SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")


def create_super_admin(db: Session):
    super_admin = db.query(SuperAdmin).filter(SuperAdmin.username == SUPER_ADMIN_USERNAME).first()

    if not super_admin:
        hashed_password = hash_password(SUPER_ADMIN_PASSWORD)
        super_admin = SuperAdmin(
            email=SUPER_ADMIN_EMAIL,
            username=SUPER_ADMIN_USERNAME,
            password=hashed_password
        )
        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)

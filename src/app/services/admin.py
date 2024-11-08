from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.app.core.exceptions import NotFound
from src.app.models.admin import Admin

class AdminService:

    @staticmethod
    def validate_admin_data(admin_data: dict, admin_id: int, db: Session):
        validation_errors = []

        admin_with_email_in_db = db.query(Admin).filter(Admin.email == admin_data["email"]).first()

        if  admin_with_email_in_db and  admin_with_email_in_db.id != admin_id:
            validation_errors.append("Email already registered.")

        admin_with_username_in_db = db.query(Admin).filter(Admin.username == admin_data["username"]).first()

        if admin_with_username_in_db and admin_with_username_in_db.id != admin_id:
            validation_errors.append("Username already taken.")

        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="; ".join(validation_errors)
            )

    @staticmethod
    def get_all_admins(db: Session) -> list[Admin]:
        admins = db.query(Admin).all()
        if not admins:
            raise NotFound("No admins found.")
        return admins

    @staticmethod
    def get_admin_by_id(db: Session, admin_id: int) -> Admin:
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            raise NotFound("Admin not found.")
        return admin

    @staticmethod
    def update_admin_by_id(db: Session, admin_id: int, admin_data: dict) -> Admin:
        admin = db.query(Admin).get(admin_id)
        if not admin:
            raise NotFound("Admin not found.")

        AdminService.validate_admin_data(admin_data, admin_id, db)

        for key, value in admin_data.items():
            setattr(admin, key, value)

        db.commit()
        db.refresh(admin)
        return admin

    @staticmethod
    def delete_admin_by_id(db: Session, admin_id: int) -> None:
        admin = db.query(Admin).get(admin_id)
        if not admin:
            raise NotFound("Admin not found.")

        db.delete(admin)
        db.commit()
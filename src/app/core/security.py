from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status

from src.app.core.hashing import hash_password
from src.app.core.jwt_handler import create_access_token, get_current_user, authenticate_admin, \
    authenticate_super_admin, is_super_admin
from src.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm

from src.app.core.dependencies import get_db
from src.app.models.admin import Admin
from src.app.models.superadmin import SuperAdmin

router = APIRouter()


class AdminRequest(BaseModel):
    email: str
    username: str
    password: str


class AdminResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True


def validate_admin_data(admin_data: dict, admin_id: Optional[id], db: Session):
    validation_errors = []

    admin_to_create = db.query(Admin).filter(
        and_(
            Admin.username == admin_data['username'],
            Admin.email == admin_data['email']
        )
    ).first()
    if admin_to_create is not None:
        validation_errors.append("User with this credentials already registered.")

    else:
        admin_with_email_in_db = db.query(Admin).filter(Admin.email == admin_data["email"]).first()

        if admin_with_email_in_db and admin_with_email_in_db.id != admin_id:
            validation_errors.append("Email already registered.")

        admin_with_username_in_db = db.query(Admin).filter(Admin.username == admin_data["username"]).first()

        if admin_with_username_in_db and admin_with_username_in_db.id != admin_id:
            validation_errors.append("Username already taken.")

    if validation_errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="; ".join(validation_errors)
        )


@router.post("/create-admin", summary="Register a new admin", response_model=AdminResponse, status_code=201)
def create_admin(create_admin_request: dict, db: Session = Depends(get_db),
                 current_super_admin: SuperAdmin = Depends(is_super_admin)):
    validate_admin_data(create_admin_request, None, db)

    hashed_password = hash_password(create_admin_request["password"])

    new_admin = Admin(email=create_admin_request["email"], username=create_admin_request["username"],
                      password=hashed_password)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


@router.post("/token", summary="Authentication endpoint to get the JWT token.")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if admin:
        jwt_claims = {"sub": admin.username, "role": "admin"}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data=jwt_claims, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    super_admin = authenticate_super_admin(db, form_data.username, form_data.password)
    if super_admin:
        jwt_claims = {"sub": super_admin.username, "role": "super_admin"}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data=jwt_claims, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/users/me", summary="Get current user information")
async def get_current_admin(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

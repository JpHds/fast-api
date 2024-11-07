from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.app.core.jwt_handler import create_access_token, get_current_user, authenticate_admin, hash_password
from src.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from src.app.models.admin_model import Admin
from src.app.core.dependencies import get_db

router = APIRouter()


class CreateAdminRequest(BaseModel):
    email: str
    username: str
    password: str


class AdminCreatedResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True

@router.post("/create-admin", summary="Registrar um novo admin", response_model=AdminCreatedResponse, status_code=201)
def create_admin(create_admin_request: CreateAdminRequest, db: Session = Depends(get_db)):
    admin_in_db = db.query(Admin).filter(Admin.email == create_admin_request.email).first()
    if admin_in_db:
        raise HTTPException(status_code=400, detail="Email já registrado")

    hashed_password = hash_password(create_admin_request.password)

    new_admin = Admin(email=create_admin_request.email, username=create_admin_request.username,
                      password=hashed_password)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


@router.post("/token", summary="Endpoint de autenticação para obter o token JWT")
async def login_admin(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    jwt_claims = {"sub": admin.username}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data=jwt_claims, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", summary="Obter informações do usuário atual")
async def get_current_admin(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

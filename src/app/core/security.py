# auth/auth_routes.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from src.app.core.jwt_handler import create_access_token, get_current_user, hash_password, authenticate_admin
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from src.app.models.admin_model import Admin
from src.app.core.dependencies import get_db

router = APIRouter()


class CreateAdminRequest(BaseModel):
    email: str
    nome: str
    senha: str


class AdminCreatedResponse(BaseModel):
    id: int
    email: str
    nome: str

    class Config:
        orm_mode = True


@router.post("/create-admin", summary="Registrar um novo admin", response_model=AdminCreatedResponse, status_code=201)
def criar_admin(create_admin_data: CreateAdminRequest, db: Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter(Admin.email == create_admin_data.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(create_admin_data.senha)

    created_admin = Admin(email= create_admin_data.email, nome=create_admin_data.nome, senha=hashed_password)

    db.add(created_admin)
    db.commit()
    db.refresh(created_admin)

    return created_admin

@router.post("/token", summary="Endpoint de autenticação para obter o token JWT")
async def generate_admin_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": admin.nome}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", summary="Obter informações do usuário atual")
async def get_current_admin(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

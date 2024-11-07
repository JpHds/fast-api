# auth/auth_routes.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from auth.jwt_handler import create_access_token, get_current_user
from pydantic import BaseModel
from sqlalchemy.orm import Session
from shared.config import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from admins.model.admin_model import Admin
from auth.jwt_handler import hash_password, authenticate_admin
from shared.dependencies import get_db

router = APIRouter(prefix="/auth")

class AdminRequest(BaseModel):
    nome: str
    senha: str

class AdminResponse(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True


@router.post("/criarAdmin", summary="Registrar um novo admin", response_model=AdminResponse, status_code=201)
def criar_admin(admin_request: AdminRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.nome == admin_request.nome).first()
    if admin:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(admin_request.senha)

    new_admin = Admin(nome = admin_request.nome, senha = hashed_password)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin

@router.post("/token", summary="Endpoint de autenticação para obter o token JWT")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):

    admin = authenticate_admin(db, form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    admin_dict = {"sub": admin.nome}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data=admin_dict, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", summary="Obter informações do usuário atual")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

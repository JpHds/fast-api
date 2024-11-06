from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from typing import List, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from clientes.model.cliente_model import Cliente
from clientes.model.cliente_status import Status
from shared.dependencies import get_db
from auth.jwt_handler import get_current_user

router = APIRouter(prefix="/clientes")

class ClienteResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    status: Status

    class Config:
        orm_mode = True
    
class ClienteRequest(BaseModel):
    nome: str
    telefone: str
    status: Status


# READ - Listar todos os clientes
@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    clientes = db.query(Cliente).all()
    if not clientes:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
    return clientes


# READ - Buscar cliente específico
@router.get("/{id_do_cliente}", response_model=ClienteResponse)
def buscar_cliente(id_do_cliente: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id_do_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


# CREATE - Cadastrar um novo cliente
@router.post("/", response_model=ClienteResponse, status_code=201)
def cadastrar_cliente(cliente_request: ClienteRequest, db: Session = Depends(get_db)):

    try:
        cliente = Cliente(**cliente_request.dict())
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar cliente: {str(e)}"
        )

# UPDATE - Editar cliente existente
@router.put("/{id_do_cliente}", response_model=ClienteResponse)
def editar_cliente(id_do_cliente: int, cliente_request: ClienteRequest, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).get(id_do_cliente)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    cliente.nome = cliente_request.nome
    cliente.telefone = cliente_request.telefone
    cliente.status = cliente_request.status

    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

# DELETE - Excluir cliente
@router.delete("/{id_do_cliente}", status_code=204)
def excluir_cliente(id_do_cliente: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).get(id_do_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    db.delete(cliente)
    db.commit()
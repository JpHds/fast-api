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


# READ
@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)) -> list[Type[Cliente]]:
    clientes = db.query(Cliente).all()  # Retrieve all clients
    if not clientes:  # Check if the list is empty
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
    return clientes


# READ 1 ITEM ONLY
@router.get("/clientes/{id_do_cliente}", response_model=ClienteResponse)
def buscar_cliente(id_do_cliente: int, db: Session = Depends(get_db)) -> Type[Cliente]:
    cliente = db.query(Cliente).filter(Cliente.id == id_do_cliente).one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return cliente


# CREATE
@router.post("/novoCliente", response_model=ClienteResponse, status_code=201)
def cadastrar_cliente(cliente_request: ClienteRequest, db: Session = Depends(get_db)) -> Cliente:

    try:
        cliente = Cliente(**cliente_request.model_dump())

        db.add(cliente)
        db.commit()
        db.refresh(cliente)

        return cliente
    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of an error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar cliente: {str(e)}"
        )

# UPDATE
@router.put("/editarCliente/{id_do_cliente}", response_model=ClienteResponse, status_code=200)
def editar_cliente(id_do_cliente: int, cliente_request: ClienteRequest, db: Session = Depends(get_db)) -> ClienteResponse:
    cliente = db.query(Cliente).get(id_do_cliente)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    if not cliente_request.nome or not cliente_request.telefone or not cliente_request.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todos os campos de informações devem ser fornecidos."
        )

    cliente.nome = cliente_request.nome
    cliente.telefone = cliente_request.telefone
    cliente.status = cliente_request.status

    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

# DELETE
@router.delete("/deletarCliente/{id_do_cliente}", status_code=204)
def excluir_cliente(id_do_cliente: int,
                    db: Session = Depends(get_db)) -> None:
    cliente = db.query(Cliente).get(id_do_cliente)
    if cliente:
        db.delete(cliente)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    db.commit()
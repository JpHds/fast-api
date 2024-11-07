from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from typing import List, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from src.app.models.client_model import Client
from src.app.models.client_model import Status
from src.app.core.dependencies import get_db
from src.app.core.jwt_handler import get_current_user

router = APIRouter()


class ClientResponse(BaseModel):
    id: int
    email: str
    username: str
    phone: str
    status: Status

    class Config:
        orm_mode = True


class ClientRequest(BaseModel):
    username: str
    email: str
    phone: str
    status: Status


# CREATE - Cadastrar um novo cliente
@router.post("/create-client", response_model=ClientResponse, status_code=201)
def create_client(client_data: ClientRequest, db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    try:
        new_client = Client(**client_data.dict())
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar cliente: {str(e)}"
        )


# READ - Listar todos os clientes
@router.get("/list_clients", response_model=List[ClientResponse])
def list_clients(db: Session = Depends(get_db),
                 current_user: dict = Depends(get_current_user)):
    clientes = db.query(Client).all()
    if not clientes:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado.")
    return clientes


# READ - Buscar cliente específico
@router.get("/{client_id}", response_model=ClientResponse)
def get_client_by_id(client_id: int, db: Session = Depends(get_db),
                     current_user: dict = Depends(get_current_user)):
    existing_client = db.query(Client).filter(Client.id == client_id).first()
    if not existing_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")
    return existing_client


# UPDATE - Editar cliente existente
@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_data: ClientRequest, db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    existing_client = db.query(Client).get(client_id)

    if not existing_client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    existing_client.username = client_data.username
    existing_client.phone = client_data.phone
    existing_client.status = client_data.status

    db.commit()
    db.refresh(existing_client)

    return existing_client


# DELETE - Excluir cliente
@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    client = db.query(Client).get(client_id)

    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado.")

    db.delete(client)
    db.commit()

    return {"detail": "Cliente excluído com sucesso."}

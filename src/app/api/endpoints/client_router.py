from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from typing import List

from sqlalchemy.orm import Session
from src.app.models.client_model import Status
from src.app.core.dependencies import get_db
from src.app.core.jwt_handler import get_current_user, is_super_admin, is_admin_or_super_admin
from src.app.services.client_service import ClientService

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


@router.post("/create-client", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client_data: ClientRequest,
                  db: Session = Depends(get_db),
                  current_user: dict = Depends(is_super_admin)):
    return ClientService.create_client(db, client_data.dict())


@router.get("/list-clients", response_model=List[ClientResponse])
def list_clients(db: Session = Depends(get_db),
                 current_user: dict = Depends(is_admin_or_super_admin())):
    return ClientService.get_all_clients(db)


@router.get("/{client_id}", response_model=ClientResponse)
def get_client_by_id(client_id: int, db: Session = Depends(get_db),
                     current_user: dict = Depends(is_admin_or_super_admin)):
    return ClientService.get_client_by_id(db, client_id)


@router.put("/{client_id}", response_model=ClientResponse)
def update_client_by_id(client_id: int, client_data: ClientRequest, db: Session = Depends(get_db),
                        current_user: dict = Depends(is_super_admin())):
    return ClientService.update_client_by_id(db, client_id, client_data.dict())


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client_by_id(client_id: int, db: Session = Depends(get_db),
                        current_user: dict = Depends(is_super_admin)):
    ClientService.delete_client_by_id(db, client_id)

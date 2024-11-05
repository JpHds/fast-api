from fastapi import APIRouter
from pydantic import BaseModel
from enum import Enum
from typing import List

router = APIRouter(prefix="/clientes")

class Status(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"
    
class ClienteResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    status: Status
    
class ClienteRequest(BaseModel):
    id: int
    nome: str
    telefone: str
    status: Status

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes() :
    return [
        ClienteResponse(
            id=1,
            nome="teste",
            telefone= "799",
            status= Status.ATIVO
        ),     
        ClienteResponse(
            id=2,
            nome="teste2",
            telefone= "798",
            status= Status.INATIVO
        ), 
        ClienteResponse(
            id=3,
            nome="teste3",
            telefone= "797",
            status= Status.SUSPENSO
        )
    ]
    
@router.post("/novoCliente", response_model=ClienteResponse, status_code=201)
def cadastrar_cliente(cliente: ClienteRequest):
    return ClienteResponse(
            id=3,
            nome="request",
            telefone= "123",
            status= Status.ATIVO
        )

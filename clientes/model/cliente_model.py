from sqlalchemy import Column, Integer, String

from clientes.model.cliente_status import Status
from shared.database import Base

class Cliente(Base):
    __tablename__ = 'clientes'

    id  = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    telefone = Column(String(15), nullable=False)
    status = Column(String, nullable=False, default=Status.ATIVO.value)

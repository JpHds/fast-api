from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from src.app.db.database import Base
from enum import Enum

class Status(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"

class Cliente(Base):
    __tablename__ = 'clientes'

    id  = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    telefone = Column(String(15), nullable=False)
    status = Column(SQLAlchemyEnum(Status), nullable=False, default=Status.ATIVO)

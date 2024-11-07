from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from src.app.db.database import Base
from enum import Enum


class Status(Enum):
    ATIVO = "ativo"
    INATIVO = "inativo"
    SUSPENSO = "suspenso"

    def __str__(self):
        return self.value.capitalize()


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)
    status = Column(SQLAlchemyEnum(Status), nullable=False, default=Status.ATIVO)

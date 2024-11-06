from sqlalchemy import Column, Integer, String

from shared.database import Base

class Admin(Base):
    __tablename__ = 'admins'

    id  = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    senha = Column(String)

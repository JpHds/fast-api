from sqlalchemy import Column, Integer, String

from src.app.db.database import Base

class Admin(Base):
    __tablename__ = 'admins'

    id  = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    nome = Column(String)
    senha = Column(String)

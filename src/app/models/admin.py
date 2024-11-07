from sqlalchemy import Column, Integer, String

from src.app.db.database import Base


class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String, nullable=False)

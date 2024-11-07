from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from src.app.models.client_model import Client
from src.app.core.exceptions import ClientNotFoundException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="security/token")


class ClientService:
    @staticmethod
    def create_client(db: Session, client_data: dict) -> Client:
        try:
            new_client = Client(**client_data)
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

    @staticmethod
    def get_all_clients(db: Session) -> list[Client]:
        clients = db.query(Client).all()
        if not clients:
            raise ClientNotFoundException("Nenhum cliente encontrado.")
        return clients

    @staticmethod
    def get_client_by_id(db: Session, client_id: int) -> Client:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ClientNotFoundException("Cliente não encontrado.")
        return client

    @staticmethod
    def update_client_by_id(db: Session, client_id: int, client_data: dict) -> Client:
        client = db.query(Client).get(client_id)
        if not client:
            raise ClientNotFoundException("Cliente não encontrado.")

        for key, value in client_data.items():
            setattr(client, key, value)

        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def delete_client_by_id(db: Session, client_id: int) -> None:
        client = db.query(Client).get(client_id)
        if not client:
            raise ClientNotFoundException("Cliente não encontrado.")

        db.delete(client)
        db.commit()

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from src.app.core.exceptions import ClientNotFoundException
from src.app.models.client import Client, Status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="security/token")


class ClientService:
    @staticmethod
    def validate_client_data(client_data: dict, db: Session):
        exceptions_list = []

        # Verificar se o email já está registrado
        client_in_db = db.query(Client).filter(Client.email == client_data["email"]).first()
        if client_in_db:
            exceptions_list.append("Email already registered.")

        # Verificar se o username já está registrado
        client_in_db = db.query(Client).filter(Client.username == client_data["username"]).first()
        if client_in_db:
            exceptions_list.append("Username already taken.")

        # Verificar se o telefone é muito longo
        if len(client_data["phone"]) > 15:
            exceptions_list.append("Phone too long.")

        if exceptions_list:
            print(exceptions_list)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="; ".join(exceptions_list)
            )

    @staticmethod
    def create_client(db: Session, client_data: dict) -> Client:
        ClientService.validate_client_data(client_data, db)
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
                detail=f"Error creating client: {str(e)}"
            )

    @staticmethod
    def get_all_clients(db: Session) -> list[Client]:
        clients = db.query(Client).all()
        if not clients:
            raise ClientNotFoundException("No clients found.")
        return clients

    @staticmethod
    def get_client_by_id(db: Session, client_id: int) -> Client:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ClientNotFoundException("Client not found.")
        return client

    @staticmethod
    def update_client_by_id(db: Session, client_id: int, client_data: dict) -> Client:
        ClientService.validate_client_data(client_data, db)
        client = db.query(Client).get(client_id)
        if not client:
            raise ClientNotFoundException("Client not found")

        for key, value in client_data.items():
            setattr(client, key, value)

        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def delete_client_by_id(db: Session, client_id: int) -> None:
        client = db.query(Client).get(client_id)
        if not client:
            raise ClientNotFoundException("Client not found.")

        db.delete(client)
        db.commit()

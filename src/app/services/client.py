from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from src.app.core.exceptions import NotFound
from src.app.models.client import Client, Status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="security/token")


class ClientService:
    @staticmethod
    def validate_client_data(client_data: dict, client_id: Optional[id], db: Session):
        validation_errors = []

        if client_id is None:
            client_to_create = db.query(Client).filter(
                or_(
                    Client.username == client_data['username'],
                    Client.email == client_data['email']
                )
            ).first()

            if client_to_create is not None:
                validation_errors.append("User with this credentials already registered.")

        else:
            client_with_email_in_db = db.query(Client).filter(Client.email == client_data["email"]).first()

            if client_with_email_in_db and client_with_email_in_db.id != client_id:
                validation_errors.append("Email already registered.")

            client_with_username_in_db = db.query(Client).filter(Client.username == client_data["username"]).first()

            if client_with_username_in_db and client_with_username_in_db.id != client_id:
                validation_errors.append("Username already taken.")

        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="; ".join(validation_errors)
            )

    @staticmethod
    def create_client(db: Session, client_data: dict) -> Client:
        ClientService.validate_client_data(client_data, None, db)
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
            raise NotFound("No clients found.")
        return clients

    @staticmethod
    def get_client_by_id(db: Session, client_id: int) -> Client:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise NotFound("Client not found.")
        return client

    @staticmethod
    def update_client_by_id(db: Session, client_id: int, client_data: dict) -> Client:
        client = db.query(Client).get(client_id)

        if not client:
            raise NotFound("Client not found")

        ClientService.validate_client_data(client_data, client_id, db)

        for key, value in client_data.items():
            setattr(client, key, value)

        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def delete_client_by_id(db: Session, client_id: int) -> None:
        client = db.query(Client).get(client_id)
        if not client:
            raise NotFound("Client not found.")

        db.delete(client)
        db.commit()

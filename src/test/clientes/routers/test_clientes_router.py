import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import jwt
from src.app.core.dependencies import get_db
from src.app.core.jwt_handler import get_current_user
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.db.database import Base

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engineTest = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engineTest)
client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    """Fixture para criar e destruir o banco de dados de testes"""
    Base.metadata.drop_all(bind=engineTest)
    Base.metadata.create_all(bind=engineTest)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def create_access_token():
    """Gera um token JWT de teste"""

    def _create_token(data: dict, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM,
                      expires_delta: timedelta = timedelta(hours=1)):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)

    return _create_token


@pytest.fixture
def client_data():
    """Dados de cliente para os testes"""
    return {
        'email': 'lucas@gmail.com',
        'username': 'Lucas',
        'phone': '987654321',
        'status': 'ativo'
    }


@pytest.fixture
def headers(create_access_token):
    """Headers com token JWT"""
    user_data = {"sub": "testuser", "id": 1}
    token = create_access_token(user_data)
    return {"Authorization": f"Bearer {token}"}


def test_create_client(db_session, client_data, headers):
    response = client.post("/clients/create-client", json=client_data, headers=headers)
    assert response.status_code == 201

    response_data = response.json()
    assert response_data['email'] == client_data['email']
    assert response_data['username'] == client_data['username']
    assert response_data['phone'] == client_data['phone']
    assert response_data['status'] == client_data['status']


def test_list_clients(db_session, client_data, headers):
    client.post("/clients/create-client", json=client_data, headers=headers)
    response = client.get("/clients/list_clients", headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1  # ajuste conforme os dados inseridos

    assert response_data[0]['email'] == client_data['email']
    assert response_data[0]['username'] == client_data['username']
    assert response_data[0]['phone'] == client_data['phone']
    assert response_data[0]['status'] == client_data['status']


def test_get_client_by_id(db_session, client_data, headers):
    response = client.post("/clients/create-client", json=client_data, headers=headers)
    client_id = response.json()['id']
    response_get = client.get(f"/clients/{client_id}", headers=headers)

    assert response_get.status_code == 200
    response_data = response_get.json()
    assert response_data['email'] == client_data['email']
    assert response_data['username'] == client_data['username']
    assert response_data['phone'] == client_data['phone']
    assert response_data['status'] == client_data['status']

    # Testando cliente não encontrado
    response_not_found = client.get("/clients/999", headers=headers)
    assert response_not_found.status_code == 404
    assert response_not_found.json()['detail'] == 'Cliente não encontrado.'

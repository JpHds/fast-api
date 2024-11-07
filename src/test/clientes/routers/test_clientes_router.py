from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import jwt
from src.app.db.database import Base
from src.app.core.dependencies import get_db
from src.app.core.jwt_handler import get_current_user
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engineTest = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engineTest)

client = TestClient(app)


# Funções auxiliares
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, secret_key: str, algorithm: str = "HS256",
                        expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "role": "super_admin"})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def recreate_tables():
    Base.metadata.drop_all(bind=engineTest)
    Base.metadata.create_all(bind=engineTest)


def override_get_current_user():
    return {"id": 1, "username": "testuser", "role": "super_admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# Função de criação de cliente
def create_client(client_data, token):
    headers = {"Authorization": f"Bearer {token}"}
    return client.post("/clientes/create-client", json=client_data, headers=headers)


# Testes

def test_create_client():
    recreate_tables()

    client_data = {'email': 'lucas@gmail.com', 'username': 'Lucas', 'phone': '987654321', 'status': 'ativo'}

    token = create_access_token({"sub": "testuser", "id": 1}, SECRET_KEY)

    response = create_client(client_data, token)

    assert response.status_code == 201

    response_data = response.json()

    assert response_data['email'] == client_data['email']
    assert response_data['username'] == client_data['username']
    assert response_data['phone'] == client_data['phone']
    assert response_data['status'] == client_data['status']


def test_list_clients():
    recreate_tables()
    client_data_1 = {'email': 'lucas@gmail.com', 'username': 'Lucas', 'phone': '987654321', 'status': 'ativo'}
    client_data_2 = {'email': 'maria@gmail.com', 'username': 'Maria', 'phone': '123456789', 'status': 'inativo'}
    token = create_access_token({"sub": "testuser", "id": 1}, SECRET_KEY)

    create_client(client_data_1, token)
    create_client(client_data_2, token)

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/clientes/list-clients", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_client_by_id():
    recreate_tables()
    client_data_1 = {'email': 'lucas@gmail.com', 'username': 'Lucas', 'phone': '987654321', 'status': 'ativo'}
    client_data_2 = {'email': 'maria@gmail.com', 'username': 'Maria', 'phone': '123456789', 'status': 'inativo'}
    token = create_access_token({"sub": "testuser", "id": 1}, SECRET_KEY)

    response_1 = create_client(client_data_1, token)
    response_2 = create_client(client_data_2, token)

    client_id_1 = response_1.json()['id']
    client_id_2 = response_2.json()['id']

    headers = {"Authorization": f"Bearer {token}"}
    response_1_get = client.get(f"/clientes/{client_id_1}", headers=headers)
    response_2_get = client.get(f"/clientes/{client_id_2}", headers=headers)

    assert response_1_get.status_code == 200
    assert response_2_get.status_code == 200


def test_update_client():
    recreate_tables()
    client_data = {'email': 'lucas@gmail.com', 'username': 'Lucas', 'phone': '987654321', 'status': 'ativo'}
    token = create_access_token({"sub": "testuser", "id": 1}, SECRET_KEY)

    response_create = create_client(client_data, token)
    client_id = response_create.json()['id']

    updated_client_data = {'username': 'Lucas Updated', 'email': '<EMAIL>', 'phone': '123456789', 'status': 'inativo'}
    headers = {"Authorization": f"Bearer {token}"}
    response_update = client.put(f"/clientes/{client_id}", json=updated_client_data, headers=headers)

    assert response_update.status_code == 200
    updated_client = response_update.json()
    assert updated_client['username'] == updated_client_data['username']
    assert updated_client['phone'] == updated_client_data['phone']
    assert updated_client['status'] == updated_client_data['status']


def test_delete_client():
    recreate_tables()
    client_data = {'email': 'lucas@gmail.com', 'username': 'Lucas', 'phone': '987654321', 'status': 'ativo'}
    token = create_access_token({"sub": "testuser", "id": 1}, SECRET_KEY)

    response_create = create_client(client_data, token)
    client_id = response_create.json()['id']

    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/clientes/{client_id}", headers=headers)

    assert response.status_code == 204
    assert not response.content, "Esperado conteúdo vazio para status code 204."

    response = client.get(f"/clientes/{client_id}", headers=headers)
    assert response.status_code == 404
    assert "Cliente não encontrado" in response.json().get("detail")

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
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def recreateTableToTesting():
    Base.metadata.drop_all(bind=engineTest)
    Base.metadata.create_all(bind=engineTest)


def override_get_current_user():
    return {"id": 1, "username": "testuser"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_create_client():
    recreateTableToTesting()

    client_data = {
        'email': 'lucas@gmail.com',
        'username': 'Lucas',
        'phone': '987654321',
        'status': 'ativo'
    }

    user_data = {"sub": "testuser", "id": 1}
    token = create_access_token(user_data, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post("/clientes/create-client", json=client_data, headers=headers)

    assert response.status_code == 201

    response_data = response.json()
    assert response_data['email'] == client_data['email']
    assert response_data['username'] == client_data['username']
    assert response_data['phone'] == client_data['phone']
    assert response_data['status'] == client_data['status']


def test_list_clients():
    recreateTableToTesting()

    client_data_1 = {
        'email': 'lucas@gmail.com',
        'username': 'Lucas',
        'phone': '987654321',
        'status': 'ativo'
    }
    client_data_2 = {
        'email': 'maria@gmail.com',
        'username': 'Maria',
        'phone': '123456789',
        'status': 'inativo'
    }

    user_data = {"sub": "testuser", "id": 1}
    token = create_access_token(user_data, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    client.post("/clientes/create-client", json=client_data_1, headers=headers)
    client.post("/clientes/create-client", json=client_data_2, headers=headers)

    response = client.get("/clientes/list_clients", headers=headers)

    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data) == 2

    assert response_data[0]['email'] == client_data_1['email']
    assert response_data[0]['username'] == client_data_1['username']
    assert response_data[0]['phone'] == client_data_1['phone']
    assert response_data[0]['status'] == client_data_1['status']

    assert response_data[1]['email'] == client_data_2['email']
    assert response_data[1]['username'] == client_data_2['username']
    assert response_data[1]['phone'] == client_data_2['phone']
    assert response_data[1]['status'] == client_data_2['status']


def test_get_client_by_id():
    recreateTableToTesting()

    client_data_1 = {
        'email': 'lucas@gmail.com',
        'username': 'Lucas',
        'phone': '987654321',
        'status': 'ativo'
    }
    client_data_2 = {
        'email': 'maria@gmail.com',
        'username': 'Maria',
        'phone': '123456789',
        'status': 'inativo'
    }

    user_data = {"sub": "testuser", "id": 1}
    token = create_access_token(user_data, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response_1 = client.post("/clientes/create-client", json=client_data_1, headers=headers)
    response_2 = client.post("/clientes/create-client", json=client_data_2, headers=headers)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    client_id_1 = response_1.json()['id']
    client_id_2 = response_2.json()['id']

    response_1_get = client.get(f"/clientes/{client_id_1}", headers=headers)
    response_2_get = client.get(f"/clientes/{client_id_2}", headers=headers)

    assert response_1_get.status_code == 200
    assert response_2_get.status_code == 200

    response_data_1 = response_1_get.json()
    response_data_2 = response_2_get.json()

    assert response_data_1['email'] == client_data_1['email']
    assert response_data_1['username'] == client_data_1['username']
    assert response_data_1['phone'] == client_data_1['phone']
    assert response_data_1['status'] == client_data_1['status']

    assert response_data_2['email'] == client_data_2['email']
    assert response_data_2['username'] == client_data_2['username']
    assert response_data_2['phone'] == client_data_2['phone']
    assert response_data_2['status'] == client_data_2['status']

    response_not_found = client.get("/clientes/999", headers=headers)
    assert response_not_found.status_code == 404
    assert response_not_found.json()['detail'] == 'Cliente não encontrado.'


def test_update_client():
    recreateTableToTesting()

    client_data = {
        'email': 'lucas@gmail.com',
        'username': 'Lucas',
        'phone': '987654321',
        'status': 'ativo'
    }

    user_data = {"sub": "testuser", "id": 1}
    token = create_access_token(user_data, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response_create = client.post("/clientes/create-client", json=client_data, headers=headers)
    assert response_create.status_code == 201

    client_id = response_create.json()['id']

    updated_client_data = {
        'username': 'Lucas Updated',
        'email': '<EMAIL>',
        'phone': '123456789',
        'status': 'inativo'
    }

    response_update = client.put(f"/clientes/{client_id}", json=updated_client_data, headers=headers)

    assert response_update.status_code == 200

    updated_client = response_update.json()
    assert updated_client['username'] == updated_client_data['username']
    assert updated_client['phone'] == updated_client_data['phone']
    assert updated_client['status'] == updated_client_data['status']

    response_not_found = client.put("/clientes/999", json=updated_client_data, headers=headers)
    assert response_not_found.status_code == 404


def test_delete_client():
    recreateTableToTesting()

    client_data = {
        'email': 'lucas@gmail.com',
        'username': 'Lucas',
        'phone': '987654321',
        'status': 'ativo'
    }

    user_data = {"sub": "testuser", "id": 1}
    token = create_access_token(user_data, SECRET_KEY)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post("/clientes/create-client", json=client_data, headers=headers)

    assert response.status_code == 201

    created_client = response.json()
    client_id = created_client['id']

    response = client.delete(f"/clientes/{client_id}", headers=headers)

    assert response.status_code == 204

    assert not response.content, "Esperado conteúdo vazio para status code 204."

    response = client.get(f"/clientes/{client_id}", headers=headers)

    assert response.status_code == 404

    assert "Cliente não encontrado" in response.json().get("detail")

from http.client import responses

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from shared.database import engine, Base
from shared.dependencies import get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engineTest = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engineTest)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def recreateTableToTesting():
    Base.metadata.drop_all(bind=engineTest)
    Base.metadata.create_all(bind=engineTest)


def test_deve_listar_clientes():
    # Recriar a tabela para garantir que não haja dados antigos
    Base.metadata.drop_all(bind=engineTest)
    Base.metadata.create_all(bind=engineTest)

    # Criar clientes com status passados como strings (valores da enumeração)
    client.post("/clientes/novoCliente/", json={'nome': 'Joao', 'telefone': '123456', 'status': 'ativo'})
    client.post("/clientes/novoCliente/", json={'nome': 'Maria', 'telefone': '321654', 'status': 'suspenso'})
    client.post("/clientes/novoCliente/", json={'nome': 'Rita', 'telefone': '234124', 'status': 'inativo'})

    # Chamar o endpoint para listar os clientes
    response = client.get("/clientes")

    # Verificar se a resposta foi bem-sucedida
    assert response.status_code == 200

    # Verificar se a resposta contém a lista de clientes com os status corretos
    assert response.json() == [
        {'nome': 'Joao', 'telefone': '123456', 'status':'ativo'},
        {'nome': 'Maria', 'telefone': '321654', 'status':'suspenso'},
        {'nome': 'Rita', 'telefone': '234124', 'status':'inativo'}
    ]

# def test_deve_criar_novo_cliente():
#     novo_cliente = {
#         'id': 3,
#         'nome': 'request',
#         'telefone': '123',
#         'status': 'ativo'
#     }
#
#     novo_cliente_copy = novo_cliente.copy()
#     novo_cliente_copy["id"] = 3
#
#     response = client.post("/clientes/novoCliente", json=novo_cliente)
#     assert response.status_code == 201
#     assert response.json() == novo_cliente_copy

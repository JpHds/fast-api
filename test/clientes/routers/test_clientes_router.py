from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_deve_listar_clientes():
    response = client.get("/clientes/")
    
    assert response.status_code == 200
    
    assert response.json() == [
        {'id': 1, 'nome': 'teste', 'telefone': '799', 'status': 'ativo'},
        {'id': 2, 'nome': 'teste2', 'telefone': '798', 'status': 'inativo'},
        {'id': 3, 'nome': 'teste3', 'telefone': '797', 'status': 'suspenso'}
    ]
    
def test_deve_criar_novo_cliente():
    novo_cliente = {
        'id': 3,
        'nome': 'request',
        'telefone': '123',
        'status': 'ativo'
    }
    
    novo_cliente_copy = novo_cliente.copy()
    novo_cliente_copy["id"] = 3
    
    response = client.post("/clientes/novoCliente", json=novo_cliente)
    assert response.status_code == 201
    assert response.json() == novo_cliente_copy
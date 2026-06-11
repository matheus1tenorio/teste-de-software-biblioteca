import pytest
from src.cliente_service.app import app
from src.cliente_service.config import get_connection


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_criar_cliente(client):
    email = "teste_integration@email.com"

    response = client.post("/clientes", json={
        "nome": "Matheus Integration",
        "email": email,
        "matricula": "2024001"
    })

    assert response.status_code == 201
    assert response.json["mensagem"] == "Cliente criado com sucesso"


def test_listar_clientes(client):
    response = client.get("/clientes")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_buscar_cliente(client):
    email = "buscar_integration@email.com"

    client.post("/clientes", json={
        "nome": "Buscar Cliente",
        "email": email,
        "matricula": "2024002"
    })

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM cliente WHERE email = %s", (email,))
    cliente = cursor.fetchone()
    conn.close()

    response = client.get(f"/clientes/{cliente['id']}")

    assert response.status_code == 200
    assert response.json["email"] == email


def test_editar_cliente(client):
    email = "editar_integration@email.com"

    client.post("/clientes", json={
        "nome": "Original",
        "email": email,
        "matricula": "2024003"
    })

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM cliente WHERE email = %s", (email,))
    cliente = cursor.fetchone()
    conn.close()

    response = client.put(f"/clientes/{cliente['id']}", json={
        "nome": "Editado",
        "email": email,
        "matricula": "9999999"
    })

    assert response.status_code == 200
    assert response.json["mensagem"] == "Cliente atualizado com sucesso"


def test_remover_cliente(client):
    email = "delete_integration@email.com"

    client.post("/clientes", json={
        "nome": "Delete",
        "email": email,
        "matricula": "2024004"
    })

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM cliente WHERE email = %s", (email,))
    cliente = cursor.fetchone()
    conn.close()

    response = client.delete(f"/clientes/{cliente['id']}")

    assert response.status_code == 200
    assert response.json["mensagem"] == "Cliente removido com sucesso"


def test_cliente_nao_encontrado(client):
    response = client.get("/clientes/999999")

    assert response.status_code == 404
    assert "erro" in response.json
from flask import Flask
from routes.cliente_routes import cliente_bp
from unittest.mock import patch

import pytest

# Ajuste de import para funcionar corretamente
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cliente_service')))


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(cliente_bp)

    with app.test_client() as client:
        yield client

@patch("routes.cliente_routes.listar_clientes")
def test_get_clientes(mock_listar, client):

    mock_listar.return_value = [
        {"id": 1, "nome": "João"},
        {"id": 2, "nome": "Maria"}
    ]

    response = client.get("/clientes")

    assert response.status_code == 200

    assert response.get_json() == [
        {"id": 1, "nome": "João"},
        {"id": 2, "nome": "Maria"}
    ]

@patch("routes.cliente_routes.buscar_cliente")
def test_get_cliente_existente(mock_buscar, client):

    mock_buscar.return_value = {
        "id": 1,
        "nome": "João"
    }

    response = client.get("/clientes/1")

    assert response.status_code == 200

    assert response.get_json() == {
        "id": 1,
        "nome": "João"
    }

@patch("routes.cliente_routes.buscar_cliente")
def test_get_cliente_inexistente(mock_buscar, client):

    mock_buscar.return_value = None

    response = client.get("/clientes/999")

    assert response.status_code == 404

    assert response.get_json() == {
        "erro": "Cliente não encontrado"
    }


@patch("routes.cliente_routes.adicionar_cliente")
def test_post_cliente(mock_adicionar, client):

    mock_adicionar.return_value = (
        {"mensagem": "Cliente criado"},
        201
    )

    novo_cliente = {
        "nome": "Pedro"
    }

    response = client.post(
        "/clientes",
        json=novo_cliente
    )

    assert response.status_code == 201

    assert response.get_json() == {
        "mensagem": "Cliente criado"
    }


@patch("routes.cliente_routes.editar_cliente")
def test_put_cliente(mock_editar, client):

    mock_editar.return_value = (
        {"mensagem": "Cliente atualizado"},
        200
    )

    response = client.put(
        "/clientes/1",
        json={"nome": "Carlos"}
    )

    assert response.status_code == 200

    assert response.get_json() == {
        "mensagem": "Cliente atualizado"
    }


@patch("routes.cliente_routes.remover_cliente")
def test_delete_cliente(mock_remover, client):

    mock_remover.return_value = (
        {"mensagem": "Cliente removido"},
        200
    )

    response = client.delete("/clientes/1")

    assert response.status_code == 200

    assert response.get_json() == {
        "mensagem": "Cliente removido"
    }




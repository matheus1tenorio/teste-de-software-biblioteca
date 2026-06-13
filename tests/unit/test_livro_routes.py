import pytest
from flask import Flask
from unittest.mock import patch

from routes.livro_routes import livro_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(livro_bp)

    with app.test_client() as client:
        yield client


@patch("routes.livro_routes.listar_livros")
def test_listar_livros(mock_listar, client):

    mock_listar.return_value = [
        {
            "id": 1,
            "titulo": "Dom Casmurro"
        }
    ]

    response = client.get("/livros")

    assert response.status_code == 200

    assert response.get_json() == [
        {
            "id": 1,
            "titulo": "Dom Casmurro"
        }
    ]


@patch("routes.livro_routes.buscar_livro")
def test_buscar_livro_existente(mock_buscar, client):

    mock_buscar.return_value = {
        "id": 1,
        "titulo": "Dom Casmurro"
    }

    response = client.get("/livros/1")

    assert response.status_code == 200

    assert response.get_json() == {
        "id": 1,
        "titulo": "Dom Casmurro"
    }


@patch("routes.livro_routes.buscar_livro")
def test_buscar_livro_inexistente(mock_buscar, client):

    mock_buscar.return_value = None

    response = client.get("/livros/999")

    assert response.status_code == 404

    assert response.get_json() == {
        "erro": "Livro não encontrado"
    }


@patch("routes.livro_routes.criar_livro")
def test_criar_livro(mock_criar, client):

    mock_criar.return_value = (
        {"mensagem": "Livro criado"},
        201
    )

    response = client.post(
        "/livros",
        json={
            "titulo": "Dom Casmurro"
        }
    )

    assert response.status_code == 201

    assert response.get_json() == {
        "mensagem": "Livro criado"
    }


@patch("routes.livro_routes.editar_livro")
def test_editar_livro(mock_editar, client):

    mock_editar.return_value = (
        {"mensagem": "Livro atualizado"},
        200
    )

    response = client.put(
        "/livros/1",
        json={
            "titulo": "Memórias Póstumas"
        }
    )

    assert response.status_code == 200

    assert response.get_json() == {
        "mensagem": "Livro atualizado"
    }


@patch("routes.livro_routes.alterar_status")
def test_alterar_status_sucesso(mock_status, client):

    response = client.put(
        "/livros/1/status",
        json={
            "disponivel": True
        }
    )

    assert response.status_code == 200

    assert response.get_json() == {
        "mensagem": "Status atualizado"
    }


def test_alterar_status_sem_campo_disponivel(client):

    response = client.put(
        "/livros/1/status",
        json={}
    )

    assert response.status_code == 400

    assert response.get_json() == {
        "erro": "Campo 'disponivel' obrigatório"
    }


@patch("routes.livro_routes.remover_livro")
def test_remover_livro(mock_remover, client):

    mock_remover.return_value = (
        {"mensagem": "Livro removido"},
        200
    )

    response = client.delete("/livros/1")

    assert response.status_code == 200

    assert response.get_json() == {
        "mensagem": "Livro removido"
    }
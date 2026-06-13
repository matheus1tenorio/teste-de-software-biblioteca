import pytest
from flask import Flask
from unittest.mock import patch

from routes.emprestimo_routes import emprestimo_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(emprestimo_bp)

    with app.test_client() as client:
        yield client


@patch("routes.emprestimo_routes.listar_emprestimos")
def test_listar_emprestimos(mock_listar, client):

    mock_listar.return_value = [
        {
            "id": 1,
            "cliente_id": 1,
            "livro_id": 1
        }
    ]

    response = client.get("/emprestimos")

    assert response.status_code == 200

    assert response.get_json() == [
        {
            "id": 1,
            "cliente_id": 1,
            "livro_id": 1
        }
    ]


@patch("routes.emprestimo_routes.criar_emprestimo")
def test_criar_emprestimo(mock_criar, client):

    mock_criar.return_value = (
        {"mensagem": "Empréstimo criado"},
        201
    )

    dados = {
        "cliente_id": 1,
        "livro_id": 1
    }

    response = client.post(
        "/emprestimos",
        json=dados
    )

    assert response.status_code == 201

    assert response.get_json() == {
        "mensagem": "Empréstimo criado"
    }


@patch("routes.emprestimo_routes.devolver_livro")
def test_devolver_livro(mock_devolver, client):

    mock_devolver.return_value = (
        {"mensagem": "Livro devolvido"},
        200
    )

    response = client.put(
        "/emprestimos/1/devolver",
        json={"status": "devolvido"}
    )

    assert response.status_code == 200

    assert response.get_json() == {
        "mensagem": "Livro devolvido"
    }


@patch("routes.emprestimo_routes.remover_emprestimo")
def test_remover_emprestimo(mock_remover, client):

    mock_remover.return_value = (
        {"mensagem": "Empréstimo removido"},
        200
    )

    response = client.delete("/emprestimos/1")

    assert response.status_code == 200

    assert response.get_json() == {
        "mensagem": "Empréstimo removido"
    }
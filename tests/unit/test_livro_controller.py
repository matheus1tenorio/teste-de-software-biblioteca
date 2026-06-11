from unittest.mock import patch

from livro_service.controllers.livro_controller import (
    listar_livros,
    buscar_livro,
    criar_livro,
    editar_livro,
    alterar_status,
    remover_livro
)


def test_listar_livros():
    livros = [
        {
            "id": 1,
            "titulo": "O Hobbit",
            "autor": "J.R.R. Tolkien",
            "ano": 1937,
            "disponivel": True
        },
        {
            "id": 2,
            "titulo": "1984",
            "autor": "George Orwell",
            "ano": 1949,
            "disponivel": False
        }
    ]

    with patch(
        "livro_service.controllers.livro_controller.get_all_livros",
        return_value=livros
    ):
        result = listar_livros()

    assert result == livros


def test_buscar_livro():
    livro = {
        "id": 1,
        "titulo": "O Hobbit",
        "autor": "J.R.R. Tolkien",
        "ano": 1937,
        "disponivel": True
    }

    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        return_value=livro
    ):
        result = buscar_livro(1)

    assert result == livro


def test_criar_livro():
    dados = {
        "titulo": "Duna",
        "autor": "Frank Herbert",
        "ano": 1965
    }

    with patch(
        "livro_service.controllers.livro_controller.create_livro"
    ) as mock_create:

        result = criar_livro(dados)

    assert result == (
        {"mensagem": "Livro criado com sucesso"},
        201
    )

    mock_create.assert_called_once_with(
        "Duna",
        "Frank Herbert",
        1965
    )


def test_criar_livro_sem_titulo():
    dados = {
        "autor": "Frank Herbert",
        "ano": 1965
    }

    result = criar_livro(dados)

    assert result == (
        {"erro": "titulo e autor são obrigatórios"},
        400
    )


def test_editar_livro():
    dados = {
        "titulo": "O Senhor dos Anéis",
        "autor": "J.R.R. Tolkien",
        "ano": 1954
    }

    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        return_value={"id": 1}
    ), patch(
        "livro_service.controllers.livro_controller.update_livro"
    ) as mock_update:

        result = editar_livro(1, dados)

    assert result == (
        {"mensagem": "Livro atualizado com sucesso"},
        200
    )

    mock_update.assert_called_once_with(
        1,
        "O Senhor dos Anéis",
        "J.R.R. Tolkien",
        1954
    )


def test_editar_livro_nao_encontrado():
    dados = {
        "titulo": "O Senhor dos Anéis",
        "autor": "J.R.R. Tolkien"
    }

    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        return_value=None
    ):
        result = editar_livro(999, dados)

    assert result == (
        {"erro": "Livro não encontrado"},
        404
    )


def test_alterar_status():
    with patch(
        "livro_service.controllers.livro_controller.update_disponibilidade"
    ) as mock_update:

        result = alterar_status(1, False)

    assert result is True

    mock_update.assert_called_once_with(1, False)


def test_remover_livro():
    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        return_value={"id": 1}
    ), patch(
        "livro_service.controllers.livro_controller.delete_livro"
    ) as mock_delete:

        result = remover_livro(1)

    assert result == (
        {"mensagem": "Livro removido com sucesso"},
        200
    )

    mock_delete.assert_called_once_with(1)


def test_remover_livro_nao_encontrado():
    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        return_value=None
    ):
        result = remover_livro(999)

    assert result == (
        {"erro": "Livro não encontrado"},
        404
    )
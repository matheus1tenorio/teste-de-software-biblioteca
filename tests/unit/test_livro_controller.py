import pytest
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

# Testes de falha
 
def test_listar_livros_falha_no_model():
    with patch(
        "livro_service.controllers.livro_controller.get_all_livros",
        side_effect=Exception("Erro de conexão com o banco")
    ):
        with pytest.raises(Exception, match="Erro de conexão com o banco"):
            listar_livros()

 
def test_buscar_livro_falha_no_model():
    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        side_effect=Exception("Tempo limite excedido ao buscar o livro no banco de dados")
    ):
        with pytest.raises(Exception, match="Tempo limite excedido ao buscar o livro no banco de dados"):
            buscar_livro(1)
 
 
def test_criar_livro_falha_no_model():

    dados = {
        "titulo": "Duna",
        "autor": "Frank Herbert",
        "ano": 1965
    }
 
    with patch(
        "livro_service.controllers.livro_controller.create_livro",
        side_effect=Exception("Já existe um livro cadastrado com este título")
    ):
        with pytest.raises(Exception, match="Já existe um livro cadastrado com este título"):
            criar_livro(dados)
 
 
def test_editar_livro_falha_ao_buscar():

    dados = {
        "titulo": "O Senhor dos Anéis",
        "autor": "J.R.R. Tolkien",
        "ano": 1954
    }
 
    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        side_effect=Exception("Não foi possível obter uma conexão com o banco de dados")
    ):
        with pytest.raises(Exception, match="Não foi possível obter uma conexão com o banco de dados"):
            editar_livro(1, dados)
 
 
def test_editar_livro_falha_no_update():

    dados = {
        "titulo": "O Senhor dos Anéis",
        "autor": "J.R.R. Tolkien",
        "ano": 1954
    }
 
    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        return_value={"id": 1}
    ), patch(
        "livro_service.controllers.livro_controller.update_livro",
        side_effect=Exception("Conflito de acesso ao banco de dados durante a atualização do registro")
    ):
        with pytest.raises(Exception, match="Conflito de acesso ao banco de dados durante a atualização do registro"):
            editar_livro(1, dados)
 
 
def test_alterar_status_falha_no_model():

    with patch(
        "livro_service.controllers.livro_controller.update_disponibilidade",
        side_effect=Exception("Erro ao atualizar disponibilidade")
    ):
        with pytest.raises(Exception, match="Erro ao atualizar disponibilidade"):
            alterar_status(1, False)
 
 
def test_remover_livro_falha_ao_buscar():

    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        side_effect=Exception("Banco inacessível")
    ):
        with pytest.raises(Exception, match="Banco inacessível"):
            remover_livro(1)
 
 
def test_remover_livro_falha_no_delete():

    with patch(
        "livro_service.controllers.livro_controller.get_livro_by_id",
        return_value={"id": 1}
    ), patch(
        "livro_service.controllers.livro_controller.delete_livro",
        side_effect=Exception("Não foi possível remover o registro porque ele está sendo utilizado por outros dados")
    ):
        with pytest.raises(Exception, match="Não foi possível remover o registro porque ele está sendo utilizado por outros dados"):
            remover_livro(1)

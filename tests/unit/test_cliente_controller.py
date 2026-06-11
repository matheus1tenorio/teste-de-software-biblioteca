from unittest.mock import patch

from cliente_service.controllers.cliente_controller import (
    listar_clientes,
    buscar_cliente,
    adicionar_cliente,
    editar_cliente,
    remover_cliente
)


def test_listar_clientes():
    clientes = [
        {"id": 1, "nome": "Matheus"},
        {"id": 2, "nome": "Filipe"}
    ]

    with patch(
        "cliente_service.controllers.cliente_controller.get_all_clientes",
        return_value=clientes
    ):
        result = listar_clientes()

    assert result == clientes


def test_buscar_cliente():
    cliente = {
        "id": 1,
        "nome": "Matheus"
    }

    with patch(
        "cliente_service.controllers.cliente_controller.get_cliente_by_id",
        return_value=cliente
    ):
        result = buscar_cliente(1)

    assert result == cliente


def test_adicionar_cliente():
    dados = {
        "nome": "Matheus",
        "email": "matheus@email.com",
        "matricula": "2024001"
    }

    with patch(
        "cliente_service.controllers.cliente_controller.create_cliente"
    ) as mock_create:

        result = adicionar_cliente(dados)

    assert result == (
        {"mensagem": "Cliente criado com sucesso"},
        201
    )

    mock_create.assert_called_once_with(
        "Matheus",
        "matheus@email.com",
        "2024001"
    )


def test_adicionar_cliente_sem_nome():
    dados = {
        "email": "matheus@email.com",
        "matricula": "2024001"
    }

    result = adicionar_cliente(dados)

    assert result == (
        {"erro": "nome e email são obrigatórios"},
        400
    )


def test_editar_cliente():
    dados = {
        "nome": "Matheus",
        "email": "matheus@email.com",
        "matricula": "2024002"
    }

    with patch(
        "cliente_service.controllers.cliente_controller.get_cliente_by_id",
        return_value={"id": 1}
    ), patch(
        "cliente_service.controllers.cliente_controller.update_cliente"
    ) as mock_update:

        result = editar_cliente(1, dados)

    assert result == (
        {"mensagem": "Cliente atualizado com sucesso"},
        200
    )

    mock_update.assert_called_once_with(
        1,
        "Matheus",
        "matheus@email.com",
        "2024002"
    )


def test_editar_cliente_nao_encontrado():
    dados = {
        "nome": "Matheus",
        "email": "matheus@email.com",
        "matricula": "2024002"
    }

    with patch(
        "cliente_service.controllers.cliente_controller.get_cliente_by_id",
        return_value=None
    ):
        result = editar_cliente(999, dados)

    assert result == (
        {"erro": "Cliente não encontrado"},
        404
    )


def test_remover_cliente():
    with patch(
        "cliente_service.controllers.cliente_controller.get_cliente_by_id",
        return_value={"id": 1}
    ), patch(
        "cliente_service.controllers.cliente_controller.delete_cliente"
    ) as mock_delete:

        result = remover_cliente(1)

    assert result == (
        {"mensagem": "Cliente removido com sucesso"},
        200
    )

    mock_delete.assert_called_once_with(1)


def test_remover_cliente_nao_encontrado():
    with patch(
        "cliente_service.controllers.cliente_controller.get_cliente_by_id",
        return_value=None
    ):
        result = remover_cliente(999)

    assert result == (
        {"erro": "Cliente não encontrado"},
        404
    )
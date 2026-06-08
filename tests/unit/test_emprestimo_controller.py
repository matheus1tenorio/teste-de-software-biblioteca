from unittest.mock import patch, MagicMock

from src.emprestimo_service.controllers.emprestimo_controller import (
    listar_emprestimos,
    criar_emprestimo,
    devolver_livro,
    remover_emprestimo
)


def test_listar_emprestimos():
    emprestimos = [
        {
            "id": 1,
            "cliente_id": 1,
            "livro_id": 1,
            "cliente_nome": "Matheus",
            "livro_titulo": "O Hobbit",
            "data_emprestimo": "2026-06-01",
            "data_devolucao": None
        }
    ]

    with patch(
        "src.emprestimo_service.controllers.emprestimo_controller.get_all_emprestimos",
        return_value=emprestimos
    ):
        result = listar_emprestimos()

    assert result == emprestimos


def test_criar_emprestimo():
    dados = {
        "cliente_id": 1,
        "livro_id": 1,
        "data_emprestimo": "2026-06-01"
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "titulo": "O Hobbit",
        "disponivel": True
    }

    with patch(
        "src.emprestimo_service.controllers.emprestimo_controller.requests.get",
        return_value=mock_response
    ), patch(
        "src.emprestimo_service.controllers.emprestimo_controller.requests.put"
    ), patch(
        "src.emprestimo_service.controllers.emprestimo_controller.create_emprestimo"
    ) as mock_create:

        result = criar_emprestimo(dados)

    assert result == (
        {"mensagem": "Empréstimo criado com sucesso"},
        201
    )

    mock_create.assert_called_once_with(
        1,
        1,
        "2026-06-01"
    )


def test_criar_emprestimo_campos_obrigatorios():
    dados = {
        "cliente_id": 1
    }

    result = criar_emprestimo(dados)

    assert result == (
        {"erro": "cliente_id, livro_id e data_emprestimo são obrigatórios"},
        400
    )


def test_criar_emprestimo_livro_nao_encontrado():
    dados = {
        "cliente_id": 1,
        "livro_id": 999,
        "data_emprestimo": "2026-06-01"
    }

    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch(
        "src.emprestimo_service.controllers.emprestimo_controller.requests.get",
        return_value=mock_response
    ):
        result = criar_emprestimo(dados)

    assert result == (
        {"erro": "Livro não encontrado"},
        404
    )


def test_criar_emprestimo_livro_indisponivel():
    dados = {
        "cliente_id": 1,
        "livro_id": 1,
        "data_emprestimo": "2026-06-01"
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "titulo": "O Hobbit",
        "disponivel": False
    }

    with patch(
        "src.emprestimo_service.controllers.emprestimo_controller.requests.get",
        return_value=mock_response
    ):
        result = criar_emprestimo(dados)

    assert result == (
        {"erro": "Livro não está disponível para empréstimo"},
        400
    )


def test_devolver_livro():
    emprestimo = {
        "id": 1,
        "livro_id": 1,
        "data_devolucao": None
    }

    with patch(
        "src.emprestimo_service.controllers.emprestimo_controller.get_emprestimo_by_id",
        return_value=emprestimo
    ), patch(
        "src.emprestimo_service.controllers.emprestimo_controller.finalizar_emprestimo"
    ) as mock_finalizar, patch(
        "src.emprestimo_service.controllers.emprestimo_controller.requests.put"
    ):

        result = devolver_livro(
            1,
            {"data_devolucao": "2026-06-10"}
        )

    assert result == (
        {"mensagem": "Livro devolvido com sucesso"},
        200
    )

    mock_finalizar.assert_called_once_with(
        1,
        "2026-06-10"
    )


def test_devolver_livro_sem_data():
    result = devolver_livro(1, {})

    assert result == (
        {"erro": "data_devolucao é obrigatória"},
        400
    )


def test_devolver_livro_nao_encontrado():
    with patch(
        "src.emprestimo_service.controllers.emprestimo_controller.get_emprestimo_by_id",
        return_value=None
    ):
        result = devolver_livro(
            999,
            {"data_devolucao": "2026-06-10"}
        )

    assert result == (
        {"erro": "Empréstimo não encontrado"},
        404
    )


def test_devolver_livro_ja_devolvido():
    emprestimo = {
        "id": 1,
        "livro_id": 1,
        "data_devolucao": "2026-06-05"
    }

    with patch(
        "src.emprestimo_service.controllers.emprestimo_controller.get_emprestimo_by_id",
        return_value=emprestimo
    ):
        result = devolver_livro(
            1,
            {"data_devolucao": "2026-06-10"}
        )

    assert result == (
        {"erro": "Este livro já foi devolvido"},
        400
    )


def test_remover_emprestimo():
    emprestimo = {
        "id": 1,
        "livro_id": 1,
        "data_devolucao": "2026-06-10"
    }

    with patch(
        "src.emprestimo_service.controllers.emprestimo_controller.get_emprestimo_by_id",
        return_value=emprestimo
    ), patch(
        "src.emprestimo_service.controllers.emprestimo_controller.delete_emprestimo"
    ) as mock_delete:

        result = remover_emprestimo(1)

    assert result == (
        {"mensagem": "Empréstimo removido com sucesso"},
        200
    )

    mock_delete.assert_called_once_with(1)


def test_remover_emprestimo_nao_encontrado():
    with patch(
        "src.emprestimo_service.controllers.emprestimo_controller.get_emprestimo_by_id",
        return_value=None
    ):
        result = remover_emprestimo(999)

    assert result == (
        {"erro": "Empréstimo não encontrado"},
        404
    )
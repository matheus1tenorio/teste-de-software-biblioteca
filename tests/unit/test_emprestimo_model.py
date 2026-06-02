from unittest.mock import MagicMock, patch

from src.emprestimo_service.models.emprestimo_model import (
    get_all_emprestimos,
    get_emprestimo_by_id,
    create_emprestimo,
    finalizar_emprestimo,
    delete_emprestimo
)


def test_get_all_emprestimos():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "cliente_id": 1,
            "livro_id": 1,
            "cliente_nome": "Matheus",
            "livro_titulo": "O Senhor dos Anéis",
            "data_emprestimo": "2026-06-01",
            "data_devolucao": None
        },
        {
            "id": 2,
            "cliente_id": 2,
            "livro_id": 2,
            "cliente_nome": "Filipe",
            "livro_titulo": "Harry Potter e a Pedra Filosofal",
            "data_emprestimo": "2026-06-02",
            "data_devolucao": None
        }
    ]

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.emprestimo_service.models.emprestimo_model.get_connection",
        return_value=mock_conn
    ):
        result = get_all_emprestimos()

    assert len(result) == 2
    assert result[0]["cliente_nome"] == "Matheus"
    assert result[1]["cliente_nome"] == "Filipe"

    mock_cursor.execute.assert_called_once()
    mock_conn.close.assert_called_once()


def test_get_emprestimo_by_id():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = {
        "id": 1,
        "cliente_id": 1,
        "livro_id": 1,
        "data_emprestimo": "2026-06-01",
        "data_devolucao": None
    }

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.emprestimo_service.models.emprestimo_model.get_connection",
        return_value=mock_conn
    ):
        result = get_emprestimo_by_id(1)

    assert result["id"] == 1
    assert result["cliente_id"] == 1
    assert result["livro_id"] == 1

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM emprestimo WHERE id = %s",
        (1,)
    )

    mock_conn.close.assert_called_once()


def test_create_emprestimo():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.emprestimo_service.models.emprestimo_model.get_connection",
        return_value=mock_conn
    ):
        create_emprestimo(
            1,
            1,
            "2026-06-01"
        )

    mock_cursor.execute.assert_called_once_with(
        """
        INSERT INTO emprestimo (cliente_id, livro_id, data_emprestimo)
        VALUES (%s, %s, %s)
    """,
        (1, 1, "2026-06-01")
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_finalizar_emprestimo():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.emprestimo_service.models.emprestimo_model.get_connection",
        return_value=mock_conn
    ):
        finalizar_emprestimo(
            1,
            "2026-06-15"
        )

    mock_cursor.execute.assert_called_once_with(
        """
        UPDATE emprestimo SET data_devolucao = %s WHERE id = %s
    """,
        ("2026-06-15", 1)
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_delete_emprestimo():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.emprestimo_service.models.emprestimo_model.get_connection",
        return_value=mock_conn
    ):
        delete_emprestimo(2)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM emprestimo WHERE id = %s",
        (2,)
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_get_emprestimo_by_id_none():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.emprestimo_service.models.emprestimo_model.get_connection",
        return_value=mock_conn
    ):
        result = get_emprestimo_by_id(999)

    assert result is None
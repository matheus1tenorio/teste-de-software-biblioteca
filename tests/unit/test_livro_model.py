from unittest.mock import MagicMock, patch

from src.livro_service.models.livro_model import (
    get_all_livros,
    get_livro_by_id,
    create_livro,
    update_livro,
    update_disponibilidade,
    delete_livro
)


def test_get_all_livros():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        {
            "id": 1,
            "titulo": "O Senhor dos Anéis",
            "autor": "J.R.R. Tolkien",
            "ano": 1954,
            "disponivel": 1
        },
        {
            "id": 2,
            "titulo": "Harry Potter e a Pedra Filosofal",
            "autor": "J.K. Rowling",
            "ano": 1997,
            "disponivel": 0
        }
    ]

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.livro_service.models.livro_model.get_connection",
        return_value=mock_conn
    ):
        result = get_all_livros()

    assert result[0]["titulo"] == "O Senhor dos Anéis"
    assert result[0]["disponivel"] is True

    assert result[1]["titulo"] == "Harry Potter e a Pedra Filosofal"
    assert result[1]["disponivel"] is False

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM livro"
    )

    mock_conn.close.assert_called_once()


def test_get_livro_by_id():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = {
        "id": 1,
        "titulo": "Duna",
        "autor": "Frank Herbert",
        "ano": 1965,
        "disponivel": 1
    }

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.livro_service.models.livro_model.get_connection",
        return_value=mock_conn
    ):
        result = get_livro_by_id(1)

    assert result == {
        "id": 1,
        "titulo": "Duna",
        "autor": "Frank Herbert",
        "ano": 1965,
        "disponivel": True
    }

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM livro WHERE id = %s",
        (1,)
    )

    mock_conn.close.assert_called_once()


def test_create_livro():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.livro_service.models.livro_model.get_connection",
        return_value=mock_conn
    ):
        create_livro(
            "O Hobbit",
            "J.R.R. Tolkien",
            1937
        )

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO livro (titulo, autor, ano, disponivel) VALUES (%s, %s, %s, %s)",
        (
            "O Hobbit",
            "J.R.R. Tolkien",
            1937,
            True
        )
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_update_livro():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.livro_service.models.livro_model.get_connection",
        return_value=mock_conn
    ):
        update_livro(
            1,
            "1984",
            "George Orwell",
            1949
        )

    mock_cursor.execute.assert_called_once_with(
        "UPDATE livro SET titulo = %s, autor = %s, ano = %s WHERE id = %s",
        (
            "1984",
            "George Orwell",
            1949,
            1
        )
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_update_disponibilidade():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.livro_service.models.livro_model.get_connection",
        return_value=mock_conn
    ):
        update_disponibilidade(1, False)

    mock_cursor.execute.assert_called_once_with(
        "UPDATE livro SET disponivel = %s WHERE id = %s",
        (
            False,
            1
        )
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_delete_livro():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.livro_service.models.livro_model.get_connection",
        return_value=mock_conn
    ):
        delete_livro(2)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM livro WHERE id = %s",
        (2,)
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_get_livro_by_id_none():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor

    with patch(
        "src.livro_service.models.livro_model.get_connection",
        return_value=mock_conn
    ):
        result = get_livro_by_id(999)

    assert result is None
from unittest.mock import MagicMock, patch

from cliente_service.models.cliente_model import (
    get_all_clientes,
    get_cliente_by_id,
    create_cliente,
    update_cliente,
    delete_cliente
)


def test_get_all_clientes():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = [
        {"id": 1, "nome": "Matheus"},
        {"id": 2, "nome": "Filipe"}
    ]

    mock_conn.cursor.return_value = mock_cursor

    with patch("cliente_service.models.cliente_model.get_connection", return_value=mock_conn):
        result = get_all_clientes()

    assert result == [
        {"id": 1, "nome": "Matheus"},
        {"id": 2, "nome": "Filipe"}
    ]

    mock_cursor.execute.assert_called_once_with("SELECT * FROM cliente")
    mock_conn.close.assert_called_once()


def test_get_cliente_by_id():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = {
        "id": 1,
        "nome": "Matheus"
    }

    mock_conn.cursor.return_value = mock_cursor

    with patch("cliente_service.models.cliente_model.get_connection", return_value=mock_conn):
        result = get_cliente_by_id(1)

    assert result == {"id": 1, "nome": "Matheus"}

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM cliente WHERE id = %s",
        (1,)
    )

    mock_conn.close.assert_called_once()


def test_create_cliente():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch("cliente_service.models.cliente_model.get_connection", return_value=mock_conn):
        create_cliente("Filipe", "filipe@email.com", "2024001")

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO cliente (nome, email, matricula) VALUES (%s, %s, %s)",
        ("Filipe", "filipe@email.com", "2024001")
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_update_cliente():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch("cliente_service.models.cliente_model.get_connection", return_value=mock_conn):
        update_cliente(1, "Matheus", "matheus@email.com", "2024002")

    mock_cursor.execute.assert_called_once_with(
        "UPDATE cliente SET nome = %s, email = %s, matricula = %s WHERE id = %s",
        ("Matheus", "matheus@email.com", "2024002", 1)
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_delete_cliente():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    with patch("cliente_service.models.cliente_model.get_connection", return_value=mock_conn):
        delete_cliente(2)

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM cliente WHERE id = %s",
        (2,)
    )

    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_get_cliente_by_id_none():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor

    with patch("cliente_service.models.cliente_model.get_connection", return_value=mock_conn):
        result = get_cliente_by_id(999)

    assert result is None
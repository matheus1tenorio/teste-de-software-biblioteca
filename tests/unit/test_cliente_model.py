import pytest
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


# Testes de falha — simulam exceções no sistema

def test_get_all_clientes_falha_na_conexao():

    with patch(

        "cliente_service.models.cliente_model.get_connection",

        side_effect=Exception("Não foi possível conectar ao banco")

    ):

        with pytest.raises(Exception, match="Não foi possível conectar ao banco"):

            get_all_clientes()


def test_get_all_clientes_falha_no_execute():

    mock_conn = MagicMock()

    mock_cursor = MagicMock()

    mock_cursor.execute.side_effect = Exception("Tabela 'cliente' não encontrada")

    mock_conn.cursor.return_value = mock_cursor


    with patch("cliente_service.models.cliente_model.get_connection", return_value=mock_conn):

        with pytest.raises(Exception, match="Tabela 'cliente' não encontrada"):

            get_all_clientes()


def test_get_cliente_by_id_falha_na_conexao():

    with patch(

        "cliente_service.models.cliente_model.get_connection",

        side_effect=Exception("Pool de conexões esgotado")

    ):

        with pytest.raises(Exception, match="Pool de conexões esgotado"):

            get_cliente_by_id(1)


def test_create_cliente_falha_na_conexao():

    with patch(

        "cliente_service.models.cliente_model.get_connection",

        side_effect=Exception("Banco de dados indisponível")

    ):

        with pytest.raises(Exception, match="Banco de dados indisponível"):

            create_cliente("Matheus", "matheus@email.com", "2024001")


def test_create_cliente_falha_no_commit():

    mock_conn = MagicMock()

    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_conn.commit.side_effect = Exception("Transação abortada por deadlock")


    with patch("cliente_service.models.cliente_model.get_connection", return_value=mock_conn):

        with pytest.raises(Exception, match="Transação abortada por deadlock"):

            create_cliente("Matheus", "matheus@email.com", "2024001")


def test_update_cliente_falha_na_conexao():

    with patch(

        "cliente_service.models.cliente_model.get_connection",

        side_effect=Exception("Credenciais de banco expiradas")

    ):

        with pytest.raises(Exception, match="Credenciais de banco expiradas"):

            update_cliente(1, "Matheus", "matheus@email.com", "2024002")


def test_update_cliente_falha_no_execute():

    mock_conn = MagicMock()

    mock_cursor = MagicMock()

    mock_cursor.execute.side_effect = Exception("Coluna 'matricula' não existe")

    mock_conn.cursor.return_value = mock_cursor


    with patch("cliente_service.models.cliente_model.get_connection", return_value=mock_conn):

        with pytest.raises(Exception, match="Coluna 'matricula' não existe"):

            update_cliente(1, "Matheus", "matheus@email.com", "2024002")


def test_delete_cliente_falha_na_conexao():

    with patch(

        "cliente_service.models.cliente_model.get_connection",

        side_effect=Exception("Banco fora do ar")

    ):

        with pytest.raises(Exception, match="Banco fora do ar"):

            delete_cliente(2)
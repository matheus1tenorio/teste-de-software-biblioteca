import datetime
from emprestimo_service.config import get_connection


def _serializar(row):
    """Converte tipos não-serializáveis do MySQL para tipos nativos Python."""
    if row is None:
        return None
    result = {}
    for key, value in row.items():
        if isinstance(value, (datetime.date, datetime.datetime)):
            result[key] = value.isoformat()
        else:
            result[key] = value
    return result


def get_all_emprestimos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            e.id,
            e.cliente_id,
            e.livro_id,
            c.nome  AS cliente_nome,
            l.titulo AS livro_titulo,
            e.data_emprestimo,
            e.data_devolucao
        FROM emprestimo e
        JOIN cliente c ON e.cliente_id = c.id
        JOIN livro   l ON e.livro_id   = l.id
        ORDER BY e.id DESC
    """)
    emprestimos = cursor.fetchall()
    conn.close()
    return [_serializar(e) for e in emprestimos]


def get_emprestimo_by_id(emprestimo_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM emprestimo WHERE id = %s", (emprestimo_id,))
    result = cursor.fetchone()
    conn.close()
    return _serializar(result)


def create_emprestimo(cliente_id, livro_id, data_emprestimo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO emprestimo (cliente_id, livro_id, data_emprestimo)
        VALUES (%s, %s, %s)
    """, (cliente_id, livro_id, data_emprestimo))
    conn.commit()
    conn.close()


def finalizar_emprestimo(emprestimo_id, data_devolucao):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE emprestimo SET data_devolucao = %s WHERE id = %s
    """, (data_devolucao, emprestimo_id))
    conn.commit()
    conn.close()


def delete_emprestimo(emprestimo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM emprestimo WHERE id = %s", (emprestimo_id,))
    conn.commit()
    conn.close()

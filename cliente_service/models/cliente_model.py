from cliente_service.config import get_connection


def get_all_clientes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente")
    result = cursor.fetchall()
    conn.close()
    return result


def get_cliente_by_id(cliente_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente WHERE id = %s", (cliente_id,))
    result = cursor.fetchone()
    conn.close()
    return result


def create_cliente(nome, email, matricula=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cliente (nome, email, matricula) VALUES (%s, %s, %s)",
        (nome, email, matricula)
    )
    conn.commit()
    conn.close()


def update_cliente(cliente_id, nome, email, matricula=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cliente SET nome = %s, email = %s, matricula = %s WHERE id = %s",
        (nome, email, matricula, cliente_id)
    )
    conn.commit()
    conn.close()


def delete_cliente(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cliente WHERE id = %s", (cliente_id,))
    conn.commit()
    conn.close()

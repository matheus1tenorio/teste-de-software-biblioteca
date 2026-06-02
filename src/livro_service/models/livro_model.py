from src.livro_service.config import get_connection


def get_all_livros():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM livro")
    livros = cursor.fetchall()
    conn.close()
    for livro in livros:
        livro["disponivel"] = bool(livro["disponivel"])
    return livros


def get_livro_by_id(livro_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM livro WHERE id = %s", (livro_id,))
    livro = cursor.fetchone()
    conn.close()
    if livro:
        livro["disponivel"] = bool(livro["disponivel"])
    return livro


def create_livro(titulo, autor, ano=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO livro (titulo, autor, ano, disponivel) VALUES (%s, %s, %s, %s)",
        (titulo, autor, ano, True)
    )
    conn.commit()
    conn.close()


def update_livro(livro_id, titulo, autor, ano=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE livro SET titulo = %s, autor = %s, ano = %s WHERE id = %s",
        (titulo, autor, ano, livro_id)
    )
    conn.commit()
    conn.close()


def update_disponibilidade(livro_id, disponivel):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE livro SET disponivel = %s WHERE id = %s",
        (disponivel, livro_id)
    )
    conn.commit()
    conn.close()


def delete_livro(livro_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livro WHERE id = %s", (livro_id,))
    conn.commit()
    conn.close()

from models.livro_model import (
    get_all_livros,
    get_livro_by_id,
    create_livro,
    update_livro,
    update_disponibilidade,
    delete_livro
)


def listar_livros():
    return get_all_livros()


def buscar_livro(livro_id):
    return get_livro_by_id(livro_id)


def criar_livro(data):
    if "titulo" not in data or "autor" not in data:
        return {"erro": "titulo e autor são obrigatórios"}, 400
    create_livro(data["titulo"], data["autor"], data.get("ano"))
    return {"mensagem": "Livro criado com sucesso"}, 201


def editar_livro(livro_id, data):
    if not get_livro_by_id(livro_id):
        return {"erro": "Livro não encontrado"}, 404
    if "titulo" not in data or "autor" not in data:
        return {"erro": "titulo e autor são obrigatórios"}, 400
    update_livro(livro_id, data["titulo"], data["autor"], data.get("ano"))
    return {"mensagem": "Livro atualizado com sucesso"}, 200


def alterar_status(livro_id, disponivel):
    update_disponibilidade(livro_id, disponivel)
    return True


def remover_livro(livro_id):
    if not get_livro_by_id(livro_id):
        return {"erro": "Livro não encontrado"}, 404
    delete_livro(livro_id)
    return {"mensagem": "Livro removido com sucesso"}, 200

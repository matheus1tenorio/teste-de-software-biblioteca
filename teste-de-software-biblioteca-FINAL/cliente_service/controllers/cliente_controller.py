from models.cliente_model import (
    get_all_clientes,
    get_cliente_by_id,
    create_cliente,
    update_cliente,
    delete_cliente
)


def listar_clientes():
    return get_all_clientes()


def buscar_cliente(cliente_id):
    return get_cliente_by_id(cliente_id)


def adicionar_cliente(data):
    if "nome" not in data or "email" not in data:
        return {"erro": "nome e email são obrigatórios"}, 400

    create_cliente(data["nome"], data["email"], data.get("matricula"))

    # Pega o ID do último cliente criado
    #from models.cliente_model import get_all_clientes
    todos = get_all_clientes()
    if todos:
        ultimo = max(todos, key=lambda x: x["id"])
        cliente_id = ultimo["id"]
    else:
        cliente_id = None

    return {
        "mensagem": "Cliente criado com sucesso",
        "id": cliente_id
    }, 201


def editar_cliente(cliente_id, dados):
    nome = dados.get("nome")
    email = dados.get("email")
    matricula = dados.get("matricula")
    if not nome or not email:
        return {"erro": "nome e email são obrigatórios"}, 400
    if not get_cliente_by_id(cliente_id):
        return {"erro": "Cliente não encontrado"}, 404
    update_cliente(cliente_id, nome, email, matricula)
    return {"mensagem": "Cliente atualizado com sucesso"}, 200


def remover_cliente(cliente_id):
    if not get_cliente_by_id(cliente_id):
        return {"erro": "Cliente não encontrado"}, 404
    delete_cliente(cliente_id)
    return {"mensagem": "Cliente removido com sucesso"}, 200

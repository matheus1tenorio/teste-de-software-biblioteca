from flask import Blueprint, request, jsonify
from src.livro_service.controllers.livro_controller import (
    listar_livros,
    buscar_livro,
    criar_livro,
    editar_livro,
    alterar_status,
    remover_livro
)

livro_bp = Blueprint("livro_bp", __name__)


@livro_bp.route("/livros", methods=["GET"])
def listar():
    return jsonify(listar_livros()), 200


@livro_bp.route("/livros/<int:id>", methods=["GET"])
def buscar(id):
    livro = buscar_livro(id)
    if livro:
        return jsonify(livro), 200
    return jsonify({"erro": "Livro não encontrado"}), 404


@livro_bp.route("/livros", methods=["POST"])
def criar():
    data = request.json
    resultado = criar_livro(data)
    return jsonify(resultado[0]), resultado[1]


@livro_bp.route("/livros/<int:id>", methods=["PUT"])
def editar(id):
    data = request.json
    resultado = editar_livro(id, data)
    return jsonify(resultado[0]), resultado[1]


@livro_bp.route("/livros/<int:id>/status", methods=["PUT"])
def status(id):
    data = request.json
    if "disponivel" not in data:
        return jsonify({"erro": "Campo 'disponivel' obrigatório"}), 400
    alterar_status(id, data["disponivel"])
    return jsonify({"mensagem": "Status atualizado"}), 200


@livro_bp.route("/livros/<int:id>", methods=["DELETE"])
def excluir(id):
    resultado = remover_livro(id)
    return jsonify(resultado[0]), resultado[1]

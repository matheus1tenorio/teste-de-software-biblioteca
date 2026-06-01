from flask import Blueprint, request, jsonify
from controllers.emprestimo_controller import (
    listar_emprestimos,
    criar_emprestimo,
    devolver_livro,
    remover_emprestimo
)

emprestimo_bp = Blueprint("emprestimo_bp", __name__)


@emprestimo_bp.route("/emprestimos", methods=["GET"])
def listar():
    return jsonify(listar_emprestimos()), 200


@emprestimo_bp.route("/emprestimos", methods=["POST"])
def criar():
    data = request.json
    resultado = criar_emprestimo(data)
    return jsonify(resultado[0]), resultado[1]


@emprestimo_bp.route("/emprestimos/<int:id>/devolver", methods=["PUT"])
def devolver(id):
    data = request.json
    resultado = devolver_livro(id, data)
    return jsonify(resultado[0]), resultado[1]


@emprestimo_bp.route("/emprestimos/<int:id>", methods=["DELETE"])
def excluir(id):
    resultado = remover_emprestimo(id)
    return jsonify(resultado[0]), resultado[1]

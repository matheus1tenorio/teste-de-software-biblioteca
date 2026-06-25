import uuid
import requests
import pytest
import time

BASE_CLIENTE = "http://localhost:5001"
BASE_LIVRO = "http://localhost:5002"
BASE_EMPRESTIMO = "http://localhost:5003"


def gerar_email():
    return f"teste.{uuid.uuid4().hex[:8]}@email.com"


def gerar_titulo():
    return f"Livro Teste {uuid.uuid4().hex[:8]}"


def test_fluxo_completo_biblioteca():
    """Teste End-to-End: Cliente → Livro → Empréstimo → Devolução"""
    
    # 1. Criar Cliente
    email = gerar_email()
    cliente_resp = requests.post(f"{BASE_CLIENTE}/clientes", json={
        "nome": "João da Silva",
        "email": email,
        "matricula": "2026001"
    })
    assert cliente_resp.status_code == 201
    
    # Aguarda 0.5 segundos antes de prosseguir (evita problemas de latência)
    time.sleep(0.5)
    cliente_id = cliente_resp.json().get("id")
    assert cliente_id is not None

    # 2. Criar Livro
    titulo = gerar_titulo()
    livro_resp = requests.post(f"{BASE_LIVRO}/livros", json={
        "titulo": titulo,
        "autor": "Autor Teste",
        "ano": 2025
    })
    assert livro_resp.status_code == 201
    
    # Aguarda 0.5 segundos antes de prosseguir (evita problemas de latência)
    time.sleep(0.5)
    livro_id = livro_resp.json().get("id")
    assert livro_id is not None

    # 3. Realizar Empréstimo
    emprestimo_resp = requests.post(f"{BASE_EMPRESTIMO}/emprestimos", json={
        "cliente_id": cliente_id,
        "livro_id": livro_id,
        "data_emprestimo": "2026-06-24"
    })
    assert emprestimo_resp.status_code == 201
    
    # Aguarda 0.5 segundos antes de prosseguir (evita problemas de latência)
    time.sleep(0.5)
    emprestimo_id = emprestimo_resp.json().get("id")
    assert emprestimo_id is not None

    # 4. Devolver o Livro
    devolucao_resp = requests.put(f"{BASE_EMPRESTIMO}/emprestimos/{emprestimo_id}/devolver", json={
        "data_devolucao": "2026-07-01"
    })
    assert devolucao_resp.status_code == 200

    # 5. Verificações finais
    # Livro deve estar disponível novamente
    livro_atual = requests.get(f"{BASE_LIVRO}/livros/{livro_id}").json()
    assert livro_atual["disponivel"] is True

    # Empréstimo deve aparecer como devolvido
    emprestimos = requests.get(f"{BASE_EMPRESTIMO}/emprestimos").json()
    emprestimo = next((e for e in emprestimos if e["id"] == emprestimo_id), None)
    assert emprestimo is not None
    assert emprestimo.get("data_devolucao") is not None # .get() evita KeyError caso a chave não exista

    print(f"Fluxo completo realizado com sucesso! IDs: Cliente={cliente_id}, Livro={livro_id}, Empréstimo={emprestimo_id}")
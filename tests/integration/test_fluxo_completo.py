import uuid
import requests
import pytest
import time

BASE_CLIENTE    = "http://localhost:5001"
BASE_LIVRO      = "http://localhost:5002"
BASE_EMPRESTIMO = "http://localhost:5003"


def gerar_email():
    return f"teste.{uuid.uuid4().hex[:8]}@email.com"


def gerar_titulo():
    return f"Livro Teste {uuid.uuid4().hex[:8]}"


def servicos_disponiveis():
    """Verifica se os três serviços estão no ar antes de rodar o teste."""
    for nome, base in [
        ("cliente-service",    BASE_CLIENTE),
        ("livro-service",      BASE_LIVRO),
        ("emprestimo-service", BASE_EMPRESTIMO),
    ]:
        try:
            requests.get(base, timeout=2)
        except requests.exceptions.ConnectionError:
            pytest.skip(
                f"⚠️  {nome} não está rodando em {base}. "
                "Suba os três serviços Flask antes de executar os testes de integração."
            )


def test_fluxo_completo_biblioteca():
    """Teste End-to-End: Cliente → Livro → Empréstimo → Devolução"""

    # Aborta com mensagem clara se algum serviço não estiver no ar
    servicos_disponiveis()

    # ------------------------------------------------------------------
    # 1. Criar Cliente
    # ------------------------------------------------------------------
    email = gerar_email()
    cliente_resp = requests.post(f"{BASE_CLIENTE}/clientes", json={
        "nome": "João da Silva",
        "email": email,
        "matricula": "2026001"
    })
    assert cliente_resp.status_code == 201

    # O POST retorna apenas {"mensagem": "Cliente criado com sucesso"} sem id.
    # Recuperamos o id buscando na listagem pelo email único (gerado com UUID).
    time.sleep(0.5)
    clientes = requests.get(f"{BASE_CLIENTE}/clientes").json()
    cliente = next((c for c in clientes if c["email"] == email), None)
    assert cliente is not None, f"Cliente com email {email} não encontrado após criação"
    cliente_id = cliente["id"]

    # ------------------------------------------------------------------
    # 2. Criar Livro
    # ------------------------------------------------------------------
    titulo = gerar_titulo()
    livro_resp = requests.post(f"{BASE_LIVRO}/livros", json={
        "titulo": titulo,
        "autor": "Autor Teste",
        "ano": 2025
    })
    assert livro_resp.status_code == 201

    # Mesmo caso: POST não devolve id — buscamos pelo titulo único na listagem.
    time.sleep(0.5)
    livros = requests.get(f"{BASE_LIVRO}/livros").json()
    livro = next((l for l in livros if l["titulo"] == titulo), None)
    assert livro is not None, f"Livro '{titulo}' não encontrado após criação"
    livro_id = livro["id"]
    assert livro["disponivel"] is True, "Livro recém-criado deve estar disponível"

    # ------------------------------------------------------------------
    # 3. Realizar Empréstimo
    # ------------------------------------------------------------------
    emprestimo_resp = requests.post(f"{BASE_EMPRESTIMO}/emprestimos", json={
        "cliente_id": cliente_id,
        "livro_id": livro_id,
        "data_emprestimo": "2026-06-24"
    })
    assert emprestimo_resp.status_code == 201

    # POST também não devolve id — buscamos na listagem pelo par cliente+livro
    # com data_devolucao ausente (empréstimo ativo recém-criado).
    time.sleep(0.5)
    emprestimos = requests.get(f"{BASE_EMPRESTIMO}/emprestimos").json()
    emprestimo = next(
        (e for e in emprestimos
         if e["cliente_id"] == cliente_id
         and e["livro_id"] == livro_id
         and e.get("data_devolucao") is None),
        None
    )
    assert emprestimo is not None, "Empréstimo ativo não encontrado após criação"
    emprestimo_id = emprestimo["id"]

    # ------------------------------------------------------------------
    # 4. Devolver o Livro
    # ------------------------------------------------------------------
    devolucao_resp = requests.put(
        f"{BASE_EMPRESTIMO}/emprestimos/{emprestimo_id}/devolver",
        json={"data_devolucao": "2026-07-01"}
    )
    assert devolucao_resp.status_code == 200

    # ------------------------------------------------------------------
    # 5. Verificações finais
    # ------------------------------------------------------------------
    time.sleep(0.5)

    # Livro deve estar disponível novamente
    livro_atual = requests.get(f"{BASE_LIVRO}/livros/{livro_id}").json()
    assert livro_atual["disponivel"] is True, "Livro deve estar disponível após devolução"

    # Empréstimo deve aparecer como devolvido na listagem
    emprestimos_final = requests.get(f"{BASE_EMPRESTIMO}/emprestimos").json()
    emprestimo_final = next(
        (e for e in emprestimos_final if e["id"] == emprestimo_id),
        None
    )
    assert emprestimo_final is not None, "Empréstimo não encontrado na listagem final"
    assert emprestimo_final.get("data_devolucao") is not None, \
        "data_devolucao deve estar preenchida após devolução"

    print(
        f"\nFluxo completo realizado com sucesso! "
        f"IDs: Cliente={cliente_id}, Livro={livro_id}, Empréstimo={emprestimo_id}"
    )
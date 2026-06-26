import uuid
import requests

BASE_URL = "http://localhost:5003"
CLIENTE_URL = "http://localhost:5001/clientes"
LIVRO_URL = "http://localhost:5002/livros"


def test_listar_emprestimos_retorna_200():

    resposta = requests.get(
        f"{BASE_URL}/emprestimos"
    )

    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)
    


    
    
def test_nao_permite_emprestar_livro_indisponivel():
    # 1. Cria um cliente e um livro dinamicamente para garantir que eles existam no banco
    cliente_id = criar_cliente_teste()
    livro_id = criar_livro_teste()
    
    # 2. Modifica o status do livro que ACABOU de ser criado para indisponível
    requests.put(
        f"{LIVRO_URL}/{livro_id}/status",
        json={"disponivel": False}
    )

    # 3. Tenta realizar o empréstimo usando os IDs reais gerados dinamicamente
    resposta = requests.post(
        f"{BASE_URL}/emprestimos",
        json={
            "cliente_id": cliente_id,
            "livro_id": livro_id,
            "data_emprestimo": "2026-06-15"
        }
    )

    # 4. Agora sim o status retornado deve ser 400 Bad Request
    assert resposta.status_code == 400

    assert resposta.json() == {
        "erro": "Livro não está disponível para empréstimo"
    }

def gerar_email():
    return f"{uuid.uuid4().hex[:8]}@teste.com"
    
    
def criar_cliente_teste():

    email = gerar_email()

    resposta = requests.post(
        CLIENTE_URL,
        json={
            "nome": "Cliente Teste",
            "email": email
        }
    )

    assert resposta.status_code == 201

    clientes = requests.get(CLIENTE_URL).json()

    cliente = next(
        c for c in clientes
        if c["email"] == email
    )

    return cliente["id"]
    
    

def criar_livro_teste():

    titulo = f"Livro Teste {uuid.uuid4().hex[:6]}"

    resposta = requests.post(
        LIVRO_URL,
        json={
            "titulo": titulo,
            "autor": "Autor Teste",
            "ano": 2026
        }
    )

    assert resposta.status_code == 201

    livros = requests.get(LIVRO_URL).json()

    livro = next(
        l for l in livros
        if l["titulo"] == titulo
    )

    return livro["id"]
    
    
def test_criar_emprestimo_com_dados_temporarios():

    cliente_id = criar_cliente_teste()

    livro_id = criar_livro_teste()

    resposta = requests.post(
        f"{BASE_URL}/emprestimos",
        json={
            "cliente_id": cliente_id,
            "livro_id": livro_id,
            "data_emprestimo": "2026-06-15"
        }
    )

    assert resposta.status_code == 201

    # Atualizado para aceitar o novo retorno com "id"
    data = resposta.json()
    assert data["mensagem"] == "Empréstimo criado com sucesso"
    assert "id" in data
    assert isinstance(data["id"], int) and data["id"] > 0
    
    
def buscar_ultimo_emprestimo():
    emprestimos = requests.get(
        f"{BASE_URL}/emprestimos"
    ).json()

    return max(emprestimos, key=lambda e: e["id"])
    
    
    
def test_devolver_livro_com_sucesso():

    cliente_id = criar_cliente_teste()

    livro_id = criar_livro_teste()

    requests.post(
        f"{BASE_URL}/emprestimos",
        json={
            "cliente_id": cliente_id,
            "livro_id": livro_id,
            "data_emprestimo": "2026-06-15"
        }
    )
    
    

    emprestimo = buscar_ultimo_emprestimo()

    resposta = requests.put(
        f"{BASE_URL}/emprestimos/{emprestimo['id']}/devolver",
        json={
            "data_devolucao": "2026-06-20"
        }
    )

    assert resposta.status_code == 200

    assert resposta.json() == {
        "mensagem": "Livro devolvido com sucesso"
    }
    
    
def test_devolucao_retorna_livro_para_disponivel():

    cliente_id = criar_cliente_teste()

    livro_id = criar_livro_teste()

    requests.post(
        f"{BASE_URL}/emprestimos",
        json={
            "cliente_id": cliente_id,
            "livro_id": livro_id,
            "data_emprestimo": "2026-06-15"
        }
    )

    emprestimo = buscar_ultimo_emprestimo()

    requests.put(
        f"{BASE_URL}/emprestimos/{emprestimo['id']}/devolver",
        json={
            "data_devolucao": "2026-06-20"
        }
    )

    livro = requests.get(
        f"{LIVRO_URL}/{livro_id}"
    ).json()

    assert livro["disponivel"] is True
    

########## A MAIS ##########
    
def test_remover_emprestimo_com_sucesso():

    cliente_id = criar_cliente_teste()

    livro_id = criar_livro_teste()

    requests.post(
        f"{BASE_URL}/emprestimos",
        json={
            "cliente_id": cliente_id,
            "livro_id": livro_id,
            "data_emprestimo": "2026-06-15"
        }
    )

    emprestimo = buscar_ultimo_emprestimo()

    resposta = requests.delete(
        f"{BASE_URL}/emprestimos/{emprestimo['id']}"
    )

    assert resposta.status_code == 200

    assert resposta.json() == {
        "mensagem": "Empréstimo removido com sucesso"
    }
    
    
def test_emprestimo_removido_nao_aparece_na_lista():

    cliente_id = criar_cliente_teste()

    livro_id = criar_livro_teste()

    requests.post(
        f"{BASE_URL}/emprestimos",
        json={
            "cliente_id": cliente_id,
            "livro_id": livro_id,
            "data_emprestimo": "2026-06-15"
        }
    )

    emprestimo = buscar_ultimo_emprestimo()
    
    resposta = requests.delete(
        f"{BASE_URL}/emprestimos/{emprestimo['id']}"
    )

    assert resposta.status_code == 200


    emprestimos = requests.get(
        f"{BASE_URL}/emprestimos"
    ).json()

    ids = [e["id"] for e in emprestimos]

    assert emprestimo["id"] not in ids
    
    

def test_fluxo_completo_emprestimo():

    cliente_id = criar_cliente_teste()

    livro_id = criar_livro_teste()

    resposta = requests.post(
        f"{BASE_URL}/emprestimos",
        json={
            "cliente_id": cliente_id,
            "livro_id": livro_id,
            "data_emprestimo": "2026-06-15"
        }
    )

    assert resposta.status_code == 201

    emprestimo = buscar_ultimo_emprestimo()

    resposta = requests.put(
        f"{BASE_URL}/emprestimos/{emprestimo['id']}/devolver",
        json={
            "data_devolucao": "2026-06-20"
        }
    )

    assert resposta.status_code == 200

    resposta = requests.delete(
        f"{BASE_URL}/emprestimos/{emprestimo['id']}"
    )

    assert resposta.status_code == 200
    
    emprestimos = requests.get(
        f"{BASE_URL}/emprestimos"
    ).json()

    ids = [e["id"] for e in emprestimos]

    assert emprestimo["id"] not in ids
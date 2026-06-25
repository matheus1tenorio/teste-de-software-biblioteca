import uuid
import requests
import pytest

BASE_URL = "http://localhost:5002"


def gerar_titulo():
    return f"Livro Teste {uuid.uuid4().hex[:8]}"


def criar_livro_teste(titulo=None):
    """Helper para criar livro e retornar seu ID"""
    if titulo is None:
        titulo = gerar_titulo()

    resposta = requests.post(
        f"{BASE_URL}/livros",
        json={
            "titulo": titulo,
            "autor": "Autor Teste",
            "ano": 2026
        }
    )
    assert resposta.status_code == 201, f"Falha ao criar livro: {resposta.text}"

    # Busca o livro pelo título (já que o POST não retorna ID)
    livros = requests.get(f"{BASE_URL}/livros").json()
    livro = next((l for l in livros if l["titulo"] == titulo), None)
    assert livro is not None, "Livro criado não foi encontrado na listagem"
    return livro["id"]


# ==================== TESTES ====================

def test_listar_livros_retorna_200():
    resposta = requests.get(f"{BASE_URL}/livros")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)


def test_criar_livro_com_dados_validos():
    titulo = gerar_titulo()
    resposta = requests.post(
        f"{BASE_URL}/livros",
        json={
            "titulo": titulo,
            "autor": "Autor Teste",
            "ano": 2026
        }
    )

    assert resposta.status_code == 201
    assert resposta.json()["mensagem"] == "Livro criado com sucesso"


def test_criar_livro_sem_titulo():
    resposta = requests.post(
        f"{BASE_URL}/livros",
        json={
            "autor": "Autor Teste",
            "ano": 2026
        }
    )

    assert resposta.status_code == 400
    assert resposta.json()["erro"] == "titulo e autor são obrigatórios"


def test_buscar_livro_por_id_retorna_200():
    livro_id = criar_livro_teste()
    
    resposta = requests.get(f"{BASE_URL}/livros/{livro_id}")
    assert resposta.status_code == 200
    assert resposta.json()["id"] == livro_id


def test_buscar_livro_inexistente_retorna_404():
    resposta = requests.get(f"{BASE_URL}/livros/999999")
    assert resposta.status_code == 404
    assert "erro" in resposta.json()


def test_atualizar_livro_retorna_200():
    livro_id = criar_livro_teste()
    
    resposta = requests.put(
        f"{BASE_URL}/livros/{livro_id}",
        json={
            "titulo": "Livro Atualizado",
            "autor": "Autor Atualizado",
            "ano": 2025
        }
    )

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Livro atualizado com sucesso"


def test_deletar_livro_retorna_200():
    livro_id = criar_livro_teste()
    
    resposta = requests.delete(f"{BASE_URL}/livros/{livro_id}")
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Livro removido com sucesso"


def test_deletar_livro_inexistente_retorna_404():
    resposta = requests.delete(f"{BASE_URL}/livros/999999")
    assert resposta.status_code == 404


# ==================== FLUXO COMPLETO ====================

def test_fluxo_crud_livro_completo():
    """Cria → Busca → Atualiza → Deleta"""
    titulo_original = gerar_titulo()
    
    # Criar
    livro_id = criar_livro_teste(titulo_original)
    
    # Buscar
    resposta = requests.get(f"{BASE_URL}/livros/{livro_id}")
    assert resposta.status_code == 200
    
    # Atualizar
    novo_titulo = gerar_titulo()
    resposta = requests.put(
        f"{BASE_URL}/livros/{livro_id}",
        json={
            "titulo": novo_titulo,
            "autor": "Autor Modificado",
            "ano": 2027
        }
    )
    assert resposta.status_code == 200
    
    # Verificar atualização
    livro_atualizado = requests.get(f"{BASE_URL}/livros/{livro_id}").json()
    assert livro_atualizado["titulo"] == novo_titulo
    
    # Deletar
    resposta = requests.delete(f"{BASE_URL}/livros/{livro_id}")
    assert resposta.status_code == 200
    
    # Verificar que foi deletado
    resposta = requests.get(f"{BASE_URL}/livros/{livro_id}")
    assert resposta.status_code == 404
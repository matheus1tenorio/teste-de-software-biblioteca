import uuid
import pytest
import requests

BASE_URL = "http://localhost:5001"
CLIENTES_URL = f"{BASE_URL}/clientes"
ID_INEXISTENTE = 9999


def gerar_email():
    """Gera um e-mail único para evitar conflitos de unicidade no banco."""
    return f"{uuid.uuid4().hex[:8]}@teste.com"


def buscar_id_por_email(email):
    """Retorna o id do cliente com o e-mail informado, ou None."""
    clientes = requests.get(CLIENTES_URL).json()
    cliente  = next((c for c in clientes if c["email"] == email), None)
    return cliente["id"] if cliente else None


class TestClienteIntegration:

    @classmethod
    def setup_class(cls):
        try:
            resposta = requests.get(CLIENTES_URL, timeout=5)
            assert resposta.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.fail(
                "Não foi possível conectar ao cliente_service em http://localhost:5001.\n"
                "Execute 'docker compose up -d' e tente novamente."
            )

        cls.email_fixture = gerar_email()
        resposta = requests.post(
            CLIENTES_URL,
            json={"nome": "Cliente Fixture", "email": cls.email_fixture},
        )
        assert resposta.status_code == 201, (
            f"Falha ao criar cliente fixture: {resposta.status_code} — {resposta.text}"
        )

        cls.cid = buscar_id_por_email(cls.email_fixture)
        assert cls.cid is not None, "Id do cliente fixture não encontrado após criação."

    @classmethod
    def teardown_class(cls):
        if getattr(cls, "cid", None):
            requests.delete(f"{CLIENTES_URL}/{cls.cid}")

    def _restaurar_fixture(self):
        requests.put(
            f"{CLIENTES_URL}/{self.cid}",
            json={"nome": "Cliente Fixture", "email": self.email_fixture},
        )

    def test_listar_clientes_retorna_200_e_lista(self):
        resposta = requests.get(CLIENTES_URL)

        assert resposta.status_code == 200
        assert isinstance(resposta.json(), list)

    def test_listar_clientes_retorna_content_type_json(self):
        resposta = requests.get(CLIENTES_URL)

        assert "application/json" in resposta.headers.get("Content-Type", "")

    def test_criar_cliente_com_dados_validos_retorna_201(self):
        email    = gerar_email()
        resposta = requests.post(CLIENTES_URL, json={"nome": "João", "email": email})

        assert resposta.status_code == 201
        assert resposta.json().get("mensagem") == "Cliente criado com sucesso"

        cid = buscar_id_por_email(email)
        if cid:
            requests.delete(f"{CLIENTES_URL}/{cid}")

    def test_criar_cliente_sem_nome_retorna_400(self):
        resposta = requests.post(CLIENTES_URL, json={"email": gerar_email()})

        assert resposta.status_code == 400
        assert "erro" in resposta.json()

    def test_criar_cliente_sem_email_retorna_400(self):
        resposta = requests.post(CLIENTES_URL, json={"nome": "João"})

        assert resposta.status_code == 400
        assert "erro" in resposta.json()

    def test_criar_cliente_sem_nenhum_campo_retorna_400(self):
        resposta = requests.post(CLIENTES_URL, json={})

        assert resposta.status_code == 400
        assert "erro" in resposta.json()

    def test_buscar_cliente_existente_retorna_200_com_dados_corretos(self):
        resposta = requests.get(f"{CLIENTES_URL}/{self.cid}")
        dados    = resposta.json()

        assert resposta.status_code == 200
        assert dados["id"]    == self.cid
        assert dados["email"] == self.email_fixture

    def test_buscar_cliente_retorna_todos_os_campos_esperados(self):
        dados = requests.get(f"{CLIENTES_URL}/{self.cid}").json()

        for campo in ("id", "nome", "email", "matricula"):
            assert campo in dados, f"Campo obrigatório ausente na resposta: '{campo}'"

    def test_buscar_cliente_inexistente_retorna_404(self):
        resposta = requests.get(f"{CLIENTES_URL}/{ID_INEXISTENTE}")

        assert resposta.status_code == 404
        assert "erro" in resposta.json()

    def test_atualizar_cliente_com_dados_validos_retorna_200(self):
        resposta = requests.put(
            f"{CLIENTES_URL}/{self.cid}",
            json={"nome": "Nome Atualizado", "email": gerar_email()},
        )

        assert resposta.status_code == 200
        assert resposta.json().get("mensagem") == "Cliente atualizado com sucesso"
        self._restaurar_fixture()

    def test_atualizar_cliente_persiste_dados_no_banco(self):
        novo_email = gerar_email()
        requests.put(
            f"{CLIENTES_URL}/{self.cid}",
            json={"nome": "Nome Persistido", "email": novo_email},
        )

        dados = requests.get(f"{CLIENTES_URL}/{self.cid}").json()
        assert dados["nome"]  == "Nome Persistido"
        assert dados["email"] == novo_email
        self._restaurar_fixture()

    def test_atualizar_cliente_sem_nome_retorna_400(self):
        resposta = requests.put(
            f"{CLIENTES_URL}/{self.cid}",
            json={"email": gerar_email()},
        )

        assert resposta.status_code == 400
        assert "erro" in resposta.json()

    def test_atualizar_cliente_sem_email_retorna_400(self):
        resposta = requests.put(
            f"{CLIENTES_URL}/{self.cid}",
            json={"nome": "Só Nome"},
        )

        assert resposta.status_code == 400
        assert "erro" in resposta.json()

    def test_atualizar_cliente_inexistente_retorna_404(self):
        resposta = requests.put(
            f"{CLIENTES_URL}/{ID_INEXISTENTE}",
            json={"nome": "Fantasma", "email": gerar_email()},
        )

        assert resposta.status_code == 404
        assert "erro" in resposta.json()

    def test_remover_cliente_inexistente_retorna_404(self):
        resposta = requests.delete(f"{CLIENTES_URL}/{ID_INEXISTENTE}")

        assert resposta.status_code == 404
        assert "erro" in resposta.json()

    def test_remover_cliente_existente_retorna_200_e_some_do_banco(self):
        email    = gerar_email()
        requests.post(CLIENTES_URL, json={"nome": "Para Remover", "email": email})
        cid_temp = buscar_id_por_email(email)
        assert cid_temp is not None, "Registro criado para remoção não foi encontrado."

        resposta = requests.delete(f"{CLIENTES_URL}/{cid_temp}")
        assert resposta.status_code == 200
        assert resposta.json().get("mensagem") == "Cliente removido com sucesso"

        assert requests.get(f"{CLIENTES_URL}/{cid_temp}").status_code == 404

    # Fluxo CRUD completo

    def test_fluxo_crud_completo(self):
        """Cria → busca → atualiza → deleta um cliente em sequência."""
        email_inicial    = gerar_email()
        email_atualizado = gerar_email()

        # Criar
        resposta = requests.post(CLIENTES_URL, json={"nome": "Ciclo", "email": email_inicial})
        assert resposta.status_code == 201

        cid = buscar_id_por_email(email_inicial)
        assert cid is not None, "Cliente criado no fluxo CRUD não foi encontrado."

        # Buscar
        resposta = requests.get(f"{CLIENTES_URL}/{cid}")
        assert resposta.status_code == 200
        assert resposta.json()["nome"] == "Ciclo"

        # Atualizar
        resposta = requests.put(
            f"{CLIENTES_URL}/{cid}",
            json={"nome": "Ciclo Atualizado", "email": email_atualizado},
        )
        assert resposta.status_code == 200
        assert requests.get(f"{CLIENTES_URL}/{cid}").json()["nome"] == "Ciclo Atualizado"

        # Deletar
        assert requests.delete(f"{CLIENTES_URL}/{cid}").status_code == 200
        assert requests.get(f"{CLIENTES_URL}/{cid}").status_code == 404
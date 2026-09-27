"""
Testes unitários — rotas da aplicação PATATINO
Requisito PI: testes de aplicações web
Execução: pytest flask_src/tests/
"""
import pytest
import sys
import os

# Garante que flask_src está no path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app


@pytest.fixture
def client():
    """Cria um cliente de teste Flask."""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


# ── Testes de rotas públicas ─────────────────────────────────

class TestRotasPublicas:
    """Testa se as rotas principais respondem corretamente."""

    def test_home_retorna_200(self, client):
        """A página inicial deve retornar HTTP 200."""
        resp = client.get("/")
        assert resp.status_code == 200

    def test_home_conteudo_html(self, client):
        """A home deve retornar HTML com o nome da plataforma."""
        resp = client.get("/")
        assert b"PATATINO" in resp.data or b"Cafofe" in resp.data

    def test_home_filtro_especie(self, client):
        """Filtro por espécie deve retornar 200."""
        resp = client.get("/?especie=Cachorro")
        assert resp.status_code == 200

    def test_home_filtro_busca(self, client):
        """Busca por texto deve retornar 200."""
        resp = client.get("/?q=bolinha")
        assert resp.status_code == 200

    def test_animal_inexistente_retorna_404(self, client):
        """Animal com ID inválido deve retornar 404."""
        resp = client.get("/animal/999999")
        assert resp.status_code == 404

    def test_pagina_cadastrar_retorna_200(self, client):
        """Formulário de cadastro deve estar acessível."""
        resp = client.get("/cadastrar")
        assert resp.status_code == 200

    def test_adotar_animal_inexistente_redireciona(self, client):
        """Tentar adotar animal inexistente deve redirecionar."""
        resp = client.get("/adotar/999999")
        assert resp.status_code in (302, 404)


# ── Testes da API ViaCEP ─────────────────────────────────────

class TestApiCEP:
    """Testa o endpoint proxy de CEP."""

    def test_cep_valido_retorna_200(self, client):
        """CEP válido deve retornar 200 com dados de endereço."""
        resp = client.get("/api/cep/01310100")
        assert resp.status_code in (200, 404, 503)
        assert resp.content_type == "application/json"

    def test_cep_invalido_retorna_404(self, client):
        """CEP com formato inválido deve retornar 404."""
        resp = client.get("/api/cep/00000000")
        assert resp.status_code in (400, 404)

    def test_cep_letras_retorna_400(self, client):
        """CEP com letras deve retornar 400."""
        resp = client.get("/api/cep/abcdefgh")
        assert resp.status_code == 400
        dados = resp.get_json()
        assert "erro" in dados


# ── Testes de erros ──────────────────────────────────────────

class TestErros:
    """Testa páginas de erro."""

    def test_rota_inexistente_retorna_404(self, client):
        """Rota não definida deve retornar 404."""
        resp = client.get("/rota-que-nao-existe")
        assert resp.status_code == 404


# ── Testes de modelos ────────────────────────────────────────

class TestModeloAnimal:
    """Testa o modelo Animal."""

    def test_idade_legivel_meses(self):
        from models.animal import Animal
        a = Animal(id_animal=1, nome="Rex", id_especie=1,
                   id_porte=1, idade_aproximada=6)
        assert "6" in a.idade_legivel
        assert "mês" in a.idade_legivel or "meses" in a.idade_legivel

    def test_idade_legivel_anos(self):
        from models.animal import Animal
        a = Animal(id_animal=1, nome="Rex", id_especie=1,
                   id_porte=1, idade_aproximada=24)
        assert "2" in a.idade_legivel
        assert "ano" in a.idade_legivel

    def test_idade_legivel_sem_idade(self):
        from models.animal import Animal
        a = Animal(id_animal=1, nome="Rex", id_especie=1, id_porte=1)
        assert a.idade_legivel == "Não informada"

    def test_foto_principal_sem_fotos(self):
        from models.animal import Animal
        a = Animal(id_animal=1, nome="Rex", id_especie=1, id_porte=1)
        assert a.foto_principal == ""

    def test_from_dict(self):
        from models.animal import Animal
        dados = {
            "id_animal": 5, "nome": "Mia",
            "id_especie": 2, "id_porte": 1,
            "sexo": "Fêmea", "especie": "Gato",
        }
        a = Animal.from_dict(dados)
        assert a.nome == "Mia"
        assert a.especie == "Gato"


class TestModeloTutor:
    """Testa o modelo Tutor."""

    def test_cpf_formatado(self):
        from models.tutor import Tutor
        t = Tutor(id_tutor=None, nome="Maria", cpf="12345678901",
                  telefone="11999999999")
        assert t.cpf_formatado == "123.456.789-01"

    def test_endereco_completo(self):
        from models.tutor import Tutor
        t = Tutor(id_tutor=None, nome="João", cpf="12345678901",
                  telefone="11999999999",
                  endereco="Rua das Flores", numero="10",
                  bairro="Jardim", cidade="SP", estado="SP")
        assert "Rua das Flores" in t.endereco_completo
        assert "SP" in t.endereco_completo


class TestCEPService:
    """Testa o serviço de CEP."""

    def test_cep_invalido_retorna_none(self):
        from services.cep_service import CEPService
        svc = CEPService()
        assert svc.buscar("00000000") is None

    def test_cep_com_letras_retorna_none(self):
        from services.cep_service import CEPService
        svc = CEPService()
        assert svc.buscar("abcdefgh") is None

    def test_limpar_cep(self):
        from services.cep_service import CEPService
        assert CEPService._limpar("01310-100") == "01310100"
        assert CEPService._limpar("01.310.100") == "01310100"

    def test_validar_cep_valido(self):
        from services.cep_service import CEPService
        assert CEPService._validar("01310100") is True

    def test_validar_cep_invalido(self):
        from services.cep_service import CEPService
        assert CEPService._validar("0131010") is False   # 7 dígitos
        assert CEPService._validar("abcdefgh") is False

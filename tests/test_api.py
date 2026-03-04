from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.infrastructure.persistence.db import veiculo_venda_repo_instance, venda_repo_instance
from app.domain.entities.veiculo_venda import VeiculoVenda
from app.domain.entities.venda import Venda


client = TestClient(app)


def _limpar_repos():
    veiculo_venda_repo_instance.storage.clear()
    venda_repo_instance.storage.clear()


class TestHealthCheck:
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.json()["service"] == "servico-vendas"


class TestSyncVeiculoAPI:
    def setup_method(self):
        _limpar_repos()

    def test_sincronizar_veiculo(self):
        response = client.post("/veiculos/sync", json={
            "id": "v1", "marca": "Toyota", "modelo": "Corolla",
            "ano": 2023, "cor": "Branco", "preco": 120000.0,
            "status": "DISPONIVEL", "created_at": "2024-01-01"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "v1"
        assert data["marca"] == "Toyota"


class TestListarVeiculosAPI:
    def setup_method(self):
        _limpar_repos()

    def test_listar_veiculos_a_venda(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=150000.0)
        v2 = VeiculoVenda(id="v2", marca="Honda", modelo="Civic", ano=2022, cor="Preto", preco=100000.0)
        veiculo_venda_repo_instance.salvar(v1)
        veiculo_venda_repo_instance.salvar(v2)
        response = client.get("/veiculos/a-venda")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["preco"] <= data[1]["preco"]

    def test_listar_veiculos_vendidos(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=150000.0)
        v1.marcar_vendido()
        veiculo_venda_repo_instance.salvar(v1)
        response = client.get("/veiculos/vendidos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_listar_veiculos_a_venda_vazio(self):
        response = client.get("/veiculos/a-venda")
        assert response.status_code == 200
        assert response.json() == []


class TestEfetuarVendaAPI:
    def setup_method(self):
        _limpar_repos()

    @patch("app.infrastructure.controllers.veiculo_venda_controller._registrar_pagamento_servico_principal")
    def test_efetuar_venda_sucesso(self, mock_registrar):
        mock_registrar.return_value = {"codigo_pagamento": "cod-test-123"}
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        veiculo_venda_repo_instance.salvar(v1)
        response = client.post("/veiculos/comprar", json={
            "veiculo_id": "v1", "cpf_comprador": "12345678901"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["veiculo_id"] == "v1"
        assert data["cpf_comprador"] == "12345678901"
        assert data["codigo_pagamento"] == "cod-test-123"

    @patch("app.infrastructure.controllers.veiculo_venda_controller._registrar_pagamento_servico_principal")
    def test_efetuar_venda_com_data(self, mock_registrar):
        mock_registrar.return_value = {}
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        veiculo_venda_repo_instance.salvar(v1)
        response = client.post("/veiculos/comprar", json={
            "veiculo_id": "v1", "cpf_comprador": "12345678901", "data_venda": "2024-06-15"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["data_venda"] == "2024-06-15"

    def test_efetuar_venda_veiculo_nao_encontrado(self):
        response = client.post("/veiculos/comprar", json={
            "veiculo_id": "nao_existe", "cpf_comprador": "12345678901"
        })
        assert response.status_code == 400

    def test_efetuar_venda_veiculo_indisponivel(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v1.marcar_vendido()
        veiculo_venda_repo_instance.salvar(v1)
        response = client.post("/veiculos/comprar", json={
            "veiculo_id": "v1", "cpf_comprador": "12345678901"
        })
        assert response.status_code == 400


class TestStatusPagamentoAPI:
    def setup_method(self):
        _limpar_repos()

    def test_atualizar_status_pagamento_pago(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v1.marcar_vendido()
        veiculo_venda_repo_instance.salvar(v1)
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        venda_repo_instance.salvar(venda)
        response = client.put("/veiculos/v1/status-pagamento", json={
            "status": "PAGO", "codigo_pagamento": "cod123"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["veiculo_status"] == "PAGO"

    def test_atualizar_status_pagamento_cancelado(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        v1.marcar_vendido()
        veiculo_venda_repo_instance.salvar(v1)
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        venda_repo_instance.salvar(venda)
        response = client.put("/veiculos/v1/status-pagamento", json={
            "status": "CANCELADO", "codigo_pagamento": "cod123"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["veiculo_status"] == "DISPONIVEL"

    def test_atualizar_status_veiculo_nao_encontrado(self):
        response = client.put("/veiculos/nao_existe/status-pagamento", json={
            "status": "PAGO", "codigo_pagamento": "cod123"
        })
        assert response.status_code == 404


class TestBuscarVeiculoAPI:
    def setup_method(self):
        _limpar_repos()

    def test_buscar_veiculo_existente(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        veiculo_venda_repo_instance.salvar(v1)
        response = client.get("/veiculos/v1")
        assert response.status_code == 200
        assert response.json()["id"] == "v1"

    def test_buscar_veiculo_nao_encontrado(self):
        response = client.get("/veiculos/nao_existe")
        assert response.status_code == 404

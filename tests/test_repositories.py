from app.infrastructure.persistence.db import InMemoryVeiculoVendaRepository, InMemoryVendaRepository
from app.domain.entities.veiculo_venda import VeiculoVenda
from app.domain.entities.venda import Venda


class TestInMemoryVeiculoVendaRepository:
    def setup_method(self):
        self.repo = InMemoryVeiculoVendaRepository()

    def test_salvar_e_buscar_por_id(self):
        veiculo = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.repo.salvar(veiculo)
        resultado = self.repo.buscar_por_id("v1")
        assert resultado is not None
        assert resultado.id == "v1"

    def test_buscar_por_id_inexistente(self):
        resultado = self.repo.buscar_por_id("nao_existe")
        assert resultado is None

    def test_listar_disponiveis(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=150000.0)
        v2 = VeiculoVenda(id="v2", marca="Honda", modelo="Civic", ano=2022, cor="Preto", preco=100000.0)
        v3 = VeiculoVenda(id="v3", marca="Ford", modelo="Ka", ano=2021, cor="Azul", preco=80000.0)
        v3.marcar_vendido()
        self.repo.salvar(v1)
        self.repo.salvar(v2)
        self.repo.salvar(v3)
        disponiveis = self.repo.listar_disponiveis()
        assert len(disponiveis) == 2
        assert disponiveis[0].preco <= disponiveis[1].preco

    def test_listar_vendidos(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=150000.0)
        v2 = VeiculoVenda(id="v2", marca="Honda", modelo="Civic", ano=2022, cor="Preto", preco=100000.0)
        v2.marcar_vendido()
        v3 = VeiculoVenda(id="v3", marca="Ford", modelo="Ka", ano=2021, cor="Azul", preco=80000.0)
        v3.marcar_pago()
        self.repo.salvar(v1)
        self.repo.salvar(v2)
        self.repo.salvar(v3)
        vendidos = self.repo.listar_vendidos()
        assert len(vendidos) == 2
        assert vendidos[0].preco <= vendidos[1].preco

    def test_atualizar(self):
        veiculo = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.repo.salvar(veiculo)
        veiculo.preco = 110000.0
        self.repo.atualizar(veiculo)
        resultado = self.repo.buscar_por_id("v1")
        assert resultado.preco == 110000.0


class TestInMemoryVendaRepository:
    def setup_method(self):
        self.repo = InMemoryVendaRepository()

    def test_salvar_e_buscar_por_id(self):
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        self.repo.salvar(venda)
        resultado = self.repo.buscar_por_id(venda.id)
        assert resultado is not None
        assert resultado.veiculo_id == "v1"

    def test_buscar_por_id_inexistente(self):
        resultado = self.repo.buscar_por_id("nao_existe")
        assert resultado is None

    def test_buscar_por_veiculo_id(self):
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        self.repo.salvar(venda)
        resultado = self.repo.buscar_por_veiculo_id("v1")
        assert resultado is not None
        assert resultado.cpf_comprador == "12345678901"

    def test_buscar_por_veiculo_id_inexistente(self):
        resultado = self.repo.buscar_por_veiculo_id("nao_existe")
        assert resultado is None

    def test_listar_todas(self):
        v1 = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        v2 = Venda(veiculo_id="v2", cpf_comprador="98765432100")
        self.repo.salvar(v1)
        self.repo.salvar(v2)
        todas = self.repo.listar_todas()
        assert len(todas) == 2

    def test_atualizar(self):
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        self.repo.salvar(venda)
        venda.confirmar_pagamento()
        self.repo.atualizar(venda)
        resultado = self.repo.buscar_por_id(venda.id)
        assert resultado.status == "PAGO"

import pytest
from app.infrastructure.persistence.db import InMemoryVeiculoVendaRepository, InMemoryVendaRepository
from app.domain.entities.veiculo_venda import VeiculoVenda
from app.application.dtos.veiculo_venda_dto import SyncVeiculoDTO
from app.application.dtos.venda_dto import EfetuarVendaDTO
from app.application.usecases.sincronizar_veiculo import SincronizarVeiculo
from app.application.usecases.listar_veiculos_a_venda import ListarVeiculosAVenda
from app.application.usecases.listar_veiculos_vendidos import ListarVeiculosVendidos
from app.application.usecases.efetuar_venda import EfetuarVenda
from app.application.usecases.atualizar_status_pagamento import AtualizarStatusPagamento


class TestSincronizarVeiculo:
    def setup_method(self):
        self.repo = InMemoryVeiculoVendaRepository()
        self.use_case = SincronizarVeiculo(self.repo)

    def test_sincronizar_novo_veiculo(self):
        dados = SyncVeiculoDTO(
            id="v1", marca="Toyota", modelo="Corolla", ano=2023,
            cor="Branco", preco=120000.0, status="DISPONIVEL", created_at="2024-01-01"
        )
        resultado = self.use_case.execute(dados)
        assert resultado.id == "v1"
        assert resultado.marca == "Toyota"

    def test_sincronizar_veiculo_existente(self):
        veiculo = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.repo.salvar(veiculo)
        dados = SyncVeiculoDTO(
            id="v1", marca="Toyota", modelo="Corolla", ano=2023,
            cor="Prata", preco=115000.0, status="DISPONIVEL", created_at="2024-01-01"
        )
        resultado = self.use_case.execute(dados)
        assert resultado.cor == "Prata"
        assert resultado.preco == 115000.0


class TestListarVeiculosAVenda:
    def setup_method(self):
        self.repo = InMemoryVeiculoVendaRepository()
        self.use_case = ListarVeiculosAVenda(self.repo)

    def test_listar_veiculos_disponiveis_ordenados_por_preco(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=150000.0)
        v2 = VeiculoVenda(id="v2", marca="Honda", modelo="Civic", ano=2022, cor="Preto", preco=100000.0)
        v3 = VeiculoVenda(id="v3", marca="Ford", modelo="Ka", ano=2021, cor="Azul", preco=80000.0)
        self.repo.salvar(v1)
        self.repo.salvar(v2)
        self.repo.salvar(v3)
        resultado = self.use_case.execute()
        assert len(resultado) == 3
        assert resultado[0].preco == 80000.0
        assert resultado[1].preco == 100000.0
        assert resultado[2].preco == 150000.0

    def test_listar_vazio(self):
        resultado = self.use_case.execute()
        assert len(resultado) == 0


class TestListarVeiculosVendidos:
    def setup_method(self):
        self.repo = InMemoryVeiculoVendaRepository()
        self.use_case = ListarVeiculosVendidos(self.repo)

    def test_listar_veiculos_vendidos_ordenados_por_preco(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=150000.0)
        v1.marcar_vendido()
        v2 = VeiculoVenda(id="v2", marca="Honda", modelo="Civic", ano=2022, cor="Preto", preco=100000.0)
        v2.marcar_pago()
        self.repo.salvar(v1)
        self.repo.salvar(v2)
        resultado = self.use_case.execute()
        assert len(resultado) == 2
        assert resultado[0].preco == 100000.0
        assert resultado[1].preco == 150000.0

    def test_listar_sem_vendidos(self):
        v1 = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=150000.0)
        self.repo.salvar(v1)
        resultado = self.use_case.execute()
        assert len(resultado) == 0


class TestEfetuarVenda:
    def setup_method(self):
        self.veiculo_repo = InMemoryVeiculoVendaRepository()
        self.venda_repo = InMemoryVendaRepository()
        self.use_case = EfetuarVenda(self.venda_repo, self.veiculo_repo)

    def test_efetuar_venda_sucesso(self):
        veiculo = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.veiculo_repo.salvar(veiculo)
        dados = EfetuarVendaDTO(veiculo_id="v1", cpf_comprador="12345678901")
        venda = self.use_case.execute(dados)
        assert venda.veiculo_id == "v1"
        assert venda.cpf_comprador == "12345678901"
        assert venda.status == "PENDENTE"
        veiculo_atualizado = self.veiculo_repo.buscar_por_id("v1")
        assert veiculo_atualizado.status == "VENDIDO"

    def test_efetuar_venda_com_data(self):
        veiculo = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.veiculo_repo.salvar(veiculo)
        dados = EfetuarVendaDTO(veiculo_id="v1", cpf_comprador="12345678901", data_venda="2024-06-15")
        venda = self.use_case.execute(dados)
        assert venda.data_venda == "2024-06-15"

    def test_efetuar_venda_veiculo_nao_encontrado(self):
        dados = EfetuarVendaDTO(veiculo_id="nao_existe", cpf_comprador="12345678901")
        with pytest.raises(ValueError, match="Veiculo nao encontrado"):
            self.use_case.execute(dados)

    def test_efetuar_venda_veiculo_indisponivel(self):
        veiculo = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        veiculo.marcar_vendido()
        self.veiculo_repo.salvar(veiculo)
        dados = EfetuarVendaDTO(veiculo_id="v1", cpf_comprador="12345678901")
        with pytest.raises(ValueError, match="Veiculo nao esta disponivel"):
            self.use_case.execute(dados)


class TestAtualizarStatusPagamento:
    def setup_method(self):
        self.veiculo_repo = InMemoryVeiculoVendaRepository()
        self.venda_repo = InMemoryVendaRepository()
        self.use_case = AtualizarStatusPagamento(self.venda_repo, self.veiculo_repo)

    def _criar_veiculo_e_venda(self):
        from app.domain.entities.venda import Venda
        veiculo = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        veiculo.marcar_vendido()
        self.veiculo_repo.salvar(veiculo)
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        self.venda_repo.salvar(venda)
        return veiculo, venda

    def test_atualizar_status_pago(self):
        veiculo, venda = self._criar_veiculo_e_venda()
        resultado = self.use_case.execute("v1", "PAGO", "cod123")
        assert resultado["veiculo_status"] == "PAGO"
        assert resultado["venda"]["status"] == "PAGO"
        assert resultado["venda"]["codigo_pagamento"] == "cod123"

    def test_atualizar_status_cancelado(self):
        veiculo, venda = self._criar_veiculo_e_venda()
        resultado = self.use_case.execute("v1", "CANCELADO", "cod123")
        assert resultado["veiculo_status"] == "DISPONIVEL"
        assert resultado["venda"]["status"] == "CANCELADO"

    def test_atualizar_status_invalido(self):
        veiculo, venda = self._criar_veiculo_e_venda()
        with pytest.raises(ValueError, match="Status invalido"):
            self.use_case.execute("v1", "INVALIDO", "cod123")

    def test_atualizar_veiculo_nao_encontrado(self):
        with pytest.raises(ValueError, match="Veiculo nao encontrado"):
            self.use_case.execute("nao_existe", "PAGO", "cod123")

    def test_atualizar_venda_nao_encontrada(self):
        veiculo = VeiculoVenda(id="v1", marca="Toyota", modelo="Corolla", ano=2023, cor="Branco", preco=120000.0)
        self.veiculo_repo.salvar(veiculo)
        with pytest.raises(ValueError, match="Venda nao encontrada"):
            self.use_case.execute("v1", "PAGO", "cod123")

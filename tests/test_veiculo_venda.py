from app.domain.entities.veiculo_venda import VeiculoVenda


class TestVeiculoVenda:
    def test_criar_veiculo_venda(self):
        veiculo = VeiculoVenda(
            id="v1", marca="Toyota", modelo="Corolla", ano=2023,
            cor="Branco", preco=120000.0, status="DISPONIVEL", created_at="2024-01-01"
        )
        assert veiculo.id == "v1"
        assert veiculo.marca == "Toyota"
        assert veiculo.modelo == "Corolla"
        assert veiculo.ano == 2023
        assert veiculo.cor == "Branco"
        assert veiculo.preco == 120000.0
        assert veiculo.status == "DISPONIVEL"

    def test_marcar_vendido(self):
        veiculo = VeiculoVenda(
            id="v1", marca="Toyota", modelo="Corolla", ano=2023,
            cor="Branco", preco=120000.0
        )
        veiculo.marcar_vendido()
        assert veiculo.status == "VENDIDO"

    def test_marcar_pago(self):
        veiculo = VeiculoVenda(
            id="v1", marca="Toyota", modelo="Corolla", ano=2023,
            cor="Branco", preco=120000.0
        )
        veiculo.marcar_pago()
        assert veiculo.status == "PAGO"

    def test_marcar_cancelado(self):
        veiculo = VeiculoVenda(
            id="v1", marca="Toyota", modelo="Corolla", ano=2023,
            cor="Branco", preco=120000.0
        )
        veiculo.marcar_cancelado()
        assert veiculo.status == "DISPONIVEL"

    def test_esta_disponivel(self):
        veiculo = VeiculoVenda(
            id="v1", marca="Toyota", modelo="Corolla", ano=2023,
            cor="Branco", preco=120000.0
        )
        assert veiculo.esta_disponivel() is True
        veiculo.marcar_vendido()
        assert veiculo.esta_disponivel() is False

    def test_to_dict(self):
        veiculo = VeiculoVenda(
            id="v1", marca="Toyota", modelo="Corolla", ano=2023,
            cor="Branco", preco=120000.0, status="DISPONIVEL", created_at="2024-01-01"
        )
        d = veiculo.to_dict()
        assert d["id"] == "v1"
        assert d["marca"] == "Toyota"
        assert d["preco"] == 120000.0
        assert d["status"] == "DISPONIVEL"

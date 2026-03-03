from app.domain.entities.venda import Venda


class TestVenda:
    def test_criar_venda(self):
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        assert venda.veiculo_id == "v1"
        assert venda.cpf_comprador == "12345678901"
        assert venda.status == "PENDENTE"
        assert venda.codigo_pagamento == ""
        assert venda.id is not None
        assert venda.data_venda != ""

    def test_criar_venda_com_data(self):
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901", data_venda="2024-06-15")
        assert venda.data_venda == "2024-06-15"

    def test_confirmar_pagamento(self):
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        venda.confirmar_pagamento()
        assert venda.status == "PAGO"

    def test_cancelar(self):
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        venda.cancelar()
        assert venda.status == "CANCELADO"

    def test_to_dict(self):
        venda = Venda(veiculo_id="v1", cpf_comprador="12345678901")
        d = venda.to_dict()
        assert d["veiculo_id"] == "v1"
        assert d["cpf_comprador"] == "12345678901"
        assert d["status"] == "PENDENTE"
        assert "id" in d
        assert "data_venda" in d
        assert "created_at" in d

from app.domain.repositories.venda_repository import VendaRepository
from app.domain.repositories.veiculo_venda_repository import VeiculoVendaRepository


class AtualizarStatusPagamento:
    def __init__(self, venda_repo: VendaRepository, veiculo_repo: VeiculoVendaRepository):
        self.venda_repo = venda_repo
        self.veiculo_repo = veiculo_repo

    def execute(self, veiculo_id: str, status: str, codigo_pagamento: str) -> dict:
        veiculo = self.veiculo_repo.buscar_por_id(veiculo_id)
        if not veiculo:
            raise ValueError("Veiculo nao encontrado")

        venda = self.venda_repo.buscar_por_veiculo_id(veiculo_id)
        if not venda:
            raise ValueError("Venda nao encontrada para este veiculo")

        venda.codigo_pagamento = codigo_pagamento

        if status == "PAGO":
            venda.confirmar_pagamento()
            veiculo.marcar_pago()
        elif status == "CANCELADO":
            venda.cancelar()
            veiculo.marcar_cancelado()
        else:
            raise ValueError("Status invalido. Use PAGO ou CANCELADO")

        self.venda_repo.atualizar(venda)
        self.veiculo_repo.atualizar(veiculo)

        return {
            "venda": venda.to_dict(),
            "veiculo_status": veiculo.status,
        }

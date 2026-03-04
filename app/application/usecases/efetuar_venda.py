from app.domain.entities.venda import Venda
from app.domain.repositories.venda_repository import VendaRepository
from app.domain.repositories.veiculo_venda_repository import VeiculoVendaRepository
from app.application.dtos.venda_dto import EfetuarVendaDTO


class EfetuarVenda:
    def __init__(self, venda_repo: VendaRepository, veiculo_repo: VeiculoVendaRepository):
        self.venda_repo = venda_repo
        self.veiculo_repo = veiculo_repo

    def execute(self, dados: EfetuarVendaDTO) -> Venda:
        veiculo = self.veiculo_repo.buscar_por_id(dados.veiculo_id)
        if not veiculo:
            raise ValueError("Veiculo nao encontrado")
        if not veiculo.esta_disponivel():
            raise ValueError("Veiculo nao esta disponivel para venda")

        veiculo.marcar_vendido()
        self.veiculo_repo.atualizar(veiculo)

        venda = Venda(
            veiculo_id=dados.veiculo_id,
            cpf_comprador=dados.cpf_comprador,
            data_venda=dados.data_venda if dados.data_venda else "",
        )
        self.venda_repo.salvar(venda)
        return venda

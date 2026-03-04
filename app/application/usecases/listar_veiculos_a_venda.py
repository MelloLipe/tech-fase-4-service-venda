from app.domain.repositories.veiculo_venda_repository import VeiculoVendaRepository
from app.domain.entities.veiculo_venda import VeiculoVenda


class ListarVeiculosAVenda:
    def __init__(self, repo: VeiculoVendaRepository):
        self.repo = repo

    def execute(self) -> list[VeiculoVenda]:
        return self.repo.listar_disponiveis()

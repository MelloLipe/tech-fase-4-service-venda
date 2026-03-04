from app.domain.entities.veiculo_venda import VeiculoVenda
from app.domain.repositories.veiculo_venda_repository import VeiculoVendaRepository
from app.application.dtos.veiculo_venda_dto import SyncVeiculoDTO


class SincronizarVeiculo:
    def __init__(self, repo: VeiculoVendaRepository):
        self.repo = repo

    def execute(self, dados: SyncVeiculoDTO) -> VeiculoVenda:
        existente = self.repo.buscar_por_id(dados.id)
        if existente:
            existente.marca = dados.marca
            existente.modelo = dados.modelo
            existente.ano = dados.ano
            existente.cor = dados.cor
            existente.preco = dados.preco
            existente.status = dados.status
            existente.created_at = dados.created_at
            self.repo.atualizar(existente)
            return existente

        veiculo = VeiculoVenda(
            id=dados.id,
            marca=dados.marca,
            modelo=dados.modelo,
            ano=dados.ano,
            cor=dados.cor,
            preco=dados.preco,
            status=dados.status,
            created_at=dados.created_at,
        )
        self.repo.salvar(veiculo)
        return veiculo

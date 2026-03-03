from typing import Optional
from app.domain.repositories.veiculo_venda_repository import VeiculoVendaRepository
from app.domain.entities.veiculo_venda import VeiculoVenda
from app.domain.repositories.venda_repository import VendaRepository
from app.domain.entities.venda import Venda


class InMemoryVeiculoVendaRepository(VeiculoVendaRepository):
    def __init__(self):
        self.storage: dict[str, VeiculoVenda] = {}

    def salvar(self, veiculo: VeiculoVenda) -> None:
        self.storage[veiculo.id] = veiculo

    def buscar_por_id(self, veiculo_id: str) -> Optional[VeiculoVenda]:
        return self.storage.get(veiculo_id)

    def listar_disponiveis(self) -> list[VeiculoVenda]:
        return sorted(
            [v for v in self.storage.values() if v.esta_disponivel()],
            key=lambda v: v.preco,
        )

    def listar_vendidos(self) -> list[VeiculoVenda]:
        return sorted(
            [v for v in self.storage.values() if v.status in ("VENDIDO", "PAGO")],
            key=lambda v: v.preco,
        )

    def atualizar(self, veiculo: VeiculoVenda) -> None:
        self.storage[veiculo.id] = veiculo


class InMemoryVendaRepository(VendaRepository):
    def __init__(self):
        self.storage: dict[str, Venda] = {}

    def salvar(self, venda: Venda) -> None:
        self.storage[venda.id] = venda

    def buscar_por_id(self, venda_id: str) -> Optional[Venda]:
        return self.storage.get(venda_id)

    def buscar_por_veiculo_id(self, veiculo_id: str) -> Optional[Venda]:
        for venda in self.storage.values():
            if venda.veiculo_id == veiculo_id:
                return venda
        return None

    def listar_todas(self) -> list[Venda]:
        return list(self.storage.values())

    def atualizar(self, venda: Venda) -> None:
        self.storage[venda.id] = venda


veiculo_venda_repo_instance = InMemoryVeiculoVendaRepository()
venda_repo_instance = InMemoryVendaRepository()

from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.veiculo_venda import VeiculoVenda


class VeiculoVendaRepository(ABC):
    @abstractmethod
    def salvar(self, veiculo: VeiculoVenda) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, veiculo_id: str) -> Optional[VeiculoVenda]:
        pass

    @abstractmethod
    def listar_disponiveis(self) -> list[VeiculoVenda]:
        pass

    @abstractmethod
    def listar_vendidos(self) -> list[VeiculoVenda]:
        pass

    @abstractmethod
    def atualizar(self, veiculo: VeiculoVenda) -> None:
        pass

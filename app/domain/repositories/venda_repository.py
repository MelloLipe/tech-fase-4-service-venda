from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.venda import Venda


class VendaRepository(ABC):
    @abstractmethod
    def salvar(self, venda: Venda) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, venda_id: str) -> Optional[Venda]:
        pass

    @abstractmethod
    def buscar_por_veiculo_id(self, veiculo_id: str) -> Optional[Venda]:
        pass

    @abstractmethod
    def listar_todas(self) -> list[Venda]:
        pass

    @abstractmethod
    def atualizar(self, venda: Venda) -> None:
        pass

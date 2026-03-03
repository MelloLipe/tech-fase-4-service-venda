from pydantic import BaseModel
from typing import Optional


class EfetuarVendaDTO(BaseModel):
    veiculo_id: str
    cpf_comprador: str
    data_venda: Optional[str] = None


class VendaResponseDTO(BaseModel):
    id: str
    veiculo_id: str
    cpf_comprador: str
    data_venda: str
    codigo_pagamento: str
    status: str
    created_at: str

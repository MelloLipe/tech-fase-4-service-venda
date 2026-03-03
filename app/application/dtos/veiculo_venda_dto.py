from pydantic import BaseModel
from typing import Optional


class SyncVeiculoDTO(BaseModel):
    id: str
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: float
    status: str = "DISPONIVEL"
    created_at: str = ""


class VeiculoVendaResponseDTO(BaseModel):
    id: str
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: float
    status: str
    created_at: str


class StatusPagamentoDTO(BaseModel):
    status: str
    codigo_pagamento: str

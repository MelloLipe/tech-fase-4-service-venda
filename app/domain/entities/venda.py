import uuid
from datetime import datetime, timezone


class Venda:
    def __init__(self, veiculo_id: str, cpf_comprador: str, data_venda: str = ""):
        self.id = str(uuid.uuid4())
        self.veiculo_id = veiculo_id
        self.cpf_comprador = cpf_comprador
        self.data_venda = data_venda if data_venda else datetime.now(timezone.utc).isoformat()
        self.codigo_pagamento = ""
        self.status = "PENDENTE"
        self.created_at = datetime.now(timezone.utc).isoformat()

    def confirmar_pagamento(self):
        self.status = "PAGO"

    def cancelar(self):
        self.status = "CANCELADO"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "veiculo_id": self.veiculo_id,
            "cpf_comprador": self.cpf_comprador,
            "data_venda": self.data_venda,
            "codigo_pagamento": self.codigo_pagamento,
            "status": self.status,
            "created_at": self.created_at,
        }

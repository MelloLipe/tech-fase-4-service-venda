class VeiculoVenda:
    def __init__(self, id: str, marca: str, modelo: str, ano: int, cor: str,
                 preco: float, status: str = "DISPONIVEL", created_at: str = ""):
        self.id = id
        self.marca = marca
        self.modelo = modelo
        self.ano = ano
        self.cor = cor
        self.preco = preco
        self.status = status
        self.created_at = created_at

    def marcar_vendido(self):
        self.status = "VENDIDO"

    def marcar_pago(self):
        self.status = "PAGO"

    def marcar_cancelado(self):
        self.status = "DISPONIVEL"

    def esta_disponivel(self) -> bool:
        return self.status == "DISPONIVEL"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "cor": self.cor,
            "preco": self.preco,
            "status": self.status,
            "created_at": self.created_at,
        }

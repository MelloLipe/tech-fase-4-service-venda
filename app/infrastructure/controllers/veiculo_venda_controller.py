import httpx
from fastapi import APIRouter, HTTPException

from app.application.dtos.veiculo_venda_dto import SyncVeiculoDTO, StatusPagamentoDTO
from app.application.dtos.venda_dto import EfetuarVendaDTO
from app.application.usecases.sincronizar_veiculo import SincronizarVeiculo
from app.application.usecases.listar_veiculos_a_venda import ListarVeiculosAVenda
from app.application.usecases.listar_veiculos_vendidos import ListarVeiculosVendidos
from app.application.usecases.efetuar_venda import EfetuarVenda
from app.application.usecases.atualizar_status_pagamento import AtualizarStatusPagamento
from app.infrastructure.persistence.db import veiculo_venda_repo_instance, venda_repo_instance
from app.config.config import settings

router = APIRouter()


@router.get("/a-venda")
def listar_veiculos_a_venda():
    use_case = ListarVeiculosAVenda(veiculo_venda_repo_instance)
    veiculos = use_case.execute()
    return [v.to_dict() for v in veiculos]


@router.get("/vendidos")
def listar_veiculos_vendidos():
    use_case = ListarVeiculosVendidos(veiculo_venda_repo_instance)
    veiculos = use_case.execute()
    return [v.to_dict() for v in veiculos]


@router.post("/comprar")
def efetuar_venda(dados: EfetuarVendaDTO):
    use_case = EfetuarVenda(venda_repo_instance, veiculo_venda_repo_instance)
    try:
        venda = use_case.execute(dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    pagamento_response = _registrar_pagamento_servico_principal(
        venda.veiculo_id, dados.cpf_comprador
    )
    if pagamento_response:
        venda.codigo_pagamento = pagamento_response.get("codigo_pagamento", "")
        venda_repo_instance.atualizar(venda)

    return venda.to_dict()


@router.post("/sync")
def sincronizar_veiculo(dados: SyncVeiculoDTO):
    use_case = SincronizarVeiculo(veiculo_venda_repo_instance)
    veiculo = use_case.execute(dados)
    return veiculo.to_dict()


@router.put("/{veiculo_id}/status-pagamento")
def atualizar_status_pagamento(veiculo_id: str, dados: StatusPagamentoDTO):
    use_case = AtualizarStatusPagamento(venda_repo_instance, veiculo_venda_repo_instance)
    try:
        resultado = use_case.execute(veiculo_id, dados.status, dados.codigo_pagamento)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return resultado


@router.get("/{veiculo_id}")
def buscar_veiculo(veiculo_id: str):
    veiculo = veiculo_venda_repo_instance.buscar_por_id(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veiculo nao encontrado")
    return veiculo.to_dict()


def _registrar_pagamento_servico_principal(veiculo_id: str, cpf_comprador: str) -> dict:
    try:
        response = httpx.post(
            f"{settings.MAIN_SERVICE_URL}/pagamentos/registrar",
            params={"veiculo_id": veiculo_id, "cpf_comprador": cpf_comprador},
            timeout=5.0,
        )
        if response.status_code == 200:
            return response.json()
    except httpx.RequestError:
        pass
    return {}

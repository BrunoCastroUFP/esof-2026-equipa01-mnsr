"""Rotas REST de geração de roteiros."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from src.business.roteiros import (
    DuracaoInvalidaError,
    RoteiroIndisponivelError,
    ServicoRoteiros,
)
from src.presentation.dependencias import obter_servico_roteiros
from src.presentation.obras_api import ObraResposta

router = APIRouter(prefix="/api", tags=["roteiros"])


class PedidoRoteiro(BaseModel):
    tempo: int


class ObraRoteiroResposta(ObraResposta):
    destaque: bool
    tempo_estimado: int


class RoteiroResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tempo_solicitado: int
    tempo_total_estimado: int
    obras: list[ObraRoteiroResposta]


@router.post("/roteiros", response_model=RoteiroResposta)
def gerar_roteiro(
    pedido: PedidoRoteiro,
    servico: ServicoRoteiros = Depends(obter_servico_roteiros),
) -> RoteiroResposta:
    try:
        roteiro = servico.gerar_roteiro(pedido.tempo)
    except DuracaoInvalidaError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    except RoteiroIndisponivelError as erro:
        raise HTTPException(status_code=422, detail=str(erro)) from erro

    return RoteiroResposta.model_validate(roteiro)

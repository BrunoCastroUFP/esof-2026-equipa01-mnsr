"""Rotas REST do acervo"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from src.business.acervo import ServicoAcervo
from src.presentation.dependencias import obter_servico_acervo


router = APIRouter(prefix="/api", tags=["acervo"])


class ObraResposta(BaseModel):
    # O que a API devolve. Só saem estes campos: se um dia a Obra tiver um campo
    # interno (por exemplo, o código secreto do QR), não aparece na API sem querermos

    # from_attributes=True permite validar diretamente a dataclass Obra sem cópia manual
    model_config = ConfigDict(from_attributes=True)

    id: str
    titulo: str
    autor: str
    sala_id: str


@router.get("/obras", response_model=list[ObraResposta])
def listar_obras(
    servico: ServicoAcervo = Depends(obter_servico_acervo),
) -> list[ObraResposta]:
    # Depends: o FastAPI chama obter_servico_acervo() e passa o resultado.
    # Nos testes troca-se esta dependência por uma falsa
    return [
        ObraResposta(id=obra.id, titulo=obra.titulo, autor=obra.autor, sala_id=obra.sala_id)
        for obra in servico.listar_obras()
    ]

"""Rotas REST da caça ao tesouro"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4, BaseModel, ConfigDict, Field
from src.business.caca_tesouro import QRCodeNaoReconhecido, ValidadorQRCode
from src.presentation.dependencias import obter_validador_qr_code

router = APIRouter(prefix="/api/desafios", tags=["caça ao tesouro"])


class PedidoLeitura(BaseModel):
    # O corpo que o telemóvel envia. Pydantic valida-o antes de a rota correr:
    # se falhar alguma regra, o FastAPI responde 422 e o validador nem é chamado

    # extra="forbid": recusa campos a mais
    model_config = ConfigDict(extra="forbid")

    # A sessão anónima tem de ser um UUID versão 4, o que o telemóvel gera.
    # Recusa texto qualquer, como nomes ou e-mails (RNF-03)
    sessao_id: UUID4
    # "MNSR-" seguido de exatamente 6 letras maiúsculas ou algarismos, e nada mais.
    # ^ e $ marcam o início e o fim: uma quebra de linha no fim também é recusada
    codigo: str = Field(pattern=r"^MNSR-[A-Z0-9]{6}$")


class LeituraResposta(BaseModel):
    # O que a API devolve. Só saem estes campos, mesmo que o resultado tenha outros
    obra_id: str
    # O texto que a issue pede: "Obra encontrada" ou "Obra já descoberta"
    mensagem: str
    # Para a PWA decidir o que mostrar sem ter de comparar textos
    ja_descoberta: bool
    pontos_ganhos: int
    pontos_totais: int


@router.post("/validar", response_model=LeituraResposta)
def validar_qr_code(pedido: PedidoLeitura,validador: ValidadorQRCode = Depends(obter_validador_qr_code)) -> LeituraResposta:
    # Depends: o FastAPI chama obter_validador_qr_code() e passa o validador já montado
    # Nos testes e2e troca-se por um com a base de dados em memória
    try:
        # str() converte o UUID em texto, sempre em minúsculas: a mesma sessão escrita
        # em maiúsculas ou em minúsculas conta como uma só
        resultado = validador.validar(str(pedido.sessao_id), pedido.codigo)
    except QRCodeNaoReconhecido as erro:
        # Cenário 3. from erro liga as duas exceções, para o log mostrar a causa
        # A mensagem é fixa: não repete o código que o cliente enviou
        raise HTTPException(status_code=404, detail="QR Code não reconhecido") from erro

    # Cenários 1 e 2: as duas são respostas válidas (200), só muda a mensagem e os pontos
    return LeituraResposta(
        obra_id=resultado.obra_id,
        mensagem="Obra já descoberta" if resultado.ja_descoberta else "Obra encontrada",
        ja_descoberta=resultado.ja_descoberta,
        pontos_ganhos=resultado.pontos_ganhos,
        pontos_totais=resultado.pontos_totais,
    )

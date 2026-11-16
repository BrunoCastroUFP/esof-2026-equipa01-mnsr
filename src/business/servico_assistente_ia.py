from collections import deque
from typing import Protocol
from uuid import UUID

Turno = tuple[str, str]
MAX_TROCAS_HISTORICO = 10


class ClienteRAG(Protocol):
    def consultar(self, pergunta: str, historico: tuple[Turno, ...]) -> str:
        ...


class ServicoAssistenteIA:
    def __init__(self, cliente_rag: ClienteRAG):
        self.cliente_rag = cliente_rag
        self._historicos: dict[UUID, deque[Turno]] = {}

    def obter_informacao(self, sessao_id: UUID, pergunta: str) -> str:
        self._validar_sessao(sessao_id)
        historico = self._historicos.get(sessao_id)
        if historico is None:
            historico = deque(maxlen=MAX_TROCAS_HISTORICO)

        resposta = self.cliente_rag.consultar(pergunta, tuple(historico))
        historico.append((pergunta, resposta))
        self._historicos[sessao_id] = historico
        return resposta

    def fechar_sessao(self, sessao_id: UUID) -> None:
        self._validar_sessao(sessao_id)
        self._historicos.pop(sessao_id, None)

    @staticmethod
    def _validar_sessao(sessao_id: UUID) -> None:
        if not isinstance(sessao_id, UUID) or sessao_id.version != 4:
            raise ValueError("A sessão tem de ser identificada por um UUID v4 anónimo.")

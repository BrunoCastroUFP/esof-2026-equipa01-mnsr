"""Regras de negócio da geração de roteiros por tempo disponível."""

from src.business.acervo import RepositorioObras
from src.business.modelos import Obra, Roteiro

DURACOES_VALIDAS = (30, 60, 90)
MENSAGEM_DURACAO_INVALIDA = "Duração inválida: escolha 30, 60 ou 90 minutos"


class DuracaoInvalidaError(ValueError):
    """Lançada quando a duração pedida não é 30, 60 nem 90 minutos."""


class RoteiroIndisponivelError(ValueError):
    """Lançada quando não existem obras de destaque compatíveis com o tempo."""


class ServicoRoteiros:
    """Gera roteiros personalizados sem ultrapassar o tempo disponível."""

    def __init__(self, repositorio: RepositorioObras):
        self._repositorio = repositorio

    def gerar_roteiro(self, tempo: int) -> Roteiro:
        if tempo not in DURACOES_VALIDAS:
            raise DuracaoInvalidaError(MENSAGEM_DURACAO_INVALIDA)

        obras_validas = [
            obra for obra in self._repositorio.listar_todas() if obra.tempo_estimado > 0
        ]
        destaques_possiveis = sorted(
            [obra for obra in obras_validas if obra.destaque and obra.tempo_estimado <= tempo],
            key=lambda obra: (obra.tempo_estimado, obra.sala_id, obra.titulo.casefold()),
        )
        if not destaques_possiveis:
            raise RoteiroIndisponivelError(
                "Não existem obras de destaque disponíveis para a duração selecionada"
            )

        primeira_obra = destaques_possiveis[0]
        selecionadas: list[Obra] = [primeira_obra]
        tempo_restante = tempo - primeira_obra.tempo_estimado

        candidatas = sorted(
            [obra for obra in obras_validas if obra.id != primeira_obra.id],
            key=lambda obra: (
                not obra.destaque,
                obra.tempo_estimado,
                obra.sala_id,
                obra.titulo.casefold(),
            ),
        )

        for obra in candidatas:
            if obra.tempo_estimado <= tempo_restante:
                selecionadas.append(obra)
                tempo_restante -= obra.tempo_estimado

        roteiro_ordenado = tuple(
            sorted(selecionadas, key=lambda obra: (obra.sala_id, obra.titulo.casefold()))
        )
        tempo_total = sum(obra.tempo_estimado for obra in roteiro_ordenado)

        return Roteiro(
            tempo_solicitado=tempo,
            tempo_total_estimado=tempo_total,
            obras=roteiro_ordenado,
        )

"""Regras de negócio do acervo. Não conhece a base de dados: recebe um repositório."""

from typing import Protocol
from src.business.modelos import Obra


# Protocol é o equivalente a uma interface em Java
class RepositorioObras(Protocol):
    # ... quer dizer que aqui não há implementação: só a assinatura.
    # A implementação real está na camada de persistência
    def listar_todas(self) -> list[Obra]: ...


class ServicoAcervo:
    """Orquestra as regras de negócio do acervo do MNSR.
    Responsável pela política de apresentação do catálogo (ex.: ordenação
    canónica por título) e, futuramente, por filtros de exposição e versão
    do acervo, isolando a apresentação da camada de persistência (ADR-001).
    """

    def __init__(self, repositorio: RepositorioObras):
        # Injeção de dependências: o repositório vem de fora
        # Nos testes passa-se um falso (mock); na app SQLite
        self._repositorio = repositorio

    def listar_obras(self) -> list[Obra]:
        # Regra de negócio: o catálogo é sempre devolvido ordenado por título,
        # independentemente da ordem devolvida pelo repositório.
        return sorted(
            self._repositorio.listar_todas(),
            key=lambda obra: obra.titulo.casefold(),
        )

"""Regras de negócio do acervo. Não conhece a base de dados: recebe um repositório."""

from typing import Protocol
from src.business.modelos import Obra


# Protocol é o equivalente a uma interface em Java
class RepositorioObras(Protocol):
    # ... quer dizer que aqui não há implementação: só a assinatura.
    # A implementação real está na camada de persistência
    def listar_todas(self) -> list[Obra]: ...


class ServicoAcervo:
    # Serviço com as regras do acervo. Por agora só lista as obras

    def __init__(self, repositorio: RepositorioObras):
        # Injeção de dependências: o repositório vem de fora
        # Nos testes passa-se um falso (mock); na app SQLite
        self._repositorio = repositorio

    def listar_obras(self) -> list[Obra]:
        return self._repositorio.listar_todas()

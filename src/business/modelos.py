"""
Modelos de domínio: as "coisas" do museu que todas as camadas partilham.
Pertence à camada de negócio e não importa nada do FastAPI nem da base de dados (ADR-001)
"""

from dataclasses import dataclass

# frozen=True
# torna a obra imutável: depois de criada, nenhuma camada lhe pode mudar os dados por engano
# @dataclass gera sozinho o construtor, a comparação (==) e a representação em texto
@dataclass(frozen=True)
class Obra:
    id: str
    titulo: str
    autor: str
    sala_id: str
    destaque: bool = False
    tempo_estimado: int = 10

@dataclass(frozen=True)
class Roteiro:
    tempo_solicitado: int
    tempo_total_estimado: int
    obras: tuple[Obra, ...]

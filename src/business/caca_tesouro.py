"""
Regras de negócio da caça ao tesouro (US-02, issue #3).
Pertence à camada de negócio: não conhece a base de dados nem o FastAPI (ADR-001)
Recebe um repositório de fora, tal como o ServicoAcervo em acervo.py
"""

from dataclasses import dataclass
from typing import Protocol


# frozen=True: depois de criado, nenhuma camada lhe pode mudar os dados por engano
@dataclass(frozen=True)
class QRCodeDesafio:
    codigo: str # Texto dentro do QR Code junto à obra (ex.: "MNSR-7F3K9Q")
    obra_id: str # A obra onde o QR está colado: liga a caça ao tesouro ao acervo
    pontos: int # Quantos pontos a obra dá na primeira vez que é encontrada


@dataclass(frozen=True)
class ResultadoLeitura:
    # O que o validador devolve à camada de apresentação depois de uma leitura.

    obra_id: str # Só tem o id da obra: o título já vem do GET /api/obras
    ja_descoberta: bool # True no cenário 2: a sessão já tinha esta obra
    pontos_ganhos: int # Os pontos desta leitura: os da obra no cenário 1, 0 no cenário 2
    pontos_totais: int # Total da sessão depois desta leitura


class QRCodeNaoReconhecido(Exception):
    """
    O código lido não pertence a nenhuma obra do desafio (cenário 3).
    É uma exceção, e não um resultado vazio, para que validar() pare logo sem registar nada.
    A camada de apresentação apanha-a e responde 404 "QR Code não reconhecido"
    """


# Protocol é o equivalente a uma interface em Java: só diz que métodos existem
# A implementação real (SQLite) fica na camada de persistência
# Nos testes unitários, o create_autospec cria um falso com esta mesma forma
class RepositorioCacaTesouro(Protocol):
    # Procura o QR pelo código. Devolve None se o código não existir no desafio
    def obter_qr_code(self, codigo: str) -> QRCodeDesafio | None: ...

    # Grava que esta sessão encontrou a obra deste QR.
    # Devolve True se a descoberta é nova e False se a sessão já a tinha
    # Quem decide é a base de dados, numa só operação:
    # se perguntássemos primeiro "já foi descoberta?" e só depois gravássemos,
    # haveria duas leituras ao mesmo tempo que causava pontos a dobrar
    def registar_descoberta(self, sessao_id: str, qr_code: QRCodeDesafio) -> bool: ...

    # Soma os pontos de todas as obras encontradas por esta sessão
    def total_pontos(self, sessao_id: str) -> int: ...


class ValidadorQRCode:
    # Valida a leitura de um QR Code e decide o que acontece em cada cenário da US-02

    def __init__(self, repositorio: RepositorioCacaTesouro):
        # Injeção de dependências: o repositório vem de fora.
        # Nos testes passa-se um falso; na app, o repositório SQLite
        self._repositorio = repositorio

    def validar(self, sessao_id: str, codigo: str) -> ResultadoLeitura:
        # 1. O código pertence a alguma obra do desafio?
        qr_code = self._repositorio.obter_qr_code(codigo)
        if qr_code is None:
            # Cenário 3: para aqui, antes de gravar o que quer que seja
            raise QRCodeNaoReconhecido()

        # 2. Tenta gravar a descoberta. A resposta da base de dados diz se é nova
        nova = self._repositorio.registar_descoberta(sessao_id, qr_code)

        # 3. Monta o resultado.
        # Cenário 1 (nova): ganha os pontos da obra.
        # Cenário 2 (repetida): 0 pontos, e o total fica igual
        return ResultadoLeitura(
            obra_id=qr_code.obra_id,
            ja_descoberta=not nova,
            pontos_ganhos=qr_code.pontos if nova else 0,
            # O total é lido depois de gravar, para já incluir esta descoberta
            pontos_totais=self._repositorio.total_pontos(sessao_id),
        )

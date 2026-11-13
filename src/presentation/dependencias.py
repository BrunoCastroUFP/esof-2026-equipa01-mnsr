"""Liga as camadas: cria o serviço do acervo com o repositório real."""

from collections.abc import Iterator
from src.business.acervo import ServicoAcervo
from src.business.roteiros import ServicoRoteiros
from src.persistence.base_dados import abrir_ligacao
from src.persistence.obra_repository import ObraRepositorySQLite
from src.business.caca_tesouro import ValidadorQRCode
from src.persistence.caca_tesouro_repository import CacaTesouroRepositorySQLite


def obter_servico_acervo() -> Iterator[ServicoAcervo]:
    # Único sítio da apresentação que conhece a persistência: aqui montam-se as peças
    # Cada pedido HTTP tem a sua ligação, que fecha no fim (finally), mesmo que o pedido falhe
    ligacao = abrir_ligacao()
    try:
        yield ServicoAcervo(ObraRepositorySQLite(ligacao))
    finally:
        ligacao.close()


def obter_servico_roteiros() -> Iterator[ServicoRoteiros]:
    ligacao = abrir_ligacao()
    try:
        yield ServicoRoteiros(ObraRepositorySQLite(ligacao))
    finally:
        ligacao.close()


def obter_validador_qr_code() -> Iterator[ValidadorQRCode]:
    # Igual à do acervo: uma ligação por pedido HTTP, fechada no fim mesmo que o pedido falhe
    ligacao = abrir_ligacao()
    try:
        yield ValidadorQRCode(CacaTesouroRepositorySQLite(ligacao))
    finally:
        ligacao.close()

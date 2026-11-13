"""
Testes de integração do repositório da caça ao tesouro
Ao contrário dos unitários, aqui o SQL corre num SQLite em memória
Provam que a base de dados faz o que o ValidadorQRCode assume que ela faz
"""

import sqlite3
import pytest
from src.business.caca_tesouro import QRCodeDesafio
from src.persistence.caca_tesouro_repository import CacaTesouroRepositorySQLite

# Duas sessões anónimas diferentes: dois visitantes, dois telemóveis
SESSAO_A = "6f1c2b9e-3d4a-4f5b-8c7d-1e2f3a4b5c6d"
SESSAO_B = "0a9b8c7d-6e5f-4a3b-9c2d-1e0f9a8b7c6d"

# Dois QR do desafio, em obras diferentes
QR_DESTERRADO = QRCodeDesafio("MNSR-7F3K9Q", "desterrado", 10)
QR_FLOR_AGRESTE = QRCodeDesafio("MNSR-2B8XQM", "flor-agreste", 15)


@pytest.fixture
def repositorio():
    # ":memory:" cria uma base de dados nova e vazia, só na RAM, para cada teste
    # Não altera mnsr.sqlite3 e desaparece quando a ligação fecha
    ligacao = sqlite3.connect(":memory:")
    repo = CacaTesouroRepositorySQLite(ligacao)
    repo.criar_tabelas()
    repo.guardar_qr_codes([QR_DESTERRADO, QR_FLOR_AGRESTE])
    # yield em vez de return: o teste corre aqui e, no fim, o código abaixo fecha a ligação, mesmo que o teste falhe
    yield repo
    ligacao.close()


def test_obter_qr_code_existente_e_inexistente(repositorio):
    # O validador usa o None para decidir o cenário 3
    assert repositorio.obter_qr_code("MNSR-7F3K9Q") == QR_DESTERRADO
    assert repositorio.obter_qr_code("MNSR-NAOEXISTE") is None


def test_a_mesma_obra_so_conta_uma_vez_por_sessao(repositorio):
    # Cenário 2 na base de dados: a primeira gravação é nova, a segunda não
    # É a chave (sessao_id, obra_id) da tabela que garante isto
    assert repositorio.registar_descoberta(SESSAO_A, QR_DESTERRADO) is True
    assert repositorio.registar_descoberta(SESSAO_A, QR_DESTERRADO) is False
    assert repositorio.total_pontos(SESSAO_A) == 10


def test_total_soma_as_obras_diferentes(repositorio):
    # Cenário 1 duas vezes, em obras diferentes: os pontos acumulam
    repositorio.registar_descoberta(SESSAO_A, QR_DESTERRADO)
    repositorio.registar_descoberta(SESSAO_A, QR_FLOR_AGRESTE)

    assert repositorio.total_pontos(SESSAO_A) == 25


def test_as_sessoes_nao_partilham_pontos(repositorio):
    # Os pontos de um visitante nunca aparecem noutro. Uma sessão sem descobertas tem 0, e não None
    repositorio.registar_descoberta(SESSAO_A, QR_DESTERRADO)

    assert repositorio.total_pontos(SESSAO_B) == 0


def test_codigo_com_sql_e_tratado_como_texto(repositorio):
    # Tentativa de SQL injection:
    # se o SQL fosse montado com f-strings, esta condição ficava sempre verdadeira e devolvia um QR qualquer.
    # Com SQL parametrizado (?), é só um código que não existe
    assert repositorio.obter_qr_code("x' OR '1'='1") is None

"""
Testes e2e da rota POST /api/desafios/validar
Fazem pedidos HTTP à app inteira: a rota, o validador e o repositório SQLite
A base de dados é trocada por uma em memória, para não alterar o mnsr.sqlite3
"""

import sqlite3
import pytest
from fastapi.testclient import TestClient
from src.business.caca_tesouro import QRCodeDesafio, ValidadorQRCode
from src.main import app
from src.persistence.caca_tesouro_repository import CacaTesouroRepositorySQLite
from src.presentation.dependencias import obter_validador_qr_code

URL = "/api/desafios/validar"
SESSAO = "6f1c2b9e-3d4a-4f5b-8c7d-1e2f3a4b5c6d"
QR_DESTERRADO = QRCodeDesafio("MNSR-7F3K9Q", "desterrado", 10)


@pytest.fixture
def cliente():
    # check_same_thread=False: o TestClient corre a rota numa thread diferente da do teste,
    # e o sqlite3 recusa por defeito usar uma ligação noutra thread
    ligacao = sqlite3.connect(":memory:", check_same_thread=False)
    repositorio = CacaTesouroRepositorySQLite(ligacao)
    repositorio.criar_tabelas()
    repositorio.guardar_qr_codes([QR_DESTERRADO])
    # Troca a dependência real, que abre o mnsr.sqlite3, por um validador com esta base de dados.
    # Tudo o resto (rota, validação do pedido, validador, SQL) é o código verdadeiro
    app.dependency_overrides[obter_validador_qr_code] = lambda: ValidadorQRCode(repositorio)
    yield TestClient(app)
    # Depois do teste: repõe a app e fecha a base de dados
    app.dependency_overrides.clear()
    ligacao.close()


def test_primeira_leitura_encontra_obra_e_da_pontos(cliente):
    # Cenário 1, como o telemóvel o vê
    resposta = cliente.post(URL, json={"sessao_id": SESSAO, "codigo": "MNSR-7F3K9Q"})

    assert resposta.status_code == 200
    assert resposta.json() == {
        "obra_id": "desterrado",
        "mensagem": "Obra encontrada",
        "ja_descoberta": False,
        "pontos_ganhos": 10,
        "pontos_totais": 10,
    }


def test_segunda_leitura_diz_obra_ja_descoberta_sem_pontos(cliente):
    # Cenário 2: o mesmo QR lido duas vezes pela mesma sessão
    cliente.post(URL, json={"sessao_id": SESSAO, "codigo": "MNSR-7F3K9Q"})

    resposta = cliente.post(URL, json={"sessao_id": SESSAO, "codigo": "MNSR-7F3K9Q"})

    # 200 e não um erro: ler outra vez um QR é uma ação válida, só não dá pontos
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Obra já descoberta"
    assert resposta.json()["pontos_ganhos"] == 0
    assert resposta.json()["pontos_totais"] == 10


def test_codigo_desconhecido_404(cliente):
    # Cenário 3. O código tem o formato certo, por isso passa a validação do pedido;
    # só falha porque não existe no desafio
    resposta = cliente.post(URL, json={"sessao_id": SESSAO, "codigo": "MNSR-ZZZZZZ"})

    assert resposta.status_code == 404
    assert resposta.json() == {"detail": "QR Code não reconhecido"}


# parametrize:
# o pytest corre este teste uma vez para cada corpo da lista
# cada vez aparece como um teste separado no resultado
@pytest.mark.parametrize(
    "corpo",
    [
        {"sessao_id": "abc", "codigo": "MNSR-7F3K9Q"},  # sessão que não é um UUID
        {"sessao_id": SESSAO, "codigo": "MNSR-7F3K9Q\n"},  # quebra de linha escondida
        {"sessao_id": SESSAO, "codigo": "x' OR '1'='1"},  # tentativa de SQL injection
        {"sessao_id": SESSAO, "codigo": "MNSR-7F3K9Q", "pontos": 999},  # campo a mais
        {"sessao_id": SESSAO},  # falta o código
    ],
)
def test_pedido_mal_formado_422(cliente, corpo):
    # O pedido é recusado à entrada, antes de chegar ao validador ou à base de dados
    resposta = cliente.post(URL, json=corpo)

    assert resposta.status_code == 422

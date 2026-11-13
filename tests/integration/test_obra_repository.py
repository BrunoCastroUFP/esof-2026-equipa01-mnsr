import sqlite3
import pytest
from src.business.modelos import Obra
from src.persistence.obra_repository import ObraRepositorySQLite

DESTERRADO = Obra("desterrado", "O Desterrado", "António Soares dos Reis", "S1")
CASAS_BRANCAS = Obra("casas-brancas-de-capri", "Casas Brancas de Capri", "Henrique Pousão", "S3")


@pytest.fixture
def repositorio():
    # SQLite em memória: uma base de dados nova e vazia para cada teste
    ligacao = sqlite3.connect(":memory:")
    repo = ObraRepositorySQLite(ligacao)
    repo.criar_tabela()
    yield repo
    ligacao.close()


def test_guarda_e_lista_obras_por_ordem_de_titulo(repositorio):
    repositorio.guardar_todas([DESTERRADO, CASAS_BRANCAS])

    assert repositorio.listar_todas() == [CASAS_BRANCAS, DESTERRADO]


def test_guardar_a_mesma_obra_duas_vezes_nao_a_duplica(repositorio):
    repositorio.guardar_todas([DESTERRADO])
    repositorio.guardar_todas([DESTERRADO])

    assert repositorio.listar_todas() == [DESTERRADO]


def test_texto_com_sql_e_guardado_como_texto(repositorio):
    # Tentativa de SQL injection: com SQL parametrizado fica guardada como título e não é executada
    obra = Obra("x", "Obra'); DROP TABLE obras; --", "Autor", "S1")

    repositorio.guardar_todas([obra])

    assert repositorio.listar_todas() == [obra]

def test_guarda_e_recupera_destaque_e_tempo_estimado(repositorio):
    obra = Obra(
        "desterrado",
        "O Desterrado",
        "António Soares dos Reis",
        "S1",
        destaque=True,
        tempo_estimado=15,
    )

    repositorio.guardar_todas([obra])
    recuperada = repositorio.listar_todas()[0]

    assert recuperada.destaque is True
    assert recuperada.tempo_estimado == 15

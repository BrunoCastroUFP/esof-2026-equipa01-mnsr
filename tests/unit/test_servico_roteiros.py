from unittest.mock import create_autospec
import pytest
from src.business.acervo import RepositorioObras
from src.business.modelos import Obra
from src.business.roteiros import (
    DuracaoInvalidaError,
    RoteiroIndisponivelError,
    ServicoRoteiros,
)

OBRAS_EXEMPLO = [
    Obra("desterrado", "O Desterrado", "António Soares dos Reis", "S1", True, 15),
    Obra("flor-agreste", "Flor Agreste", "António Soares dos Reis", "S1", False, 10),
    Obra("infancia-de-caim", "Infância de Caim", "António Teixeira Lopes", "S2", True, 15),
    Obra("casas-brancas", "Casas Brancas de Capri", "Henrique Pousão", "S3", True, 20),
    Obra("autorretrato", "Autorretrato", "Aurélia de Souza", "S3", True, 20),
]


@pytest.mark.parametrize("tempo", [30, 60, 90])
def test_gerar_roteiro_valido_inclui_destaque_e_respeita_tempo(tempo):
    repositorio = create_autospec(RepositorioObras, instance=True)
    repositorio.listar_todas.return_value = OBRAS_EXEMPLO

    roteiro = ServicoRoteiros(repositorio).gerar_roteiro(tempo)

    assert roteiro.tempo_solicitado == tempo
    assert roteiro.tempo_total_estimado <= tempo
    assert any(obra.destaque for obra in roteiro.obras)
    assert sum(obra.tempo_estimado for obra in roteiro.obras) == roteiro.tempo_total_estimado


@pytest.mark.parametrize("tempo_invalido", [0, -15, 45, 75, 120])
def test_gerar_roteiro_com_duracao_invalida_lanca_erro(tempo_invalido):
    repositorio = create_autospec(RepositorioObras, instance=True)

    with pytest.raises(
        DuracaoInvalidaError,
        match="Duração inválida: escolha 30, 60 ou 90 minutos",
    ):
        ServicoRoteiros(repositorio).gerar_roteiro(tempo_invalido)

    repositorio.listar_todas.assert_not_called()


def test_gerar_roteiro_sem_destaques_compativeis_lanca_erro():
    repositorio = create_autospec(RepositorioObras, instance=True)
    repositorio.listar_todas.return_value = [
        Obra("flor-agreste", "Flor Agreste", "António Soares dos Reis", "S1", False, 10),
        Obra("obra-longa", "Obra Longa", "Autor", "S2", True, 45),
    ]

    with pytest.raises(RoteiroIndisponivelError):
        ServicoRoteiros(repositorio).gerar_roteiro(30)

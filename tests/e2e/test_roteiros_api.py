from unittest.mock import create_autospec
import pytest
from fastapi.testclient import TestClient
from src.business.acervo import RepositorioObras
from src.business.modelos import Obra
from src.business.roteiros import ServicoRoteiros
from src.main import app
from src.presentation.dependencias import obter_servico_roteiros


@pytest.fixture(name="cliente")
def criar_cliente():
    repositorio = create_autospec(RepositorioObras, instance=True)
    repositorio.listar_todas.return_value = [
        Obra("desterrado", "O Desterrado", "António Soares dos Reis", "S1", True, 15),
        Obra("flor-agreste", "Flor Agreste", "António Soares dos Reis", "S1", False, 10),
        Obra("infancia-de-caim", "Infância de Caim", "António Teixeira Lopes", "S2", True, 15),
        Obra("casas-brancas", "Casas Brancas de Capri", "Henrique Pousão", "S3", True, 20),
    ]
    app.dependency_overrides[obter_servico_roteiros] = lambda: ServicoRoteiros(repositorio)
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.mark.parametrize("tempo", [30, 60, 90])
def test_post_roteiros_devolve_200_com_destaque_e_tempo_valido(cliente, tempo):
    resposta = cliente.post("/api/roteiros", json={"tempo": tempo})

    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["tempo_solicitado"] == tempo
    assert dados["tempo_total_estimado"] <= tempo
    assert any(obra["destaque"] is True for obra in dados["obras"])


def test_post_roteiros_com_duracao_invalida_devolve_400(cliente):
    resposta = cliente.post("/api/roteiros", json={"tempo": 45})

    assert resposta.status_code == 400
    assert resposta.json() == {"detail": "Duração inválida: escolha 30, 60 ou 90 minutos"}

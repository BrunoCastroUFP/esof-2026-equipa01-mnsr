from unittest.mock import create_autospec
import pytest
from fastapi.testclient import TestClient
from src.business.acervo import RepositorioObras, ServicoAcervo
from src.business.modelos import Obra
from src.main import app
from src.presentation.dependencias import obter_servico_acervo


@pytest.fixture
def cliente():
    # Troca o repositório real por um falso, só durante o teste
    repositorio = create_autospec(RepositorioObras, instance=True)
    repositorio.listar_todas.return_value = [
        Obra("desterrado", "O Desterrado", "António Soares dos Reis", "S1")
    ]
    app.dependency_overrides[obter_servico_acervo] = lambda: ServicoAcervo(repositorio)
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_get_obras_devolve_200_e_a_lista_de_obras(cliente):
    resposta = cliente.get("/api/obras")

    assert resposta.status_code == 200
    assert resposta.json() == [
        {"id": "desterrado", "titulo": "O Desterrado", "autor": "António Soares dos Reis", "sala_id": "S1"}
    ]

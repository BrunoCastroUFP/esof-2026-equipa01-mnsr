from unittest.mock import create_autospec
from src.business.acervo import RepositorioObras, ServicoAcervo
from src.business.modelos import Obra


def test_listar_obras_devolve_as_obras_do_repositorio():
    # Repositório falso com a mesma forma da interface RepositorioObras:
    # só aceita os métodos que a interface tem, por isso um nome errado faz o teste falhar
    obras = [Obra("desterrado", "O Desterrado", "António Soares dos Reis", "S1")]
    repositorio = create_autospec(RepositorioObras, instance=True)
    repositorio.listar_todas.return_value = obras

    assert ServicoAcervo(repositorio).listar_obras() == obras
    repositorio.listar_todas.assert_called_once_with()

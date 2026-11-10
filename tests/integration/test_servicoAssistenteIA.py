from unittest.mock import Mock
from src.business.servicoAssistenteIA import ServicoAssistenteIA

def test_consultarObraComMock():

    # Configuração do Mock
    cliente_rag_mock= Mock()
    cliente_rag_mock.consultar.return_value= 'Escultura em mármore de António Soares dos Reis (1872).'

    # Injetar o Mock no serviço
    servico = ServicoAssistenteIA(cliente_rag=cliente_rag_mock)
    resposta = servico.obter_informacao('O Desterro')

    # Verificar se o Mock foi usado corretamente
    cliente_rag_mock.consultar.assert_called_once_with('O Desterro')
    assert resposta == 'Escultura em mármore de António Soares dos Reis (1872).'
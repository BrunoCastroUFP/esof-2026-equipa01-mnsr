from unittest.mock import create_autospec
from src.business.servico_assistente_ia import ServicoAssistenteIA, ClienteRAG

def test_consultar_obra_com_mock():

    # Configuração do Mock
    cliente_rag_mock= create_autospec(ClienteRAG)
    resposta_esperada= 'Escultura em mármore de António Soares dos Reis (1872).'
    cliente_rag_mock.consultar.return_value = resposta_esperada

    # Injetar o Mock no serviço
    servico = ServicoAssistenteIA(cliente_rag=cliente_rag_mock)
    resposta = servico.obter_informacao('O Desterro')

    # Verificar se o Mock foi usado corretamente
    cliente_rag_mock.consultar.assert_called_once_with('O Desterro')
    assert resposta == 'Escultura em mármore de António Soares dos Reis (1872).'

import gc
import tracemalloc
from uuid import uuid4
from unittest.mock import create_autospec

from src.business.servico_assistente_ia import ServicoAssistenteIA, ClienteRAG


def test_consultar_obra_com_mock():
    # Configuração do Mock
    cliente_rag_mock= create_autospec(ClienteRAG)
    resposta_esperada= 'Escultura em mármore de António Soares dos Reis (1872).'
    cliente_rag_mock.consultar.return_value = resposta_esperada

    # Injetar o Mock no serviço
    servico = ServicoAssistenteIA(cliente_rag=cliente_rag_mock)
    sessao_id = uuid4()
    resposta = servico.obter_informacao(sessao_id, 'O Desterro')

    # Verificar se o Mock foi usado corretamente
    cliente_rag_mock.consultar.assert_called_once_with('O Desterro', ())
    assert resposta == 'Escultura em mármore de António Soares dos Reis (1872).'


def test_fechar_sessao_apaga_historico_antes_da_consulta_seguinte():
    cliente_rag_mock = create_autospec(ClienteRAG)
    cliente_rag_mock.consultar.side_effect = [
        "Resposta 1",
        "Resposta 2",
        "Resposta após fechar",
    ]
    servico = ServicoAssistenteIA(cliente_rag=cliente_rag_mock)
    sessao_id = uuid4()

    servico.obter_informacao(sessao_id, "Pergunta 1")
    servico.obter_informacao(sessao_id, "Pergunta 2")
    assert cliente_rag_mock.consultar.call_args_list[1].args[1] == (
        ("Pergunta 1", "Resposta 1"),
    )

    servico.fechar_sessao(sessao_id)
    servico.obter_informacao(sessao_id, "Pergunta após fechar")

    assert cliente_rag_mock.consultar.call_args_list[2].args[1] == ()


def test_historico_isolado_por_sessao_anonima():
    cliente_rag_mock = create_autospec(ClienteRAG)
    cliente_rag_mock.consultar.side_effect = [
        "Resposta A",
        "Resposta B",
        "Resposta A2",
    ]
    servico = ServicoAssistenteIA(cliente_rag=cliente_rag_mock)
    sessao_a = uuid4()
    sessao_b = uuid4()

    servico.obter_informacao(sessao_a, "Pergunta A")
    servico.obter_informacao(sessao_b, "Pergunta B")
    servico.obter_informacao(sessao_a, "Pergunta A2")

    assert cliente_rag_mock.consultar.call_args_list[1].args[1] == ()
    assert cliente_rag_mock.consultar.call_args_list[2].args[1] == (
        ("Pergunta A", "Resposta A"),
    )


def test_historico_tem_no_maximo_dez_trocas():
    cliente_rag_mock = create_autospec(ClienteRAG)
    cliente_rag_mock.consultar.side_effect = lambda pergunta, historico: f"Resposta {pergunta}"
    servico = ServicoAssistenteIA(cliente_rag=cliente_rag_mock)
    sessao_id = uuid4()

    for indice in range(12):
        servico.obter_informacao(sessao_id, f"Pergunta {indice}")

    historico = cliente_rag_mock.consultar.call_args_list[-1].args[1]
    assert len(historico) == 10
    assert historico[0] == ("Pergunta 1", "Resposta Pergunta 1")
    assert historico[-1] == ("Pergunta 10", "Resposta Pergunta 10")


def test_fechar_sessao_liberta_memoria_do_historico():
    class ClienteRAGSemEstado:
        def consultar(self, pergunta, historico=()):
            return f"Resposta a {pergunta} ({len(historico)} trocas)"

    servico = ServicoAssistenteIA(cliente_rag=ClienteRAGSemEstado())
    sessao_id = uuid4()
    tracemalloc.start()
    try:
        for indice in range(10):
            servico.obter_informacao(sessao_id, f"{indice}:" + "x" * 250_000)
        gc.collect()
        memoria_antes = tracemalloc.get_traced_memory()[0]

        servico.fechar_sessao(sessao_id)
        gc.collect()
        memoria_depois = tracemalloc.get_traced_memory()[0]
    finally:
        tracemalloc.stop()

    assert memoria_antes - memoria_depois > 1_000_000

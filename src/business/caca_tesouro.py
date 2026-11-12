"""
Testes unitários do ValidadorQRCode (US-02, issue #3)
Cada teste corresponde a um cenário BDD da issue.
São unitários: testam só a regra de negócio, sem base de dados nem API. O repositório é substituído por um falso (mock)
"""

from unittest.mock import create_autospec
import pytest

from src.business.caca_tesouro import (
    QRCodeDesafio,
    QRCodeNaoReconhecido,
    RepositorioCacaTesouro,
    ValidadorQRCode,
)

# Uma sessão anónima: só um UUID aleatório, sem nome, idade ou e-mail (RNF-03)
SESSAO = "6f1c2b9e-3d4a-4f5b-8c7d-1e2f3a4b5c6d"

# O QR Code colado junto ao Desterrado: código opaco (não dá para adivinhar os outros), a obra a que pertence e quantos pontos vale
QR_DESTERRADO = QRCodeDesafio("MNSR-7F3K9Q", "desterrado", 10)


@pytest.fixture
def repositorio():
    # Fixture: o pytest corre esta função antes de cada teste que tenha um parâmetro chamado "repositorio" e passa-lhe o resultado.
    # Cada teste recebe um falso novo, por isso o que um teste configura não passa para o seguinte
    # create_autospec copia a forma da interface RepositorioCacaTesouro:
    # se o validador chamar um método que não existe nela, o teste falha
    return create_autospec(RepositorioCacaTesouro, instance=True)


def test_qr_valido_regista_obra_e_soma_pontos(repositorio):
    # Cenário 1: o visitante lê o QR de uma obra do desafio pela primeira vez

    # Preparar: dizemos ao repositório falso o que responder quando o validador perguntar
    repositorio.obter_qr_code.return_value = QR_DESTERRADO  # o código existe
    repositorio.registar_descoberta.return_value = True  # a descoberta é nova
    repositorio.total_pontos.return_value = 10  # depois de registar, 10 pontos

    # Agir: a única linha que corre o código de produção
    resultado = ValidadorQRCode(repositorio).validar(SESSAO, "MNSR-7F3K9Q")

    # Verificar: a obra fica "Encontrada" e os pontos foram somados à sessão
    assert resultado.obra_id == "desterrado"
    assert not resultado.ja_descoberta
    assert resultado.pontos_ganhos == 10
    assert resultado.pontos_totais == 10

    # Validador pede ao repositório para gravar, uma só vez, com esta sessão e este QR.
    # Sem isto, um validador que não grava nada passava no teste
    repositorio.registar_descoberta.assert_called_once_with(SESSAO, QR_DESTERRADO)


def test_qr_ja_registado_nao_da_pontos_duplicados(repositorio):
    # Cenário 2: a mesma sessão lê outra vez um QR que já tinha encontrado

    # Preparar: o código existe, mas a base de dados diz que a descoberta não é nova (False)
    # O total continua 10, os pontos da primeira leitura
    repositorio.obter_qr_code.return_value = QR_DESTERRADO
    repositorio.registar_descoberta.return_value = False
    repositorio.total_pontos.return_value = 10

    # Agir
    resultado = ValidadorQRCode(repositorio).validar(SESSAO, "MNSR-7F3K9Q")

    # Verificar: a API vai mostrar "Obra já descoberta" e não há pontos a dobrar
    assert resultado.ja_descoberta
    assert resultado.pontos_ganhos == 0
    assert resultado.pontos_totais == 10


def test_qr_desconhecido_nao_regista_nada(repositorio):
    # Cenário 3: o código lido não pertence a nenhuma obra do desafio

    # Preparar: o repositório não encontra o código
    repositorio.obter_qr_code.return_value = None

    # Agir e verificar ao mesmo tempo: o teste só passa se validar() lançar esta exceção.
    # Se não lançar nenhuma, ou lançar outra, o teste falha.
    # Na API, esta exceção vai ser transformada em 404 "QR Code não reconhecido"
    with pytest.raises(QRCodeNaoReconhecido):
        ValidadorQRCode(repositorio).validar(SESSAO, "MNSR-NAOEXISTE")

    # Verificar: nada foi gravado, por isso também não há pontos
    repositorio.registar_descoberta.assert_not_called()

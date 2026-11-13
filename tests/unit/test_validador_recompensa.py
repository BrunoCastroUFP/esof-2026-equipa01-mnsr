"""
Testes unitários do ValidadorRecompensa (issue #29, regra do cenário 1 da US-08 #18)
Cada teste é um critério de aceitação da #29
Unitários puros: a regra recebe números, por isso não precisa de mock nem de base de dados
"""

from src.business.validador_recompensa import Recompensa, ValidadorRecompensa

# fica escrito à mão no teste e não importado do código:
# se alguém mudar o desconto no código, o teste apanha
EXPLORADOR = Recompensa(medalha="Explorador", desconto_percentagem=10)


def test_duas_obras_nao_dao_recompensa():
    assert ValidadorRecompensa().avaliar(obras_encontradas=2, ja_descoberta=False) is None


def test_terceira_obra_da_medalha_explorador_e_voucher_de_10():
    assert ValidadorRecompensa().avaliar(obras_encontradas=3, ja_descoberta=False) == EXPLORADOR


def test_leitura_repetida_nao_conta_como_obra_nova():
    # A sessão já tinha 3 obras e voltou a ler uma delas: o total continua 3
    assert ValidadorRecompensa().avaliar(obras_encontradas=3, ja_descoberta=True) is None


def test_quarta_obra_nao_da_segundo_voucher():
    assert ValidadorRecompensa().avaliar(obras_encontradas=4, ja_descoberta=False) is None

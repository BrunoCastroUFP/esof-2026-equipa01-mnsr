from src.business.calculadorAfluencia import CalculadorAfluencia


def test_AfluenciaBaixaQuandoAbaixo40Porcento():
    calculador = CalculadorAfluencia()
    assert calculador.calcular_nivel(15, 40) == "Baixa"

def test_AfluenciaMediaQuandoEntre40e79Porcento():
    calculador = CalculadorAfluencia()
    assert calculador.calcular_nivel(16, 40) == "Média"
    assert calculador.calcular_nivel(17, 40) == "Média"

def test_AfluenciaElevadaQuandoAcima80Porcento():
    calculador = CalculadorAfluencia()
    assert calculador.calcular_nivel(32, 40) == "Elevada"
    assert calculador.calcular_nivel(34, 40) == "Elevada"

def test_AfluenciaComTetoMaximo100Porcento():
    calculador = CalculadorAfluencia()
    assert calculador.calcular_nivel(50, 40) == "Elevada"

# def test_DeveRetornarAfluenciaElevadaQuandoVisitantesSuperam500():
#     calculador = CalculadorAfluencia()
#
#     resultado = calculador.calcular_nivel(501)
#
#     assert resultado == "Elevada"
#
# def test_DeveRetornarAfluenciaBaixaQuandoVisitantesSao500OuMenos():
#     calculador = CalculadorAfluencia()
#
#     resultado = calculador.calcular_nivel(500)
#
#     assert resultado == "Baixa"
from src.business.calculadorAfluencia import CalculadorAfluencia

def test_DeveRetornarAfluenciaElevadaQuandoVisitantesSuperam500():
    calculador = CalculadorAfluencia()

    resultado = calculador.calcular_nivel(501)

    assert resultado == "Elevada"

def test_DeveRetornarAfluenciaBaixaQuandoVisitantesSao500OuMenos():
    calculador = CalculadorAfluencia()

    resultado = calculador.calcular_nivel(500)

    assert resultado == "Baixa"
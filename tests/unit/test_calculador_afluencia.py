from src.business.calculador_afluencia import CalculadorAfluencia


def test_afluencia_baixa_quando_abaixo_40porcento():
    calculador = CalculadorAfluencia()
    assert calculador.calcular_nivel(15, 40) == "Baixa"

def test_afluencia_media_quando_entre_40e79porcento():
    calculador = CalculadorAfluencia()
    assert calculador.calcular_nivel(16, 40) == "Média"
    assert calculador.calcular_nivel(17, 40) == "Média"

def test_afluencia_elevada_quando_acima_80porcento():
    calculador = CalculadorAfluencia()
    assert calculador.calcular_nivel(32, 40) == "Elevada"
    assert calculador.calcular_nivel(34, 40) == "Elevada"

def test_afluencia_com_teto_maximo_100porcento():
    calculador = CalculadorAfluencia()
    assert calculador.calcular_nivel(50, 40) == "Elevada"

from src.business.calculador_afluencia import CalculadorAfluencia, Sala


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

def test_calculador_afluencia_com_salas_circulares():
    sala_a = Sala("S1",  10)
    sala_b = Sala("S2", 15)

    # Cria o percurso circular: A -> B -> A
    sala_a.contiguas.append(sala_b)
    sala_b.contiguas.append(sala_a)

    calculador = CalculadorAfluencia()
    assert calculador.calcular_ocupacao_total(sala_a) == 25
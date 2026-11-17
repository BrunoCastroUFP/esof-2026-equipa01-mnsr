from scripts import carregar_acervo, carregar_desafio


def test_scripts_de_carga_importam_sem_erro():
    assert callable(carregar_acervo.main)
    assert callable(carregar_desafio.main)

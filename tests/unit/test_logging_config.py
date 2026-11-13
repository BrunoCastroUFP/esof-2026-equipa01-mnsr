import json
import logging
import uuid

from src.logging_config import (
    _correlation_id_ctx,
    configurar_logging,
    gerar_correlation_id,
    obter_correlation_id,
)


def test_obter_correlation_id_gera_automaticamente_se_vazio():
    _correlation_id_ctx.set("")
    cid_gerado = obter_correlation_id()

    assert cid_gerado != ""
    assert uuid.UUID(cid_gerado).version == 4

def test_log_emite_json_valido_com_campos_obrigatorios(capsys, monkeypatch):
    monkeypatch.setenv("API_ENV", "development")
    configurar_logging()
    capsys.readouterr()

    cid_esperado = gerar_correlation_id()
    logger = logging.getLogger("teste.modulo")
    logger.info("Operação concluída com sucesso")

    # Captura do stdout
    capturado = capsys.readouterr()
    linha = capturado.out.strip()

    # Garante que o JSON é válido
    dados = json.loads(linha)
    assert "timestamp" in dados
    assert dados["level"] == "INFO"
    assert dados["origin"] == "teste.modulo"
    assert "thread" in dados
    assert dados["message"] == "Operação concluída com sucesso"
    assert dados["correlation_id"] == cid_esperado

    # Valida que é mesmo um UUID válido
    assert uuid.UUID(dados["correlation_id"]).version == 4

def test_nivel_log_muda_consoante_ambiente(capsys, monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    configurar_logging()
    capsys.readouterr()

    logger= logging.getLogger("teste.ambiente")
    logger.debug("Mensagem oculta em produção")
    logger.info("Mensagem visível em produção")

    linhas = capsys.readouterr().out.strip().splitlines()
    print(linhas)
    assert len(linhas) == 1
    assert json.loads(linhas[0])["message"] == "Mensagem visível em produção"

def test_log_inclui_excecao_quando_ocorre_erro(capsys, monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    configurar_logging()
    capsys.readouterr()

    logger = logging.getLogger("teste.erro")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Falha matematica simulada")

    linha = capsys.readouterr().out.strip()
    dados = json.loads(linha)

    assert dados["level"] == "ERROR"
    assert dados["message"] == "Falha matematica simulada"
    assert "ZeroDivisionError" in dados["exception"]

import contextvars
import json
import logging
import os
import sys
import uuid
from datetime import datetime, timezone


_correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("correlation_id",
                                                                            default="")

def gerar_correlation_id() ->str:
    """Gera um novo UUID v4, guarda no contexto atual e devolve-lo"""
    novo_id= str(uuid.uuid4())
    _correlation_id_ctx.set(novo_id)
    return novo_id

def obter_correlation_id() ->str:
    """Obtém o Correlation ID atual (ou gera se estiver fora do pedido HTTP)"""
    cid = _correlation_id_ctx.get()
    if not cid:
        cid = gerar_correlation_id()
    return cid

class JsonFormatter(logging.Formatter):
    """Formata cada linha da log com um objeto válido"""

    def format(self, record: logging.LogRecord)-> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created,
            tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "origin": record.name,
            "thread": record.threadName,
            "message": record.getMessage(),
            "correlation_id": obter_correlation_id(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)
def configurar_logging()->None:
    """Configurar o logger raiz para emitir JSON estruturado consoante o ambiente"""
    ambiente = os.getenv("APP_ENV", "development").strip().lower()
    nivel = logging.INFO if ambiente in ("production", "prod") else logging.DEBUG

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(nivel)

    # Limpa os handlers antigos para evitar duplicados
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

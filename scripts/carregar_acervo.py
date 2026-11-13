"""Carrega as obras de data/acervo.json na base de dados SQLite.
Correr a partir da raiz do projeto: python -m scripts.carregar_acervo
"""

import json
import logging

from logging_config import configurar_logging
from pathlib import Path
from src.business.modelos import Obra
from src.persistence.base_dados import CAMINHO_BD, abrir_ligacao
from src.persistence.obra_repository import ObraRepositorySQLite


CAMINHO_ACERVO = Path(__file__).resolve().parents[1] / "data" / "acervo.json"
logger = logging.getLogger(__name__)

def main() -> None:
    configurar_logging()
    with open(CAMINHO_ACERVO, encoding="utf-8") as ficheiro:
        # Obra(**dados) falha logo se o JSON tiver um campo a mais ou a menos
        obras = [Obra(**dados) for dados in json.load(ficheiro)]
    ligacao = abrir_ligacao()
    try:
        repositorio = ObraRepositorySQLite(ligacao)
        repositorio.criar_tabela()
        repositorio.guardar_todas(obras)
    finally:
        ligacao.close()
    logger.info(f"{len(obras)} obras carregadas em {CAMINHO_BD.name}")


# Só corre quando o ficheiro é executado diretamente, não quando é importado
if __name__ == "__main__":
    main()

"""
Carrega os QR Codes de data/desafio_qr.json na base de dados SQLite.
Correr a partir da raiz do projeto: python -m scripts.carregar_desafio
"""

import json
from pathlib import Path
from src.business.caca_tesouro import QRCodeDesafio
from src.persistence.base_dados import CAMINHO_BD, abrir_ligacao
from src.persistence.caca_tesouro_repository import CacaTesouroRepositorySQLite

# Caminho absoluto: parents[1] sobe de scripts/ até à raiz do projeto
CAMINHO_DESAFIO = Path(__file__).resolve().parents[1] / "data" / "desafio_qr.json"


def main() -> None:
    with open(CAMINHO_DESAFIO, encoding="utf-8") as ficheiro:
        # QRCodeDesafio(**dados) falha logo se o JSON tiver um campo a mais ou a menos
        qr_codes = [QRCodeDesafio(**dados) for dados in json.load(ficheiro)]
    ligacao = abrir_ligacao()
    try:
        repositorio = CacaTesouroRepositorySQLite(ligacao)
        # IF NOT EXISTS e INSERT OR REPLACE:
        # pode correr-se outra vez sem duplicar nada e sem apagar as descobertas já feitas
        repositorio.criar_tabelas()
        repositorio.guardar_qr_codes(qr_codes)
    finally:
        ligacao.close()
    print(f"{len(qr_codes)} QR Codes carregados em {CAMINHO_BD.name}")


# Só corre quando o ficheiro é executado diretamente, não quando é importado
if __name__ == "__main__":
    main()

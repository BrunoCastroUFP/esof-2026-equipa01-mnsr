"""Ligação à base de dados SQLite do projeto."""
import sqlite3

from pathlib import Path


# Caminho absoluto, calculado a partir deste ficheiro:
# parents[2] sobe de src/persistence/ até à raiz
# O ficheiro .sqlite3 está no .gitignore e nunca vai para o GitHub
CAMINHO_BD = Path(__file__).resolve().parents[2] / "mnsr.sqlite3"


def abrir_ligacao() -> sqlite3.Connection:
    # check_same_thread=False porque o FastAPI pode abrir a ligação numa thread e usá-la noutra
    # É seguro porque cada pedido tem a sua ligação, nunca partilhada.
    return sqlite3.connect(CAMINHO_BD, check_same_thread=False)

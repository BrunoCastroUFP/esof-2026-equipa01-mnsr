"""Repositório de obras em SQLite: implementa o RepositorioObras do negócio."""

import sqlite3

from src.business.modelos import Obra

SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS obras (
    id TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    sala_id TEXT NOT NULL
)
"""


class ObraRepositorySQLite:
    def __init__(self, ligacao: sqlite3.Connection):
        self._ligacao = ligacao

    def criar_tabela(self) -> None:
        self._ligacao.execute(SQL_CRIAR_TABELA)

    def guardar_todas(self, obras: list[Obra]) -> None:
        # SQL parametrizado: os valores vão nos " e nunca são colados no texto do SQL
        # Impede SQL injection
        self._ligacao.executemany(
            "INSERT OR REPLACE INTO obras (id, titulo, autor, sala_id) VALUES (?, ?, ?, ?)",
            [(obra.id, obra.titulo, obra.autor, obra.sala_id) for obra in obras],
        )
        self._ligacao.commit()

    def listar_todas(self) -> list[Obra]:
        linhas = self._ligacao.execute(
            "SELECT id, titulo, autor, sala_id FROM obras ORDER BY titulo"
        ).fetchall()
        # Converte cada linha da tabela numa Obra: o resto da app nunca vê SQL
        return [Obra(*linha) for linha in linhas]

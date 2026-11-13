"""Repositório de obras em SQLite: implementa o RepositorioObras do negócio."""

import sqlite3

from src.business.modelos import Obra

SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS obras (
    id TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    sala_id TEXT NOT NULL,
    destaque INTEGER NOT NULL DEFAULT 0,
    tempo_estimado INTEGER NOT NULL DEFAULT 10
)
"""
# Lista única de colunas usada nas queries (INSERT e SELECT)
COLUNAS = ("id", "titulo", "autor", "sala_id", "destaque", "tempo_estimado")
COLUNAS_SQL = ", ".join(COLUNAS)
PLACEHOLDERS_SQL = ", ".join("?" for _ in COLUNAS)


class ObraRepositorySQLite:
    def __init__(self, ligacao: sqlite3.Connection):
        self._ligacao = ligacao

    def criar_tabela(self) -> None:
        self._ligacao.execute(SQL_CRIAR_TABELA)

    def guardar_todas(self, obras: list[Obra]) -> None:
        valores = [
            (
                obra.id,
                obra.titulo,
                obra.autor,
                obra.sala_id,
                int(obra.destaque),
                obra.tempo_estimado,
            )
            for obra in obras
        ]

        self._ligacao.executemany(
            f"INSERT OR REPLACE INTO obras ({COLUNAS_SQL}) VALUES ({PLACEHOLDERS_SQL})",
            valores,
        )
        self._ligacao.commit()

    def listar_todas(self) -> list[Obra]:
        linhas = self._ligacao.execute(
            f"SELECT {COLUNAS_SQL} FROM obras ORDER BY titulo"
        ).fetchall()
        # Converte cada linha da tabela numa Obra: o resto da app nunca vê SQL
        return [
            Obra(
                id=obra_id,
                titulo=titulo,
                autor=autor,
                sala_id=sala_id,
                destaque=bool(destaque),
                tempo_estimado=tempo_estimado,
            )
            for obra_id, titulo, autor, sala_id, destaque, tempo_estimado in linhas
        ]

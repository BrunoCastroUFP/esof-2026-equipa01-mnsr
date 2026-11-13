"""
Repositório da caça ao tesouro em SQLite: implementa RepositorioCacaTesouro do negócio
É o único sítio com o SQL da caça ao tesouro.
Todos os valores vão como parâmetros (?), nunca colados no texto do SQL, o que impede SQL injection
"""

import sqlite3

from src.business.caca_tesouro import QRCodeDesafio

# Os QR Codes do desafio: um por obra, colado junto a ela
SQL_CRIAR_QR_CODES = """
CREATE TABLE IF NOT EXISTS qr_codes_desafio (
    codigo TEXT PRIMARY KEY,
    obra_id TEXT NOT NULL,
    pontos INTEGER NOT NULL CHECK (pontos > 0)
)
"""

# As descobertas de cada sessão anónima. Não há nome, idade nem e-mail (RNF-03).
# PRIMARY KEY (sessao_id, obra_id): uma sessão só pode ter cada obra uma vez.
# É esta chave que impede os pontos a dobrar do cenário 2.
# Os pontos são copiados do QR no momento da descoberta:
# se um dia o museu mudar os pontos de uma obra, o total de quem já a encontrou não muda
SQL_CRIAR_DESCOBERTAS = """
CREATE TABLE IF NOT EXISTS descobertas (
    sessao_id TEXT NOT NULL,
    obra_id TEXT NOT NULL,
    pontos INTEGER NOT NULL,
    PRIMARY KEY (sessao_id, obra_id)
)
"""


class CacaTesouroRepositorySQLite:
    def __init__(self, ligacao: sqlite3.Connection):
        # A ligação vem de fora: na app abre-se uma por pedido (dependencias.py);
        # nos testes é um SQLite em memória
        self._ligacao = ligacao

    def criar_tabelas(self) -> None:
        # IF NOT EXISTS: pode correr-se várias vezes sem apagar nada
        self._ligacao.execute(SQL_CRIAR_QR_CODES)
        self._ligacao.execute(SQL_CRIAR_DESCOBERTAS)

    def guardar_qr_codes(self, qr_codes: list[QRCodeDesafio]) -> None:
        # Usado pelos testes e, no passo 5, pelo script que carrega os QR do desafio
        # INSERT OR REPLACE: carregar o mesmo ficheiro duas vezes não duplica os QR
        self._ligacao.executemany(
            "INSERT OR REPLACE INTO qr_codes_desafio (codigo, obra_id, pontos) VALUES (?, ?, ?)",
            [(qr.codigo, qr.obra_id, qr.pontos) for qr in qr_codes],
        )
        self._ligacao.commit()

    def obter_qr_code(self, codigo: str) -> QRCodeDesafio | None:
        # (codigo,) com vírgula: o execute pede um tuplo, mesmo com um só valor.
        # Sem a vírgula, (codigo) era só o texto entre parênteses
        linha = self._ligacao.execute(
            "SELECT codigo, obra_id, pontos FROM qr_codes_desafio WHERE codigo = ?", (codigo,)
        ).fetchone()
        # fetchone() devolve None se não houver linha: é o cenário 3.
        # Se houver, *linha passa as 3 colunas como os 3 campos do QRCodeDesafio
        return QRCodeDesafio(*linha) if linha else None

    def registar_descoberta(self, sessao_id: str, qr_code: QRCodeDesafio) -> bool:
        # INSERT OR IGNORE: se chave (sessao_id, obra_id) já existir, não grava nada e não dá erro.
        # A pergunta "já existe?" e a gravação são uma só operação na base de dados,
        # por isso duas leituras ao mesmo tempo não dão pontos a dobrar
        cursor = self._ligacao.execute(
            "INSERT OR IGNORE INTO descobertas (sessao_id, obra_id, pontos) VALUES (?, ?, ?)",
            (sessao_id, qr_code.obra_id, qr_code.pontos),
        )
        self._ligacao.commit()
        # rowcount diz quantas linhas o INSERT gravou:
        # 1 se a descoberta é nova (cenário 1)
        # 0 se foi ignorada porque a sessão já tinha a obra (cenário 2)
        return cursor.rowcount == 1

    def total_pontos(self, sessao_id: str) -> int:
        # SUM de uma sessão sem descobertas dá NULL (None em Python);
        # o COALESCE troca esse NULL por 0
        (total,) = self._ligacao.execute(
            "SELECT COALESCE(SUM(pontos), 0) FROM descobertas WHERE sessao_id = ?", (sessao_id,)
        ).fetchone()
        return total

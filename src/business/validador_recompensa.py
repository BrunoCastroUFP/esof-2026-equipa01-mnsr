"""
Regra das recompensas da caça ao tesouro (issue #29, cenário 1 da US-08 #18)
Camada de negócio pura, não conhece:
 - base de dados;
 - FastAPI;
 - códigos de voucher
Só decide se a leitura que acabou de acontecer dá recompensa. Emitir o voucher é da #18
"""

from dataclasses import dataclass

# Os valores do cenário 1 da US-08, num só sítio
OBRAS_PARA_EXPLORADOR = 3
MEDALHA_EXPLORADOR = "Explorador"
DESCONTO_EXPLORADOR = 10  # percentagem na loja


@dataclass(frozen=True)
class Recompensa:
    medalha: str
    # Só o direito ao desconto: o código do voucher é gerado no servidor (#18)
    desconto_percentagem: int


class ValidadorRecompensa:
    def avaliar(self, obras_encontradas: int, ja_descoberta: bool) -> Recompensa | None:
        # obras_encontradas: total da sessão já com esta leitura
        # Vem sempre da base de dados, nunca do pedido do cliente

        # A recompensa só existe no momento em que a sessão chega à 3.ª obra:
        # - leitura repetida: o total não mudou, por isso não conta
        # - da 4.ª obra em diante: o limite já foi atingido, não há segundo voucher
        if not ja_descoberta and obras_encontradas == OBRAS_PARA_EXPLORADOR:
            return Recompensa(MEDALHA_EXPLORADOR, DESCONTO_EXPLORADOR)
        return None

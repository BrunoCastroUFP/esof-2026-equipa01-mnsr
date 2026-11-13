from dataclasses import dataclass


@dataclass(frozen=True)
class Recompensa:
    medalha: str
    desconto_percentagem: int


class ValidadorRecompensa:
    def avaliar(self, obras_encontradas: int, ja_descoberta: bool) -> Recompensa | None:
        if not ja_descoberta and obras_encontradas == 3:
            return Recompensa("Explorador", 10)
        return None

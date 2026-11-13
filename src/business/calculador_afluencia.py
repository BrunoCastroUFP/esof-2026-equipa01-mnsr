from isort.settings import field

class Sala:
    def __init__(self, id_sala: str, visitantes: int):
        self.id = id_sala
        self.visitantes = visitantes
        self.contiguas: list["Sala"] = []


class CalculadorAfluencia:

    def calcular_nivel(self, visitantes: int, capacidade: int) -> str:
        percentagem = min((visitantes / capacidade) * 100, 100.0)
        if percentagem < 40.0:
            return "Baixa"
        if percentagem < 80.0:
            return "Média"

        return "Elevada"

    def calcular_ocupacao_total(self, sala: Sala)-> int:
        total = sala.visitantes
        for contigua in sala.contiguas:
            total+= self.calcular_ocupacao_total(contigua)
        return total
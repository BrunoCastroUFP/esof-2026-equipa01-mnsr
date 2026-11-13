class CalculadorAfluencia:


    def calcular_nivel(self, visitantes: int, capaciadade: int) -> str:
        percentagem = (visitantes/capaciadade)*100

        if percentagem > 100.0:
            percentagem = 100.0

        if percentagem < 40.0:
            return "Baixa"
        elif percentagem < 80.0:
            return "Média"
        else:
            return "Elevada"
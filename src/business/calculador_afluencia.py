class CalculadorAfluencia:


    def calcular_nivel(self, visitantes: int, capaciadade: int) -> str:
        percentagem = min((visitantes/capaciadade)*100, 100.0)
        if percentagem < 40.0:
            return "Baixa"
        if percentagem < 80.0:
            return "Média"

        return "Elevada"

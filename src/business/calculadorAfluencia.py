class CalculadorAfluencia:
    # ⚪ Fase Refactor: Criação da constante para eliminar o número mágico 500
    CAPACIDADE_MAXIMA_SALAS = 500

    def calcular_nivel(self, visitantes: int) -> str:
        # 🟢 Fase Green: Código para satisfazer a condição
        if visitantes > self.CAPACIDADE_MAXIMA_SALAS:
            return "Elevada"
        return "Baixa"
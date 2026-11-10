class ServicoAssistenteIA:
    def __init__(self, cliente_rag):

        # Recebemos o cliente RAG/Mock no teste
        self.cliente_rag = cliente_rag

    def obter_informacao(self, obra: str)-> str:

        # Consulta a IA e devolve o texto
        return self.cliente_rag.consultar(obra)
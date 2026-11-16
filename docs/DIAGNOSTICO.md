## Bug A — Ciclo infinito ao calcular ocupação total de salas contíguas

* **Sintoma:** Ao somar a ocupação de uma sala com a das salas contíguas através de `CalculadorAfluencia.calcular_ocupacao_total`, um grafo com ligações circulares (`A -> B -> A`) entra em recursão infinita e termina com `RecursionError: maximum recursion depth exceeded`.
* **Hipótese:** O percurso recursivo pelos nós adjacentes não regista as salas já contabilizadas, revisitando indefinidamente os mesmos vértices sempre que existe um ciclo na planta do museu.
* **Teste falsificável:** Criado o teste unitário `test_calculador_afluencia_com_salas_circulares` em `tests/unit/test_calculador_afluencia.py`, ligando duas salas em ciclo (`S1 -> S2 -> S1`) e confirmando inicialmente a falha por `RecursionError`.
* **Causa raiz:** Ausência de controlo de estado de visita (`visited set`) na travessia em profundidade (`DFS`) do método `calcular_ocupacao_total`.
* **Correção e Commit:** Adicionado um conjunto (`set[str]`) para memorizar os identificadores das salas já visitadas e interromper a chamada recursiva (`return 0`) caso a sala já tenha sido processada.
  * **Commit do fix:** [`2c58ab2`](../../commit/2c58ab2290e0b6d8c5d5741e2aaaf9856943f664)

## Bug B — Histórico de conversa retido depois do fecho da sessão

* **Sintoma:** O histórico de conversa pode continuar disponível depois de uma sessão fechar, fazendo a memória crescer com sessões novas.
* **Hipótese:** O serviço não associa o contexto a uma sessão anónima nem tem uma operação explícita para o eliminar; sem limite por sessão, o contexto pode crescer durante a conversa.
* **Teste falsificável:** `test_fechar_sessao_apaga_historico_antes_da_consulta_seguinte` confirma que uma conversa recebe o histórico anterior e que, depois do fecho, a consulta seguinte começa sem histórico. `test_fechar_sessao_liberta_memoria_do_historico` mede a libertação com `tracemalloc`.
* **Causa raiz:** `ServicoAssistenteIA` apenas encaminhava a pergunta para o cliente RAG; não tinha histórico por sessão, limite de tamanho ou operação de fecho. Como o serviço original era sem estado, a falha inicial dos testes foi a ausência dessa API, não um histórico persistido reproduzível no código existente.
* **Correção:** O serviço aceita apenas um UUID v4 anónimo, mantém no máximo 10 trocas pergunta/resposta por sessão em memória e elimina a entrada ao fechar. Não guarda nome, e-mail ou idade, nem persiste o histórico em SQLite ou ficheiro.
* **Medição de memória:** Com `tracemalloc`, numa sessão sintética de 10 perguntas de 250 000 caracteres cada, foram medidos 0 bytes antes de criar o histórico, 2 501 350 bytes antes do fecho e 192 bytes depois do fecho (redução de 2 501 158 bytes; pico de 2 751 758 bytes).
* **Commits:** Os testes foram registados antes da correção:
  * **Commit de teste do fecho:** [`6c431ad`](../../commit/6c431ad1e8704ef0a184a10e921050661ed3467d)
  * **Commit de teste do isolamento:** [`c1fe303`](../../commit/c1fe303cba76554933241209c012c2f5276d45e9)
  * **Commit de teste de privacidade:** [`116c294`](../../commit/116c294a91d0d526e6c6e83b61f8a1cf2d831b72)
  * **Commit do fix:** [`9e5c9ff`](../../commit/9e5c9ff84d384f03be495b77ed8e1a43e5bc907d)
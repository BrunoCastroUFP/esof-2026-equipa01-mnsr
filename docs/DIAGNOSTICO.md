## Bug A — Ciclo infinito ao calcular ocupação total de salas contíguas

* **Sintoma:** Ao somar a ocupação de uma sala com a das salas contíguas através de `CalculadorAfluencia.calcular_ocupacao_total`, um grafo com ligações circulares (`A -> B -> A`) entra em recursão infinita e termina com `RecursionError: maximum recursion depth exceeded`.
* **Hipótese:** O percurso recursivo pelos nós adjacentes não regista as salas já contabilizadas, revisitando indefinidamente os mesmos vértices sempre que existe um ciclo na planta do museu.
* **Teste falsificável:** Criado o teste unitário `test_calculador_afluencia_com_salas_circulares` em `tests/unit/test_calculador_afluencia.py`, ligando duas salas em ciclo (`S1 -> S2 -> S1`) e confirmando inicialmente a falha por `RecursionError`.
* **Causa raiz:** Ausência de controlo de estado de visita (`visited set`) na travessia em profundidade (`DFS`) do método `calcular_ocupacao_total`.
* **Correção e Commit:** Adicionado um conjunto (`set[str]`) para memorizar os identificadores das salas já visitadas e interromper a chamada recursiva (`return 0`) caso a sala já tenha sido processada.
  * **Commit do fix:** [`2c58ab2`](../../commit/2c58ab2290e0b6d8c5d5741e2aaaf9856943f664)
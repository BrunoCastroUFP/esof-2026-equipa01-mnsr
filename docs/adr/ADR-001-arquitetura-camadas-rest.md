# ADR-001: Arquitetura em 3 camadas com API REST e cliente PWA offline-first
- **Estado:** Aceite
- **Data:** 2026-11-08 (revisão da versão de 14/10)
- **Decisores:** Equipa 01

## Contexto
- As paredes de pedra deixam salas sem rede, mas os roteiros, o mapa e a leitura de QR Codes têm de funcionar (RNF-02)
- Os 4 módulos usam os mesmos dados e têm de ser testados isoladamente, com cobertura ≥ 80 % (RNF-05)
- As chaves do LLM e a validação dos vouchers não podem estar no telemóvel, e não podemos guardar dados pessoais de menores (RNF-03)

## Alternativas consideradas
**Organização do sistema**
1. **Só app, sem backend.** Rejeitada: os segredos e as validações ficariam no telemóvel, onde qualquer pessoa os extrai
2. **Backend sem camadas, com as regras nas rotas.** Rejeitada: as regras não se testam sem HTTP e base de dados, e fica tudo acoplado
3. **Um microserviço por módulo.** Rejeitada: testar e pôr no CI 4 serviços é demasiado para a equipa
4. **Backend em 3 camadas com API REST.** Escolhida

**Tipo de cliente**
1. **App nativa em React Native.** Rejeitada: obriga a emuladores e builds e dificulta o blind test. A sua vantagem seria ler beacons Bluetooth, mas não temos esse hardware
2. **PWA.** Escolhida: instala-se com um link, funciona offline e acede à câmara para ler QR Codes

## Decisão
- **Apresentação:** rotas REST que validam os pedidos, sem regras de negócio
- **Negócio:** as regras. Não conhece o framework nem a base de dados; recebe os repositórios por parâmetro
- **Persistência:** o único sítio com SQL
- **Cliente PWA** que guarda os dados no telemóvel quando há rede (detalhe na ADR-002). A localização nas salas passa a fazer-se com um QR Code à entrada de cada sala

## Consequências
- **Positivas:** as regras testam-se com mocks; os segredos ficam no servidor; a app funciona sem rede; o blind test é fácil
- **Negativas:** há algum código de ligação entre camadas; é preciso atualizar a cópia local quando o acervo muda; não há beacons
- **Riscos:** a câmara e o Service Worker só funcionam em HTTPS ou em `localhost`, por isso a demo num telemóvel precisa de HTTPS

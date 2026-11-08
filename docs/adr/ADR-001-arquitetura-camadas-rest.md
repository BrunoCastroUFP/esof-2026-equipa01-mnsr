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
1. **Só app, sem backend:** toda a lógica e todos os dados ficam no telemóvel, que fala diretamente com serviços externos como o LLM.
Rejeitada: os segredos (chave do LLM) e as validações (vouchers) ficariam no telemóvel, onde qualquer pessoa pode abrir o código e extraí-los.
2. **Backend sem camadas:** um servidor em que as regras de negócio e o SQL estão escritos diretamente dentro das rotas HTTP.
Rejeitada: para testar uma regra é preciso arrancar o servidor e a base de dados, e qualquer mudança mexe em tudo, porque fica tudo acoplado.
3. **Microserviços:** um servidor independente para cada módulo (roteiros, caça ao tesouro, IA e afluência), que comunicam entre si pela rede.
Rejeitada: obriga a implementar, testar e pôr no CI quatro serviços, o que é demasiado para a equipa e para o prazo.
4. **Backend em 3 camadas com API REST:** um só servidor dividido em apresentação (rotas), negócio (regras) e persistência (base de dados), em que cada camada só fala com a de baixo.
Escolhida: as regras testam-se isoladamente com mocks e cada camada pode mudar sem afetar as outras.

**Tipo de cliente**
1. **App nativa em React Native:** app instalada pela loja (ou por um `.apk`), com acesso total ao telemóvel, incluindo o Bluetooth.
Rejeitada: obriga a emuladores e builds e dificulta o blind test. A sua vantagem seria ler beacons Bluetooth, mas não temos esse hardware.
2. **PWA (Progressive Web App):** um site que se instala como app a partir de um link e que funciona sem rede graças ao Service Worker e ao armazenamento local do browser.
Escolhida: instala-se com um link, funciona offline e acede à câmara para ler QR Codes.

## Decisão
- **Apresentação:** rotas REST que validam os pedidos, sem regras de negócio
- **Negócio:** as regras. Não conhece o framework nem a base de dados; recebe os repositórios por parâmetro
- **Persistência:** o único sítio com SQL
- **Cliente PWA** que guarda os dados no telemóvel quando há rede (detalhe na ADR-002). A localização nas salas passa a fazer-se com um QR Code à entrada de cada sala

## Consequências
- **Positivas:** as regras testam-se com mocks; os segredos ficam no servidor; a app funciona sem rede; o blind test é fácil
- **Negativas:** há algum código de ligação entre camadas; é preciso atualizar a cópia local quando o acervo muda; não há beacons
- **Riscos:** a câmara e o Service Worker só funcionam em HTTPS ou em `localhost`, por isso a demo num telemóvel precisa de HTTPS

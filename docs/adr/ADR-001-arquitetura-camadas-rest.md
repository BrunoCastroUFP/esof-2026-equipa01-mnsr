# ADR-001: Adoção de Arquitetura em Camadas com API RESTful e Caching Offline
* Status: Aceite (Accepted)
* Data: 2026-10-12
* Decisores: Equipa de Engenharia de Software (Grupo 01)
## 1. Contexto (Context)
As paredes espessas de pedra do Palácio dos Carrancas (MNSR) provocam zonas cegas de
conectividade 4G/Wi-Fi nas galerias de escultura. Adicionalmente, a app precisa de
responder em menos de 1,5 segundos durante os picos de visitação.
## 2. Decisão (Decision)
Adotar uma arquitetura em 3 Camadas com Backend API RESTful e uma estratégia de Caching
Local "Offline-First" no cliente móvel (PWA/IndexedDB). Os dados dos roteiros e obras
são descarregados na entrada do museu.
## 3. Consequências (Consequences)
* Positivas: Funcionamento garantido mesmo sem sinal Wi-Fi nas salas; resposta
instantânea da interface.
* Negativas / Riscos: Maior complexidade na sincronização de dados e na gestão do
armazenamento local do dispositivo.
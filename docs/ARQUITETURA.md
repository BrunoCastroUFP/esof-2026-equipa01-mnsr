# Arquitetura de Software — App MNSR Digital

## 1. Visão Geral
A App MNSR Digital adota o padrão de Arquitetura em 3 Camadas (Layered Architecture / API REST) para garantir a Separação de Responsabilidades , Alta Coesão e Baixo Acoplamento:  

1. Camada de Apresentação (UI / REST Controllers): Captura interações do visitante na interface móvel/PWA e expõe/consome endpoints RESTful em formato JSON
2. Camada de Lógica de Negócio (Service Layer): Contém as regras de negócio, algoritmos de geração de roteiros por tempo, validação de QR Codes e orquestração do assistente de IA (RAG)
3. Camada de Persistência / Dados (Repository Layer): Encapsula o acesso à base de dados SQL e gere a cache local offline no dispositivo móvel

--- 
## 2. Diagrama de Classes UML (Visão Estrutural) 
```mermaid
classDiagram
   class Obra {
     +String id
     +String titulo
     +String autor
     +int pontosGamificacao
     +getDetalhes()
   }

   class Roteiro {
     +String id
     +String nome
     +int duracaoEstimada
     +addObra(Obra o)
   }

   class Visitante {
     +String id
     +int pontosAcumulados
     +registarVisita()
   }

  class DesafioGamificado {
    +String id
    +String qrCodeHash
    +String pergunta
    +int pontos
    +validarResposta(resposta) bool
  }

  Roteiro "1" *-- "1..*" Obra : contém
  Visitante "1" --> "0..*" Roteiro : percorre
  DesafioGamificado "1" --> "1" Obra : associado_a
  Visitante "1" --> "0..*" DesafioGamificado : resolve
```

--- 
## 3. Diagrama de Sequência UML (Visão Dinâmica) 
### US-01 (Gerar Roteiro por Tempo Disponível)
```mermaid
sequenceDiagram
  autonumber
  actor Visitante
  participant UI as RoteiroView (Apresentação)
  participant Ctrl as RoteiroController (Apresentação)
  participant Srv as ServicoRoteiro (Negócio)
  participant Repo as ObraRepository (Persistência)

  Visitante->>UI: Seleciona tempo (30 min) e perfil
  UI->>Ctrl: POST /api/roteiros {tempo: 30, perfil: "escultura"}
  Ctrl->>Srv: gerarRoteiro(tempo=30, perfil)
  Srv->>Repo: buscarObrasPorPerfil(perfil)
  Repo-->>Srv: Lista de Obras candidatas (cache/SQL)
  Note right of Srv: Algoritmo seleciona e ordena obras até 30 min
  Srv-->>Ctrl: Instância do Roteiro gerado
  Ctrl-->>UI: 200 OK (JSON do Roteiro)
  UI-->>Visitante: Apresenta o itinerário otimizado na app
```
### US-02 (Validação de QR Code na Caça ao Tesouro)

```mermaid
sequenceDiagram
  autonumber
  actor Visitante
  participant UI as QRScanView (Apresentação)
  participant Ctrl as GamificacaoController (Apresentação)
  participant Srv as ServicoGamificacao (Negócio)
  participant Repo as DesafioRepository (Persistência)
  
  Visitante->>UI: Digitaliza o QR Code junto à estátua "O Desterro"
  UI->>Ctrl: POST /api/desafios/validar {qrCodeHash: "MNSR-DEST-01"}
  Ctrl->>Srv: validarQRCode("MNSR-DEST-01", visitanteId)
  Srv->>Repo: buscarDesafioPorHash("MNSR-DEST-01") 
  Repo-->>Srv: Instância do DesafioGamificado (cache/SQL)
  Note right of Srv: Valida o código, calcula a pontuação e atribui a medalha
  Srv->>Repo: atualizarPontosVisitante(visitanteId, +10)
  Repo-->>Srv: Confirmação de atualização
  Srv-->>Ctrl: DTO com Resultado do Desafio (Pontos + Troféu)
  Ctrl-->>UI: 200 OK (JSON Sucesso + Pista Desbloqueada)
  UI-->>Visitante: Exibe animação de conquista e desbloqueia a próxima pista
```
---

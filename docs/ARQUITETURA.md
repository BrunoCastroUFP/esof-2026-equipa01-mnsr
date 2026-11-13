# Arquitetura de Software — App MNSR Digital

## 1. Visão Geral
A App MNSR Digital adota o padrão de Arquitetura em 3 Camadas (Layered Architecture / API REST) para garantir a Separação de Responsabilidades , Alta Coesão e Baixo Acoplamento:  

1. Camada de Apresentação (UI / REST Controllers): Captura interações do visitante na interface móvel/PWA e expõe/consome endpoints RESTful em formato JSON
2. Camada de Lógica de Negócio (Service Layer): Contém as regras de negócio, algoritmos de geração de roteiros por tempo, validação de QR Codes e orquestração do assistente de IA (RAG)
3. Camada de Persistência / Dados (Repository Layer): Encapsula o acesso à base de dados SQL do servidor. A cópia offline no telemóvel pertence à PWA (ADR-002)

--- 
## 2. Diagrama de Classes UML (Visão Estrutural) 
```mermaid
classDiagram
  class Obra {
    +String id
    +String titulo
    +String autor
    +String sala_id
  }

  class RepositorioObras {
    <<interface>>
    +listar_todas() list~Obra~
  }

  class ServicoAcervo {
    -RepositorioObras _repositorio
    +listar_obras() list~Obra~
  }

  class ObraRepositorySQLite {
    -Connection _ligacao
    +criar_tabela()
    +guardar_todas(obras)
    +listar_todas() list~Obra~
  }

  class Roteiro {
    <<planeada>>
    +String id
    +String nome
    +int duracaoEstimada
    +addObra(Obra o)
  }

  class Visitante {
    <<planeada>>
    +String id
    +int pontosAcumulados
    +registarVisita()
  }

  class DesafioGamificado {
    <<planeada>>
    +String id
    +String qrCodeHash
    +String pergunta
    +int pontos
    +validarResposta(resposta) bool
  }

  ServicoAcervo --> RepositorioObras : usa
  ObraRepositorySQLite ..|> RepositorioObras : implementa
  RepositorioObras ..> Obra : devolve
  Roteiro "1" -- "1..*" Obra : inclui
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
  participant API as desafios_api (Apresentação)
  participant Val as ValidadorQRCode (Negócio)
  participant Repo as CacaTesouroRepositorySQLite (Persistência)

  Visitante->>API: POST /api/desafios/validar {sessao_id, codigo}
  alt Pedido mal formado
    API-->>Visitante: 422 (sessão não é UUID v4, código fora do formato ou campos a mais)
  else Pedido válido
    API->>Val: validar(sessao_id, codigo)
    Val->>Repo: obter_qr_code(codigo)
    alt Código não existe no desafio (cenário 3)
      Repo-->>Val: None
      Val-->>API: QRCodeNaoReconhecido
      API-->>Visitante: 404 "QR Code não reconhecido"
    else Código existe
      Repo-->>Val: QRCodeDesafio
      Val->>Repo: registar_descoberta(sessao_id, qr_code)
      Note right of Repo: INSERT OR IGNORE com a chave (sessao_id, obra_id)
      Repo-->>Val: True se nova, False se repetida
      Val->>Repo: total_pontos(sessao_id)
      Repo-->>Val: total
      Val-->>API: ResultadoLeitura
      API-->>Visitante: 200 "Obra encontrada" (cenário 1) ou "Obra já descoberta" (cenário 2)
    end
  end
```
---

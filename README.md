# App MNSR DIGITAL - ESOF 2026

## Autores - Grupo 01:  
- Bruno Castro 2024118435
- Filipe Silva 2024118471
- Rayssa Santos 2024118083
- Tiago Chousal 2024116801

## Visão do Produto
- **PARA** os jovens, famílias e turistas culturais que visitam a cidade do Porto,
- **QUE** procuram uma experiência museológica dinâmica, personalizada e interativa,
- **A APP MNSR DIGITAL** é uma aplicação móvel inteligente e gamificada,
- **QUE** oferece roteiros personalizados pelo tempo disponível, caça ao tesouro por QR Code e um guia conversacional de IA para responder a dúvidas sobre as obras,
- **AO CONTRÁRIO DOS** guias áudio estáticos e brochuras em papel tradicionais,
- **O NOSSO PRODUTO** aumenta o envolvimento do visitante, promove o regresso do público local e permite gerir eficientemente o fluxo nas salas do museu.

## Tabela de EPICs
| ID EPIC / Issues | Área Funcional | Descrição da EPIC | 
| --- | --- | --- | 
| **EPIC-01** | Roteiros Inteligentes | Gestão e geração de percursos temáticos personalizados em função do tempo e perfil do visitante | 
| **EPIC-02** | Gamificação & QR Codes | Sistema de caça ao tesouro com leitura de QR Codes e atribuição de recompensas virtuais | 
| **EPIC-03** | Assistente IA / RAG | Guia conversacional inteligente para esclarecimento de dúvidas sobre obras do acervo em linguagem natural |
| **EPIC-04** | Afluência em Tempo Real | Indicador de ocupação das salas e sugestões de salas alternativas e de eventos próximos |

## Instruções de instalação e requisitos do sistema
### Requisitos
- Python 3.14

### Instalar
No Windows, na pasta do repositório:
```powershell
py -3.14 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

### Correr a API
```powershell
# Cria a base de dados mnsr.sqlite3 e guarda nela as obras de data/acervo.json.
# Só é preciso da primeira vez, ou quando o acervo.json mudar; pode correr-se outra vez sem criar obras duplicadas.
.venv\Scripts\python -m scripts.carregar_acervo

# Arranca a API em http://127.0.0.1:8000 com o uvicorn. "src.main:app" é o objeto app do ficheiro src/main.py.
# --reload reinicia o servidor sozinho sempre que um ficheiro .py muda (só para desenvolvimento). Para parar: Ctrl+C.
.venv\Scripts\python -m uvicorn src.main:app --reload
```

Depois, abrir no browser:
- http://127.0.0.1:8000/api/obras: lista das obras de exemplo
- http://127.0.0.1:8000/docs: documentação interativa da API (Swagger)

O servidor só aceita ligações da própria máquina (127.0.0.1). 
Não usar `--host 0.0.0.0` numa rede pública, porque isso abre a API a toda a rede


### Correr os testes e o linter
Os mesmos comandos que o CI corre em cada push e PR (`.github/workflows/ci.yml`):
```powershell
# Todos os testes (unit, integration e e2e); -v mostra o nome de cada teste
.venv\Scripts\python -m pytest -v

# Testes com cobertura: falha se a cobertura do src/ for menor do que 80 %, como no CI
.venv\Scripts\python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=80

# Linter: o CI falha se a nota for menor do que 8
.venv\Scripts\python -m pylint src/ --fail-under=8.0

# Procura vulnerabilidades conhecidas nas dependências do requirements.txt
.venv\Scripts\python -m pip_audit -r requirements.txt
```

Usar sempre `python -m pytest` e não só `pytest`: no Windows 11, o Smart App Control pode bloquear o `pytest.exe` do venv, por não ter assinatura digital. Não desligar o Smart App Control por causa disto.

## Estrutura do projeto
O backend segue uma arquitetura em 3 camadas (ADR-001): 
- apresentação recebe os pedidos HTTP, 
- negócio tem as regras,
- persistência fala com a base de dados.  
A apresentação e a persistência dependem do negócio; o negócio não depende de nenhuma das duas

```text
esof-2026-equipa01-mnsr/
├── src/                      # código da aplicação (backend)
│   ├── main.py               # cria a app FastAPI e regista as rotas
│   ├── presentation/         # camada de apresentação: a API REST
│   ├── business/             # camada de negócio: regras e modelos
│   └── persistence/          # camada de persistência: base de dados
├── tests/                    # testes automáticos (pytest)
│   ├── unit/                 # negócio isolado, com mocks
│   ├── integration/          # repositórios com SQLite em memória
│   └── e2e/                  # pedidos HTTP à app inteira
├── scripts/                  # ferramentas de apoio, corridas à mão
├── data/                     # dados de exemplo
├── docs/                     # documentação do projeto
├── .github/workflows/ci.yml  # pipeline de CI
├── pyproject.toml            # configuração do pytest e do pylint
├── requirements.txt          # dependências com versões fixas
└── LICENSE                   # todos os direitos reservados
```

### O que faz cada ficheiro

| Ficheiro | Camada | Responsabilidade |
| --- | --- | --- |
| `src/main.py` | — | Cria a aplicação FastAPI e regista as rotas. É o ponto de entrada (`uvicorn src.main:app`) |
| `src/presentation/obras_api.py` | Apresentação | Rota `GET /api/obras` e o modelo `ObraResposta`, que define os campos que saem na API |
| `src/presentation/dependencias.py` | Apresentação | Monta o serviço com o repositório real; abre e fecha a ligação à base de dados em cada pedido |
| `src/business/modelos.py` | Negócio | Modelos de domínio partilhados pelas camadas, como a `Obra` |
| `src/business/acervo.py` | Negócio | `ServicoAcervo` (regras do acervo) e `RepositorioObras` (a interface que a persistência cumpre) |
| `src/persistence/base_dados.py` | Persistência | Caminho da base de dados SQLite e abertura das ligações |
| `src/persistence/obra_repository.py` | Persistência | `ObraRepositorySQLite`: o único sítio com SQL das obras, sempre parametrizado |
| `scripts/carregar_acervo.py` | Apoio | Lê `data/acervo.json` e grava as obras na base de dados (`python -m scripts.carregar_acervo`) |
| `data/acervo.json` | Dados | Obras de exemplo do acervo do MNSR (as salas são fictícias) |
| `tests/unit/` | Testes | Testam o negócio isolado, com um repositório falso (mock) |
| `tests/integration/` | Testes | Testam o repositório com um SQLite em memória |
| `tests/e2e/` | Testes | Fazem pedidos HTTP à API com o `TestClient` |
| `.github/workflows/ci.yml` | CI | Em cada push e PR: lint, testes, cobertura ≥ 80 % e auditoria das dependências |
| `pyproject.toml` | Configuração | Opções do pytest e do pylint |
| `requirements.txt` | Configuração | Versões exatas de todas as dependências |
| `docs/adr/` | Documentação | Decisões de arquitetura (ADR-001 a ADR-003) |
| `docs/ARQUITETURA.md` | Documentação | Camadas e diagramas UML de classes e de sequência |
| `docs/AI_LOG.md` | Documentação | Registo de cada uso de IA e da validação feita |
| `docs/CARTA_IA.md` | Documentação | Regras da equipa para o uso de IA |
| `docs/EQUIPA.md` | Documentação | Elementos da equipa e funções |

- Uma regra nova vai para `src/business/`
- uma consulta nova à base de dados para `src/persistence/`
- uma rota nova para `src/presentation/`  
Cada ficheiro novo entra nesta tabela. O `.venv/` e o `mnsr.sqlite3` não vão para o Git: cada pessoa cria-os no seu PC

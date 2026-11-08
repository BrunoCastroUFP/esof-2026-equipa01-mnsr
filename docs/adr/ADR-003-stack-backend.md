# ADR-003: Backend em Python com FastAPI e SQLite
- **Estado:** Aceite
- **Data:** 2026-11-08
- **Decisores:** Equipa 01

## Contexto
- O enunciado aceita o backend em Java (Spring Boot) ou em Python (FastAPI)
- Os 4 elementos têm de correr o projeto no seu PC, e outra equipa tem de o instalar no blind test (M6)

## Alternativas consideradas
**Linguagem e framework**
1. **Java com Spring Boot:** a linguagem que melhor conhecemos, com JUnit, Mockito e JaCoCo.
Rejeitada: obriga a mais configuração (Maven, anotações e injeção de dependências do Spring) e afasta-nos dos exemplos das fichas.
2. **Python com FastAPI:** pouco código por rota, valida os pedidos com Pydantic e gera sozinho a documentação da API (Swagger, em `/docs`).
Escolhida: usa as mesmas ferramentas das fichas e chega para o tamanho do projeto.

**Base de dados no servidor**
1. **PostgreSQL:** servidor de base de dados feito para muitos utilizadores em simultâneo.
Rejeitada: cada pessoa, o CI e o blind test teriam de instalar e configurar um servidor.
2. **SQLite, com o módulo `sqlite3` do Python:** a base de dados é um só ficheiro, sem servidor; nos testes usa-se uma base em memória.
Escolhida: não precisa de instalação e, como só a camada de persistência a conhece (ADR-001), pode ser trocada sem mexer no negócio.

**Ambiente e dependências**
1. **uv:** gestor de pacotes muito rápido, feito em Rust.
Rejeitada: é mais uma ferramenta para todos aprenderem, e a rapidez não faz diferença num projeto deste tamanho.
2. **venv e pip:** já vêm com o Python.
Escolhida: funcionam da mesma forma em todos os PCs e no CI.

## Decisão
- Python 3.14, com FastAPI e uvicorn
- SQLite com `sqlite3`, sempre com SQL parametrizado
- pytest e pytest-cov para os testes; httpx2 para o `TestClient`, porque o httpx gerava um aviso de descontinuação no Starlette
- pylint e pip-audit no CI, para a qualidade do código e as vulnerabilidades das dependências
- Todas as versões fixas no `requirements.txt`

## Consequências
- **Positivas:** menos código; as mesmas ferramentas das fichas e do T1; documentação da API sem trabalho extra; instalação com dois comandos
- **Negativas:** temos de aprender Python
- **Riscos:** o SQLite só faz uma escrita de cada vez, o que pode não chegar para os 200 utilizadores em simultâneo do RNF-01; se for preciso, troca-se só a camada de persistência. As versões fixas têm de ser atualizadas sempre que o pip-audit encontrar uma vulnerabilidade

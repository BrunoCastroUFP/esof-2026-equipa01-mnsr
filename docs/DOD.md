# Definition of Done (DoD) — Equipa 01

**Projeto:** App MNSR Digital

Uma tarefa, *User Story* ou *Pull Request* só é considerada **Concluída (*Done*)** quando cumpre cumulativamente todos os critérios abaixo:

## 1. Código e Arquitetura
- O código respeita a arquitetura em 3 camadas (`presentation`, `business`, `persistence` — ver `ADR-001`) e não expõe segredos ou dados pessoais (`ADR-002`, RNF-03).
- O código corre sem erros nem avisos em ambiente limpo (Python 3.14 / `.venv`).
- **Linter sem violações:** o `pylint` passa conforme a configuração em `pyproject.toml`.
- **Segurança das dependências:** o `pip-audit` passa sem vulnerabilidades conhecidas (quando houver alteração em `requirements.txt`).
- Ficheiros novos adicionados à tabela de ficheiros do `README.md`, quando aplicável.

## 2. Testes Automatizados e Cobertura
- Existem testes unitários (`tests/unit/`), de integração (`tests/integration/`) e/ou E2E (`tests/e2e/`) adequados ao código alterado.
- **100 % dos testes a passar** (`pytest`) localmente e no pipeline de CI (`.github/workflows/ci.yml`).
- **Cobertura mínima de 80 %** (`pytest-cov`), garantida pelo CI.

## 3. Revisão por Pares (*Peer Review*)
- O trabalho foi desenvolvido numa *feature branch* dedicada (zero *commits* diretos na `main`).
- O *Pull Request* foi analisado por **pelo menos 1 colega da equipa**, com revisão efetiva do *diff*, pelo menos um comentário técnico construtivo (quando aplicável), sem comentários pendentes e com aprovação formal (*Approve*).

## 4. Rastreabilidade e Uso Responsável de IA
- Todos os *commits* seguem a convenção de *Conventional Commits* definida em `CONTRIBUTING.md` e incluem o identificador do *issue* (`tipo(escopo): descrição curta #ID`).
- O *Pull Request* associa o respetivo *issue* (`Closes #ID`).
- O cartão correspondente foi atualizado no GitHub Projects (*Sprint Board* -> *Done*).
- Qualquer uso relevante de IA generativa foi validado pela equipa e registado em `docs/AI_LOG.md`, cumprindo a `docs/CARTA_IA.md`.
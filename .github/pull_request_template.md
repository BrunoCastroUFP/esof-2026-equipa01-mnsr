## Resumo das alterações
<!-- Descreve de forma clara o que foi alterado e porquê. -->


## Issue associado
Closes #<!-- Substituir pelo número do issue (ex.: Closes #12) -->

## Checklist — Definition of Done (DoD)
<!-- Consulta os detalhes em docs/DOD.md. Marca [x] apenas após verificar cada item. -->

- [ ] **Linter:** `pylint` sem violações.
- [ ] **Testes e Cobertura:** todos os testes (`pytest`) passam a 100 % e a cobertura é **≥ 80 %** (CI verde).
- [ ] **Arquitetura:** respeita a separação em 3 camadas (`ADR-001`) e não introduz segredos nem dados pessoais.
- [ ] **Commits rastreáveis:** todos os *commits* seguem `CONTRIBUTING.md` e incluem `#ID` do *issue*.
- [ ] **Registo de IA:** uso de IA registado e validado em `docs/AI_LOG.md` (ou não aplicável).
- [ ] **Revisão por colega (*Peer Review*):** pelo menos 1 aprovação de um colega após revisão do *diff* e sem comentários pendentes.

## Notas para o Revisor
<!-- (Opcional) Indica como testar localmente ou pontos específicos do diff que merecem atenção. -->
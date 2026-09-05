---
type: Changelog
version: 0.2.4
date: 2026-09-05
---

# Cross-session Handoff runtime

- adiciona `Handoff` como conceito OKF tipado para trabalho material deixado entre sessões;
- separa `RunOutcome.result_state` de `work_status: complete | partial`;
- exige Handoff ativo quando uma rodada declara trabalho parcial;
- faz `context` e `start` exporem handoffs ativos e relevantes;
- adiciona criação, listagem e continuação/arquivamento com provenance `created_by_run → continued_by_run`;
- expõe o lifecycle na CLI e no FastMCP;
- cobre o ciclo completo com testes de retomada entre duas `LoopRun`.

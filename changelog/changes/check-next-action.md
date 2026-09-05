---
type: Changelog
version: 0.2.2
date: 2026-09-05
---

# Actionable contract-guided checks

- faz `WikiSkill.check_run()` devolver `next_action` derivado da primeira exigência tipada ainda não satisfeita;
- devolve uma ação explícita `complete` quando a rodada satisfaz seu `RunSpec`;
- preserva `unsatisfied` como diagnóstico completo e mantém CLI/MCP alinhados pela mesma resposta do runtime;
- cobre o comportamento com contrato TDD para scaffold incompleto e rodada conforme.

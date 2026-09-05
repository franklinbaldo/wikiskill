---
type: Changelog
version: 0.2.0
date: 2026-09-05
---

# Contract-guided live runs

- adiciona `WikiSkill.start_run()` e `WikiSkill.check_run()`;
- expõe `wikiskill start` e `wikiskill check` no CLI;
- expõe `wikiskill_start` e `wikiskill_check` no FastMCP;
- combina validação estrutural do `okf-parser` com requisitos operacionais definidos por `RunSpec`;
- adiciona testes para o ciclo scaffold incompleto → contrato satisfeito.

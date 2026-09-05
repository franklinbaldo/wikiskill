---
type: Changelog
version: 0.2.1
date: 2026-09-05
---

# Typed schemas for contract-guided runs

- declara schemas para `RunSpec`, `LoopRun`, `RunReading`, `RunGoal`, `RunDecision`, `RunEvidence`, `RunCheck` e `RunOutcome`;
- garante que modelos Pydantic e demais exports possam ser gerados antes de existirem instâncias concretas desses tipos no bundle;
- adiciona testes de cobertura dos contratos declarados.

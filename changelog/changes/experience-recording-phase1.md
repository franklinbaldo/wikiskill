---
type: Changelog
version: 0.1.0
date: 2026-09-02
---

# Experience Recording inicia dogfooding Phase 1

- Adiciona preview determinístico e persistência validada de `Experience` no runtime.
- Expõe `wikiskill experience preview|record` na CLI e tools FastMCP de preview/write com efeitos explícitos.
- Adota o Sinos/SinusTDD como protocolo causal externo para o desenvolvimento do próprio WikiSkill, mantendo a evidência causal separada da memória `Experience`.

---
type: WikiEntry
id: wiki-okf-infrastructure-boundary
title: OKF Parser is infrastructure, not domain runtime
status: active
tags: [architecture, okf, boundary]
---

# Knowledge: OKF Parser as Structural Substrate

## Summary
`okf-parser` provides domain-agnostic graph, relational, and format infrastructure. It must not absorb application-level concepts like agent memory, proposals, or evaluations.

## Context & Scope
Applies to all architectures utilizing Open Knowledge Format for agent systems.

## Key Rules
1. **Infrastructure Responsibility**: AST parsing, link extraction, frontmatter validation, NetworkX graph compilation, DuckDB tables.
2. **Domain Runtime Responsibility**: Semantic lifecycle, consolidation heuristics, prompt synthesis, evaluation harnesses, and CLI/MCP ergonomics.

## Evidence
- Direct evidence from bootstrap: [Decoupling Experience](../experiences/records/2026-09-02-bootstrap-okf-boundary.md).

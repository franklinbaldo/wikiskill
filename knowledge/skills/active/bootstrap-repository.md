---
type: AgentSkill
id: skill-bootstrap-repository
title: Bootstrap new OKF-driven agent repository
version: "0.1.0"
status: active
tags: [bootstrap, setup, git]
---

# Skill: Bootstrap New OKF-Driven Repository

## Purpose
Establishes a compliant Open Knowledge Format repository with strict architectural boundaries and CI validation from day one.

## Procedure
1. Create Git repository with clean directory hierarchy (`src/`, `knowledge/`, `specs/`, `docs/`, `tests/`).
2. Define `pyproject.toml` targeting Python 3.12+, pinning `okf-parser`, `fastmcp`, `cyclopts`, `ibis-framework`.
3. Scaffold concept specifications in `specs/`.
4. Run `okf-parser check` and establish pre-commit validation.
5. Create initial authentic bootstrap `Experience` and `WikiEntry` records documenting the genesis decisions.

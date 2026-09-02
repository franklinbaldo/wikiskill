# Architecture & Design Boundaries

`wikiskill` implements the lifecycle of continuous agent learning as described in Google Research's **WikiSkill (2026)**.

---

## 1. Separation of Responsibilities

```text
┌────────────────────────────────────────────────────────┐
│                   okf-parser                           │
│  - Generic OKF parser, AST, link resolution            │
│  - NetworkX graph generation & Ibis/DuckDB backend     │
│  - Universal schema generation & format validation     │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   wikiskill                            │
│  - Domain semantics: Experience, Wiki, Skills          │
│  - Consolidation, proposals, evaluations, rollback     │
│  - Context extraction, lineage & impact inspection     │
│  - High-level CLI (Cyclopts) & MCP server (FastMCP)    │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                  Consumers                             │
│  - wikiskill itself (Primary dogfooding consumer)      │
│  - External agent workflows (e.g. ovigia-dados)        │
└────────────────────────────────────────────────────────┘
```

### Invariants:
1. `wikiskill` **never** reimplements frontmatter parsing, link resolution, graph compilation, or DuckDB translation.
2. `okf-parser` **never** contains WikiSkill-specific types or opinionated agent logic.

---

## 2. The Concept Graph

All concepts are stored as standard OKF Markdown documents in `knowledge/`:

- `knowledge/experiences/`: Raw execution evidence.
- `knowledge/wiki/`: Consolidated domain knowledge.
- `knowledge/skills/`: Active agent procedural skills.
- `knowledge/proposals/`: Pending skill evolution proposals.
- `knowledge/evaluations/`: Test and benchmark results for candidate skills.
- `knowledge/runs/`: Traceability records for loop iterations.

Lineage is expressed directly through standard Markdown links (e.g. `[Wiki Entry](../wiki/patter-abc.md)`), allowing full graph traversal via `okf-parser` without parallel registry databases.

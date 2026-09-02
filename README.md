# WikiSkill

> **Persistent agent learning runtime built on OKF: experience → wiki → skills → evaluation → evolution.**

`wikiskill` is an experimental implementation inspired by Google Research's **"WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution" (2026)**.

It uses [Open Knowledge Format (OKF)](https://github.com/franklinbaldo/okf-parser) and `okf-parser` to represent agent experience, persistent knowledge, skills, evaluations, and their lineage as an auditable, typed knowledge graph.

---

## The Problem

Standard AI agent sessions suffer from catastrophic operational amnesia:
1. **Session A** learns a non-trivial workaround or discovers an undocumented tool constraint.
2. **Session A** terminates.
3. **Session B** starts from scratch and reproduces the exact same mistakes.

Even when naive memory or vector databases exist, they often mix raw traces, unverified hypotheses, and procedural rules into an unstructured pile.

## The WikiSkill Cycle

WikiSkill separates operational memory by lifecycle and stability:

```text
    ┌────────────────────────────────────────┐
    │          Agent Execution Traces        │
    └───────────────────┬────────────────────┘
                        │
                        ▼
    ┌────────────────────────────────────────┐
    │       Experience (Raw Evidence)        │
    └───────────────────┬────────────────────┘
                        │ (Consolidation)
                        ▼
    ┌────────────────────────────────────────┐
    │   WikiEntry (Persistent Knowledge)     │
    └───────────────────┬────────────────────┘
                        │ (Proposal)
                        ▼
    ┌────────────────────────────────────────┐
    │     AgentSkill / SkillProposal         │
    └───────────────────┬────────────────────┘
                        │ (Objective Evaluation)
                        ▼
    ┌────────────────────────────────────────┐
    │       Accept  OR  Asymmetric Rollback   │
    └────────────────────────────────────────┘
```

### Core Concepts (OKF Types)

- **`Experience`**: What actually happened during a specific run (inputs, tool calls, error codes, successes). Episodic evidence.
- **`WikiEntry`**: Distilled, persistent knowledge synthesized across multiple experiences. Describes *what was learned*.
- **`AgentSkill`**: Executable, concise, procedural guide for agents. Describes *how to act*.
- **`SkillProposal`**: Candidate modification or addition to a skill, linked to motivating evidence.
- **`SkillEvaluation`**: Objective benchmark and regression check of a candidate skill against historical cases.
- **`LoopRun`**: Complete traceability trace tying together the context, skills used, experiences gathered, and decisions made.

### Asymmetric Rollback

> **Skill state is reversible; knowledge is cumulative.**

When a candidate skill fails an evaluation:
1. The skill proposal is **rejected/rolled back**.
2. The `Experience`, `WikiEntry` (explaining why it failed), and `SkillEvaluation` are **retained forever**.
3. The system starts the next session smarter, knowing what failed and why.

---

## Architecture & Boundary

`wikiskill` relies strictly on `okf-parser` for structural primitives:

```text
okf-parser (Generic Infrastructure)
  ├── Markdown parsing & frontmatter validation
  ├── Concept identity & Link graph traversal
  ├── Ibis / DuckDB / NetworkX integration
  └── Schema compilation (Pydantic / SQL)

wikiskill (Agent Learning Semantics)
  ├── Experience recording & Trace ingestion
  ├── Wiki knowledge consolidation
  ├── Skill synthesis & versioning
  ├── Evaluation harness & Asymmetric rollback
  └── FastMCP runtime & CLI
```

---

## Installation & Setup

```bash
# Clone the repository
git clone https://github.com/franklinbaldo/wikiskill.git
cd wikiskill

# Install dependencies and sync environment
uv sync
```

---

## Progressive Dogfooding

This repository dogfoods its own runtime: the development of `wikiskill` is tracked, evaluated, and evolved using its own internal `knowledge/` bundle.

See [`docs/architecture.md`](docs/architecture.md) and [`docs/dogfooding.md`](docs/dogfooding.md).

---

## License

MIT © Franklin Silveira Baldo

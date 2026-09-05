# WikiSkill

> **Contract-guided agent execution and persistent learning on OKF.**

`wikiskill` is an experimental agent runtime inspired by Google Research's **"WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution" (2026)**.

It uses [Open Knowledge Format (OKF)](https://github.com/franklinbaldo/okf-parser) and `okf-parser` to represent both **live execution state** and **persistent learning** as an auditable typed knowledge graph.

## What WikiSkill does

Most agent systems have two separate problems:

1. sessions start from prompts with weak structural guidance about what a good execution must establish;
2. whatever the agent learns during the session is easily lost or mixed into unstructured memory.

WikiSkill addresses both.

A run begins from a typed `RunSpec`, is scaffolded as an intentionally incomplete `LoopRun`, and is progressively filled with readings, goals, decisions, evidence, checks and an outcome. `okf-parser` validation is used throughout the session as operational feedback.

After execution, that evidence feeds the persistent learning cycle.

```text
RunSpec
  -> LoopRun scaffold
  -> RunReading / RunGoal / RunDecision / RunEvidence / RunCheck
  -> RunOutcome
  -> Experience
  -> WikiEntry
  -> AgentSkill / SkillProposal
  -> SkillEvaluation
  -> evolved skill and/or RunSpec
```

## Contract-guided execution

The run artifact is not a report written at the end. It exists before substantive work begins.

A typical session follows:

```text
create scaffold
-> validate with okf-parser
-> inspect missing/unsatisfied requirements
-> perform the next useful action
-> record typed state and evidence
-> validate again
-> leave a coherent outcome and handoff
```

This makes the run simultaneously a plan, typed checklist, state machine, evidence ledger, memory boundary and handoff.

### Core execution concepts

- **`RunSpec`** — operational contract for a class of runs.
- **`LoopRun`** — live execution instance governed by a RunSpec.
- **`RunReading`** — source/artifact read plus the finding derived from it.
- **`RunGoal`** — intended advancement with rationale and observable `success_signal`.
- **`RunDecision`** — consequential choice and rationale.
- **`RunEvidence`** — typed evidence such as tests, CI, runtime observation, diff, source, PR, review or benchmark.
- **`RunCheck`** — explicit verification procedure and result.
- **`RunOutcome`** — coherent state reached by this round and its natural continuation.

Consumers specialize `RunSpec` rather than forcing domain rules into WikiSkill core. Software development, journalism, legal analysis, research and other workflows can define different required readings, goals, evidence and completion states while sharing the same runtime.

## Persistent learning

Execution evidence feeds WikiSkill's original learning lifecycle:

- **`Experience`** — episodic evidence distilled from runs.
- **`WikiEntry`** — durable knowledge synthesized across experiences.
- **`AgentSkill`** — reusable procedural guidance.
- **`SkillProposal`** — candidate evolution of a skill or execution contract.
- **`SkillEvaluation`** — benchmark/regression evidence for a proposal.

### Asymmetric rollback

**Procedural state is reversible; evidence and knowledge are cumulative.**

When an evolved skill or RunSpec performs badly, the candidate can be rejected or rolled back while its `Experience`, `WikiEntry`, evaluation evidence and run history remain available to future sessions.

## Architecture boundary

```text
okf-parser
  ├── Markdown/frontmatter parsing
  ├── concept identity and graph traversal
  ├── Ibis / DuckDB / NetworkX integration
  └── schema compilation and validation

wikiskill
  ├── RunSpec + live execution semantics
  ├── run scaffolding/state/evidence semantics
  ├── experience and knowledge consolidation
  ├── skill/spec evolution and evaluation
  └── CLI + FastMCP runtime
```

WikiSkill does not duplicate generic parsing or validation machinery from `okf-parser`.

## Runtime today and direction

The current runtime can inspect bundle inventory and retrieve task-relevant `RunSpec`, skills, wiki knowledge and recent experiences.

The next runtime surface is:

```text
wikiskill start <task>
wikiskill check <run>
```

with equivalent FastMCP tools. `start` will create the intentionally incomplete live scaffold; `check` will expose unsatisfied contract requirements through `okf-parser`.

See [RFC 0002](docs/rfc/0002-contract-guided-execution-runtime.md).

## Progressive dogfooding

WikiSkill develops itself through the same protocol. The repository includes an experimental development RunSpec in `knowledge/run-specs/wikiskill-development.md`.

See [docs/architecture.md](docs/architecture.md) and [docs/dogfooding.md](docs/dogfooding.md).

## Installation

```bash
git clone https://github.com/franklinbaldo/wikiskill.git
cd wikiskill
uv sync
```

## License

MIT © Franklin Silveira Baldo

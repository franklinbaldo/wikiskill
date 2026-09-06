# WikiSkill

> **Contract-guided agent execution and persistent learning on OKF.**

`wikiskill` is an experimental agent runtime inspired by Google Research's **"WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution" (2026)**.

It uses [Open Knowledge Format (OKF)](https://github.com/franklinbaldo/okf-parser) to represent both live execution state and persistent learning as an auditable typed knowledge graph.

## Consumer quickstart

WikiSkill is intended to be adopted by an existing repository, not reconstructed from a long prompt.

After installing the tool, the normal path is:

```bash
cd my-repository
wikiskill init .
wikiskill session start-next "Do the best useful work available in this repository"
```

`init` creates a managed `.wikiskill/` bundle containing compatible normative contracts, the canonical learning roles, and the standard consumer profile. Later CLI commands automatically discover `.wikiskill/knowledge` from the repository root, so the external agent prompt can stay small.

Managed runtime files can be refreshed with:

```bash
wikiskill upgrade .
```

Upgrade checks hashes before writing. If a WikiSkill-managed file was edited locally, the command reports a conflict and leaves the installation untouched. Consumer-owned files and runtime knowledge are never overwritten by managed upgrade.

See [RFC 0005](docs/rfc/0005-consumer-golden-path.md).

## What WikiSkill does

Agent repositories face two related problems:

1. a session can start from a prompt with weak structural guidance about what good execution must establish;
2. useful lessons from execution are easily lost or mixed into unstructured memory.

WikiSkill addresses both.

A work session starts from a typed `RunSpec`, creates an intentionally incomplete `LoopRun`, and progressively records readings, goals, decisions, evidence, checks, and an outcome. `okf-parser` validation makes missing contract state visible while the work is still happening.

```text
RunSpec
  → LoopRun scaffold
  → RunReading / RunGoal / RunDecision / RunEvidence / RunCheck
  → RunOutcome
  → Experience
```

That episodic evidence feeds a three-role learning cycle:

```text
Skill creates/refines a candidate
              ↓
Experience executes real work and records what happened
              ↓
Wiki synthesizes and compares durable evidence
              ↓
Skill revisits the candidate and decides its lifecycle
              └──────────────→ next Experience
```

The canonical roles are **Experience**, **Wiki**, and **Skill**. Skill evaluation is cross-session lineage, not a mandatory fourth orchestration role. `SkillEvaluation` remains available as an optional explicit benchmark/review artifact when a consumer benefits from materializing one.

See [RFC 0004](docs/rfc/0004-canonical-learning-cycle.md).

## Standard profile

`wikiskill init` installs an opinionated but replaceable standard profile.

- **Experience** is ordinary useful work and is the on-demand fallback for an explicit `session start-next` call.
- **Wiki** becomes eligible after three new Experiences and has higher priority than ordinary Experience.
- **Skill** becomes eligible after six new Experiences. Wiki has higher priority, so if both are due, synthesis runs first and Skill can act on fresh knowledge on the following invocation.

The resulting default rhythm is roughly:

```text
Experience × 3 → Wiki
Experience × 3 → Wiki → Skill
repeat
```

Those thresholds are product defaults, not universal laws. A consumer can specialize SessionTypes, RunSpecs, context policies, and cadence without redefining the core learning roles.

## Contract-guided execution

The run artifact is not a report written after the work. It exists before substantive execution begins.

A typical session follows:

```text
create scaffold
→ validate with okf-parser
→ inspect the next unsatisfied requirement
→ perform the next useful action
→ record typed state and evidence
→ validate again
→ leave a coherent outcome or handoff
```

### Core execution concepts

- **`RunSpec`** — operational contract for a class of runs.
- **`LoopRun`** — live execution instance governed by a RunSpec.
- **`RunReading`** — source/artifact read plus the finding derived from it.
- **`RunGoal`** — intended advancement with rationale and observable `success_signal`.
- **`RunDecision`** — consequential choice and rationale.
- **`RunEvidence`** — typed evidence such as tests, CI, runtime observation, diff, source, PR, review, or benchmark.
- **`RunCheck`** — explicit verification procedure and result.
- **`RunOutcome`** — coherent state reached by this round and its natural continuation.
- **`Handoff`** — explicit continuation state for later sessions.

Consumers specialize `RunSpec` rather than forcing domain rules into WikiSkill core. Software development, journalism, legal work, research, and other domains can require different readings, evidence, checks, and result states while sharing the same runtime.

## Persistent learning concepts

- **`Experience`** — episodic evidence distilled from real execution.
- **`WikiEntry`** — durable knowledge synthesized across experiences.
- **`AgentSkill`** — reusable procedural guidance; active and experimental versions may coexist.
- **`SkillProposal`** — explicit change record/rationale for procedural evolution.
- **`SkillEvaluation`** — optional explicit benchmark or review record.

### Candidate lifecycle

A proposed replacement does not immediately erase its incumbent. The normal experiment is:

```text
active AgentSkill + experimental AgentSkill
          ↓
Experience records skill_used + skill_version
          ↓
Wiki preserves the comparison across episodes
          ↓
Skill refines / continues experiment / promotes / rejects
```

This prevents the session that invents a procedure from being the sole judge of whether that procedure works.

### Asymmetric rollback

**Procedural state is reversible; evidence and durable knowledge are cumulative.**

When an evolved skill performs badly, the candidate can be rejected or rolled back while its execution evidence and the lessons learned from failure remain available to future sessions.

## Consumer specialization

WikiSkill-managed files live under `.wikiskill/` and are tracked in `.wikiskill/manifest.json`. Consumers should keep their own specializations separate from those managed paths.

A domain repository can, for example, define:

```yaml
type: SessionType
id: session-types/my-domain-experience
extends: session-types/standard-experience
run_spec: run-specs/my-domain-experience
```

The local RunSpec can then add domain-specific checks and readings. The repository does not need to redefine the meaning of Experience itself.

Responsibility stays intentionally split:

- WikiSkill supplies learning architecture, compatible contracts, bootstrap, upgrade, and recommended defaults;
- the consumer supplies domain objectives, tools, checks, institutional/access policy, and merge/publication/deployment rules.

## CLI

Important entry points include:

```text
wikiskill init [repository]
wikiskill upgrade [repository]
wikiskill context <task>
wikiskill session next
wikiskill session start-next <task>
wikiskill start <task> [--session-type ...]
wikiskill check <run>
wikiskill run reading|goal|decision|evidence|check|outcome ...
wikiskill experience preview|record ...
wikiskill handoff list|create|continue ...
wikiskill serve
```

`session next` reports automatically due work. `session start-next` is an explicit request to work, so the standard profile can fall back to Experience when neither Wiki nor Skill is due.

## Architecture boundary

```text
okf-parser
  ├── Markdown/frontmatter parsing
  ├── concept identity and graph traversal
  ├── Ibis / DuckDB / NetworkX integration
  └── schema compilation and validation

wikiskill
  ├── RunSpec + live execution semantics
  ├── SessionType + policy/cadence composition
  ├── experience and knowledge consolidation
  ├── skill evolution lifecycle
  ├── consumer bootstrap + upgrade
  └── CLI + FastMCP runtime
```

WikiSkill does not duplicate generic parsing or validation machinery from `okf-parser`.

## Development and dogfooding

WikiSkill develops itself through the same runtime. The repository's own `knowledge/` tree is a dogfood consumer with additional development-specific SessionTypes and policies.

The canonical Experience/Wiki/Skill roles are deliberately policy-neutral so other repositories do not inherit WikiSkill's software-development assumptions.

See [docs/architecture.md](docs/architecture.md) and [docs/dogfooding.md](docs/dogfooding.md).

## Installation for development

```bash
git clone https://github.com/franklinbaldo/wikiskill.git
cd wikiskill
uv sync
uv run wikiskill info
```

## License

MIT © Franklin Baldo

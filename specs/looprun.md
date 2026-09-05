---
type: ConceptSpecification
concept_type: LoopRun
description: "Live execution instance scaffolded from a RunSpec and progressively satisfied through typed evidence and checks."
---

# Concept: LoopRun

A `LoopRun` is the live state of one agent execution round.

It exists before substantive work begins, starts intentionally incomplete, and accumulates typed readings, goals, decisions, evidence, checks and an outcome as the session progresses.

The applicable `RunSpec` defines what a well-formed run of this class requires. Repeated `okf-parser` validation provides operational feedback about missing or inconsistent state.

## Required Frontmatter Fields

- `type`: `"LoopRun"`
- `id`: Run identifier
- `title`: Short summary of the run
- `timestamp`: ISO-8601 start timestamp
- `status`: `"scaffold"`, `"in_progress"`, or `"closed"`
- `run_spec`: Link to the governing `RunSpec`
- `task`: Task or session intent

## Progressive Frontmatter Fields

These fields are expected to be populated as the run advances according to its `RunSpec`:

- `readings`: Links to `RunReading`
- `goals`: Links to `RunGoal`
- `decisions`: Links to `RunDecision`
- `evidence`: Links to `RunEvidence`
- `checks`: Links to `RunCheck`
- `outcome`: Link to `RunOutcome`
- `skills_consulted`: Links to `AgentSkill`
- `experiences_recorded`: Links to `Experience`
- `proposals_generated`: Links to `SkillProposal`

## Operational semantics

A new run should be created from a scaffold before meaningful execution work. It is normal for that scaffold to fail completion validation initially.

The agent then cycles through:

```text
validate live run
-> inspect unsatisfied requirements
-> perform the next useful action
-> record typed state/evidence
-> validate again
```

The final run is both an auditable record of what happened and a structured handoff describing the state reached and the next natural move.

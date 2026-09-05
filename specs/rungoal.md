---
type: ConceptSpecification
concept_type: RunGoal
description: "An intended advancement for a live run with rationale and an observable success signal."
---

# Concept: RunGoal

A `RunGoal` states what the run intends to advance and how the agent will recognize meaningful progress.

## Required Frontmatter Fields

- `type`: `"RunGoal"`
- `id`: Goal identifier
- `run`: Link to the `LoopRun`
- `kind`: Goal category defined by the applicable `RunSpec`
- `goal`: Concise desired advancement
- `rationale`: Why this goal is worth advancing now
- `success_signal`: Observable evidence or state that demonstrates progress
- `status`: `"planned"`, `"active"`, `"advanced"`, `"achieved"`, or `"carried_forward"`

## Semantics

Goals should describe product or task progress rather than agent activity. `success_signal` makes the goal testable against evidence accumulated by the run.

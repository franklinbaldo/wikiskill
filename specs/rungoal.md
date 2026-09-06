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

A LoopRun cannot close while one of its goals remains `planned`, `active`, or `advanced`. Every run-owned goal must reach one of two terminal states:

- `achieved`: the run itself resolved the intent;
- `carried_forward`: the intent remains material and is explicitly transferred to a Handoff created by the same run.

A carried-forward goal must be listed in that Handoff's `goals` field. This makes closing a run mean that no intent it assumed was left without a destination.

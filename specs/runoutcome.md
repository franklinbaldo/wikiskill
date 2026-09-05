---
type: ConceptSpecification
concept_type: RunOutcome
description: "The coherent state reached at the end of the current run and its natural continuation."
---

# Concept: RunOutcome

A `RunOutcome` closes the current execution round without requiring that the larger task or feature be finished.

## Required Frontmatter Fields

- `type`: `"RunOutcome"`
- `id`: Outcome identifier
- `run`: Link to the `LoopRun`
- `result_state`: State reached by this run
- `summary`: What materially changed
- `next_move`: Natural continuation available to a future run

## Optional Frontmatter Fields

- `goals_advanced`: Links to `RunGoal`
- `evidence`: Links to decisive `RunEvidence`
- `checks`: Links to final `RunCheck`
- `experiences_recorded`: Links to `Experience` distilled from this run

## Semantics

A coherent outcome is a handoff boundary. It may be RED, GREEN, review-ready, merged, blocked, published, investigated, or any domain-specific state allowed by the applicable `RunSpec`.

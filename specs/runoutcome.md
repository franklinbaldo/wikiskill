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
- `result_state`: Domain state reached by this run
- `work_status`: Whether the material work owned by this run is `complete` or `partial`
- `summary`: What materially changed
- `next_move`: Natural continuation available to a future run

## Optional Frontmatter Fields

- `goals_advanced`: Links to `RunGoal`
- `evidence`: Links to decisive `RunEvidence`
- `checks`: Links to final `RunCheck`
- `experiences_recorded`: Links to `Experience` distilled from this run

## Semantics

`result_state` remains domain-specific: RED, GREEN, review-ready, merged, blocked, published, investigated, or another state allowed by the applicable `RunSpec`.

`work_status` answers a separate operational question. `complete` means the work intentionally owned by this round has been closed. `partial` means material work remains and must be represented by an active `Handoff` so that a later `LoopRun` can resume it explicitly.

---
type: ConceptSpecification
concept_type: Handoff
description: "Resumable unfinished work transferred from one LoopRun to a future LoopRun."
---

# Concept: Handoff

A `Handoff` represents material work intentionally transferred between agent sessions.

## Required frontmatter

- `type`: `Handoff`
- `id`: stable identifier
- `title`: concise description of the unfinished work
- `created_at`: ISO-8601 timestamp
- `status`: `active` or `archived`
- `created_by_run`: LoopRun that emitted the handoff
- `state`: concrete state in which the work was left
- `next_action`: natural resumption point
- `references`: relevant PRs, issues, files, concepts, evidence or other identifiers

## Goal accountability

- `goals`: RunGoals from `created_by_run` whose unfinished intent this Handoff carries forward.

A LoopRun may close only after every owned RunGoal reaches a terminal state. `achieved` means the run resolved that intent itself. `carried_forward` means responsibility moved to a Handoff, and the corresponding RunGoal must therefore appear in the Handoff's `goals` list. The Handoff continues to satisfy that historical provenance after it is archived by a later run.

## Optional routing

- `target_session_type`: SessionType that is the natural continuation owner. A compatible cadence policy may treat this active Handoff as an eligibility trigger.

## Archived handoffs

When a later session continues the work, the handoff is archived and records:

- `continued_by_run`: LoopRun that resumed it
- `archived_at`: ISO-8601 timestamp
- `resolution`: what the continuing session did with the handoff

Archiving is semantic rather than destructive: the document remains queryable as provenance between sessions.

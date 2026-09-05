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

## Archived handoffs

When a later session continues the work, the handoff is archived and records:

- `continued_by_run`: LoopRun that resumed it
- `archived_at`: ISO-8601 timestamp
- `resolution`: what the continuing session did with the handoff

Archiving is semantic rather than destructive: the document remains queryable as provenance between sessions.

---
type: ConceptSpecification
concept_type: LoopRun
description: "Traceability record linking context, experiences, wiki updates, and skill evolution."
---

# Concept: LoopRun

A `LoopRun` is an execution trace representing a complete iteration of the continuous learning loop.

## Required Frontmatter Fields

- `type`: Must be `"LoopRun"`
- `id`: Run identifier (e.g. `run-2026-09-02-01`)
- `title`: Short summary of the loop iteration
- `timestamp`: ISO-8601 timestamp
- `status`: Run status (`"completed"`, `"failed"`, `"in_progress"`)

## Optional Frontmatter Fields

- `task`: Task or session goal
- `skills_consulted`: List of links to `AgentSkill`
- `experiences_recorded`: List of links to `Experience`
- `proposals_generated`: List of links to `SkillProposal`

## Content Structure

The body details the sequence of events, outcomes, and state transitions during the run.

---
type: ConceptSpecification
concept_type: AgentSkill
description: "Actionable, procedural guidance and policies executed by agents."
---

# Concept: AgentSkill

An `AgentSkill` is a concise, procedural rulebook. It answers: *given what we learned, how should the agent act?*

## Required Frontmatter Fields

- `type`: Must be `"AgentSkill"`
- `id`: Skill identifier (e.g. `skill-develop-feature`)
- `title`: Human-readable skill name
- `version`: Semver or incremental version string (e.g. `"1.0.0"`)
- `status`: Skill lifecycle state (`"active"`, `"deprecated"`, `"experimental"`)

## Optional Frontmatter Fields

- `derived_from`: Links to `[WikiEntry](../wiki/...)` justifying this procedure
- `tags`: List of domain/tool tags

## Content Structure

The body must be:
- Concise, procedural, step-by-step.
- Free of raw conversation dumps or unverified notes.

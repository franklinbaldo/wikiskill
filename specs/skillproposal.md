---
type: ConceptSpecification
concept_type: SkillProposal
description: "Proposed candidate version or modification for an AgentSkill."
---

# Concept: SkillProposal

A `SkillProposal` represents an explicit proposal to create, modify, or deprecate an `AgentSkill`.

## Required Frontmatter Fields

- `type`: Must be `"SkillProposal"`
- `id`: Proposal identifier (e.g. `prop-2026-09-02-01`)
- `title`: Short title of the proposed change
- `target_skill`: Link or identifier to the target `AgentSkill`
- `status`: Proposal status (`"draft"`, `"evaluating"`, `"accepted"`, `"rejected"`)

## Optional Frontmatter Fields

- `motivation`: Summary of the reason for the proposal
- `based_on`: Links to motivating `[WikiEntry](../wiki/...)` or `[Experience](../experiences/...)`

## Content Structure

The body should present:
1. **Current Procedure vs Proposed Procedure**: Diff or before/after comparison.
2. **Rationale**: Evidence justifying the change.

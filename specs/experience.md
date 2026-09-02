---
type: ConceptSpecification
concept_type: Experience
description: "Raw episodic execution trace or observation recorded by an agent."
---

# Concept: Experience

An `Experience` represents an episodic record of what happened during an execution. It is historical evidence, not a consolidated rule.

## Required Frontmatter Fields

- `type`: Must be `"Experience"`
- `id`: Unique identifier (e.g. `exp-2026-09-02-01`)
- `title`: Short descriptive title of what was attempted
- `timestamp`: ISO-8601 timestamp
- `status`: Execution outcome (`"success"`, `"failure"`, `"partial"`, `"observation"`)

## Optional Frontmatter Fields

- `skill_used`: Link or identifier of the skill executed
- `skill_version`: Version of the skill used
- `task`: High-level goal or task description
- `error_code`: Error identifier if applicable
- `context`: Contextual notes or environment flags

## Content Structure

The body should describe:
1. **Context & Intent**: What the agent wanted to achieve.
2. **Action & Observed Output**: Concrete trace, response, or command output.
3. **Findings**: What was surprising, what broke, or what succeeded.

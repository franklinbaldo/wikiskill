---
type: ConceptSpecification
concept_type: WikiEntry
description: "Persistent, distilled knowledge synthesized across experiences."
---

# Concept: WikiEntry

A `WikiEntry` represents consolidated, durable domain knowledge extracted from one or more `Experience` records. It answers: *what did we learn?*

## Required Frontmatter Fields

- `type`: Must be `"WikiEntry"`
- `id`: Unique identifier (e.g. `wiki-okf-boundary`)
- `title`: Concept or rule name
- `status`: Knowledge status (`"draft"`, `"active"`, `"deprecated"`)

## Optional Frontmatter Fields

- `tags`: List of topical tags
- `evidence`: List of links to supporting `Experience` records

## Content Structure

The body should describe:
1. **Summary**: Concise distillation of the pattern or invariant.
2. **Context & Scope**: Where and when this rule/insight holds true.
3. **Evidence & Lineage**: Links to relevant `[Experience](../experiences/...)` files.

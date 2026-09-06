---
type: ConceptSpecification
concept_type: SessionType
description: "Defines the purpose and inherited operating contract for one class of WikiSkill session."
---

# Concept: SessionType

A `SessionType` describes what kind of execution session is being started. It is intentionally separate from `RunSpec`: the session type selects an execution contract and may also contribute prompt nudges and later policy links.

## Required Frontmatter Fields

- `type`: `"SessionType"`
- `id`: Stable session type identifier
- `title`: Human-readable name
- `purpose`: Concise statement of what the session exists to accomplish
- `run_spec`: Link to the governing `RunSpec`

## Optional Frontmatter Fields

- `extends`: Parent `SessionType`; child configuration refines the parent
- `nudges`: Short instructions inherited and appended through the hierarchy

## Semantics

Inheritance is shallow by design. Scalar child fields override inherited values; `nudges` append in parent-to-child order. Cycles are invalid.

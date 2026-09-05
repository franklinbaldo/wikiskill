---
type: ConceptSpecification
concept_type: RunReading
description: "A source or artifact consulted during a live run, together with the relevant finding derived from it."
---

# Concept: RunReading

A `RunReading` proves that a run consulted a relevant source and records what mattered from that reading.

## Required Frontmatter Fields

- `type`: `"RunReading"`
- `id`: Reading identifier
- `run`: Link to the `LoopRun`
- `kind`: Reading category defined by the applicable `RunSpec`
- `subject`: What was read
- `reference`: Stable path, URL, concept link, issue/PR reference, or other locator
- `finding`: Relevant finding produced by the reading

## Semantics

A reading is stronger than a boolean acknowledgement. It captures both provenance and the useful observation that should influence the run.

---
type: ConceptSpecification
concept_type: RunCheck
description: "A verification performed during a live run, including procedure, result, and supporting evidence."
---

# Concept: RunCheck

A `RunCheck` records an explicit verification of the current run state.

## Required Frontmatter Fields

- `type`: `"RunCheck"`
- `id`: Check identifier
- `run`: Link to the `LoopRun`
- `kind`: Check category defined by the applicable `RunSpec`
- `procedure`: Command, query, review procedure, or other verification method
- `result`: Concise observed result
- `status`: `"pass"`, `"fail"`, or `"inconclusive"`

## Optional Frontmatter Fields

- `evidence`: Link to supporting `RunEvidence`
- `goal`: Link to the `RunGoal` being verified

## Semantics

Checks turn evidence into explicit verification. The generic type is domain-neutral; RunSpecs define which checks matter for a particular class of work.

---
type: ConceptSpecification
concept_type: RunSpec
description: "Typed operational contract that defines how a class of agent runs should progress and what evidence makes them well formed."
---

# Concept: RunSpec

A `RunSpec` defines the operational protocol for a class of agent executions. A run is scaffolded from it before substantive work begins.

## Required Frontmatter Fields

- `type`: `"RunSpec"`
- `id`: Stable spec identifier
- `title`: Human-readable name
- `version`: Version of the operational contract
- `status`: `"active"`, `"experimental"`, or `"deprecated"`
- `required_reading_kinds`: Reading categories expected before the run can be considered informed
- `required_goal_kinds`: Goal categories the run must articulate
- `required_evidence_kinds`: Evidence categories expected for the run class
- `required_check_kinds`: Verification categories expected for the run class

## Optional Frontmatter Fields

- `skill`: Link to the `AgentSkill` this spec operationalizes
- `parent_spec`: Link to a more general `RunSpec`
- `allowed_entry_states`: Domain-specific entry states
- `allowed_result_states`: Domain-specific result states
- `completion_notes`: Additional semantic completion guidance

## Semantics

A `RunSpec` is not a prompt template. It is a typed contract whose unsatisfied requirements provide operational feedback during a live `LoopRun`.

Consumers may define specialized specs while reusing WikiSkill's generic run component types.

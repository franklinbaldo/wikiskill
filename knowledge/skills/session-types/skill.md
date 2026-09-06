---
type: SessionType
id: session-types/skill
title: Skill
purpose: "Change future procedural behavior using durable knowledge and supporting execution evidence."
run_spec: run-specs/skill
extends: session-types/base
context_policy: context-policies/skill-evolver
access_policy: access-policies/development
nudges:
  - "Create or revise a candidate only when accumulated knowledge supports a procedural intervention."
  - "Keep an incumbent available while an experimental candidate is gathering evidence; creating a candidate is not promotion."
  - "Use later Wiki synthesis to decide whether to refine, continue experimenting, promote, reject, deprecate, or replace a candidate."
  - "Preserve lineage from the decision back to WikiEntry and Experience evidence."
---

# Skill session

Canonical procedural-evolution role in the WikiSkill learning cycle. Scheduling belongs to the consumer specialization, not the abstract role.

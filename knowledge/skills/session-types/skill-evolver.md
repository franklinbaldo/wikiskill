---
type: SessionType
id: session-types/skill-evolver
title: Skill evolver / proposer
purpose: "Turn accumulated WikiEntry knowledge and supporting experiences into evidence-backed skill proposals and later lifecycle decisions."
run_spec: run-specs/skill-evolution
extends: session-types/skill
context_policy: context-policies/skill-evolver
access_policy: access-policies/development
cadence_policy: cadence-policies/skill-evolver
nudges:
  - "Propose changes only when the accumulated knowledge supports a procedural improvement."
  - "Link the proposal to the WikiEntry and experiences that justify it."
  - "Do not promote an isolated observation directly into global procedure."
---

# Skill evolver session

Backward-compatible proposer-oriented specialization of the canonical Skill role. A later Skill session may also refine, promote, or reject candidates after Wiki synthesis accumulates.

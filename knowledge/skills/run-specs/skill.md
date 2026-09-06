---
type: RunSpec
id: run-specs/skill
title: Skill evolution run
version: "1.0.0"
status: experimental
required_reading_kinds:
  - wiki
  - experiences
  - active-skills
  - active-handoffs
required_goal_kinds:
  - evolve-skill
required_evidence_kinds:
  - intervention
required_check_kinds:
  - lineage
allowed_result_states:
  - proposed
  - refined
  - promoted
  - rejected
  - no-change
  - partial
  - blocked
completion_notes: "Make a justified procedural intervention or lifecycle decision, preserving lineage to the WikiEntry and Experience evidence that supports it."
---

# Skill RunSpec

The canonical procedural-evolution contract. `lineage` asks whether the intervention or lifecycle action is supported by durable knowledge and traceable execution evidence. Creating a candidate does not satisfy promotion; promotion is a later possible result after evidence accumulates.

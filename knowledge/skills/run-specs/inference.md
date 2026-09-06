---
type: RunSpec
id: run-specs/inference
title: Inference execution run
version: "1.0.0"
status: experimental
required_reading_kinds:
  - active-handoffs
  - active-skills
required_goal_kinds:
  - task-advance
required_evidence_kinds:
  - execution
required_check_kinds:
  - verification
allowed_result_states:
  - success
  - partial
  - blocked
completion_notes: "Execute useful work and leave episodic evidence; partial work emits a Handoff."
---

# Inference RunSpec

Minimal execution contract for work-oriented sessions.

---
type: RunSpec
id: run-specs/experience
title: Experience run
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
  - no-useful-change
completion_notes: "Do useful work when available, verify the observed result, and preserve truthful episodic evidence including the skill/version actually used."
---

# Experience RunSpec

The canonical execution contract. `verification` asks whether the claimed observed effect is supported by the execution evidence. It does not decide whether a skill should be promoted globally.

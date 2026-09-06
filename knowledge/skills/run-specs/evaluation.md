---
type: RunSpec
id: run-specs/evaluation
title: Skill and change evaluation run
version: "1.0.0"
status: experimental
required_reading_kinds:
  - proposal
  - prior-evaluations
  - active-handoffs
required_goal_kinds:
  - evaluate-change
required_evidence_kinds:
  - evaluation
required_check_kinds:
  - tests
allowed_result_states:
  - accepted
  - rejected
  - revision
  - partial
  - blocked
completion_notes: "Evaluate the candidate with executed evidence and preserve failures as learning even when state is rolled back."
---

# Evaluation RunSpec

Contract for reviewer/evaluator sessions.

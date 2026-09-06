---
type: SessionType
id: session-types/evaluator
title: Evaluator / reviewer
purpose: "Determine whether a proposed skill or repository change is actually beneficial and safe to accept."
run_spec: run-specs/evaluation
extends: session-types/base
context_policy: context-policies/evaluator
access_policy: access-policies/development
cadence_policy: cadence-policies/evaluator
nudges:
  - "Prefer executed checks and comparative evidence over confidence in the proposal narrative."
  - "Preserve failed evaluations as durable evidence; rollback skill state without erasing what was learned."
---

# Evaluator session

Evaluation-oriented session for acceptance, revision, rejection, or rollback decisions.

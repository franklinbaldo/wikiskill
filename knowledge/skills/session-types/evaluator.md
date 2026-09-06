---
type: SessionType
id: session-types/evaluator
title: Evaluator / reviewer
purpose: "Run an explicit review or benchmark when a consumer needs one; this is not a fourth canonical learning role."
run_spec: run-specs/evaluation
extends: session-types/base
context_policy: context-policies/evaluator
access_policy: access-policies/development
cadence_policy: cadence-policies/evaluator
nudges:
  - "Prefer executed checks and comparative evidence over confidence in the proposal narrative."
  - "Treat this session as an optional specialized review surface, not as the owner of skill evolution."
  - "Preserve failed evaluations as durable evidence; rollback skill state without erasing what was learned."
---

# Evaluator session

Optional consumer/reviewer specialization. Canonical skill learning proceeds through Experience → Wiki → Skill; consumers may still schedule a dedicated evaluator when their workflow benefits from explicit benchmark or review work.

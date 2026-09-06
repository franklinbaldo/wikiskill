---
type: CadencePolicy
id: cadence-policies/evaluator
title: Evaluator cadence
on_demand: true
event_triggers:
  - active-handoff
cooldown_seconds: 0
priority: 90
max_parallel: 2
max_runs_per_hour: 6
handoff_compatible: true
---

# Evaluator cadence

Evaluation starts on demand or when review/evaluation work is explicitly handed off.

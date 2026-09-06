---
type: CadencePolicy
id: cadence-policies/inference
title: Inference cadence
on_demand: true
event_triggers:
  - active-handoff
cooldown_seconds: 0
priority: 100
max_parallel: 3
max_runs_per_hour: 12
handoff_compatible: true
---

# Inference cadence

Inference normally starts on demand or when unfinished execution work is explicitly handed to it.

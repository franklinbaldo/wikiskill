---
type: CadencePolicy
id: cadence-policies/development
title: Development cadence
on_demand: true
event_triggers:
  - active-handoff
cooldown_seconds: 0
priority: 80
max_parallel: 4
max_runs_per_hour: 12
handoff_compatible: true
---

# Development cadence

Development is normally explicitly requested; targeted unfinished repository work may also activate it.

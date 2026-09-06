---
type: CadencePolicy
id: cadence-policies/skill-evolver
title: Skill evolver cadence
on_demand: true
event_triggers:
  - active-handoff
cooldown_seconds: 21600
max_delay_seconds: 604800
priority: 50
max_parallel: 1
max_runs_per_hour: 1
handoff_compatible: true
---

# Skill evolver cadence

Skill evolution is normally deliberate, but a targeted Handoff can activate it and the max delay prevents indefinite neglect.

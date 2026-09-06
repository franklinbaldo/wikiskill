---
type: CadencePolicy
id: cadence-policies/wiki-maintainer
title: Wiki maintainer cadence
on_demand: true
event_triggers:
  - active-handoff
threshold_metric: experiences-since-last-run
threshold_gte: 3
cooldown_seconds: 3600
max_delay_seconds: 86400
priority: 70
max_parallel: 1
max_runs_per_hour: 1
handoff_compatible: true
---

# Wiki maintainer cadence

Consolidate when enough new experience accumulates, while guaranteeing the wiki is revisited at least daily.

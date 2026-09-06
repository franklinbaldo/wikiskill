---
type: ConceptSpecification
concept_type: CadencePolicy
description: "Declares when a SessionType becomes eligible to start and the execution limits used to rank candidates."
---

# Concept: CadencePolicy

`CadencePolicy` models session eligibility rather than reducing orchestration to cron.

## Required Frontmatter Fields

- `type`: `"CadencePolicy"`
- `id`: Stable identifier
- `title`: Human-readable name

## Optional Frontmatter Fields

- `on_demand`: Session may always be selected explicitly
- `event_triggers`: Named events that make the session eligible
- `interval_seconds`: Regular interval trigger
- `threshold_metric`: Named runtime metric
- `threshold_gte`: Minimum metric value for eligibility
- `cooldown_seconds`: Minimum time after a prior run before automatic re-entry
- `max_delay_seconds`: Maximum tolerated time without a run; exceeding it makes the session eligible
- `priority`: Higher values rank first among eligible sessions
- `max_parallel`: Maximum simultaneous active runs of this type
- `max_runs_per_hour`: Rolling run budget
- `handoff_compatible`: Whether a targeted active Handoff may activate this type

Eligibility is inspectable: the runtime reports triggering reasons and blocking controls separately.

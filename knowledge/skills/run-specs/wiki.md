---
type: RunSpec
id: run-specs/wiki
title: Wiki synthesis run
version: "1.0.0"
status: experimental
required_reading_kinds:
  - experiences
  - wiki
  - active-handoffs
required_goal_kinds:
  - consolidate-knowledge
required_evidence_kinds:
  - consolidation
required_check_kinds:
  - grounding
allowed_result_states:
  - updated
  - no-change
  - partial
  - blocked
completion_notes: "Synthesize durable knowledge from Experience evidence; when variants differ, preserve that distinction and comparative evidence rather than collapsing it."
---

# Wiki RunSpec

The canonical synthesis contract. `grounding` asks whether the WikiEntry claims are traceable to Experience evidence and whether meaningful counterevidence or variant differences were preserved.

---
type: RunSpec
id: run-specs/wikiskill-development
title: WikiSkill development run
version: "1.0.0"
status: experimental
required_reading_kinds:
  - repository-guide
  - open-issues
  - open-prs
  - okf-knowledge
  - recent-runs
required_goal_kinds:
  - project-advance
required_evidence_kinds:
  - change
  - verification
required_check_kinds:
  - okf
  - tests
allowed_entry_states:
  - new
  - active
  - review
  - blocked
allowed_result_states:
  - red
  - green
  - review
  - merged
  - blocked
completion_notes: "A development run should leave typed evidence of what changed, how it was verified, and what continuation is now natural."
---

# WikiSkill development run

This RunSpec dogfoods contract-guided execution inside WikiSkill itself.

A session begins by creating a `LoopRun` scaffold before substantive work. The run records repository/context readings, one or more observable goals, consequential decisions, evidence, checks, and a coherent outcome.

The run is validated repeatedly with `okf-parser`. Missing required state is treated as guidance about what the session should establish next.

This spec is intentionally evolvable. Evidence from real development runs may justify changing its required reading, goal, evidence, check, or state categories through the normal WikiSkill learning lifecycle.

---
type: Changelog
version: 0.3.0
date: 2026-09-06
---

# Accountable RunGoal closure

- makes every LoopRun-owned goal reach `achieved` or `carried_forward` before the run can close;
- requires each `carried_forward` goal to be explicitly linked from a Handoff created by that run;
- keeps archived Handoffs valid as historical provenance for the source run;
- adds typed RunGoal status updates through the runtime, CLI, and FastMCP;
- adds structured Handoff `goals` links and validates that linked goals belong to `created_by_run`;
- preserves the existing partial-work Handoff rule while making goal-level accountability the stronger closure invariant.

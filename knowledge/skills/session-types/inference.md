---
type: SessionType
id: session-types/inference
title: Inference / work execution
purpose: "Execute real work using active skills and produce episodic evidence of what happened."
run_spec: run-specs/inference
extends: session-types/experience
context_policy: context-policies/inference
access_policy: access-policies/development
cadence_policy: cadence-policies/inference
nudges:
  - "Use active skills as operating procedure and focus on the task in front of the session."
  - "Record reusable execution evidence as Experience rather than silently carrying it to the next session."
---

# Inference session

Backward-compatible paper-oriented name for an Experience session. New consumers should normally extend `session-types/experience` directly.

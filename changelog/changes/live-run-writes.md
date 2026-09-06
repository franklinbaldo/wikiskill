---
type: Changelog
version: 0.2.10
date: 2026-09-06
---

# Typed live-run writes

- adds runtime methods for `RunReading`, `RunGoal`, `RunDecision`, `RunEvidence`, `RunCheck`, and `RunOutcome`;
- derives stable component identities from the owning LoopRun and an explicit component identifier;
- attaches each component to the LoopRun while transitioning `scaffold -> in_progress -> closed`;
- validates the normative OKF bundle after each multi-file write and restores the prior run state on failure;
- prevents an outcome from closing a run while required pre-outcome contract state remains unsatisfied;
- rejects writes to closed runs and makes component collisions explicit.

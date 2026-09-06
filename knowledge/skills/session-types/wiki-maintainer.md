---
type: SessionType
id: session-types/wiki-maintainer
title: Wiki maintainer
purpose: "Consolidate episodic execution evidence into durable WikiEntry knowledge."
run_spec: run-specs/wiki-maintenance
extends: session-types/wiki
context_policy: context-policies/wiki-maintainer
access_policy: access-policies/development
cadence_policy: cadence-policies/wiki-maintainer
nudges:
  - "Prefer updating an existing WikiEntry when new evidence supports the same lesson."
  - "Create a new WikiEntry when the lesson is materially distinct, not merely phrased differently."
  - "When useful, write the entry in pattern form: observable signals, context, supported cause or mechanism, evidence, successful strategy, and limits or counterexamples."
  - "Pattern is a writing nudge, not a separate ontology type."
---

# Wiki maintainer session

Backward-compatible maintenance-oriented specialization of the canonical Wiki role. It consolidates Experience into persistent knowledge while preserving provenance and avoiding duplicate entries.

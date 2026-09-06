---
type: SessionType
id: session-types/wiki-maintainer
title: Wiki maintainer
purpose: "Consolidate episodic execution evidence into durable WikiEntry knowledge."
run_spec: run-specs/wiki-maintenance
extends: session-types/base
context_policy: context-policies/wiki-maintainer
access_policy: access-policies/development
nudges:
  - "Prefer updating an existing WikiEntry when new evidence supports the same lesson."
  - "Create a new WikiEntry when the lesson is materially distinct, not merely phrased differently."
  - "When useful, write the entry in pattern form: observable signals, context, supported cause or mechanism, evidence, successful strategy, and limits or counterexamples."
  - "Pattern is a writing nudge, not a separate ontology type."
---

# Wiki maintainer session

Consolidates Experience into persistent knowledge while preserving provenance and avoiding duplicate entries.

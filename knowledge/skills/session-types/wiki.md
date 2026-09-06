---
type: SessionType
id: session-types/wiki
title: Wiki
purpose: "Synthesize episodic evidence into durable knowledge, including comparison across skill variants when relevant."
run_spec: run-specs/wiki
extends: session-types/base
context_policy: context-policies/wiki-maintainer
access_policy: access-policies/development
nudges:
  - "Ground durable knowledge in Experience records rather than intuition or one-off narrative."
  - "When incumbent and candidate skills were both exercised, keep their evidence distinguishable and synthesize the comparison explicitly."
  - "Describe scope, strengths, regressions, trade-offs, failure modes, and counterevidence when the experiences support them."
  - "Do not promote or reject a skill; produce knowledge that a later Skill session can act on."
---

# Wiki session

Canonical synthesis role in the WikiSkill learning cycle. Consumers decide when this role should run by supplying cadence in a specialization.

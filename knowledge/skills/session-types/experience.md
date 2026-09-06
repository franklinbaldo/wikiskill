---
type: SessionType
id: session-types/experience
title: Experience
purpose: "Execute real work under available skills and record truthful episodic evidence of what happened."
run_spec: run-specs/experience
extends: session-types/base
context_policy: context-policies/inference
access_policy: access-policies/development
nudges:
  - "Do useful external work; the session exists to generate experience, not to judge a skill globally."
  - "Record which AgentSkill and version actually guided the execution so incumbent and experimental candidates remain distinguishable."
  - "Treat one successful or failed execution as evidence, not as automatic promotion or rejection of a skill."
---

# Experience session

Canonical execution role in the WikiSkill learning cycle. Consumer work sessions normally specialize this role and define their own cadence when scheduled execution is desired.

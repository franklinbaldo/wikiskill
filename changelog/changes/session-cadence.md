---
type: Changelog
version: 0.2.8
date: 2026-09-05
---

# Declarative session cadence

- adds typed `CadencePolicy` with on-demand, event, interval, threshold, cooldown, max-delay, priority, concurrency, and hourly-budget controls;
- makes eligibility inspectable as activating reasons plus blocking controls;
- adds deterministic `eligible_sessions` and `next_session` selection;
- lets active Handoffs target a compatible SessionType and activate it;
- adds built-in cadence policies for inference, wiki maintenance, skill evolution, evaluation, and development;
- exposes eligibility and next-session selection through MCP.

---
type: Changelog
version: 0.2.5
date: 2026-09-05
---

# SessionType runtime

- adds typed `SessionType` concepts with deterministic inheritance;
- binds every newly started `LoopRun` to its effective session type;
- lets session types select a default `RunSpec` and contribute inherited prompt nudges;
- exposes explicit session selection through CLI and MCP;
- preserves `development` as the default session type for existing repository workflows.

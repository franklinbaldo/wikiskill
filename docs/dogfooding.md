# Progressive Dogfooding Protocol

`wikiskill` adheres to an avid self-application rule: **the development of this library is guided, recorded, and evolved by `wikiskill` itself.**

---

## Dogfooding Phases

### Phase 0: Manual Bootstrap
- Initial `Experience` and `WikiEntry` concepts are written by hand following OKF specs.
- Every manual entry explicitly states that it is a bootstrap artifact.

### Phase 1: Automated Experience Recording
- As soon as `wikiskill experience record` (CLI/Python API) passes tests, all subsequent engineering steps and agent findings are recorded via the tool.

### Phase 2: Knowledge Consolidation
- When `wikiskill wiki consolidate` is operational, learnings and patterns discovered during development are compiled through the runtime.

### Phase 3: Skill Proposals & Evaluation
- Changes to core workflow skills (e.g. `develop-feature`, `evaluate-skill`) are handled strictly via `SkillProposal` and `SkillEvaluation`.

### Phase 4: MCP-Driven Agent Operation
- Agent sessions operate the repository primarily via `wikiskill_*` FastMCP tools.

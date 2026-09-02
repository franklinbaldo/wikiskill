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

---

## Causal implementation protocol: Sinos / SinusTDD

Substantive implementation work in this repository should use `franklinbaldo/sinustdd` as an external causal TDD verifier. It is a development/dogfooding tool, **not** a runtime dependency of `wikiskill`.

The currently adopted reference is:

```text
d4c3c04f64946f82d73ae92402d20f79b84f2a1f
```

That revision provides the OKF-native evidence v2 ledger verified through `okf-parser` and DuckDB.

Run Sinos inside the WikiSkill project environment without adding it to `pyproject.toml`:

```bash
SINUSTDD_REF=d4c3c04f64946f82d73ae92402d20f79b84f2a1f
SINUSTDD="sinustdd @ git+https://github.com/franklinbaldo/sinustdd.git@${SINUSTDD_REF}"

uv run --with "$SINUSTDD" sinustdd begin
# add/commit only the failing verification contract
uv run --with "$SINUSTDD" sinustdd red
# implement without changing the frozen RED contract
uv run --with "$SINUSTDD" sinustdd green
uv run --with "$SINUSTDD" sinustdd refactor
uv run --with "$SINUSTDD" sinustdd complete
```

Rules:

- a GitHub Actions failure with no allocated/executed steps is infrastructure failure, never a `RedWitness`;
- `.sinustdd/evidence/**` is durable causal evidence and should be committed;
- `.sinustdd/session.json`, `.sinustdd/workspace-guard-state.json`, and the legacy/derived `.sinustdd/cycles/` snapshots are operational state and are ignored here;
- WikiSkill `Experience` and Sinos evidence serve different purposes: Sinos proves **the causal order of the implementation**, while WikiSkill records **what happened and what was learned**;
- after a successful feature cycle, use `wikiskill experience record` to preserve the useful engineering lesson in `knowledge/experiences/`.

At the pinned revision, `PosixPermissionGuard` exists and is integrated with `SinusTDDEngine`, but the stock `sinustdd` CLI does not yet instantiate it. Therefore the commands above provide the real causal ledger but not automatic POSIX write-locking. Do not claim filesystem enforcement unless the engine was actually instantiated with that guard.

---
type: Changelog
version: 0.2.9
date: 2026-09-06
---

# Pin governing RunSpec in LoopRun

- freezes the complete governing RunSpec frontmatter in each newly created LoopRun;
- records the authored RunSpec version and a SHA-256 digest alongside the snapshot;
- makes `check_run()` validate pinned runs against their historical contract rather than the mutable current RunSpec;
- detects snapshot digest, version, and identity divergence as explicit contract failures;
- preserves compatibility for legacy LoopRuns that predate pinning by falling back to their current RunSpec reference.

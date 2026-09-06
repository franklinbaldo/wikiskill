---
type: Changelog
version: 0.2.6
date: 2026-09-05
---

# Session policies and three-stage layout

- adds typed `ContextPolicy`, `AccessPolicy`, and `OutputPolicy` concepts;
- separates advisory/curated context guidance from host-level access control;
- composes policies through SessionType inheritance;
- routes new artifacts beneath `experiences/`, `wiki/`, or `skills/` only;
- migrates existing Experiences, LoopRun components, SessionTypes, RunSpecs, and active skills into semantic subfolders;
- preserves `WikiEntry` as the generic wiki knowledge concept.

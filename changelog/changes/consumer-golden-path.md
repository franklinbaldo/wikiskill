---
type: Changelog
version: 0.3.0
date: 2026-09-06
---

# Consumer golden path

- adds non-destructive `wikiskill init` for existing repositories;
- installs managed normative specs, canonical Experience/Wiki/Skill contracts, and a standard consumer profile;
- adds manifest-backed `wikiskill upgrade` with SHA-256 conflict detection and no partial write on validation failure;
- makes explicit `session start-next` fall back to on-demand Experience while preserving automatic `session next` semantics;
- autodiscovers `.wikiskill/knowledge` from the repository root in CLI commands;
- packages normative and canonical bootstrap assets in the wheel;
- documents the canonical cross-session Experience → Wiki → Skill evaluation lifecycle and consumer/core responsibility boundary.

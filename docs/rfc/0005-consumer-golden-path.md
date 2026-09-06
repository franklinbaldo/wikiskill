---
title: "RFC 0005 — Consumer golden path"
status: proposed
created: 2026-09-06
---

# RFC 0005 — Consumer golden path

## Summary

WikiSkill should be opinionated about how a repository adopts the learning runtime while remaining neutral about the repository's domain.

A consumer should not have to reproduce WikiSkill's internal directory layout, copy normative specs by hand, pin private implementation details, or rediscover the canonical Experience → Wiki → Skill cycle. The normal path should be:

```bash
wikiskill init .
wikiskill session start-next "Faça o melhor avanço possível neste repositório"
```

The consumer owns domain specialization. WikiSkill owns the learning architecture, compatible contracts, bootstrap, upgrade mechanics, and a useful default scheduling profile.

## Product boundary

### WikiSkill owns

- the canonical Experience, Wiki, and Skill roles;
- their canonical RunSpecs;
- normative specs compatible with the installed runtime;
- a recommended standard profile that schedules the three roles coherently;
- bootstrap and upgrade of WikiSkill-managed files;
- the manifest that identifies managed state;
- safe conflict detection before managed files are replaced;
- CLI ergonomics that let an explicit `session start-next` fall back to ordinary Experience work when no higher-value maintenance session is due.

### The consumer owns

- repository objectives and domain meaning;
- domain-specific readings, checks, tools, and evidence;
- access/institutional policy;
- merge, publication, deployment, or approval rules;
- local SessionType and RunSpec specializations;
- local cadence changes when the standard profile is not appropriate.

## Managed and local state

Bootstrap creates `.wikiskill/` with two conceptual surfaces:

```text
.wikiskill/
  manifest.json
  specs/                  # managed normative contracts
  knowledge/
    system/               # managed WikiSkill roles/profile
    local/                # consumer-owned specializations
    experiences/          # runtime-produced state
    wiki/                 # runtime-produced durable knowledge
    skills/               # runtime-produced/local skill state as policies allow
```

Physical output paths used by existing runtime concepts may coexist with this structure. The key invariant is ownership: files listed in `manifest.json` are managed by WikiSkill; files outside that set are consumer/runtime state and are never overwritten by `upgrade`.

## Standard profile

The standard profile makes the canonical cycle useful without requiring a scheduler-specific prompt.

### Experience

Experience is normal work. It is available on explicit `start-next` invocation and has the lowest automatic priority of the three learning roles.

### Wiki

Wiki becomes eligible after three new Experiences since its previous run. It has higher priority than Experience so accumulated evidence is periodically synthesized.

### Skill

Skill becomes eligible after six new Experiences since its previous run. Wiki has higher priority than Skill. Therefore, when both thresholds are reached, Wiki runs first; on the next invocation Skill can act on fresh synthesis.

This yields a simple causal rhythm without adding a fourth evaluator or a new persistence metric:

```text
Experience × 3 → Wiki
Experience × 3 → Wiki → Skill
repeat
```

Consumers may replace these thresholds. They are a product default, not a universal law.

## Explicit start semantics

`session next` remains an explanation of automatically eligible work.

`session start-next` is itself an explicit request to do useful work. It considers on-demand eligibility in addition to automatic triggers. The standard profile marks only Experience as on-demand, so an invocation behaves as follows:

1. if Wiki or Skill is due, the higher-priority due session runs;
2. otherwise Experience starts;
3. a targeted Handoff may still make its compatible session eligible according to cadence policy.

This makes the short external prompt reliable without configuring an arbitrary clock interval merely to keep Experience selectable.

## Bootstrap

`wikiskill init <repository>` is non-destructive.

It:

1. refuses to overwrite an existing managed installation;
2. creates the minimum `.wikiskill/` structure;
3. installs normative specs and system profile files shipped with the installed WikiSkill version;
4. records SHA-256 hashes and format/runtime version in `manifest.json`;
5. validates the resulting bundle;
6. reports the canonical next command.

An existing unrelated `.wikiskill/` directory is not silently adopted. Migration of legacy/manual installations is a distinct operation because guessing ownership is unsafe.

## Upgrade

`wikiskill upgrade <repository>` updates only manifest-managed files.

Before writing anything it compares each managed file with the hash recorded by the previous installation. If a managed file was edited locally and the new version would replace it, upgrade reports a conflict and performs no partial upgrade.

When there are no conflicts, upgrade:

- refreshes managed files from the installed runtime;
- adds newly managed files;
- removes obsolete managed files only when they still match the previous recorded hash;
- leaves all consumer/runtime files untouched;
- writes a new manifest only after the managed update succeeds.

The first implementation intentionally has no force-overwrite mode. Resolving an ownership conflict should be explicit.

## Distribution assets

The wheel must carry the normative `specs/` and canonical role/RunSpec sources used by bootstrap. Source checkouts may read the repository copies directly, but installed consumers must not depend on the WikiSkill Git checkout being present.

The source repository remains the authority for canonical specs and role definitions; packaging should include those same files rather than maintaining divergent hand-copied versions.

## Local specialization

A repository needing stronger domain rules should add local concepts that extend the installed system roles. For example:

```yaml
type: SessionType
id: session-types/judicial-experience
extends: session-types/standard-experience
run_spec: run-specs/judicial-experience
```

The local RunSpec can add legal/repository-specific readings and checks. The consumer does not need to redefine what Experience means globally.

## Upgrade compatibility

The manifest has its own `format_version`, independent of the package semantic version. A future runtime that cannot understand an older manifest must fail with an actionable migration message rather than guessing.

## Success criterion

A new repository can adopt WikiSkill through `init`, immediately run `session start-next`, and receive the canonical learning behavior. A real consumer such as Judicial should then be able to delete most of its hand-built WikiSkill bootstrap and retain only domain specialization.

If a consumer must understand WikiSkill's package topology or manually synchronize core specs to remain correct, this RFC has not been satisfied.

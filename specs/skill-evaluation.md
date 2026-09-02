---
type: ConceptSpecification
concept_type: SkillEvaluation
description: "Objective evaluation and benchmark record of a SkillProposal."
---

# Concept: SkillEvaluation

A `SkillEvaluation` records the verification of a candidate skill against objective fixtures, regression tests, or historical experiences.

## Required Frontmatter Fields

- `type`: Must be `"SkillEvaluation"`
- `id`: Evaluation identifier (e.g. `eval-2026-09-02-01`)
- `title`: Short evaluation title
- `proposal`: Link to `[SkillProposal](../proposals/...)`
- `decision`: Evaluation decision (`"accepted"`, `"rejected"`, `"inconclusive"`)
- `timestamp`: ISO-8601 timestamp

## Optional Frontmatter Fields

- `metrics`: Dictionary/mapping of scores or pass/fail counts
- `regressions`: Count or list of detected regressions

## Content Structure

The body should present:
1. **Methodology**: Fixtures, historical scenarios, or tasks evaluated.
2. **Results & Regressions**: Comparison of baseline vs candidate performance.
3. **Conclusion & Decision**: Recommendation to accept or perform asymmetric rollback.

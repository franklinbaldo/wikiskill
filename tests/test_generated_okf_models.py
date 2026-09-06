from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

import pytest

from wikiskill import WikiSkill
from wikiskill.generated.okf_models import ExperienceConcept, LoopRunConcept, RunReadingConcept
from wikiskill.models import generated_model_for, project_frontmatter

ROOT = Path(__file__).parent.parent


def _copy_bundle(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(ROOT / "knowledge", repo / "knowledge")
    shutil.copytree(ROOT / "specs", repo / "specs")
    return repo / "knowledge"


def test_generated_models_follow_okf_parser_names() -> None:
    assert generated_model_for("LoopRun") is LoopRunConcept
    assert generated_model_for("Experience") is ExperienceConcept
    assert generated_model_for("RunReading") is RunReadingConcept

    with pytest.raises(ValueError, match="Generated Pydantic model not found"):
        generated_model_for("DoesNotExist")


def test_projection_types_present_fields_without_requiring_future_run_state() -> None:
    run = project_frontmatter(
        LoopRunConcept,
        {
            "type": "LoopRun",
            "id": "runs/scaffold",
            "title": "Scaffold",
            "timestamp": "2026-09-06T11:50:00Z",
            "status": "scaffold",
            "run_spec": "run-specs/inference",
            "session_type": "session-types/inference",
            "task": "exercise generated typing",
            "readings": [],
            "goals": [],
            "decisions": [],
            "evidence": [],
            "checks": [],
        },
    )

    assert run.id == "runs/scaffold"
    assert run.status == "scaffold"
    assert run.readings == []
    assert not hasattr(run, "outcome")

    experience = project_frontmatter(
        ExperienceConcept,
        {
            "type": "Experience",
            "id": "exp-typed",
            "title": "Typed projection",
            "timestamp": "2026-09-06T11:51:00Z",
            "status": "success",
        },
    )
    assert isinstance(experience.timestamp, datetime)


def test_record_experience_updates_producing_looprun_backlink(tmp_path: Path) -> None:
    knowledge = _copy_bundle(tmp_path)
    ws = WikiSkill.open(knowledge)
    run_id = "runs/20260905-contract-guided-runtime"

    result = ws.record_experience(
        experience_id="exp-generated-model-backlink",
        title="Generated models close provenance in both directions",
        timestamp="2026-09-06T11:52:00Z",
        status="success",
        task="Use generated Pydantic projections in WikiSkill",
        context="Dogfood typed runtime provenance",
        run=run_id,
        body="# Generated model provenance\n\nThe Experience and LoopRun now link each other.\n",
    )

    assert result["written"] is True
    _, run = WikiSkill.open(knowledge)._typed_record("LoopRun", run_id, LoopRunConcept)
    assert "exp-generated-model-backlink" in run.experiences_recorded


def test_record_experience_rejects_unknown_run_before_writing(tmp_path: Path) -> None:
    knowledge = _copy_bundle(tmp_path)
    ws = WikiSkill.open(knowledge)

    with pytest.raises(ValueError, match="LoopRun not found"):
        ws.record_experience(
            experience_id="exp-no-run",
            title="Unknown run",
            timestamp="2026-09-06T11:53:00Z",
            status="failure",
            run="runs/does-not-exist",
            body="# Unknown run\n",
        )

    assert not (knowledge / "experiences" / "records" / "exp-no-run.md").exists()

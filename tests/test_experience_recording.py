from __future__ import annotations

import shutil
from pathlib import Path

from wikiskill import WikiSkill


ROOT = Path(__file__).parent.parent


def _copy_bundle(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    shutil.copytree(ROOT / "knowledge", repo / "knowledge")
    shutil.copytree(ROOT / "specs", repo / "specs")
    return repo / "knowledge"


def _experience_kwargs() -> dict[str, str]:
    return {
        "experience_id": "exp-2026-09-02-experience-recording-red-green",
        "title": "Implement Experience Recording through causal TDD",
        "timestamp": "2026-09-02T19:15:00-04:00",
        "status": "success",
        "task": "Implement wikiskill Experience Recording",
        "context": "SinusTDD BASELINE -> RED -> GREEN dogfooding cycle",
        "body": (
            "# Experience Recording Dogfood\n\n"
            "## Context & Intent\n"
            "Make WikiSkill persist its first post-bootstrap Experience through its own runtime.\n\n"
            "## Action & Observed Output\n"
            "A failing contract was introduced before the implementation.\n\n"
            "## Findings\n"
            "Experience persistence must remain OKF-native and validated after every write.\n"
        ),
    }


def test_preview_experience_is_pure_and_deterministic(tmp_path: Path) -> None:
    knowledge_path = _copy_bundle(tmp_path)
    ws = WikiSkill.open(knowledge_path)

    preview = ws.preview_experience(**_experience_kwargs())

    assert preview["id"] == "exp-2026-09-02-experience-recording-red-green"
    assert preview["path"] == (
        "experiences/exp-2026-09-02-experience-recording-red-green.md"
    )
    assert preview["content"].startswith("---\ntype: Experience\n")
    assert "status: success" in preview["content"]
    assert "task: \"Implement wikiskill Experience Recording\"" in preview["content"]
    assert "# Experience Recording Dogfood" in preview["content"]
    assert not (knowledge_path / preview["path"]).exists()


def test_record_experience_writes_valid_okf_and_refreshes_runtime(tmp_path: Path) -> None:
    knowledge_path = _copy_bundle(tmp_path)
    ws = WikiSkill.open(knowledge_path)
    before = ws.inventory()["Experience"]
    preview = ws.preview_experience(**_experience_kwargs())

    result = ws.record_experience(**_experience_kwargs())

    target = knowledge_path / result["path"]
    assert result == {
        "id": "exp-2026-09-02-experience-recording-red-green",
        "path": "experiences/exp-2026-09-02-experience-recording-red-green.md",
        "written": True,
    }
    assert target.read_text(encoding="utf-8") == preview["content"]
    assert ws.inventory()["Experience"] == before + 1
    assert WikiSkill.open(knowledge_path).inventory()["Experience"] == before + 1

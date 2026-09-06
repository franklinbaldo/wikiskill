from __future__ import annotations

import shutil
from pathlib import Path

from wikiskill import WikiSkill

ROOT = Path(__file__).parent.parent


def _copy_bundle(tmp_path: Path) -> Path:
    shutil.copytree(ROOT / "knowledge", tmp_path / "knowledge")
    shutil.copytree(ROOT / "specs", tmp_path / "specs")
    return tmp_path / "knowledge"


def test_builtin_session_types_are_declared() -> None:
    ws = WikiSkill.open(ROOT / "knowledge")
    ids = {item["id"] for item in ws.session_types()}
    assert {
        "session-types/inference",
        "session-types/wiki-maintainer",
        "session-types/skill-evolver",
        "session-types/evaluator",
        "session-types/development",
    } <= ids


def test_inference_context_uses_skills_without_injected_wiki() -> None:
    context = WikiSkill.open(ROOT / "knowledge").context(
        "bootstrap repository", "session-types/inference"
    )
    assert context["skills"]
    assert context["wiki"] == []
    assert context["recent_experiences"] == []
    assert context["context_policy"]["mode"] == "curated"


def test_wiki_maintainer_keeps_pattern_as_prompt_nudge_not_type() -> None:
    ws = WikiSkill.open(ROOT / "knowledge")
    session = ws.effective_session_type("session-types/wiki-maintainer")
    text = " ".join(session["nudges"])
    assert "Pattern is a writing nudge" in text
    assert "WikiEntry" in text
    assert "WikiPattern" not in ws.inventory()


def test_session_type_selects_its_own_runspec(tmp_path: Path) -> None:
    knowledge = _copy_bundle(tmp_path)
    result = WikiSkill.open(knowledge).start_run(
        "execute a task with active skills",
        session_type_id="session-types/inference",
    )
    assert result["session_type"] == "session-types/inference"
    assert result["run_spec"] == "run-specs/inference"
    requirements = {item["requirement"] for item in result["check"]["unsatisfied"]}
    assert "reading:active-skills" in requirements
    assert "goal:task-advance" in requirements

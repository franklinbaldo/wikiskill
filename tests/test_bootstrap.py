from __future__ import annotations

import json
from pathlib import Path

from wikiskill import WikiSkill
from wikiskill.bootstrap import init_repository, upgrade_repository


def _record_experiences(ws: WikiSkill, count: int) -> None:
    for index in range(count):
        ws.record_experience(
            experience_id=f"consumer-exp-{index}",
            title=f"Consumer experience {index}",
            timestamp=f"2026-09-06T1{index}:00:00+00:00",
            status="success",
            body=f"# Experience {index}\n\nObserved useful repository work {index}.",
        )


def test_init_creates_conformant_managed_consumer_bundle(tmp_path: Path) -> None:
    result = init_repository(tmp_path)

    assert result["status"] == "initialized"
    assert result["conformant"] is True
    root = tmp_path / ".wikiskill"
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["format_version"] == 1
    assert manifest["profile"] == "standard"
    assert "specs/sessiontype.md" in manifest["managed_files"]
    assert (
        root / "knowledge/system/profiles/standard/session-types/standard-experience.md"
    ).is_file()

    ws = WikiSkill.open(root / "knowledge")
    assert ws.next_session() is None
    started = ws.start_next_session("Do the next useful repository work")
    assert started["session_type"] == "session-types/standard-experience"
    assert started["run_spec"] == "run-specs/experience"


def test_standard_profile_runs_wiki_then_skill_as_experience_accumulates(tmp_path: Path) -> None:
    init_repository(tmp_path)
    knowledge = tmp_path / ".wikiskill/knowledge"
    ws = WikiSkill.open(knowledge)
    _record_experiences(ws, 6)

    due = WikiSkill.open(knowledge).next_session()
    assert due is not None
    assert due["session_type"] == "session-types/standard-wiki"

    wiki_run = WikiSkill.open(knowledge).start_next_session("Do the next useful work")
    assert wiki_run["session_type"] == "session-types/standard-wiki"

    after_wiki = WikiSkill.open(knowledge).next_session()
    assert after_wiki is not None
    assert after_wiki["session_type"] == "session-types/standard-skill"


def test_init_refuses_unmanaged_existing_state_without_touching_it(tmp_path: Path) -> None:
    root = tmp_path / ".wikiskill"
    root.mkdir()
    marker = root / "legacy.txt"
    marker.write_text("keep me", encoding="utf-8")

    result = init_repository(tmp_path)

    assert result["status"] == "unmanaged-existing-state"
    assert marker.read_text(encoding="utf-8") == "keep me"
    assert not (root / "manifest.json").exists()


def test_upgrade_preserves_consumer_owned_files(tmp_path: Path) -> None:
    init_repository(tmp_path)
    local = tmp_path / ".wikiskill/knowledge/local/repository-note.txt"
    local.parent.mkdir(parents=True)
    local.write_text("consumer-owned", encoding="utf-8")

    result = upgrade_repository(tmp_path)

    assert result["status"] == "upgraded"
    assert result["conformant"] is True
    assert local.read_text(encoding="utf-8") == "consumer-owned"


def test_upgrade_detects_edited_managed_file_before_writing(tmp_path: Path) -> None:
    init_repository(tmp_path)
    root = tmp_path / ".wikiskill"
    managed = root / "knowledge/system/canonical/session-types/experience.md"
    managed.write_text(managed.read_text(encoding="utf-8") + "\nlocal edit\n", encoding="utf-8")
    before_manifest = (root / "manifest.json").read_text(encoding="utf-8")

    result = upgrade_repository(tmp_path)

    assert result["status"] == "conflict"
    assert "knowledge/system/canonical/session-types/experience.md" in result["conflicts"]
    assert managed.read_text(encoding="utf-8").endswith("local edit\n")
    assert (root / "manifest.json").read_text(encoding="utf-8") == before_manifest

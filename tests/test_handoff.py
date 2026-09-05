from __future__ import annotations

import json
import shutil
from pathlib import Path

from wikiskill import WikiSkill

ROOT = Path(__file__).parent.parent


def _temp_bundle(tmp_path: Path) -> Path:
    shutil.copytree(ROOT / "knowledge", tmp_path / "knowledge")
    shutil.copytree(ROOT / "specs", tmp_path / "specs")
    return tmp_path / "knowledge"


def _write_concept(path: Path, frontmatter: dict[str, object]) -> None:
    lines = ["---"]
    for key, value in frontmatter.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.extend(["---", "", "# Test concept", ""])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def test_partial_run_requires_handoff_and_future_run_archives_it(tmp_path: Path) -> None:
    knowledge_path = _temp_bundle(tmp_path)
    ws = WikiSkill.open(knowledge_path)
    source = ws.start_run("wikiskill handoff development", "run-specs/wikiskill-development")
    source_run = source["run_id"]

    _write_concept(
        knowledge_path / "runs" / "partial-outcome.md",
        {
            "type": "RunOutcome",
            "id": "run-outcomes/handoff-source",
            "run": source_run,
            "result_state": "red",
            "work_status": "partial",
            "summary": "handoff capability is only partially implemented",
            "next_move": "continue the Handoff lifecycle implementation",
        },
    )

    before = WikiSkill.open(knowledge_path).check_run(source_run)
    assert "handoff" in {item["requirement"] for item in before["unsatisfied"]}

    ws = WikiSkill.open(knowledge_path)
    created = ws.create_handoff(
        handoff_id="handoff-runtime",
        title="Finish Handoff runtime",
        created_by_run=source_run,
        state="The type and RED contract exist; lifecycle implementation remains.",
        next_action="Implement create/list/continue and make checks GREEN.",
        references=["#38", "src/wikiskill/handoff.py"],
    )
    assert created["id"] == "handoffs/handoff-runtime"
    assert created["status"] == "active"

    after = WikiSkill.open(knowledge_path).check_run(source_run)
    assert "handoff" not in {item["requirement"] for item in after["unsatisfied"]}
    assert after["active_handoffs_created"] == 1

    context = WikiSkill.open(knowledge_path).context("finish handoff runtime")
    assert context["active_handoffs"][0]["id"] == "handoffs/handoff-runtime"
    assert context["active_handoffs"][0]["next_action"].startswith("Implement create")

    continuing = WikiSkill.open(knowledge_path).start_run(
        "finish handoff runtime", "run-specs/wikiskill-development"
    )
    continuing_run = continuing["run_id"]
    assert continuing["active_handoffs"][0]["id"] == "handoffs/handoff-runtime"

    archived = WikiSkill.open(knowledge_path).continue_handoff(
        handoff="handoffs/handoff-runtime",
        continued_by_run=continuing_run,
        resolution="The later run adopted the handoff and continued its implementation.",
    )
    assert archived == {
        "id": "handoffs/handoff-runtime",
        "status": "archived",
        "continued_by_run": continuing_run,
    }
    assert WikiSkill.open(knowledge_path).active_handoffs() == []

    handoff_doc = (knowledge_path / "handoffs" / "handoff-runtime.md").read_text(
        encoding="utf-8"
    )
    assert 'status: "archived"' in handoff_doc
    assert f'continued_by_run: "{continuing_run}"' in handoff_doc
    assert "archived_at:" in handoff_doc
    assert "resolution:" in handoff_doc


def test_complete_run_does_not_require_handoff(tmp_path: Path) -> None:
    knowledge_path = _temp_bundle(tmp_path)
    ws = WikiSkill.open(knowledge_path)
    started = ws.start_run("wikiskill development", "run-specs/wikiskill-development")
    run_id = started["run_id"]

    _write_concept(
        knowledge_path / "runs" / "complete-outcome.md",
        {
            "type": "RunOutcome",
            "id": "run-outcomes/complete",
            "run": run_id,
            "result_state": "green",
            "work_status": "complete",
            "summary": "the run-owned work is complete",
            "next_move": "a future run may choose another useful goal",
        },
    )

    result = WikiSkill.open(knowledge_path).check_run(run_id)
    assert "handoff" not in {item["requirement"] for item in result["unsatisfied"]}

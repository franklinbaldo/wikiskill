from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from fastmcp import Client
from okf_parser import get_pydantic_source, get_schema_contracts
from okf_parser.service import check_bundle

from wikiskill import WikiSkill, __version__

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


def test_version() -> None:
    assert __version__ == "0.2.6"


def test_bundle_conformance() -> None:
    report = check_bundle(
        str(ROOT / "knowledge"),
        require_spec="../specs/{slug}.md",
        normative_spec=True,
    )
    assert report["conformant"] is True
    concept_types = {concept.concept_type for concept in WikiSkill.open(ROOT / "knowledge").bundle.concepts.execute().itertuples()}
    assert "Experience" in concept_types
    assert "WikiEntry" in concept_types
    assert "AgentSkill" in concept_types
    assert "RunSpec" in concept_types
    assert "SessionType" in concept_types
    assert "ContextPolicy" in concept_types
    assert "AccessPolicy" in concept_types
    assert "OutputPolicy" in concept_types


def test_wikiskill_runtime_inventory_and_context() -> None:
    knowledge_path = ROOT / "knowledge"
    ws = WikiSkill.open(knowledge_path)
    inv = ws.inventory()
    assert inv["Experience"] >= 1
    assert inv["WikiEntry"] >= 1
    assert inv["AgentSkill"] >= 1
    assert inv["RunSpec"] >= 1
    assert inv["SessionType"] >= 2

    ctx = ws.context(task="wikiskill development")
    assert ctx["task"] == "wikiskill development"
    assert ctx["session_type"] == "session-types/development"
    assert ctx["context_policy"]["id"] == "context-policies/development"
    assert any(s["id"] == "run-specs/wikiskill-development" for s in ctx["run_specs"])
    assert "active_handoffs" in ctx

    bootstrap_ctx = ws.context(task="bootstrap repository setup")
    assert len(bootstrap_ctx["skills"]) >= 1
    assert any(s["id"] == "skill-bootstrap-repository" for s in bootstrap_ctx["skills"])
    assert len(bootstrap_ctx["recent_experiences"]) >= 1


def test_run_start_is_incomplete_and_contract_guided(tmp_path: Path) -> None:
    knowledge_path = _temp_bundle(tmp_path)
    ws = WikiSkill.open(knowledge_path)

    started = ws.start_run(
        "wikiskill development",
        "run-specs/wikiskill-development",
    )
    assert started["run_spec"] == "run-specs/wikiskill-development"
    assert started["status"] == "scaffold"
    assert started["session_type"] == "session-types/development"
    assert started["session"]["purpose"]
    assert started["check"]["conformant"] is False
    unsatisfied = {item["requirement"] for item in started["check"]["unsatisfied"]}
    assert "reading:repository-guide" in unsatisfied
    assert "reading:active-handoffs" in unsatisfied
    assert "goal:project-advance" in unsatisfied
    assert "evidence:change" in unsatisfied
    assert "check:okf" in unsatisfied
    assert "outcome" in unsatisfied
    assert started["check"]["next_action"]["requirement"] == "reading:repository-guide"


def test_run_check_turns_green_when_contract_is_satisfied(tmp_path: Path) -> None:
    knowledge_path = _temp_bundle(tmp_path)
    ws = WikiSkill.open(knowledge_path)
    started = ws.start_run(
        "wikiskill development",
        "run-specs/wikiskill-development",
    )
    run_id = started["run_id"]
    run_dir = knowledge_path / "experiences" / "runs"

    for index, kind in enumerate(
        [
            "repository-guide",
            "open-issues",
            "open-prs",
            "okf-knowledge",
            "recent-runs",
            "active-handoffs",
        ]
    ):
        _write_concept(
            run_dir / f"reading-{index}.md",
            {
                "type": "RunReading",
                "id": f"run-readings/{index}",
                "run": run_id,
                "kind": kind,
                "reference": f"source-{index}",
                "finding": f"finding-{index}",
            },
        )

    _write_concept(
        run_dir / "goal.md",
        {
            "type": "RunGoal",
            "id": "run-goals/main",
            "run": run_id,
            "kind": "project-advance",
            "statement": "advance runtime",
            "rationale": "prove the contract",
            "success_signal": "checks become conformant",
            "status": "achieved",
        },
    )
    for index, kind in enumerate(["change", "verification"]):
        _write_concept(
            run_dir / f"evidence-{index}.md",
            {
                "type": "RunEvidence",
                "id": f"run-evidence/{index}",
                "run": run_id,
                "kind": kind,
                "reference": f"evidence-{index}",
                "summary": f"summary-{index}",
            },
        )
    for index, kind in enumerate(["okf", "tests"]):
        _write_concept(
            run_dir / f"check-{index}.md",
            {
                "type": "RunCheck",
                "id": f"run-checks/{index}",
                "run": run_id,
                "kind": kind,
                "command": f"check-{index}",
                "result": "passed",
                "passed": True,
            },
        )
    _write_concept(
        run_dir / "outcome.md",
        {
            "type": "RunOutcome",
            "id": "run-outcomes/main",
            "run": run_id,
            "result_state": "green",
            "work_status": "complete",
            "summary": "contract satisfied",
            "next_move": "continue useful work",
        },
    )

    result = WikiSkill.open(knowledge_path).check_run(run_id)
    assert result["conformant"] is True
    assert result["unsatisfied"] == []
    assert result["next_action"]["kind"] == "complete"


def test_fastmcp_tools_registered() -> None:
    from wikiskill.mcp import mcp

    async def check() -> None:
        async with Client(mcp) as client:
            tools = await client.list_tools()
            names = {tool.name for tool in tools}
            assert "wikiskill_inventory" in names
            assert "wikiskill_context" in names
            assert "wikiskill_start" in names
            assert "wikiskill_check" in names
            assert "wikiskill_experience_preview" in names
            assert "wikiskill_experience_record" in names
            assert "wikiskill_handoffs" in names
            assert "wikiskill_handoff_create" in names
            assert "wikiskill_handoff_continue" in names

    import asyncio

    asyncio.run(check())


def test_pydantic_schema_contracts_derivation() -> None:
    contracts = get_schema_contracts(ROOT / "knowledge")
    assert "Experience" in contracts
    assert "WikiEntry" in contracts
    assert "AgentSkill" in contracts
    assert "RunSpec" in contracts
    assert "SessionType" in contracts
    assert "ContextPolicy" in contracts
    assert "AccessPolicy" in contracts
    assert "OutputPolicy" in contracts
    source = get_pydantic_source(ROOT / "knowledge")
    assert "class Experience" in source
    assert "class WikiEntry" in source
    assert "class AgentSkill" in source
    assert "class RunSpec" in source
    assert "class SessionType" in source
    assert "class ContextPolicy" in source
    assert "class AccessPolicy" in source
    assert "class OutputPolicy" in source


def test_mcp_tool_execution() -> None:
    from wikiskill.mcp import wikiskill_context, wikiskill_inventory

    inventory = wikiskill_inventory(str(ROOT / "knowledge"))
    assert inventory["Experience"] >= 1
    result = wikiskill_context("wikiskill development", str(ROOT / "knowledge"))
    assert result["task"] == "wikiskill development"


def test_cli_execution() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "wikiskill.cli", "info"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert f"v{__version__}" in result.stdout

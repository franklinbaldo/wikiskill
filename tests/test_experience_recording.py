from __future__ import annotations

import asyncio
import shutil
from pathlib import Path

import pytest

from wikiskill import WikiSkill
from wikiskill.mcp import mcp


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


def test_fastmcp_experience_tools_registered() -> None:
    async def _check() -> None:
        tools = await mcp.list_tools()
        tool_names = {tool.name for tool in tools}
        assert "wikiskill_experience_preview" in tool_names
        assert "wikiskill_experience_record" in tool_names

    asyncio.run(_check())


def test_fastmcp_experience_tools_execute(tmp_path: Path) -> None:
    from wikiskill.mcp import wikiskill_experience_preview, wikiskill_experience_record

    knowledge_path = _copy_bundle(tmp_path)
    kwargs = _experience_kwargs()

    preview = wikiskill_experience_preview(path=str(knowledge_path), **kwargs)
    assert preview["id"] == kwargs["experience_id"]
    assert not (knowledge_path / preview["path"]).exists()

    result = wikiskill_experience_record(path=str(knowledge_path), **kwargs)
    assert result["written"] is True
    assert (knowledge_path / result["path"]).exists()


def test_cli_experience_preview_and_record(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from wikiskill.cli import experience_preview, experience_record

    knowledge_path = _copy_bundle(tmp_path)
    kwargs = _experience_kwargs()

    experience_preview(path=str(knowledge_path), **kwargs)
    captured = capsys.readouterr()
    assert "type: Experience" in captured.out
    assert kwargs["experience_id"] in captured.out
    assert not (knowledge_path / f"experiences/{kwargs['experience_id']}.md").exists()

    experience_record(path=str(knowledge_path), **kwargs)
    captured = capsys.readouterr()
    assert f"Recorded Experience {kwargs['experience_id']}" in captured.out
    assert (knowledge_path / f"experiences/{kwargs['experience_id']}.md").exists()

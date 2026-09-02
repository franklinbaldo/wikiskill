from __future__ import annotations

import asyncio
from pathlib import Path

import pytest
from okf_parser import load_bundle

from wikiskill import WikiSkill, __version__
from wikiskill.mcp import mcp
from wikiskill.models import generate_pydantic_code, get_schema_contracts


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_bundle_conformance() -> None:
    knowledge_path = Path(__file__).parent.parent / "knowledge"
    bundle = load_bundle(knowledge_path)
    count = bundle.concepts.count().execute()
    assert count >= 3

    concept_types = set(bundle.concepts.select("concept_type").distinct().execute()["concept_type"])
    assert "Experience" in concept_types
    assert "WikiEntry" in concept_types
    assert "AgentSkill" in concept_types


def test_wikiskill_runtime_inventory_and_context() -> None:
    knowledge_path = Path(__file__).parent.parent / "knowledge"
    ws = WikiSkill.open(knowledge_path)
    inv = ws.inventory()
    assert inv["Experience"] >= 1
    assert inv["WikiEntry"] >= 1
    assert inv["AgentSkill"] >= 1

    ctx = ws.context(task="bootstrap repository setup")
    assert ctx["task"] == "bootstrap repository setup"
    assert len(ctx["skills"]) >= 1
    assert any(s["id"] == "skills/bootstrap-repository" for s in ctx["skills"])
    assert len(ctx["recent_experiences"]) >= 1


def test_fastmcp_tools_registered() -> None:
    async def _check() -> None:
        tools = await mcp.list_tools()
        tool_names = [t.name for t in tools]
        assert "wikiskill_inventory" in tool_names
        assert "wikiskill_context" in tool_names

    asyncio.run(_check())


def test_pydantic_schema_contracts_derivation() -> None:
    knowledge_path = Path(__file__).parent.parent / "knowledge"
    code = generate_pydantic_code(knowledge_path)
    assert "class AgentSkillConcept(BaseModel):" in code
    assert "class ExperienceConcept(BaseModel):" in code
    assert "class WikiEntryConcept(BaseModel):" in code

    contracts = get_schema_contracts(knowledge_path)
    contract_types = {c.concept_type for c in contracts}
    assert contract_types >= {"AgentSkill", "Experience", "WikiEntry"}


def test_mcp_tool_execution() -> None:
    from wikiskill.mcp import wikiskill_context, wikiskill_inventory

    inv = wikiskill_inventory()
    assert inv["Experience"] >= 1

    ctx = wikiskill_context("bootstrap")
    assert ctx["task"] == "bootstrap"
    assert len(ctx["skills"]) >= 1


def test_cli_execution(capsys: pytest.CaptureFixture[str]) -> None:
    from wikiskill.cli import context, info

    info()
    captured = capsys.readouterr()
    assert "wikiskill runtime v0.1.0" in captured.out

    context("bootstrap")
    captured = capsys.readouterr()
    assert "Context for: bootstrap" in captured.out
    assert "Skills found" in captured.out

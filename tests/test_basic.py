from __future__ import annotations

from pathlib import Path

from okf_parser import load_bundle

from wikiskill import WikiSkill, __version__


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

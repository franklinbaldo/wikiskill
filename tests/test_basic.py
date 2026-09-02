from __future__ import annotations

from pathlib import Path

from okf_parser import load_bundle

from wikiskill import __version__


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

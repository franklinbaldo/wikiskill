"""FastMCP server for wikiskill."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from wikiskill.runtime import WikiSkill

mcp = FastMCP(
    name="wikiskill",
)


def _get_runtime() -> WikiSkill:
    return WikiSkill.open(Path("knowledge"))


@mcp.tool(
    name="wikiskill_inventory",
    description="Get concept counts grouped by concept type in the WikiSkill OKF bundle.",
    annotations={"readOnlyHint": True},
)
def wikiskill_inventory() -> dict[str, int]:
    """Return counts of concepts grouped by concept_type."""
    return _get_runtime().inventory()


@mcp.tool(
    name="wikiskill_context",
    description=(
        "Retrieve task-relevant RunSpecs, skills, wiki knowledge, and recent experiences "
        "for contract-guided agent execution."
    ),
    annotations={"readOnlyHint": True},
)
def wikiskill_context(task: str) -> dict[str, Any]:
    """Retrieve execution and learned context for an agent task."""
    return _get_runtime().context(task)

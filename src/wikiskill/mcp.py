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


@mcp.tool(
    name="wikiskill_start",
    description=(
        "Create an intentionally incomplete LoopRun scaffold governed by a RunSpec, then "
        "return its first contract check so the agent can see what to establish next."
    ),
)
def wikiskill_start(task: str, run_spec: str | None = None) -> dict[str, Any]:
    """Create a live contract-guided run."""
    return _get_runtime().start_run(task, run_spec)


@mcp.tool(
    name="wikiskill_check",
    description=(
        "Validate a live LoopRun with okf-parser and report unsatisfied RunSpec requirements."
    ),
    annotations={"readOnlyHint": True},
)
def wikiskill_check(run: str) -> dict[str, Any]:
    """Check the current structural and semantic state of a live run."""
    return _get_runtime().check_run(run)

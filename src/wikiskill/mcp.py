"""FastMCP server for wikiskill."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from wikiskill.runtime import WikiSkill

mcp = FastMCP(
    name="wikiskill",
)


def _get_runtime(path: str | Path = "knowledge") -> WikiSkill:
    return WikiSkill.open(Path(path))


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
    description="Retrieve relevant skills, wiki knowledge, and recent experiences for a task.",
    annotations={"readOnlyHint": True},
)
def wikiskill_context(task: str) -> dict[str, Any]:
    """Retrieve relevant context for an agent given a task description."""
    return _get_runtime().context(task)


@mcp.tool(
    name="wikiskill_experience_preview",
    description="Preview an OKF Experience document without writing it to the bundle.",
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
def wikiskill_experience_preview(
    experience_id: str,
    title: str,
    timestamp: str,
    status: str,
    body: str,
    path: str = "knowledge",
    skill_used: str | None = None,
    skill_version: str | None = None,
    task: str | None = None,
    error_code: str | None = None,
    context: str | None = None,
) -> dict[str, str]:
    """Preview one Experience using the same runtime path as the commit tool."""
    return _get_runtime(path).preview_experience(
        experience_id=experience_id,
        title=title,
        timestamp=timestamp,
        status=status,
        body=body,
        skill_used=skill_used,
        skill_version=skill_version,
        task=task,
        error_code=error_code,
        context=context,
    )


@mcp.tool(
    name="wikiskill_experience_record",
    description="Write one validated OKF Experience document to the WikiSkill bundle.",
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
def wikiskill_experience_record(
    experience_id: str,
    title: str,
    timestamp: str,
    status: str,
    body: str,
    path: str = "knowledge",
    skill_used: str | None = None,
    skill_version: str | None = None,
    task: str | None = None,
    error_code: str | None = None,
    context: str | None = None,
) -> dict[str, str | bool]:
    """Persist one Experience through the canonical WikiSkill runtime."""
    return _get_runtime(path).record_experience(
        experience_id=experience_id,
        title=title,
        timestamp=timestamp,
        status=status,
        body=body,
        skill_used=skill_used,
        skill_version=skill_version,
        task=task,
        error_code=error_code,
        context=context,
    )

"""FastMCP server for wikiskill."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from wikiskill.runtime import WikiSkill

mcp = FastMCP(name="wikiskill")


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
        "Validate a live LoopRun and return unmet RunSpec requirements plus the next action."
    ),
    annotations={"readOnlyHint": True},
)
def wikiskill_check(run: str) -> dict[str, Any]:
    """Check the current structural and semantic state of a live run."""
    return _get_runtime().check_run(run)


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
    run: str | None = None,
) -> dict[str, str]:
    """Preview one Experience using the canonical runtime rendering path."""
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
        run=run,
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
    run: str | None = None,
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
        run=run,
    )

"""FastMCP server for wikiskill."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from wikiskill import WikiSkill

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
        "Retrieve task-relevant RunSpecs, active handoffs, skills, wiki knowledge, and recent "
        "experiences for contract-guided agent execution."
    ),
    annotations={"readOnlyHint": True},
)
def wikiskill_context(task: str) -> dict[str, Any]:
    """Retrieve execution and learned context for an agent task."""
    return _get_runtime().context(task)


@mcp.tool(
    name="wikiskill_start",
    description=(
        "Create an intentionally incomplete LoopRun scaffold governed by a RunSpec and surface "
        "active handoffs that the new session can resume."
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
    name="wikiskill_handoffs",
    description="List active cross-session handoffs, ranking task-relevant work first.",
    annotations={"readOnlyHint": True},
)
def wikiskill_handoffs(task: str | None = None, path: str = "knowledge") -> list[dict[str, Any]]:
    """List resumable unfinished work."""
    return _get_runtime(path).active_handoffs(task)


@mcp.tool(
    name="wikiskill_handoff_create",
    description="Create a validated active Handoff for material work left by a LoopRun.",
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
def wikiskill_handoff_create(
    handoff_id: str,
    title: str,
    created_by_run: str,
    state: str,
    next_action: str,
    references: list[str] | None = None,
    path: str = "knowledge",
) -> dict[str, Any]:
    """Persist one cross-session Handoff."""
    return _get_runtime(path).create_handoff(
        handoff_id=handoff_id,
        title=title,
        created_by_run=created_by_run,
        state=state,
        next_action=next_action,
        references=references,
    )


@mcp.tool(
    name="wikiskill_handoff_continue",
    description=(
        "Archive an active Handoff and record the later LoopRun that resumed the work."
    ),
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
def wikiskill_handoff_continue(
    handoff: str,
    continued_by_run: str,
    resolution: str,
    path: str = "knowledge",
) -> dict[str, Any]:
    """Consume a Handoff with provenance to the continuing run."""
    return _get_runtime(path).continue_handoff(
        handoff=handoff,
        continued_by_run=continued_by_run,
        resolution=resolution,
    )


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

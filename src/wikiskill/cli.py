"""CLI interface for wikiskill using Cyclopts."""

from __future__ import annotations

import json

import cyclopts

from wikiskill import WikiSkill, __version__

app = cyclopts.App(
    name="wikiskill",
    help="Contract-guided agent execution and persistent learning runtime built on OKF.",
    version=__version__,
)
experience_app = app.command(
    cyclopts.App(name="experience", help="Preview and record episodic Experience evidence.")
)
handoff_app = app.command(
    cyclopts.App(name="handoff", help="Create, list, and continue cross-session Handoffs.")
)


@app.command
def info() -> None:
    """Show wikiskill version and runtime information."""
    print(f"wikiskill runtime v{__version__} (OKF-backed)")


@app.command
def serve() -> None:
    """Start the FastMCP server over stdio."""
    from wikiskill.mcp import mcp

    mcp.run()


@app.command
def context(task: str) -> None:
    """Show contract and learned context for a given agent task."""
    ws = WikiSkill.open("knowledge")
    res = ws.context(task)
    print(f"--- Context for: {task} ---")
    print(f"Active handoffs ({len(res['active_handoffs'])}):")
    for handoff in res["active_handoffs"]:
        print(f"  - [{handoff['id']}] {handoff['title']} -> {handoff['next_action']}")
    print(f"RunSpecs found ({len(res['run_specs'])}):")
    for spec in res["run_specs"]:
        print(f"  - [{spec['id']}] {spec['title']}")
    print(f"Skills found ({len(res['skills'])}):")
    for skill in res["skills"]:
        print(f"  - [{skill['id']}] {skill['title']}")
    print(f"Wiki knowledge found ({len(res['wiki'])}):")
    for wiki in res["wiki"]:
        print(f"  - [{wiki['id']}] {wiki['title']}")


@app.command
def start(
    task: str,
    run_spec: str | None = None,
    session_type: str | None = None,
) -> None:
    """Create a live LoopRun scaffold for a task and SessionType."""
    result = WikiSkill.open("knowledge").start_run(task, run_spec, session_type)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


@app.command
def check(run: str) -> None:
    """Check a live run and show unsatisfied operational requirements."""
    result = WikiSkill.open("knowledge").check_run(run)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


@handoff_app.command(name="list")
def handoff_list(task: str | None = None, *, path: str = "knowledge") -> None:
    """List active handoffs, prioritizing work relevant to a task."""
    result = WikiSkill.open(path).active_handoffs(task)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


@handoff_app.command(name="create")
def handoff_create(
    handoff_id: str,
    title: str,
    created_by_run: str,
    state: str,
    next_action: str,
    *,
    path: str = "knowledge",
    references: list[str] | None = None,
) -> None:
    """Persist an active handoff emitted by one LoopRun."""
    result = WikiSkill.open(path).create_handoff(
        handoff_id=handoff_id,
        title=title,
        created_by_run=created_by_run,
        state=state,
        next_action=next_action,
        references=references,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


@handoff_app.command(name="continue")
def handoff_continue(
    handoff: str,
    continued_by_run: str,
    resolution: str,
    *,
    path: str = "knowledge",
) -> None:
    """Archive a handoff with provenance to the later LoopRun that resumed it."""
    result = WikiSkill.open(path).continue_handoff(
        handoff=handoff,
        continued_by_run=continued_by_run,
        resolution=resolution,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


@experience_app.command(name="preview")
def experience_preview(
    experience_id: str,
    title: str,
    timestamp: str,
    status: str,
    body: str,
    *,
    path: str = "knowledge",
    skill_used: str | None = None,
    skill_version: str | None = None,
    task: str | None = None,
    error_code: str | None = None,
    context: str | None = None,
    run: str | None = None,
) -> None:
    """Preview an Experience document without changing the bundle."""
    result = WikiSkill.open(path).preview_experience(
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
    print(result["content"], end="")


@experience_app.command(name="record")
def experience_record(
    experience_id: str,
    title: str,
    timestamp: str,
    status: str,
    body: str,
    *,
    path: str = "knowledge",
    skill_used: str | None = None,
    skill_version: str | None = None,
    task: str | None = None,
    error_code: str | None = None,
    context: str | None = None,
    run: str | None = None,
) -> None:
    """Persist one validated Experience document into the bundle."""
    result = WikiSkill.open(path).record_experience(
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
    print(f"Recorded Experience {result['id']} -> {result['path']}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()

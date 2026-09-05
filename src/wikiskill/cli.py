"""CLI interface for wikiskill using Cyclopts."""

from __future__ import annotations

import json

import cyclopts

from wikiskill import __version__
from wikiskill.runtime import WikiSkill

app = cyclopts.App(
    name="wikiskill",
    help="Contract-guided agent execution and persistent learning runtime built on OKF.",
    version=__version__,
)
experience_app = app.command(
    cyclopts.App(name="experience", help="Preview and record episodic Experience evidence.")
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
def start(task: str, run_spec: str | None = None) -> None:
    """Create a live LoopRun scaffold for a task."""
    result = WikiSkill.open("knowledge").start_run(task, run_spec)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


@app.command
def check(run: str) -> None:
    """Check a live run and show unsatisfied operational requirements."""
    result = WikiSkill.open("knowledge").check_run(run)
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

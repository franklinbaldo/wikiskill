"""CLI interface for wikiskill using Cyclopts."""

from __future__ import annotations

import cyclopts

from wikiskill import __version__
from wikiskill.runtime import WikiSkill

app = cyclopts.App(
    name="wikiskill",
    help="Persistent agent learning runtime built on OKF.",
    version=__version__,
)
experience_app = app.command(
    cyclopts.App(name="experience", help="Preview and record episodic agent Experience evidence.")
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
    """Show context for a given agent task."""
    ws = WikiSkill.open("knowledge")
    res = ws.context(task)
    print(f"--- Context for: {task} ---")
    print(f"Skills found ({len(res['skills'])}):")
    for s in res["skills"]:
        print(f"  - [{s['id']}] {s['title']}")
    print(f"Wiki knowledge found ({len(res['wiki'])}):")
    for w in res["wiki"]:
        print(f"  - [{w['id']}] {w['title']}")


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
) -> None:
    """Preview an Experience document without changing the bundle."""
    ws = WikiSkill.open(path)
    result = ws.preview_experience(
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
) -> None:
    """Persist one validated Experience document into the bundle."""
    ws = WikiSkill.open(path)
    result = ws.record_experience(
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
    print(f"Recorded Experience {result['id']} -> {result['path']}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()

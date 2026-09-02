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


def main() -> None:
    app()


if __name__ == "__main__":
    main()

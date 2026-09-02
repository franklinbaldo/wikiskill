"""CLI interface for wikiskill using Cyclopts."""

from __future__ import annotations

import cyclopts

app = cyclopts.App(
    name="wikiskill",
    help="Persistent agent learning runtime built on OKF.",
    version="0.1.0",
)


@app.command
def info() -> None:
    """Show wikiskill version and runtime information."""
    print("wikiskill runtime v0.1.0 (OKF-backed)")


def main() -> None:
    app()


if __name__ == "__main__":
    main()

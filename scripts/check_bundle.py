# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "okf-parser>=0.45.6",
#     "rich>=13.0",
# ]
# ///
"""Standalone verification script for OKF bundle integrity adhering to PEP 723."""

from __future__ import annotations

import sys
from pathlib import Path

from okf_parser import load_bundle
from rich.console import Console

console = Console()


def verify_bundle(path: Path) -> bool:
    console.print(f"[bold cyan]Verifying OKF bundle at:[/bold cyan] {path}")
    bundle = load_bundle(path)
    count = bundle.concepts.count().execute()
    console.print(f"[green]✓ Concepts found:[/green] {count}")

    if count == 0:
        console.print("[red]✗ Error: Bundle is empty[/red]")
        return False

    console.print("[bold green]✓ OKF bundle is valid and healthy![/bold green]")
    return True


def main() -> int:
    root = Path(__file__).parent.parent / "knowledge"
    if not verify_bundle(root):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Pydantic model generation and typed query helpers derived from OKF contracts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from okf_parser.schema_export import TypeContract, build_schema_contracts, export_pydantic_source

if TYPE_CHECKING:
    from pathlib import Path


def generate_pydantic_code(knowledge_path: Path) -> str:
    """Generate dynamic Pydantic models directly from the OKF bundle schema contracts."""
    return export_pydantic_source(str(knowledge_path))


def get_schema_contracts(knowledge_path: Path) -> tuple[TypeContract, ...]:
    """Inspect schema contracts discovered by okf-parser across the bundle."""
    return build_schema_contracts(str(knowledge_path))

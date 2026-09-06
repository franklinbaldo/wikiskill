"""Pydantic projections and schema helpers derived from canonical OKF contracts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, TypeVar, cast

from okf_parser.schema_contract import model_name
from okf_parser.schema_export import TypeContract, build_schema_contracts, export_pydantic_source
from pydantic import BaseModel, TypeAdapter

from wikiskill.generated import okf_models

if TYPE_CHECKING:
    from pathlib import Path

SPEC_TEMPLATE = "../specs/{slug}.md"
ModelT = TypeVar("ModelT", bound=BaseModel)


def generate_pydantic_code(knowledge_path: Path) -> str:
    """Generate deterministic Pydantic source from WikiSkill's OKF contracts."""
    return export_pydantic_source(
        str(knowledge_path),
        spec_template=SPEC_TEMPLATE,
    )


def get_schema_contracts(knowledge_path: Path) -> tuple[TypeContract, ...]:
    """Inspect observed and contract-first schemas discovered by okf-parser."""
    return build_schema_contracts(
        str(knowledge_path),
        spec_template=SPEC_TEMPLATE,
    )


def generated_model_for(concept_type: str) -> type[BaseModel]:
    """Resolve the committed generated model using okf-parser's naming policy."""
    class_name = model_name(concept_type, "Concept")
    candidate = getattr(okf_models, class_name, None)
    if not isinstance(candidate, type) or not issubclass(candidate, BaseModel):
        raise ValueError(f"Generated Pydantic model not found for OKF type: {concept_type}")
    return cast("type[BaseModel]", candidate)


def project_frontmatter(model: type[ModelT], frontmatter: Mapping[str, object]) -> ModelT:
    """Project already-OKF-validated metadata into a statically visible Pydantic model.

    OKF remains the authority for document conformance. Generated Pydantic models are
    a Python projection of that contract, so this helper validates/coerces fields that
    are present but deliberately does not reinterpret missing progressive fields as an
    additional source of truth.
    """
    values: dict[str, object] = {}
    authored_names: set[str] = set()
    for python_name, field in model.model_fields.items():
        authored_name = field.alias or python_name
        authored_names.add(authored_name)
        if authored_name not in frontmatter:
            continue
        annotation = field.annotation
        raw = frontmatter[authored_name]
        values[python_name] = raw if annotation is None else TypeAdapter(annotation).validate_python(raw)

    values.update(
        (name, value) for name, value in frontmatter.items() if name not in authored_names
    )
    return model.model_construct(_fields_set=set(values), **values)

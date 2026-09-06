"""Runtime layer that projects canonical OKF records into generated Pydantic types."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from okf_parser import load_bundle
from pydantic import BaseModel

from wikiskill.generated.okf_models import ExperienceConcept, LoopRunConcept
from wikiskill.live_run import LiveRunWikiSkill
from wikiskill.models import project_frontmatter


class TypedWikiSkill(LiveRunWikiSkill):
    """Live runtime whose Python-facing state uses generated OKF model projections."""

    @classmethod
    def open(cls, path: str | Path = "knowledge") -> TypedWikiSkill:
        """Open a bundle while preserving the generated-model runtime type."""
        root = Path(path).resolve()
        return cls(bundle=load_bundle(root), root_path=root)

    def _typed_record[ModelT: BaseModel](
        self,
        concept_type: str,
        identifier: str,
        model: type[ModelT],
    ) -> tuple[dict[str, Any], ModelT]:
        """Resolve one OKF record and project its frontmatter into a generated model."""
        record = self._find_record(concept_type, identifier)
        frontmatter = cast("dict[str, object]", record["frontmatter"])
        return record, project_frontmatter(model, frontmatter)

    def record_experience(
        self,
        *,
        experience_id: str,
        title: str,
        timestamp: str,
        status: str,
        body: str,
        skill_used: str | None = None,
        skill_version: str | None = None,
        task: str | None = None,
        error_code: str | None = None,
        context: str | None = None,
        run: str | None = None,
    ) -> dict[str, str | bool]:
        """Persist Experience and its LoopRun backlink as one validated mutation."""
        run_record: dict[str, Any] | None = None
        run_model: LoopRunConcept | None = None
        canonical_run = run
        if run is not None:
            run_record, run_model = self._typed_record("LoopRun", run, LoopRunConcept)
            canonical_run = run_model.id

        preview = self.preview_experience(
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
            run=canonical_run,
        )
        experience_frontmatter: dict[str, object] = {
            "type": "Experience",
            "id": preview["id"],
            "title": title,
            "timestamp": timestamp,
            "status": status,
        }
        optional_fields = {
            "skill_used": skill_used,
            "skill_version": skill_version,
            "task": task,
            "error_code": error_code,
            "context": context,
            "run": canonical_run,
        }
        experience_frontmatter.update(
            {key: value for key, value in optional_fields.items() if value is not None}
        )
        experience = project_frontmatter(ExperienceConcept, experience_frontmatter)
        target = self.root_path / preview["path"]
        target.parent.mkdir(parents=True, exist_ok=True)

        run_path: Path | None = None
        previous_run: str | None = None
        updated_run_content: str | None = None
        if run_record is not None and run_model is not None:
            run_path = self.root_path / str(run_record["path"])
            previous_run = run_path.read_text(encoding="utf-8")
            run_frontmatter = dict(cast("dict[str, object]", run_record["frontmatter"]))
            links = list(getattr(run_model, "experiences_recorded", []) or [])
            if experience.id not in links:
                links.append(experience.id)
            run_frontmatter["experiences_recorded"] = links
            project_frontmatter(LoopRunConcept, run_frontmatter)
            updated_run_content = self._render_markdown(
                run_frontmatter,
                self._body_from_document(previous_run),
            )

        try:
            with target.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(preview["content"])
            if run_path is not None and updated_run_content is not None:
                run_path.write_text(updated_run_content, encoding="utf-8", newline="\n")
            self._require_conformant_bundle()
        except Exception:
            target.unlink(missing_ok=True)
            if run_path is not None and previous_run is not None:
                run_path.write_text(previous_run, encoding="utf-8", newline="\n")
            self._reload()
            raise

        self._reload()
        return {
            "id": experience.id,
            "path": preview["path"],
            "written": True,
        }

"""Core WikiSkill runtime facade."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from okf_parser import Bundle, load_bundle
from okf_parser.service import check_bundle

_EXPERIENCE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_EXPERIENCE_STATUSES = frozenset({"success", "failure", "partial", "observation"})


def _yaml_string(value: str) -> str:
    """Render a JSON string literal, which is also a safe YAML scalar."""
    return json.dumps(value, ensure_ascii=False)


class WikiSkill:
    """Opinionated agent learning runtime backed by Open Knowledge Format (OKF)."""

    def __init__(self, bundle: Bundle, root_path: Path) -> None:
        self.bundle = bundle
        self.root_path = root_path

    @classmethod
    def open(cls, path: str | Path = "knowledge") -> WikiSkill:
        """Open an existing OKF knowledge bundle."""
        root = Path(path).resolve()
        bundle = load_bundle(root)
        return cls(bundle=bundle, root_path=root)

    def inventory(self) -> dict[str, int]:
        """Return counts of concepts grouped by concept_type."""
        df = (
            self.bundle.concepts.group_by("concept_type")
            .aggregate(count=self.bundle.concepts.count())
            .execute()
        )
        return dict(zip(df["concept_type"], df["count"], strict=True))

    def preview_experience(
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
    ) -> dict[str, str]:
        """Render an Experience document without mutating the bundle."""
        if not _EXPERIENCE_ID_RE.fullmatch(experience_id):
            msg = "experience_id must be a filename-safe identifier"
            raise ValueError(msg)
        if status not in _EXPERIENCE_STATUSES:
            allowed = ", ".join(sorted(_EXPERIENCE_STATUSES))
            msg = f"status must be one of: {allowed}"
            raise ValueError(msg)
        if not title.strip():
            raise ValueError("title must not be empty")
        if not timestamp.strip():
            raise ValueError("timestamp must not be empty")
        if not body.strip():
            raise ValueError("body must not be empty")

        relative_path = Path("experiences") / f"{experience_id}.md"
        if (self.root_path / relative_path).exists():
            raise FileExistsError(self.root_path / relative_path)

        fields: list[tuple[str, str]] = [
            ("type", "Experience"),
            ("id", experience_id),
            ("title", _yaml_string(title)),
            ("timestamp", _yaml_string(timestamp)),
            ("status", status),
        ]
        optional_fields = (
            ("skill_used", skill_used),
            ("skill_version", skill_version),
            ("task", task),
            ("error_code", error_code),
            ("context", context),
        )
        fields.extend((key, _yaml_string(value)) for key, value in optional_fields if value is not None)

        frontmatter = "\n".join(f"{key}: {value}" for key, value in fields)
        normalized_body = body.rstrip() + "\n"
        content = f"---\n{frontmatter}\n---\n\n{normalized_body}"
        return {
            "id": experience_id,
            "path": relative_path.as_posix(),
            "content": content,
        }

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
    ) -> dict[str, str | bool]:
        """Persist one Experience and reject any write that makes the OKF bundle invalid."""
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
        )
        target = self.root_path / preview["path"]
        target.parent.mkdir(parents=True, exist_ok=True)

        try:
            with target.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(preview["content"])

            report = check_bundle(
                str(self.root_path),
                require_spec="../specs/{slug}.md",
                normative_spec=True,
            )
            if not bool(report["conformant"]):
                diagnostics = report.get("diagnostics", [])
                msg = f"Experience write would make the OKF bundle invalid: {diagnostics!r}"
                raise ValueError(msg)

            self.bundle = load_bundle(self.root_path)
        except Exception:
            target.unlink(missing_ok=True)
            self.bundle = load_bundle(self.root_path)
            raise

        return {
            "id": experience_id,
            "path": preview["path"],
            "written": True,
        }

    def context(self, task: str) -> dict[str, Any]:
        """Extract relevant skills, wiki entries, and recent experiences for a given task."""
        keywords = [k.lower() for k in task.split() if len(k) > 2]

        concepts_df = self.bundle.concepts.execute()
        relevant_skills: list[dict[str, Any]] = []
        relevant_wiki: list[dict[str, Any]] = []
        recent_experiences: list[dict[str, Any]] = []

        for _, row in concepts_df.iterrows():
            ctype = row["concept_type"]
            title = str(row.get("title") or "")
            cid = str(row["concept_id"])
            text_corpus = f"{cid} {title}".lower()
            matched = any(k in text_corpus for k in keywords) if keywords else True

            record = {
                "id": cid,
                "type": ctype,
                "title": title,
                "path": str(row.get("path") or ""),
            }

            if ctype == "AgentSkill" and matched:
                relevant_skills.append(record)
            elif ctype == "WikiEntry" and matched:
                relevant_wiki.append(record)
            elif ctype == "Experience":
                recent_experiences.append(record)

        return {
            "task": task,
            "skills": relevant_skills,
            "wiki": relevant_wiki,
            "recent_experiences": recent_experiences[:5],
        }

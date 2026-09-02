"""Core WikiSkill runtime facade."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from okf_parser import Bundle, load_bundle


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

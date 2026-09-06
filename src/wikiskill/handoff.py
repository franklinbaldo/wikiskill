"""Cross-session Handoff lifecycle for the WikiSkill runtime."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from okf_parser import load_bundle
from okf_parser.service import check_bundle

from wikiskill.runtime import WikiSkill as BaseWikiSkill

_HANDOFF_STATUS_ACTIVE = "active"
_HANDOFF_STATUS_ARCHIVED = "archived"


class HandoffWikiSkill(BaseWikiSkill):
    """WikiSkill runtime with resumable cross-session handoffs."""

    @classmethod
    def open(cls, path: str | Path = "knowledge") -> HandoffWikiSkill:
        """Open an OKF bundle while preserving the Handoff-enabled runtime type."""
        root = Path(path).resolve()
        return cls(bundle=load_bundle(root), root_path=root)

    def active_handoffs(self, task: str | None = None) -> list[dict[str, Any]]:
        """List active handoffs, ranking task-relevant work first."""
        keywords = {
            word for word in re.findall(r"[a-z0-9_-]+", (task or "").lower()) if len(word) > 2
        }
        handoffs: list[dict[str, Any]] = []
        for record in self._records("Handoff"):
            fm = record["frontmatter"]
            if str(fm.get("status") or "") != _HANDOFF_STATUS_ACTIVE:
                continue
            references = [str(item) for item in fm.get("references", [])]
            corpus = " ".join(
                [
                    record["id"],
                    record["title"],
                    str(fm.get("state") or ""),
                    str(fm.get("next_action") or ""),
                    *references,
                ]
            ).lower()
            relevant = any(word in corpus for word in keywords) if keywords else True
            handoffs.append(
                {
                    "id": record["id"],
                    "title": record["title"],
                    "path": record["path"],
                    "created_by_run": str(fm.get("created_by_run") or ""),
                    "target_session_type": str(fm.get("target_session_type") or ""),
                    "state": str(fm.get("state") or ""),
                    "next_action": str(fm.get("next_action") or ""),
                    "references": references,
                    "relevant": relevant,
                }
            )
        return sorted(handoffs, key=lambda item: (not item["relevant"], item["id"]))

    def create_handoff(
        self,
        *,
        handoff_id: str,
        title: str,
        created_by_run: str,
        state: str,
        next_action: str,
        references: list[str] | None = None,
        target_session_type: str | None = None,
    ) -> dict[str, Any]:
        """Persist active unfinished work emitted by one LoopRun."""
        self._find_record("LoopRun", created_by_run)
        slug = self._slug(handoff_id.rsplit("/", 1)[-1])
        if not slug:
            raise ValueError("handoff_id must contain a usable identifier")
        if not title.strip() or not state.strip() or not next_action.strip():
            raise ValueError("title, state and next_action must not be empty")

        canonical_id = f"handoffs/{slug}"
        directory = self.root_path / "handoffs"
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{slug}.md"
        if path.exists():
            raise FileExistsError(path)

        now = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        frontmatter: dict[str, Any] = {
            "type": "Handoff",
            "id": canonical_id,
            "title": title,
            "created_at": now,
            "status": _HANDOFF_STATUS_ACTIVE,
            "created_by_run": created_by_run,
            "state": state,
            "next_action": next_action,
            "references": references or [],
        }
        if target_session_type:
            frontmatter["target_session_type"] = target_session_type
        path.write_text(self._render_markdown(frontmatter, "# Handoff\n"), encoding="utf-8")
        try:
            self._require_conformant_bundle()
        except Exception:
            path.unlink(missing_ok=True)
            self._reload()
            raise
        self._reload()
        return {"id": canonical_id, "path": str(path), "status": _HANDOFF_STATUS_ACTIVE}

    def continue_handoff(
        self,
        *,
        handoff: str,
        continued_by_run: str,
        resolution: str,
    ) -> dict[str, Any]:
        """Archive a handoff and identify the LoopRun that resumed it."""
        self._find_record("LoopRun", continued_by_run)
        record = self._find_record("Handoff", handoff)
        frontmatter = dict(record["frontmatter"])
        if str(frontmatter.get("status") or "") != _HANDOFF_STATUS_ACTIVE:
            raise ValueError(f"Handoff is already archived: {record['id']}")
        created_by_run = str(frontmatter.get("created_by_run") or "")
        if continued_by_run == created_by_run:
            raise ValueError("continued_by_run must identify a later LoopRun")
        if not resolution.strip():
            raise ValueError("resolution must not be empty")

        path = self.root_path / record["path"]
        previous = path.read_text(encoding="utf-8")
        body = self._body_from_document(previous)
        frontmatter.update(
            {
                "status": _HANDOFF_STATUS_ARCHIVED,
                "continued_by_run": continued_by_run,
                "archived_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "resolution": resolution,
            }
        )
        path.write_text(self._render_markdown(frontmatter, body), encoding="utf-8")
        try:
            self._require_conformant_bundle()
        except Exception:
            path.write_text(previous, encoding="utf-8")
            self._reload()
            raise
        self._reload()
        return {
            "id": record["id"],
            "status": _HANDOFF_STATUS_ARCHIVED,
            "continued_by_run": continued_by_run,
        }

    def context(self, task: str) -> dict[str, Any]:
        """Include active handoffs alongside learned and contract context."""
        result = super().context(task)
        result["active_handoffs"] = self.active_handoffs(task)
        return result

    def start_run(self, task: str, run_spec_id: str | None = None) -> dict[str, Any]:
        """Start a run and surface resumable work before the agent proceeds."""
        result = super().start_run(task, run_spec_id)
        result["active_handoffs"] = self.active_handoffs(task)
        return result

    def check_run(self, run_id_or_path: str) -> dict[str, Any]:
        """Require a Handoff when a run declares material work partial."""
        result = super().check_run(run_id_or_path)
        run = self._find_record("LoopRun", run_id_or_path)
        run_id = str(run["frontmatter"].get("id") or run["id"])
        outcomes = self._run_components("RunOutcome", run_id)
        if not outcomes:
            return result

        work_status = str(outcomes[-1]["frontmatter"].get("work_status") or "")
        active_for_run = [
            item
            for item in self._records("Handoff")
            if str(item["frontmatter"].get("status") or "") == _HANDOFF_STATUS_ACTIVE
            and str(item["frontmatter"].get("created_by_run") or "") == run_id
        ]
        if work_status == "partial" and not active_for_run:
            requirement = {
                "requirement": "handoff",
                "kind": "handoff",
                "message": "Record a Handoff for material work left to a future LoopRun.",
            }
            result["unsatisfied"].append(requirement)
            result["conformant"] = False
            if result["next_action"].get("kind") == "complete":
                result["next_action"] = dict(requirement)
        result["active_handoffs_created"] = len(active_for_run)
        return result

    def _require_conformant_bundle(self) -> None:
        report = check_bundle(
            str(self.root_path),
            require_spec="../specs/{slug}.md",
            normative_spec=True,
        )
        if not bool(report["conformant"]):
            diagnostics = report.get("diagnostics", [])
            raise ValueError(f"Handoff write would make the OKF bundle invalid: {diagnostics!r}")

    @staticmethod
    def _body_from_document(content: str) -> str:
        parts = content.split("---", 2)
        if len(parts) < 3:
            return "# Handoff\n"
        body = parts[2].lstrip("\n")
        return body or "# Handoff\n"

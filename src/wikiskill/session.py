"""SessionType resolution and LoopRun binding."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from okf_parser import load_bundle

from wikiskill.handoff import HandoffWikiSkill


class SessionWikiSkill(HandoffWikiSkill):
    """WikiSkill runtime with typed, inheritable session behavior."""

    @classmethod
    def open(cls, path: str | Path = "knowledge") -> SessionWikiSkill:
        root = Path(path).resolve()
        return cls(bundle=load_bundle(root), root_path=root)

    def session_types(self) -> list[dict[str, Any]]:
        """List declared SessionTypes with their effective inherited configuration."""
        return [self.effective_session_type(item["id"]) for item in self._records("SessionType")]

    def effective_session_type(self, identifier: str) -> dict[str, Any]:
        """Resolve one SessionType through a shallow, cycle-safe inheritance chain."""
        return self._resolve_session_type(identifier, stack=())

    def _resolve_session_type(self, identifier: str, stack: tuple[str, ...]) -> dict[str, Any]:
        record = self._find_record("SessionType", identifier)
        session_id = str(record["frontmatter"].get("id") or record["id"])
        if session_id in stack:
            chain = " -> ".join((*stack, session_id))
            raise ValueError(f"SessionType inheritance cycle: {chain}")

        fm = dict(record["frontmatter"])
        parent_ref = str(fm.get("extends") or "")
        effective: dict[str, Any] = {}
        if parent_ref:
            effective.update(self._resolve_session_type(parent_ref, (*stack, session_id)))

        parent_nudges = [str(item) for item in effective.get("nudges", [])]
        child_nudges = [str(item) for item in fm.get("nudges", [])]
        effective.update({key: value for key, value in fm.items() if key != "nudges"})
        effective["nudges"] = [*parent_nudges, *child_nudges]
        effective["id"] = session_id
        effective["path"] = record["path"]
        effective["inheritance"] = [*effective.get("inheritance", []), session_id]
        return effective

    def _select_session_type(self, requested: str | None) -> dict[str, Any]:
        if requested:
            return self.effective_session_type(requested)
        try:
            return self.effective_session_type("session-types/development")
        except ValueError:
            sessions = self._records("SessionType")
            if not sessions:
                raise ValueError("No SessionType concepts are available in the knowledge bundle.")
            return self.effective_session_type(sessions[0]["id"])

    def start_run(
        self,
        task: str,
        run_spec_id: str | None = None,
        session_type_id: str | None = None,
    ) -> dict[str, Any]:
        """Start a LoopRun governed by an effective SessionType."""
        session = self._select_session_type(session_type_id)
        session_spec = str(session.get("run_spec") or "")
        selected_spec = run_spec_id or session_spec or None
        result = super().start_run(task, selected_spec)

        run = self._find_record("LoopRun", result["run_id"])
        path = self.root_path / run["path"]
        previous = path.read_text(encoding="utf-8")
        frontmatter = dict(run["frontmatter"])
        frontmatter["session_type"] = session["id"]
        body = self._body_from_document(previous)
        path.write_text(self._render_markdown(frontmatter, body), encoding="utf-8")
        try:
            self._require_conformant_bundle()
        except Exception:
            path.write_text(previous, encoding="utf-8")
            self._reload()
            raise
        self._reload()
        result["session_type"] = session["id"]
        result["session"] = {
            "id": session["id"],
            "purpose": str(session.get("purpose") or ""),
            "nudges": list(session.get("nudges", [])),
            "inheritance": list(session.get("inheritance", [])),
        }
        result["check"] = self.check_run(result["run_id"])
        return result

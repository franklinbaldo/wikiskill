"""Composable context, access, and output policies for SessionTypes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from okf_parser import load_bundle

from wikiskill.session import SessionWikiSkill

_POLICY_KEYS = ("context_policy", "access_policy", "output_policy")
_OUTPUT_FIELDS = {
    "Experience": "experience_path",
    "LoopRun": "run_path",
    "RunReading": "run_path",
    "RunGoal": "run_path",
    "RunDecision": "run_path",
    "RunEvidence": "run_path",
    "RunCheck": "run_path",
    "RunOutcome": "run_path",
    "Handoff": "handoff_path",
    "WikiEntry": "wiki_path",
    "AgentSkill": "skill_path",
    "SkillProposal": "proposal_path",
    "SkillEvaluation": "evaluation_path",
    "SessionType": "session_type_path",
    "RunSpec": "run_spec_path",
    "ContextPolicy": "context_policy_path",
    "AccessPolicy": "access_policy_path",
    "OutputPolicy": "output_policy_path",
}


class PolicyWikiSkill(SessionWikiSkill):
    """Session runtime that resolves and explains policy composition."""

    @classmethod
    def open(cls, path: str | Path = "knowledge") -> PolicyWikiSkill:
        root = Path(path).resolve()
        return cls(bundle=load_bundle(root), root_path=root)

    def effective_session_type(self, identifier: str) -> dict[str, Any]:
        session = super().effective_session_type(identifier)
        session["policies"] = {
            key: self._resolve_policy(key, str(session.get(key) or "")) for key in _POLICY_KEYS
        }
        return session

    def _resolve_policy(self, key: str, identifier: str) -> dict[str, Any] | None:
        if not identifier:
            return None
        concept_type = {
            "context_policy": "ContextPolicy",
            "access_policy": "AccessPolicy",
            "output_policy": "OutputPolicy",
        }[key]
        record = self._find_record(concept_type, identifier)
        result = dict(record["frontmatter"])
        result["id"] = str(result.get("id") or record["id"])
        result["path"] = record["path"]
        return result

    def policy_for(self, session_type_id: str | None = None) -> dict[str, Any]:
        """Return the effective policies for one SessionType."""
        session = self._select_session_type(session_type_id)
        return {
            "session_type": session["id"],
            **session.get("policies", {}),
        }

    def context(self, task: str, session_type_id: str | None = None) -> dict[str, Any]:
        """Return context plus explicit policy guidance for the selected session."""
        result = super().context(task)
        session = self._select_session_type(session_type_id)
        policies = session.get("policies", {})
        context_policy = policies.get("context_policy")
        access_policy = policies.get("access_policy")
        result["session_type"] = session["id"]
        result["session_purpose"] = str(session.get("purpose") or "")
        result["session_nudges"] = list(session.get("nudges", []))
        result["context_policy"] = context_policy
        result["access_policy"] = access_policy

        if context_policy and str(context_policy.get("mode") or "advisory") == "curated":
            include = {str(item) for item in context_policy.get("include", [])}
            exclude = {str(item) for item in context_policy.get("exclude", [])}
            surfaces = {
                "skills": "skills",
                "wiki": "wiki",
                "experiences": "recent_experiences",
                "handoffs": "active_handoffs",
                "run-specs": "run_specs",
            }
            for category, key in surfaces.items():
                if category in exclude or (include and category not in include):
                    result[key] = []
        return result

    def output_path(self, concept_type: str, session_type_id: str | None = None) -> str:
        """Resolve the semantic output directory for a concept type."""
        session = self._select_session_type(session_type_id)
        policy = session.get("policies", {}).get("output_policy")
        field = _OUTPUT_FIELDS.get(concept_type)
        if not policy or field is None:
            return super()._output_dir(concept_type).as_posix()
        value = str(policy.get(field) or "")
        if not value:
            return super()._output_dir(concept_type).as_posix()
        return value.strip("/")

    def _output_dir(self, concept_type: str) -> Path:
        try:
            relative = self.output_path(concept_type)
        except (ValueError, RecursionError):
            return super()._output_dir(concept_type)
        return Path(relative)

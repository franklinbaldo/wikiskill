"""Declarative eligibility and scheduling for WikiSkill SessionTypes."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from okf_parser import load_bundle

from wikiskill.policy import PolicyWikiSkill


class CadenceWikiSkill(PolicyWikiSkill):
    """Policy-aware runtime that can explain and select eligible sessions."""

    @classmethod
    def open(cls, path: str | Path = "knowledge") -> CadenceWikiSkill:
        root = Path(path).resolve()
        return cls(bundle=load_bundle(root), root_path=root)

    def effective_session_type(self, identifier: str) -> dict[str, Any]:
        session = super().effective_session_type(identifier)
        cadence_ref = str(session.get("cadence_policy") or "")
        session["cadence"] = self._cadence_policy(cadence_ref) if cadence_ref else None
        return session

    def _cadence_policy(self, identifier: str) -> dict[str, Any]:
        record = self._find_record("CadencePolicy", identifier)
        result = dict(record["frontmatter"])
        result["id"] = str(result.get("id") or record["id"])
        result["path"] = record["path"]
        return result

    def session_eligibility(
        self,
        session_type_id: str,
        *,
        now: datetime | None = None,
        requested: bool = False,
    ) -> dict[str, Any]:
        """Explain whether a SessionType is eligible at this instant."""
        current = (now or datetime.now(UTC)).astimezone(UTC)
        session = self.effective_session_type(session_type_id)
        cadence = session.get("cadence")
        if not cadence:
            return {
                "session_type": session["id"],
                "eligible": requested,
                "priority": 0,
                "reasons": ["explicit-request"] if requested else [],
                "blockers": [] if requested else ["no-cadence-policy"],
                "metrics": {},
            }

        runs = self._session_runs(session["id"])
        last_run = self._latest_timestamp(runs)
        active_runs = sum(
            1
            for run in runs
            if str(run["frontmatter"].get("status") or "") in {"scaffold", "active", "in_progress"}
        )
        runs_last_hour = sum(
            1
            for run in runs
            if (stamp := self._timestamp(run)) is not None and current - stamp <= timedelta(hours=1)
        )
        matching_handoffs = [
            item
            for item in self.active_handoffs()
            if item.get("target_session_type") == session["id"]
        ]
        threshold_value = self._metric_value(
            str(cadence.get("threshold_metric") or ""),
            session["id"],
            last_run,
        )

        reasons: list[str] = []
        blockers: list[str] = []
        if requested and bool(cadence.get("on_demand")):
            reasons.append("explicit-request")
        if matching_handoffs and bool(cadence.get("handoff_compatible")):
            reasons.append("active-handoff")

        interval = self._int(cadence.get("interval_seconds"))
        if interval and (last_run is None or (current - last_run).total_seconds() >= interval):
            reasons.append("interval")

        threshold_gte = self._int(cadence.get("threshold_gte"))
        threshold_reached = (
            threshold_gte is not None
            and threshold_value is not None
            and threshold_value >= threshold_gte
        )
        if threshold_reached:
            reasons.append("threshold")

        max_delay = self._int(cadence.get("max_delay_seconds"))
        if max_delay and (last_run is None or (current - last_run).total_seconds() >= max_delay):
            reasons.append("max-delay")

        cooldown = self._int(cadence.get("cooldown_seconds"))
        if cooldown and last_run is not None and (current - last_run).total_seconds() < cooldown:
            blockers.append("cooldown")

        max_parallel = self._int(cadence.get("max_parallel"))
        if max_parallel is not None and active_runs >= max_parallel:
            blockers.append("max-parallel")

        max_runs_per_hour = self._int(cadence.get("max_runs_per_hour"))
        if max_runs_per_hour is not None and runs_last_hour >= max_runs_per_hour:
            blockers.append("hourly-budget")

        return {
            "session_type": session["id"],
            "eligible": bool(reasons) and not blockers,
            "priority": self._int(cadence.get("priority")) or 0,
            "reasons": reasons,
            "blockers": blockers,
            "metrics": {
                "active_runs": active_runs,
                "runs_last_hour": runs_last_hour,
                "threshold_value": threshold_value,
                "targeted_handoffs": len(matching_handoffs),
                "last_run": last_run.isoformat().replace("+00:00", "Z") if last_run else None,
            },
        }

    def eligible_sessions(self, *, now: datetime | None = None) -> list[dict[str, Any]]:
        """Return automatically eligible sessions ordered deterministically."""
        candidates = [
            self.session_eligibility(item["id"], now=now)
            for item in self.session_types()
            if item["id"] != "session-types/base"
        ]
        eligible = [item for item in candidates if item["eligible"]]
        return sorted(eligible, key=lambda item: (-item["priority"], item["session_type"]))

    def next_session(self, *, now: datetime | None = None) -> dict[str, Any] | None:
        """Return the highest-priority automatically eligible SessionType."""
        eligible = self.eligible_sessions(now=now)
        return eligible[0] if eligible else None

    def start_next_session(self, task: str, *, now: datetime | None = None) -> dict[str, Any]:
        """Select and start the next automatically eligible session."""
        candidate = self.next_session(now=now)
        if candidate is None:
            raise ValueError("No SessionType is currently eligible for automatic start.")
        return self.start_run(task, session_type_id=candidate["session_type"])

    def _session_runs(self, session_type_id: str) -> list[dict[str, Any]]:
        return [
            run
            for run in self._records("LoopRun")
            if str(run["frontmatter"].get("session_type") or "") == session_type_id
        ]

    def _metric_value(
        self,
        metric: str,
        session_type_id: str,
        last_run: datetime | None,
    ) -> int | None:
        if not metric:
            return None
        if metric == "experiences-since-last-run":
            return sum(
                1
                for item in self._records("Experience")
                if last_run is None
                or (stamp := self._timestamp(item)) is not None
                and stamp > last_run
            )
        if metric == "active-handoffs":
            return sum(
                1
                for item in self.active_handoffs()
                if not item.get("target_session_type")
                or item.get("target_session_type") == session_type_id
            )
        raise ValueError(f"Unknown cadence threshold metric: {metric}")

    def _latest_timestamp(self, records: list[dict[str, Any]]) -> datetime | None:
        stamps = [stamp for item in records if (stamp := self._timestamp(item)) is not None]
        return max(stamps) if stamps else None

    @staticmethod
    def _timestamp(record: dict[str, Any]) -> datetime | None:
        frontmatter = record["frontmatter"]
        value = str(frontmatter.get("timestamp") or frontmatter.get("created_at") or "")
        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
        except ValueError:
            return None

    @staticmethod
    def _int(value: Any) -> int | None:
        if value is None or value == "":
            return None
        return int(value)

# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Fail when a built WikiSkill wheel cannot bootstrap a consumer repository."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

REQUIRED = {
    "wikiskill/_assets/specs/sessiontype.md",
    "wikiskill/_assets/specs/runspec.md",
    "wikiskill/_assets/specs/experience.md",
    "wikiskill/_assets/canonical/session-types/experience.md",
    "wikiskill/_assets/canonical/session-types/wiki.md",
    "wikiskill/_assets/canonical/session-types/skill.md",
    "wikiskill/_assets/canonical/run-specs/experience.md",
    "wikiskill/_assets/canonical/run-specs/wiki.md",
    "wikiskill/_assets/canonical/run-specs/skill.md",
    "wikiskill/profiles/standard/session-types/standard-experience.md",
    "wikiskill/profiles/standard/session-types/standard-wiki.md",
    "wikiskill/profiles/standard/session-types/standard-skill.md",
}


def main() -> int:
    wheels = sorted(Path("dist").glob("wikiskill-*.whl"))
    if len(wheels) != 1:
        print(f"expected exactly one wikiskill wheel in dist/, found {len(wheels)}")
        return 1
    with zipfile.ZipFile(wheels[0]) as wheel:
        names = set(wheel.namelist())
    missing = sorted(REQUIRED - names)
    if missing:
        print("wheel is missing consumer bootstrap assets:")
        for path in missing:
            print(f"  - {path}")
        return 1
    print(f"wheel contains all {len(REQUIRED)} required consumer bootstrap assets")
    return 0


if __name__ == "__main__":
    sys.exit(main())

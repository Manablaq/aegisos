#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from importlib.metadata import (
    PackageNotFoundError,
    distribution,
    version,
)
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_LOCK_SHA = (
    "14db5fb5adbf7ae14575c19f9779d7c2c996d20d44192a79e28bf601b649d20c"
)

EXPECTED_DIRECT = {
    "genlayer-py":
        "cf421edc0d20e567cc5a3b4da198fce61f1e579f",
    "genlayer-test":
        "9c09578b143905471fb0657dd53bdaf18da8e35f",
    "genvm-linter":
        "928bb51c42da8ff2512d81465d3e704f599aca47",
}

EXPECTED_VERSIONS = {
    "genlayer-py": "0.18.0",
    "genlayer-test": "0.29.2",
    "genvm-linter": "0.11.0",
}

LOCK = ROOT / "requirements-lock.txt"
DEV = ROOT / "requirements-dev.txt"
REPRO = (
    ROOT
    / "verification"
    / "toolchain"
    / "r4-reproducibility.json"
)
RAW_FREEZE = (
    ROOT
    / "verification"
    / "toolchain"
    / "r4-r3-freeze.txt"
)
RAW_REPORT = (
    ROOT
    / "verification"
    / "toolchain"
    / "r4-r3-install-report.json"
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--runtime",
    action="store_true",
    help="also verify installed package versions and VCS provenance",
)
args = parser.parse_args()

for path in (
    LOCK,
    DEV,
    REPRO,
    RAW_FREEZE,
    RAW_REPORT,
):
    if not path.is_file():
        raise SystemExit(
            f"missing toolchain evidence: {path.relative_to(ROOT)}"
        )

lock_bytes = LOCK.read_bytes()
lock_sha = hashlib.sha256(lock_bytes).hexdigest()

if lock_sha != EXPECTED_LOCK_SHA:
    raise SystemExit(
        f"requirements lock SHA mismatch: {lock_sha}"
    )

if RAW_FREEZE.read_bytes() != lock_bytes:
    raise SystemExit(
        "preserved R4-R3 freeze differs from requirements-lock.txt"
    )

lock_lines = [
    line.strip()
    for line in LOCK.read_text(
        encoding="utf-8"
    ).splitlines()
    if line.strip()
]

if len(lock_lines) != 55:
    raise SystemExit(
        f"unexpected requirements-lock line count: {len(lock_lines)}"
    )

for line in lock_lines:
    if " @ git+" in line:
        continue

    if "==" not in line:
        raise SystemExit(
            f"non-exact requirement in lock: {line}"
        )

dev_text = DEV.read_text(encoding="utf-8")

for package, commit in EXPECTED_DIRECT.items():
    expected_fragment = (
        f"{package} @ git+https://github.com/genlayerlabs/"
    )

    if package == "genlayer-py":
        expected_line = (
            "genlayer-py @ "
            "git+https://github.com/genlayerlabs/genlayer-py.git@"
            + commit
        )
    elif package == "genlayer-test":
        expected_line = (
            "genlayer-test @ "
            "git+https://github.com/genlayerlabs/"
            "genlayer-testing-suite.git@"
            + commit
        )
    else:
        expected_line = (
            "genvm-linter @ "
            "git+https://github.com/genlayerlabs/genvm-linter.git@"
            + commit
        )

    if expected_line not in dev_text:
        raise SystemExit(
            f"missing direct pinned dependency: {package}"
        )

    if not any(
        line.startswith(package + " @ ")
        and line.endswith("@" + commit)
        for line in lock_lines
    ):
        raise SystemExit(
            f"lock missing exact VCS pin: {package}"
        )

repro = json.loads(
    REPRO.read_text(encoding="utf-8")
)

if (
    repro.get("schema")
    != "AEGISOS_GATE0_R4_REPRODUCIBILITY_V1"
):
    raise SystemExit(
        "unexpected R4 reproducibility schema"
    )

if (
    repro["preserved_evidence"]["requirements_lock_sha256"]
    != EXPECTED_LOCK_SHA
):
    raise SystemExit(
        "R4 reproducibility lock SHA mismatch"
    )

research = json.loads(
    (ROOT / "toolchain" / "research-lock.json").read_text(
        encoding="utf-8"
    )
)

toolchain_repro = research.get(
    "toolchain_reproducibility",
    {},
)

if (
    toolchain_repro.get("requirements_lock_sha256")
    != EXPECTED_LOCK_SHA
):
    raise SystemExit(
        "research lock toolchain SHA mismatch"
    )

if (
    toolchain_repro.get("full_freeze_parity")
    is not True
):
    raise SystemExit(
        "research lock does not record full freeze parity"
    )

if research.get("production_toolchain_frozen") is not False:
    raise SystemExit(
        "production toolchain was frozen prematurely"
    )

if args.runtime:
    for package, expected_version in EXPECTED_VERSIONS.items():
        try:
            actual_version = version(package)
        except PackageNotFoundError as exc:
            raise SystemExit(
                f"runtime package missing: {package}"
            ) from exc

        if actual_version != expected_version:
            raise SystemExit(
                f"{package} version mismatch: "
                f"{actual_version}"
            )

        dist = distribution(package)
        direct_url_raw = dist.read_text(
            "direct_url.json"
        )

        if direct_url_raw is None:
            raise SystemExit(
                f"{package} direct_url.json missing"
            )

        direct_url = json.loads(direct_url_raw)
        vcs = direct_url.get("vcs_info", {})

        expected_commit = EXPECTED_DIRECT[package]

        if vcs.get("commit_id") != expected_commit:
            raise SystemExit(
                f"{package} installed commit mismatch"
            )

        if (
            vcs.get("requested_revision")
            != expected_commit
        ):
            raise SystemExit(
                f"{package} requested revision mismatch"
            )

    print("AEGISOS_TOOLCHAIN_RUNTIME_GATE=PASS")

print("AEGISOS_TOOLCHAIN_LOCK_GATE=PASS")
print(f"REQUIREMENTS_LOCK_SHA256={EXPECTED_LOCK_SHA}")
print("LOCK_LINE_COUNT=55")
print("FULL_FREEZE_PARITY=PASS")
print("PRODUCTION_TOOLCHAIN_FROZEN=NO")

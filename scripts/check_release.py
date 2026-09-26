#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SHA256 = {
    "contracts/aegis_core.py":
        "df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b",
    "contracts/aegis_digest_helper.py":
        "624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73",
    "tests/test_aegis_core_direct.py":
        "b3368fe053abe0fc1e2290b8b839f173b31e126ccc94a3e14ff3f2676962cab6",
    "tests/conftest.py":
        "a5841fda3e29ec53714f0385ec5b217f19cb203a1ed19db89ad391e60f4c22d9",
    "requirements-lock.txt":
        "14db5fb5adbf7ae14575c19f9779d7c2c996d20d44192a79e28bf601b649d20c",
}

REQUIRED = (
    "README.md",
    "docs/API.md",
    "docs/ARCHITECTURE.md",
    "docs/BRADBURY_VERIFICATION.md",
    "docs/SECURITY.md",
    "scripts/check_supported_runtime_bundle.py",
    "verification/supported_runtime/README.md",
)

FORBIDDEN_PRODUCT_PATHS = (
    "package.json",
    "next.config.js",
    "next.config.mjs",
    "vite.config.js",
    "vite.config.ts",
    "vercel.json",
    "app",
    "pages",
    "public",
    "src/app",
    "src/pages",
    "frontend",
    "web",
)

STALE_PATHS = (
    "docs/ARCHITECTURE_V1.md",
    "docs/BRADBURY_RUNTIME_BASELINE.md",
    "docs/DEPLOYMENT_BUDGET.md",
    "docs/ESCROW_AND_RECOVERY.md",
    "docs/EVIDENCE_TRUST_MODEL.md",
    "docs/GENLAYER_ENGINEERING_ENVELOPE.md",
    "docs/RESEARCH_SOURCES.md",
    "docs/REVIEWER_GATES.md",
    "docs/RUNNER_COMPATIBILITY.md",
    "docs/RUNTIME_COMPATIBILITY_MATRIX.md",
    "docs/SECURITY_INVARIANTS.md",
    "docs/SETTLEMENT_ARCHITECTURE_V1.md",
    "docs/STATE_MACHINE_V1.md",
    "docs/TOOLCHAIN_CANDIDATE.md",
    "docs/TOOLCHAIN_REPRODUCIBILITY.md",
    "toolchain/research-lock.json",
    "verification/bradbury/gate0-r3-d1-readonly.json",
    "verification/runner",
    "verification/toolchain",
)

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

for relative, wanted in EXPECTED_SHA256.items():
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"missing release artifact: {relative}")
    actual = sha256(path)
    if actual != wanted:
        raise SystemExit(
            f"release SHA mismatch for {relative}: {actual}"
        )

for relative in REQUIRED:
    if not (ROOT / relative).is_file():
        raise SystemExit(f"missing required publication file: {relative}")

for relative in FORBIDDEN_PRODUCT_PATHS:
    if (ROOT / relative).exists():
        raise SystemExit(
            f"non-Intelligent-Contract product surface present: {relative}"
        )

for relative in STALE_PATHS:
    if (ROOT / relative).exists():
        raise SystemExit(f"stale pre-release artifact present: {relative}")

contract_files = sorted(
    path.name
    for path in (ROOT / "contracts").iterdir()
    if path.is_file()
)
if contract_files != [
    "aegis_core.py",
    "aegis_digest_helper.py",
]:
    raise SystemExit(
        "canonical contracts/ must contain only the Core and digest helper: "
        + repr(contract_files)
    )

readme = (ROOT / "README.md").read_text(encoding="utf-8")
required_readme_markers = (
    "Reusable GenLayer Intelligent Contract",
    "Bradbury Testnet live verification complete",
    "Intelligent-Contract-only",
    "0x532de68bd897529c06803efed843d814b1744ba0",
    "0xf557028b465a6f87ae76b0f520edb2b3e6e4eec9",
    "0x96b759e96ff23c4064469fc1a3278232116b9e85e9185b43914ffa7deffb74e1",
    "does **not** claim that the GenVM core itself currently custodies or transfers",
)
for marker in required_readme_markers:
    if marker not in readme:
        raise SystemExit(f"README release marker missing: {marker}")

dev = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
pins = (
    "cf421edc0d20e567cc5a3b4da198fce61f1e579f",
    "9c09578b143905471fb0657dd53bdaf18da8e35f",
    "928bb51c42da8ff2512d81465d3e704f599aca47",
)
for pin in pins:
    if pin not in dev:
        raise SystemExit(f"development dependency pin missing: {pin}")

print("AEGISOS_RELEASE_PUBLICATION_GATE=PASS")
print("REPOSITORY_SCOPE=INTELLIGENT_CONTRACT_ONLY")
print(
    "CORE_SHA256="
    "df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b"
)
print(
    "HELPER_SHA256="
    "624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73"
)
print("BRADBURY_LIVE_VERIFICATION=COMPLETE")

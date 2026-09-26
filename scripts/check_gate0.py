#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    ROOT / "README.md",
    ROOT / "docs" / "GENLAYER_ENGINEERING_ENVELOPE.md",
    ROOT / "docs" / "ARCHITECTURE_V1.md",
    ROOT / "docs" / "SECURITY_INVARIANTS.md",
    ROOT / "docs" / "STATE_MACHINE_V1.md",
    ROOT / "docs" / "EVIDENCE_TRUST_MODEL.md",
    ROOT / "docs" / "ESCROW_AND_RECOVERY.md",
    ROOT / "docs" / "DEPLOYMENT_BUDGET.md",
    ROOT / "docs" / "REVIEWER_GATES.md",
    ROOT / "docs" / "RESEARCH_SOURCES.md",
    ROOT / "toolchain" / "research-lock.json",
]

missing = [str(path.relative_to(ROOT)) for path in REQUIRED if not path.is_file()]
if missing:
    raise SystemExit(f"missing Gate-0 files: {missing}")

lock = json.loads((ROOT / "toolchain" / "research-lock.json").read_text())

if lock.get("schema") != "AEGISOS_GATE0_RESEARCH_LOCK_V1":
    raise SystemExit("invalid research lock schema")

if lock.get("status") != "UNFROZEN":
    raise SystemExit(
        "Gate-0 research lock changed from UNFROZEN without a dedicated freeze gate"
    )

network = lock.get("target_network", {})

if network.get("chain_id") != 4221:
    raise SystemExit("unexpected Bradbury chain ID in research lock")

if network.get("genlayer_rpc") != "https://rpc-bradbury.genlayer.com":
    raise SystemExit("unexpected Bradbury RPC in research lock")

if (
    network.get("consensus_main", "").lower()
    != "0x0112bf6e83497965a5fdd6dad1e447a6e004271d"
):
    raise SystemExit("unexpected Bradbury consensus-main address")

for key in (
    "production_toolchain_frozen",
    "production_runner_frozen",
    "deployment_budget_frozen",
    "payout_transport_frozen",
):
    if lock.get(key) is not False:
        raise SystemExit(f"{key} must remain false during current Gate 0")

CANONICAL_CONTRACT_PATH = Path(
    "contracts/aegis_core.py"
)
CANONICAL_HELPER_PATH = Path(
    "contracts/aegis_digest_helper.py"
)
CANONICAL_CONTRACT = ROOT / CANONICAL_CONTRACT_PATH
CANONICAL_HELPER = ROOT / CANONICAL_HELPER_PATH
EXPECTED_CANONICAL_CONTRACT_SHA256 = (
    "df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b"
)
EXPECTED_CANONICAL_HELPER_SHA256 = (
    "624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73"
)

contract_files = sorted(
    (
        p
        for p in (ROOT / "contracts").rglob("*")
        if (
            p.is_file()
            and p.name != ".gitkeep"
            and "__pycache__" not in p.parts
            and p.suffix not in {".pyc", ".pyo"}
        )
    ),
    key=lambda p: p.as_posix(),
)

expected_contract_files = [
    CANONICAL_CONTRACT,
    CANONICAL_HELPER,
]

if contract_files != expected_contract_files:
    raise SystemExit(
        "unexpected Intelligent Contract surface: "
        + ", ".join(
            str(p.relative_to(ROOT))
            for p in contract_files
        )
    )

actual_contract_sha256 = hashlib.sha256(
    CANONICAL_CONTRACT.read_bytes()
).hexdigest()
actual_helper_sha256 = hashlib.sha256(
    CANONICAL_HELPER.read_bytes()
).hexdigest()

if actual_contract_sha256 != EXPECTED_CANONICAL_CONTRACT_SHA256:
    raise SystemExit(
        "canonical AegisOS core SHA-256 mismatch"
    )

if actual_helper_sha256 != EXPECTED_CANONICAL_HELPER_SHA256:
    raise SystemExit(
        "canonical AegisOS digest helper SHA-256 mismatch"
    )

print("AEGISOS_GATE0_BASELINE=PASS")
print("CANONICAL_CONTRACT_PRESENT=YES")
print(
    "CANONICAL_CONTRACT_PATH="
    + CANONICAL_CONTRACT_PATH.as_posix()
)
print(
    "CANONICAL_CONTRACT_SHA256="
    + actual_contract_sha256
)
print(
    "CANONICAL_HELPER_PATH="
    + CANONICAL_HELPER_PATH.as_posix()
)
print(
    "CANONICAL_HELPER_SHA256="
    + actual_helper_sha256
)
print("PRODUCTION_CONTRACT_FROZEN=NO")
print("PRODUCTION_TOOLCHAIN_FROZEN=NO")
print("PAYOUT_TRANSPORT_FROZEN=NO")
print("BLOCKCHAIN_WRITE_REQUIRED=NO")

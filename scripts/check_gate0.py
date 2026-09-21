#!/usr/bin/env python3

from __future__ import annotations

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

contract_files = [
    path
    for path in (ROOT / "contracts").rglob("*")
    if path.is_file() and path.name != ".gitkeep"
]

if contract_files:
    raise SystemExit(
        "production contract code appeared before Gate-0 freeze: "
        + ", ".join(str(p.relative_to(ROOT)) for p in contract_files)
    )

print("AEGISOS_GATE0_BASELINE=PASS")
print("PRODUCTION_CONTRACT_PRESENT=NO")
print("PRODUCTION_TOOLCHAIN_FROZEN=NO")
print("PAYOUT_TRANSPORT_FROZEN=NO")
print("BLOCKCHAIN_WRITE_REQUIRED=NO")

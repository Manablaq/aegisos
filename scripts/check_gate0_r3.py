#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EVIDENCE = (
    ROOT
    / "verification"
    / "bradbury"
    / "gate0-r3-d1-readonly.json"
)

EXPECTED_SHA = (
    "57219cfb6d8f0f19cd1c2ec5c2b40876d8322ee694742ad5a7b4c2b6c93d3620"
)

if not EVIDENCE.is_file():
    raise SystemExit("missing R3-D1 Bradbury evidence")

raw = EVIDENCE.read_bytes()
actual_sha = hashlib.sha256(raw).hexdigest()

if actual_sha != EXPECTED_SHA:
    raise SystemExit(
        f"R3-D1 evidence SHA mismatch: {actual_sha}"
    )

probe = json.loads(raw)

if probe.get("schema") != "AEGISOS_GATE0_R3_D1_V1":
    raise SystemExit("unexpected R3-D1 evidence schema")

if probe.get("read_only") is not True:
    raise SystemExit("R3-D1 evidence is not marked read-only")

if probe.get("signing_performed") is not False:
    raise SystemExit("R3-D1 unexpectedly reports signing")

if probe.get("blockchain_write_performed") is not False:
    raise SystemExit("R3-D1 unexpectedly reports blockchain write")

for endpoint in (
    "genlayer_rpc",
    "chain_rpc",
):
    info = probe["endpoints"][endpoint]

    if info["chain_id"] != 4221:
        raise SystemExit(
            f"{endpoint} chain ID mismatch"
        )

    if info["latest_block"]["gas_limit"] != 100000000:
        raise SystemExit(
            f"{endpoint} recorded block gas limit mismatch"
        )

for field in (
    "GENPerTimeUnit",
    "storageUnitPrice",
):
    for endpoint in (
        "genlayer_rpc",
        "chain_rpc",
    ):
        entry = probe["fee_views"][endpoint][field]

        if entry["supported"] is not True:
            raise SystemExit(
                f"stable Bradbury FeeManager view missing: "
                f"{endpoint} {field}"
            )

for field in (
    "quoteGasPrice",
    "messageFeeParamsBudgetFloor",
):
    for endpoint in (
        "genlayer_rpc",
        "chain_rpc",
    ):
        entry = probe["fee_views"][endpoint][field]

        if entry["supported"] is not False:
            raise SystemExit(
                f"v0.6-only FeeManager view unexpectedly marked "
                f"supported: {endpoint} {field}"
            )

implementation = (
    probe["eip1967"]["genlayer_rpc"]["implementation"].lower()
)

if implementation != (
    "0x31199772507933c5ad94da28ab7b02bf9c41069c"
):
    raise SystemExit(
        "recorded FeeManager implementation mismatch"
    )

if (
    probe["interpretation"]["v06_fee_views_supported"]
    != "NO"
):
    raise SystemExit(
        "R3-D1 did not record V06 fee views as unsupported"
    )

lock = json.loads(
    (ROOT / "toolchain" / "research-lock.json").read_text(
        encoding="utf-8"
    )
)

toolchain = lock.get("candidate_toolchain", {})

expected_toolchain = {
    "genlayer_py":
        "cf421edc0d20e567cc5a3b4da198fce61f1e579f",
    "genlayer_test":
        "9c09578b143905471fb0657dd53bdaf18da8e35f",
    "genvm_linter":
        "928bb51c42da8ff2512d81465d3e704f599aca47",
    "status":
        "CANDIDATE_BRADBURY_STABLE_ALIGNED",
}

if toolchain != expected_toolchain:
    raise SystemExit(
        "Bradbury-aligned toolchain candidate mismatch"
    )

baseline = lock.get("bradbury_runtime_baseline", {})

if baseline.get("evidence_sha256") != EXPECTED_SHA:
    raise SystemExit(
        "research lock R3 evidence SHA mismatch"
    )

if baseline.get("deployment_family") != "v0.5:9c68608":
    raise SystemExit(
        "unexpected Bradbury deployment family"
    )

if baseline.get("v06_fee_views_supported") is not False:
    raise SystemExit(
        "research lock incorrectly enables v0.6 fee views"
    )

for key in (
    "production_toolchain_frozen",
    "production_runner_frozen",
    "deployment_budget_frozen",
    "payout_transport_frozen",
):
    if lock.get(key) is not False:
        raise SystemExit(
            f"{key} must remain false after R3"
        )

contract_files = [
    p
    for p in (ROOT / "contracts").rglob("*")
    if p.is_file() and p.name != ".gitkeep"
]

if contract_files:
    raise SystemExit(
        "production contract code exists before Gate-0 freeze"
    )

print("AEGISOS_GATE0_R3_BASELINE=PASS")
print("BRADBURY_CHAIN_ID=4221")
print("OBSERVED_BLOCK_GAS_LIMIT=100000000")
print("BRADBURY_DEPLOYMENT_FAMILY=v0.5:9c68608")
print("STABLE_FEE_SURFACE=CONFIRMED")
print("V06_FEE_VIEWS_SUPPORTED=NO")
print("TOOLCHAIN_CANDIDATE=BRADBURY_STABLE_ALIGNED")
print("PRODUCTION_TOOLCHAIN_FROZEN=NO")
print("PRODUCTION_CONTRACT_PRESENT=NO")

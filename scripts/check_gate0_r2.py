#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = (
    "SETTLEMENT_ARCHITECTURE_V1.md",
    "TOOLCHAIN_CANDIDATE.md",
    "RUNTIME_COMPATIBILITY_MATRIX.md",
)

for name in REQUIRED_DOCS:
    path = ROOT / "docs" / name
    if not path.is_file():
        raise SystemExit(f"missing Gate-0 R2 document: {name}")

lock_path = ROOT / "toolchain" / "research-lock.json"
lock = json.loads(lock_path.read_text(encoding="utf-8"))

if lock.get("schema") != "AEGISOS_GATE0_RESEARCH_LOCK_V1":
    raise SystemExit("unexpected research-lock schema")

docs = lock.get("official_docs_revision", {})
if docs != {
    "repository": "genlayerlabs/genlayer-docs",
    "commit": "1cd8e2d11f743141b441be91ed65f321139814cc",
}:
    raise SystemExit("official documentation revision mismatch")

runner = lock.get("candidate_runner", {})
if runner != {
    "id": "py-genlayer",
    "hash": "1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6",
    "genvm_version": "v0.2.16",
    "genvm_bundle_sha256": "4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2",
    "status": "V0_2_16_DEFAULT_AND_CURRENT_DOCS_VERIFIED",
}:
    raise SystemExit("candidate runner mismatch")

toolchain = lock.get("candidate_toolchain", {})
if toolchain != {
    "genlayer_py": "cf421edc0d20e567cc5a3b4da198fce61f1e579f",
    "genlayer_test": "9c09578b143905471fb0657dd53bdaf18da8e35f",
    "genvm_linter": "928bb51c42da8ff2512d81465d3e704f599aca47",
    "status": "CANDIDATE_BRADBURY_STABLE_ALIGNED",
}:
    raise SystemExit("candidate toolchain mismatch")

settlement = lock.get("settlement_architecture", {})
expected_settlement = {
    "model": "ONE_GENLAYER_IC_PLUS_MINIMAL_EVM_SETTLEMENT_VAULT",
    "principal_in_genvm": False,
    "publication_value": 0,
    "publication_permissionless": True,
    "receiver_idempotency_required": True,
    "live_bradbury_certification_required": True,
    "status": "CANDIDATE",
}
if settlement != expected_settlement:
    raise SystemExit("settlement architecture mismatch")

# These remain deliberately unfrozen.
for key in (
    "production_toolchain_frozen",
    "production_runner_frozen",
    "deployment_budget_frozen",
    "payout_transport_frozen",
):
    if lock.get(key) is not False:
        raise SystemExit(f"{key} was frozen prematurely")

CANONICAL_CONTRACT_PATH = Path(
    "contracts/aegis_core.py"
)
CANONICAL_CONTRACT = ROOT / CANONICAL_CONTRACT_PATH
EXPECTED_CANONICAL_CONTRACT_SHA256 = (
    "26401d771d3c554dc848792a44c1df35c56955bae5fd4070b3a6273992621a51"
)

contract_files = sorted(
    (
        p
        for p in (ROOT / "contracts").rglob("*")
        if p.is_file() and p.name != ".gitkeep"
    ),
    key=lambda p: p.as_posix(),
)

if contract_files != [CANONICAL_CONTRACT]:
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

if (
    actual_contract_sha256
    != EXPECTED_CANONICAL_CONTRACT_SHA256
):
    raise SystemExit(
        "canonical AegisOS contract SHA-256 mismatch"
    )

print("AEGISOS_GATE0_R2=PASS")
print("SETTLEMENT_MODEL=ONE_IC_PLUS_MINIMAL_EVM_VAULT")
print("PRINCIPAL_IN_GENVM=NO")
print("EXTERNAL_PUBLICATION_VALUE=0")
print("PUBLICATION_RETRY_MODEL=PERMISSIONLESS_IDEMPOTENT")
print("CANONICAL_CONTRACT_PRESENT=YES")
print(
    "CANONICAL_CONTRACT_PATH="
    + CANONICAL_CONTRACT_PATH.as_posix()
)
print(
    "CANONICAL_CONTRACT_SHA256="
    + actual_contract_sha256
)
print("PRODUCTION_CONTRACT_FROZEN=NO")
print("BLOCKCHAIN_WRITE_REQUIRED=NO")

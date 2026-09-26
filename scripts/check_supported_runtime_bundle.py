#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "verification" / "supported_runtime"

EXPECTED = {
    ROOT / "contracts" / "aegis_core.py": "df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b",
    ROOT / "contracts" / "aegis_digest_helper.py": "624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73",
    ROOT / "tests" / "test_aegis_core_direct.py": "b3368fe053abe0fc1e2290b8b839f173b31e126ccc94a3e14ff3f2676962cab6",
    ROOT / "tests" / "conftest.py": "a5841fda3e29ec53714f0385ec5b217f19cb203a1ed19db89ad391e60f4c22d9",
    BASE / "contracts" / "aegis_core.py": "df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b",
    BASE / "contracts" / "aegis_digest_helper.py": "624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73",
    BASE / "contracts" / "aegis_stack_witness.py": "17eedc64edf915a178a379fc831118a3ffa8faeefc34acc7225abfdefa27bb7e",
    BASE / "contracts" / "aegis_stack_relay.py": "e0747eaf2fd847bedf4992aaa2a175714b010203a4c1ef17ef009246dce06962",
    BASE / "tests" / "test_r94_r14c9c_supported_runtime.py": "4fa940bbed6058f2f9f31e5fa7906e3fc202737e69c9043daf1360f676588a10",
    BASE / "gltest.config.yaml": "fca00eb484211ff73bfb55a1d6247a67d45d14eb3ba4a9efccafda815575270b",
    BASE / "requirements-lock.txt": "9857b82e02039a9e1549e106d876d9b2ed7154a832702285f65f0b84b315c869",
    BASE / "run_supported_runtime.sh": "9dde2da9cb512d4966b40e7c5cb97c726d882246d7c7d08a8114dc27eb5b8756",
}

for path, wanted in EXPECTED.items():
    if not path.is_file():
        raise SystemExit("missing certified artifact: " + str(path.relative_to(ROOT)))
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != wanted:
        raise SystemExit(
            "certified artifact SHA mismatch: "
            + str(path.relative_to(ROOT))
            + ": "
            + actual
        )

config_text = (BASE / "gltest.config.yaml").read_text(encoding="utf-8")
if "http://127.0.0.1:4101/api" not in config_text:
    raise SystemExit("supported-runtime RPC binding mismatch")
if "leader_only: false" not in config_text:
    raise SystemExit("supported-runtime leader_only mismatch")

test_text = (BASE / "tests" / "test_r94_r14c9c_supported_runtime.py").read_text(encoding="utf-8")
for marker in (
    "R94_R14C9C_FOREIGN_SENDER_REJECTION=PASS",
    "R94_R14C9C_REAL_CALLCONTRACT_STACK_SEMANTICS=PASS",
    "R94_R14C9C_CANDIDATE_STACK_GUARD_RUNTIME_BINDING=PASS",
    "R94_R14C9C_SUPPORTED_RUNTIME_PROOF=PASS",
    "decoded_transaction_error_evidence",
    "CalldataAddress",
):
    if marker not in test_text:
        raise SystemExit("supported-runtime marker missing: " + marker)

runner_text = (BASE / "run_supported_runtime.sh").read_text(encoding="utf-8")
for marker in (
    "I_EXPLICITLY_AUTHORIZE_LOCAL_SUPPORTED_RUNTIME_WRITES",
    "SUPPORTED_RUNTIME_TOOLCHAIN_GATE=PASS",
    "eth_chainId",
    '"0xf22f"',
    "AEGISOS_R94_R14C9C_ROOT",
):
    if marker not in runner_text:
        raise SystemExit("supported-runtime runner hardening marker missing: " + marker)

lock_text = (BASE / "requirements-lock.txt").read_text(encoding="utf-8")
if "/Users/" in lock_text or "file://" in lock_text:
    raise SystemExit("supported-runtime lock contains local filesystem reference")

print("AEGISOS_SUPPORTED_RUNTIME_BUNDLE_GATE=PASS")
print("SUPPORTED_RUNTIME_CHAIN_ID=61999")
print("SUPPORTED_RUNTIME_LEADER_ONLY=FALSE")
print("CANONICAL_CORE_SHA256=df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b")
print("CANONICAL_HELPER_SHA256=624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73")
print("SUPPORTED_RUNTIME_TEST_SHA256=4fa940bbed6058f2f9f31e5fa7906e3fc202737e69c9043daf1360f676588a10")

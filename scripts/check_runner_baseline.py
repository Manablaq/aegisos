#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNNER = (
    "1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6"
)

EXPECTED = {
    "runner-probe.py":
        "8c6ce8c285322268dc2996262822f8a31a42566fd7d8d78de9c2c827d603f865",
    "r5-r1-v0216-runner-index.json":
        "5cd081e136ea9e0e637bdfa93416fbd50df7fe903c66ecc6b8dd0c5985b648e0",
    "r5-r1-validate.json":
        "6cb32b7592022c8dea41519345dc2f8173128c751945112adaa5f8eaf48a7b28",
    "r5-r1-schema.json":
        "54522efbde5abe9240b1888cab914c78cf93f4820c07aea6758e4cfad22bb923",
    "r5-r2-typecheck.json":
        "23dda178344a1e4734041ea64d4582355199dfbb1be74dbf515bc4295d0af35d",
    "r5-r2-check.json":
        "c26315db7bb0fe11bc512d16aa7521918a609218bae32b499f03cf423fac3953",
    "r5-r2-schema.json":
        "54522efbde5abe9240b1888cab914c78cf93f4820c07aea6758e4cfad22bb923",
}

BASE = ROOT / "verification" / "runner"

for name, expected_sha in EXPECTED.items():
    path = BASE / name

    if not path.is_file():
        raise SystemExit(
            f"missing runner evidence: {name}"
        )

    actual_sha = hashlib.sha256(
        path.read_bytes()
    ).hexdigest()

    if actual_sha != expected_sha:
        raise SystemExit(
            f"runner evidence SHA mismatch: "
            f"{name}: {actual_sha}"
        )

baseline = json.loads(
    (BASE / "r5-runner-baseline.json").read_text(
        encoding="utf-8"
    )
)

if (
    baseline.get("schema")
    != "AEGISOS_GATE0_R5_RUNNER_BASELINE_V1"
):
    raise SystemExit(
        "unexpected runner baseline schema"
    )

if baseline.get("genvm_version") != "v0.2.16":
    raise SystemExit(
        "unexpected runner GenVM version"
    )

if baseline.get("genvm_bundle_sha256") != (
    "4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2"
):
    raise SystemExit(
        "unexpected GenVM bundle SHA"
    )

runner = baseline.get("runner", {})

if runner != {
    "id": "py-genlayer",
    "hash": RUNNER,
    "present_in_v0_2_16": True,
    "is_v0_2_16_default": True,
    "matches_pinned_current_docs": True,
}:
    raise SystemExit(
        "runner baseline identity mismatch"
    )

probe_text = (
    BASE / "runner-probe.py"
).read_text(encoding="utf-8")

expected_header = (
    '# { "Depends": "py-genlayer:'
    + RUNNER
    + '" }'
)

if not probe_text.startswith(
    expected_header + "\n"
):
    raise SystemExit(
        "runner probe dependency header mismatch"
    )

index = json.loads(
    (
        BASE
        / "r5-r1-v0216-runner-index.json"
    ).read_text(encoding="utf-8")
)

if index.get("linter_default_runner") != RUNNER:
    raise SystemExit(
        "v0.2.16 default runner mismatch"
    )

if index.get("docs_runner") != RUNNER:
    raise SystemExit(
        "pinned docs runner mismatch"
    )

if index.get("docs_runner_present") is not True:
    raise SystemExit(
        "runner absent from v0.2.16 index"
    )

validate = json.loads(
    (
        BASE / "r5-r1-validate.json"
    ).read_text(encoding="utf-8")
)

if validate.get("ok") is not True:
    raise SystemExit(
        "preserved runner validation is not successful"
    )

typecheck = json.loads(
    (
        BASE / "r5-r2-typecheck.json"
    ).read_text(encoding="utf-8")
)

if typecheck.get("ok") is not True:
    raise SystemExit(
        "preserved runner typecheck is not successful"
    )

if typecheck.get("diagnostics") != []:
    raise SystemExit(
        "preserved runner typecheck has diagnostics"
    )

check = json.loads(
    (
        BASE / "r5-r2-check.json"
    ).read_text(encoding="utf-8")
)

if check.get("ok") is not True:
    raise SystemExit(
        "preserved full runner check is not successful"
    )

if check.get("lint", {}).get("ok") is not True:
    raise SystemExit(
        "preserved runner lint component failed"
    )

if check.get("validate", {}).get("ok") is not True:
    raise SystemExit(
        "preserved runner semantic component failed"
    )

schema = json.loads(
    (
        BASE / "r5-r2-schema.json"
    ).read_text(encoding="utf-8")
)

if schema.get("ok") is not True:
    raise SystemExit(
        "preserved runner schema is not successful"
    )

methods = (
    schema.get("schema", {})
    .get("methods", {})
)

if set(methods) != {
    "get_value",
    "set_value",
}:
    raise SystemExit(
        "unexpected runner probe ABI"
    )

lock = json.loads(
    (
        ROOT / "toolchain" / "research-lock.json"
    ).read_text(encoding="utf-8")
)

expected_candidate = {
    "id": "py-genlayer",
    "hash": RUNNER,
    "genvm_version": "v0.2.16",
    "genvm_bundle_sha256":
        "4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2",
    "status":
        "V0_2_16_DEFAULT_AND_CURRENT_DOCS_VERIFIED",
}

if lock.get("candidate_runner") != expected_candidate:
    raise SystemExit(
        "research-lock candidate runner mismatch"
    )

if lock.get("production_runner_frozen") is not False:
    raise SystemExit(
        "production runner frozen prematurely"
    )

print("AEGISOS_RUNNER_BASELINE_GATE=PASS")
print(
    "RUNNER=py-genlayer:"
    + RUNNER
)
print("GENVM_VERSION=v0.2.16")
print("V0216_DEFAULT_RUNNER=YES")
print("CURRENT_DOCS_RUNNER_MATCH=YES")
print("LOCAL_LINT=PASS")
print("LOCAL_SEMANTIC_VALIDATION=PASS")
print("LOCAL_SCHEMA_EXTRACTION=PASS")
print("LOCAL_TYPECHECK=PASS")
print("PRODUCTION_RUNNER_FROZEN=NO")

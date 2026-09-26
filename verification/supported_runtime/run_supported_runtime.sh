#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
EXPECTED_LOCK_SHA="9857b82e02039a9e1549e106d876d9b2ed7154a832702285f65f0b84b315c869"

scrub() {
  "$PYTHON_BIN" - "$ROOT/evidence" <<'PY' >/dev/null 2>&1 || true
from pathlib import Path
import json
import sys

root = Path(sys.argv[1])

for path in root.glob("*.json"):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        continue

    def clean(value):
        if isinstance(value, dict):
            return {
                key: clean(child)
                for key, child in value.items()
                if key not in {"private_key", "privateKey"}
            }
        if isinstance(value, list):
            return [clean(child) for child in value]
        return value

    path.write_text(
        json.dumps(clean(obj), sort_keys=True, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
PY
  rm -f "$ROOT/.env"
}

trap scrub EXIT

if [ "${I_EXPLICITLY_AUTHORIZE_LOCAL_SUPPORTED_RUNTIME_WRITES:-}" != "YES" ]; then
  echo "STOP: set I_EXPLICITLY_AUTHORIZE_LOCAL_SUPPORTED_RUNTIME_WRITES=YES to run local supported-runtime writes"
  exit 2
fi

test -x "$PYTHON_BIN" || {
  echo "STOP: PYTHON_BIN is not executable: $PYTHON_BIN"
  exit 1
}

ACTUAL_LOCK_SHA="$(
  "$PYTHON_BIN" - "$ROOT/requirements-lock.txt" <<'PY'
from pathlib import Path
import hashlib
import sys

print(hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest())
PY
)"

test "$ACTUAL_LOCK_SHA" = "$EXPECTED_LOCK_SHA" || {
  echo "STOP: supported-runtime requirements lock SHA mismatch"
  exit 1
}

"$PYTHON_BIN" - <<'PY'
from importlib.metadata import version
import sys

if sys.version_info[:2] != (3, 12):
    raise SystemExit(f"Python 3.12 required, found {sys.version.split()[0]}")

expected = {
    "genlayer-test": "0.24.0",
    "genlayer-py": "0.9.0",
    "pytest": "9.0.2",
    "web3": "7.14.1",
    "eth-account": "0.13.7",
}

for package, wanted in expected.items():
    got = version(package)
    print(f"SUPPORTED_RUNTIME_TOOL::{package}={got}")
    if got != wanted:
        raise SystemExit(f"{package} version mismatch: {got} != {wanted}")

print("SUPPORTED_RUNTIME_TOOLCHAIN_GATE=PASS")
PY

"$PYTHON_BIN" - <<'PY'
import json
import urllib.request

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "eth_chainId",
    "params": [],
}

request = urllib.request.Request(
    "http://127.0.0.1:4101/api",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)

with urllib.request.urlopen(request, timeout=10) as response:
    body = json.loads(response.read())

if body.get("result") != "0xf22f":
    raise SystemExit(f"supported runtime chain mismatch: {body}")

print("SUPPORTED_RUNTIME_CHAIN_ID=61999")
print("SUPPORTED_RUNTIME_RPC_PREFLIGHT=PASS")
PY

mkdir -p "$ROOT/evidence"
: > "$ROOT/.env"
cd "$ROOT"

AEGISOS_R94_R14C9C_ROOT="$ROOT" \
PYTHONDONTWRITEBYTECODE=1 \
"$PYTHON_BIN" -m pytest \
  tests/test_r94_r14c9c_supported_runtime.py \
  -s \
  -vv

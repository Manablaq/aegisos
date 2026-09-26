# AegisOS supported-runtime verification

This directory preserves the reproducible multi-validator runtime proof for the exact R94 Core and digest-helper source hashes.

It is a **verification bundle**, not a second product implementation. The canonical product contracts remain:

- `../../contracts/aegis_core.py`
- `../../contracts/aegis_digest_helper.py`

The local supported runtime uses chain ID `61999` (`0xf22f`), JSON-RPC at `http://127.0.0.1:4101/api`, and `leader_only: false`.

## Purpose

The proof exercises runtime properties that Direct Mode alone cannot establish:

- direct bound-authority sender acceptance;
- foreign-sender `BOUND_AUTHORITY_ONLY` rejection;
- top-level call-stack depth `0`;
- nested `call_contract` stack depth greater than `0`;
- exact binding of the R94 direct-authority stack guard.

The test-only `aegis_stack_witness.py` and `aegis_stack_relay.py` contracts exist solely for those runtime checks.

## Running

Use Python 3.12 in an isolated environment and install the exact local lock.

The test performs local supported-runtime writes, so it fails closed unless explicit local authorization is supplied:

```sh
PYTHON_BIN=/path/to/venv/bin/python I_EXPLICITLY_AUTHORIZE_LOCAL_SUPPORTED_RUNTIME_WRITES=YES ./run_supported_runtime.sh
```

Generated evidence is scrubbed for `private_key` / `privateKey` fields on exit.

## Certified identities

- canonical R94 Core SHA-256:
  `df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b`
- pure digest helper SHA-256:
  `624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73`
- executed Phase-1 test SHA-256:
  `b104040655a74112ca6063d43a0814f06f2f38eedd2f8cec95aa9e3e5c02e856`
- repository-normalized test SHA-256:
  `4fa940bbed6058f2f9f31e5fa7906e3fc202737e69c9043daf1360f676588a10`
- rejection classification SHA-256:
  `0924a4d52f71644cfe5d24d8f39bff1e5e8a6c38e62fe6133bbdf32f8d8efc12`
- pytest log SHA-256:
  `51290fdfcdda7f992f0092446ad540da7204ce5cdf6e8a3f77fd3c4aaf65fc83`
- finality-status SHA-256:
  `a96a9feb045d0dcab29c8215ed506e415d0b48e8c31a80dcb76692e12db4aa03`

Bradbury deployment/finality is independently documented in `../../docs/BRADBURY_VERIFICATION.md`.

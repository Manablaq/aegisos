# AegisOS supported-runtime verification

This directory preserves a repository-normalized, Python-AST-identical copy of the AegisOS R94 multi-validator supported-runtime test that completed Phase 1. The exact executed Phase-1 bytes remain identified below by their historical SHA-256.

It is intentionally separate from Bradbury live verification. The certified local runtime uses chain ID `61999` (`0xf22f`) and JSON-RPC at `http://127.0.0.1:4101/api` with `leader_only: false`.

## Runtime baseline

The Phase-1 proof used the GenLayer Studio simulator service family `v0.121.15`, GenVM webdriver `0.0.9`, and a compatible Hardhat backend. The runtime must already be healthy before this runner is invoked.

## Python environment

Use Python 3.12 in an isolated virtual environment and install the exact dependencies in `requirements-lock.txt`.

## Running

The test performs local supported-runtime writes, so the runner fails closed unless explicit authorization is supplied:

```sh
PYTHON_BIN=/path/to/venv/bin/python \
I_EXPLICITLY_AUTHORIZE_LOCAL_SUPPORTED_RUNTIME_WRITES=YES \
./run_supported_runtime.sh
```

The runner verifies the release-matched client versions and chain ID before any pytest write path executes. Generated JSON evidence is scrubbed for `private_key` / `privateKey` fields on exit.

## Certified Phase-1 identities

- canonical R94 core SHA-256: `df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b`
- pure digest helper SHA-256: `624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73`
- Phase-1 executed supported-runtime test SHA-256: `b104040655a74112ca6063d43a0814f06f2f38eedd2f8cec95aa9e3e5c02e856`
- repository-normalized supported-runtime test SHA-256: `4fa940bbed6058f2f9f31e5fa7906e3fc202737e69c9043daf1360f676588a10`
- normalization: removed one trailing ASCII space from line 840 only; Python AST unchanged
- Phase-1 rejection classification SHA-256: `0924a4d52f71644cfe5d24d8f39bff1e5e8a6c38e62fe6133bbdf32f8d8efc12`
- Phase-1 pytest log SHA-256: `51290fdfcdda7f992f0092446ad540da7204ce5cdf6e8a3f77fd3c4aaf65fc83`
- Phase-1 finality status SHA-256: `a96a9feb045d0dcab29c8215ed506e415d0b48e8c31a80dcb76692e12db4aa03`

Phase 1 proved the foreign-sender `BOUND_AUTHORITY_ONLY` rejection, direct stack depth `0`, nested `call_contract` stack depth greater than `0`, and finalization of all local proof transactions. It does not claim Bradbury deployment or Bradbury finality.

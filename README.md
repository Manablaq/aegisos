# AegisOS

**Verifiable Autonomous Agreement & Settlement Protocol**

AegisOS is a GenLayer Intelligent Contract protocol for autonomous agreements, evidence-bound adjudication, escrow, finality-gated settlement, recovery, reputation, and agent-to-agent coordination.

## Current status

**R94 repository-promotion candidate — local Direct Mode and supported-runtime certification complete; live Bradbury release admission remains pending.**

The canonical implementation is split across:

- `contracts/aegis_core.py` — stateful AegisOS Core, SHA-256 `df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b`;
- `contracts/aegis_digest_helper.py` — stateless pure digest helper, SHA-256 `624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73`.

The repository Direct Mode suite is `tests/test_aegis_core_direct.py` with its canonical fixture in `tests/conftest.py`. It contains nine proofs covering bound-sender authority enforcement, divergent-origin top-level compatibility, nonempty-call-stack rejection, exact `CREATOR` and `COUNTERPARTY` consequences, the non-settling `REPAIR` path, validator disagreement, and malformed/error result rejection.

A repository-normalized, Python-AST-identical copy of the Phase-1 multi-validator supported-runtime harness is preserved under `verification/supported_runtime/`. The bundle README records both the exact executed Phase-1 test SHA-256 and the normalized repository test SHA-256. Phase 1 proved the foreign-sender `BOUND_AUTHORITY_ONLY` rejection and real nested `call_contract` stack semantics on local chain ID `61999`, with all proof writes finalized.

This certification does **not** claim Bradbury deployment, Bradbury validator finality, production toolchain freeze, deployment-budget freeze, or payout-transport freeze. Those remain separate release gates.

The development rule remains:

> Research and certify the execution envelope first. Implement inside that envelope second. Deploy only after reproducible admission checks pass.

## Constitutional principles

AegisOS is designed around the following non-negotiable properties:

- no consequential action without the required finality;
- no hidden administrator verdict;
- no mutable evidence authority after agreement activation;
- no stale or replayed evidence;
- no approximate consensus for consequential values;
- no duplicate economic consequence;
- no indefinite value lock;
- temporary evidence failure must remain recoverable where policy permits;
- deployment must fail closed when the target runtime cannot be proven safe.

See `docs/` on the Gate-0 branch for the engineering specification.

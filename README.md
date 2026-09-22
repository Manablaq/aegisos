# AegisOS

**Verifiable Autonomous Agreement & Settlement Protocol**

AegisOS is a GenLayer Intelligent Contract protocol for autonomous agreements, evidence-bound adjudication, escrow, finality-gated settlement, recovery, reputation, and agent-to-agent coordination.

## Current status

**Gate 0 — certified implementation candidate; live release admission remains pending.**

The canonical AegisOS Core implementation now exists at
`contracts/aegis_core.py`.

Current local certification binds that file to SHA-256
`26401d771d3c554dc848792a44c1df35c56955bae5fd4070b3a6273992621a51` and verifies it against the pinned
Bradbury-compatible GenVM `v0.2.16` execution surface.

The repository-relative Direct Mode suite is
`tests/test_aegis_core_direct.py`. It covers bound-authority enforcement,
direct-origin rejection, exact `CREATOR` and `COUNTERPARTY` consequences,
the non-settling `REPAIR` path, validator disagreement, and malformed/error
result rejection.

This local certification does **not** claim live Bradbury deployment,
validator finality, production toolchain freeze, deployment-budget freeze,
or payout-transport freeze. Those remain separate release gates.

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

# AegisOS

**Verifiable Autonomous Agreement & Settlement Protocol**

AegisOS is a GenLayer Intelligent Contract protocol for autonomous agreements, evidence-bound adjudication, escrow, finality-gated settlement, recovery, reputation, and agent-to-agent coordination.

## Current status

**Gate 0 — GenLayer engineering-envelope certification.**

Production Intelligent Contract implementation has intentionally not started.

AegisOS will first freeze:

- the exact Bradbury-compatible execution surface;
- deployment and resource budgets;
- consensus and evidence rules;
- economic/finality invariants;
- recovery and liveness guarantees;
- the exact pinned toolchain;
- reproducible reviewer and release gates.

The development rule is:

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

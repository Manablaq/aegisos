# AegisOS Architecture

## Purpose

AegisOS is a reusable GenLayer Intelligent Contract protocol for agreements whose outcome depends on authenticated evidence and validator reasoning.

The design separates three concerns:

1. **Agreement state** — deterministic participant, policy, evidence, challenge, recovery, and decision records.
2. **Reasoning** — GenLayer nondeterministic execution constrained to a small outcome surface.
3. **Digest construction** — deterministic pure hashing delegated to a stateless helper.

The R94 release intentionally does not combine asset custody with adjudication.

## Components

### AegisOS Core

Canonical source: `contracts/aegis_core.py`

SHA-256:

`df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b`

Bradbury address:

`0x532de68bd897529c06803efed843d814b1744ba0`

The Core owns all mutable protocol state:

- agreement registry;
- authority attestations;
- evidence generation;
- evidence-set commitment;
- challenge state;
- recovery deadline;
- final decision fields;
- used-decision replay protection.

### AegisPureDigestHelper

Canonical source: `contracts/aegis_digest_helper.py`

SHA-256:

`624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73`

Bradbury address:

`0xf557028b465a6f87ae76b0f520edb2b3e6e4eec9`

The helper is stateless. It has no mutable agreement state, authority role, adjudication role, economic authority, administrator capability, or nondeterministic reasoning.

The Core supplies every input to the helper explicitly.

## Reusable agreement record

Each agreement contains its own creator, counterparty, policy hash, authority-set hash, primary authority, corroborating authority, maximum evidence age, challenge-window duration, recovery deadline, principal reference amount, evidence state, final outcome/consequence, beneficiary and entitlement, and decision nonce/digest.

The contract therefore supports multiple independent agreements without redeployment.

## State machine

| Code | Meaning |
| ---: | --- |
| `1` | draft |
| `2` | active |
| `3` | challenge window |
| `4` | challenged |
| `5` | repair required |
| `7` | decision recorded |

There is no semantic state assigned to code `6` in R94.

### Normal path

```text
DRAFT
  ↓ counterparty acceptance
ACTIVE
  ↓ two authority attestations + evidence binding
CHALLENGE_WINDOW
  ├── challenge → CHALLENGED
  └── no challenge
        ↓
ADJUDICATION
  ├── CREATOR      → DECISION_RECORDED
  ├── COUNTERPARTY → DECISION_RECORDED
  └── REPAIR       → REPAIR_REQUIRED
```

A repair generation can submit fresh authority attestations and re-enter the evidence-binding path while the recovery horizon remains open.

### Recovery path

Any unresolved agreement can be expired only after its bound recovery deadline.

```text
unresolved + recovery deadline reached
        ↓
expired refund
        ↓
DECISION_RECORDED
beneficiary = creator
entitlement = principal reference amount
```

This liveness path was finalized on Bradbury in the R94 verification.

## Evidence architecture

Authority attestations bind:

- authority address and role;
- evidence record ID;
- evidence record version;
- immutable source reference;
- evidence payload hash;
- source content hash;
- publication time;
- expiry time;
- generation.

The Core requires separate primary and corroborating authorities and rejects evidence pairs that reuse the same record ID or immutable source reference.

Evidence is accepted only when it is fresh enough and remains valid beyond the challenge window.

## Adjudication architecture

Before nondeterministic reasoning, the Core deterministically verifies policy/authority preimages, both bound attestations, evidence generation, authority identity, record/source independence, freshness, expiry, evidence payload preimages, evidence-set commitment, and the challenge preimage when challenged.

The model receives authority/evidence material as explicitly untrusted data.

The permitted result is exactly one token:

- `CREATOR`;
- `COUNTERPARTY`;
- `REPAIR`.

A validator independently evaluates the same prompt and accepts the leader result only on exact equality.

The final consequence is deterministic after that exact result.

## Decision architecture

A final decision records:

- outcome code;
- consequence code;
- beneficiary;
- entitlement amount;
- incremented decision nonce;
- deterministic decision digest.

The digest is marked in `used_decisions` to prevent replay.

Outcome codes:

| Code | Meaning |
| ---: | --- |
| `1` | creator |
| `2` | counterparty |
| `3` | expired refund |

Consequence codes:

| Code | Meaning |
| ---: | --- |
| `1` | creator entitlement |
| `2` | counterparty entitlement |

The R94 constant names retain `PAY_*` terminology, but the Core records entitlement state; it does not itself transport funds.

## ABI compatibility

The deployed source retains the historical `*_probe` method suffix and `AegisKernelBoundaryProbe` class name.

These identifiers are frozen because the exact source hash is part of the live Bradbury evidence. Renaming them would create a different release.

See [API](API.md) for the product-level interpretation of the deployed ABI.

## Non-product verification contracts

`verification/supported_runtime/contracts/aegis_stack_witness.py` and `aegis_stack_relay.py` exist only to reproduce runtime stack semantics. They are not part of AegisOS protocol state and are not deployed product components.

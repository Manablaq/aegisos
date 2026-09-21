# AegisOS State Machine V1

Status: **CANDIDATE — PAYOUT TRANSPORT NOT YET FROZEN**

The state machine separates agreement judgment from payout transport.

## Primary lifecycle

`DRAFT`

→ `FUNDED`

→ `ACTIVE`

→ `SUBMITTED`

→ `CHALLENGED` or `ACCEPTANCE_PENDING`

→ `REVIEW_PENDING`

→ `DECIDED`

→ `FINALIZED_ENTITLEMENT`

→ `WITHDRAWABLE`

→ `SETTLED`

## Recovery branches

The protocol also needs explicit bounded states for:

- `EVIDENCE_REPAIR`;
- `EXPIRED`;
- `REFUNDABLE`;
- `CANCELLED`.

No value-holding state may omit a transition deadline or recovery rule.

## Important separation

`FINALIZED_ENTITLEMENT` means the consequential right has been finalized.

It does NOT mean an arbitrary external transfer has already succeeded.

This separation prevents payout transport failure from destroying adjudication
liveness.

## Replay rule

A final consequence is keyed by an immutable decision nonce.

The same finalized decision nonce cannot:

- create a second entitlement;
- pay twice;
- be applied to another agreement;
- be reused under another policy revision.

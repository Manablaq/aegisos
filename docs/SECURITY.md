# AegisOS Security Model

## Security objective

AegisOS is designed so that consequential agreement state cannot be changed by an unbound administrator, stale evidence, a single uncorroborated source, approximate validator agreement, or an indefinitely blocked workflow.

## Core invariants

### No administrator verdict

R94 exposes no owner method that can choose a winner, overwrite a decision, redirect an entitlement, or bypass the challenge/recovery lifecycle.

### Frozen agreement trust commitments

At creation, each agreement binds its policy hash, authority-set hash, primary/corroborating authorities, evidence-age bound, challenge duration, and recovery deadline.

### Sender-bound authorities

An attestation is accepted only from the address bound to its authority role. Primary and corroborating authority addresses must be distinct.

R94 also rejects nested contract calls for authority attestations through the direct-transaction stack guard.

### Independent corroboration

Primary and corroborating evidence cannot reuse the same evidence record ID or immutable source reference.

### Freshness and expiry

The Core checks publication time, maximum evidence age, record expiry, and that bound evidence survives the challenge window.

### Exact evidence commitments

The Core re-verifies policy, authority, evidence payload, evidence-set, generation, and challenge commitments before adjudication.

### Prompt-injection boundary

Authority metadata, evidence payloads, source references, and challenge data are explicitly presented as untrusted data, never instructions.

Deterministic state/cryptographic checks remain the authorization boundary.

### Exact consequential consensus

The allowed reasoning result is the closed set `CREATOR`, `COUNTERPARTY`, or `REPAIR`.

A validator independently evaluates the same surface and requires exact equality with the leader result. There is no numeric tolerance for beneficiary or entitlement selection.

### Repair instead of unsafe settlement

`REPAIR` is non-settling. It permits a later evidence generation while the recovery horizon remains open.

### Replay protection

Every final decision increments the decision nonce, commits consequential fields into a deterministic digest, and marks that digest used.

### Bounded liveness

Every agreement has a recovery deadline. An unresolved agreement can be deterministically expired after that deadline.

The live Bradbury proof demonstrates this path reaches natural finality.

### Consequence bounds

Entitlement cannot be negative or exceed the principal reference amount.

## Trust assumptions

R94 assumes agreement creators correctly choose their counterparty, participants commit the intended policy/authority set, bound authority addresses correspond to intended entities, and adjudication preimages are supplied exactly.

The contract deliberately does not infer authority trust from a URL alone.

## Asset-custody boundary

R94 does not implement token custody or payout transport.

Any future custody/withdrawal layer must independently prove deposit accounting, solvency, authorization, exactly-once withdrawal, failed-transfer recovery, replay protection, and no administrator diversion path.

That would be a new release scope and require new live verification.

## Verification layers

AegisOS uses three complementary verification layers:

1. **Direct Mode** — deterministic contract behavior and adversarial state cases.
2. **Supported runtime** — multi-validator/runtime boundary behavior, including authority sender and nested call-stack semantics.
3. **Bradbury live proof** — deployment identity, transaction submission, natural finalization, execution result, and terminal state.

See [BRADBURY_VERIFICATION.md](BRADBURY_VERIFICATION.md).

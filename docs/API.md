# AegisOS R94 API

This document describes the public interface of the Bradbury-verified R94 Intelligent Contract.

## ABI naming note

R94 was deployed while the engineering interface still used `*_probe` names. The source hash is now evidence-bound, so those method names are retained for compatibility.

The methods below are production agreement operations despite the historical suffix.

## Constructor

### `__init__(h: Address)`

Binds the stateless `AegisPureDigestHelper` address.

Bradbury helper:

`0xf557028b465a6f87ae76b0f520edb2b3e6e4eec9`

## Agreement operations

### `create_probe(...)`

**Protocol meaning:** create agreement.

Parameters:

- `agreement_id: str`
- `counterparty: str`
- `policy_hash: str`
- `authority_set_hash: str`
- `primary_authority: str`
- `corroborating_authority: str`
- `principal_amount: int`
- `challenge_window_seconds: int`
- `max_evidence_age_seconds: int`
- `recovery_deadline: int`

The caller becomes the creator. Agreement ID, hash format, participants, authority independence, timing bounds, and principal reference amount are validated before storage.

### `accept_probe(agreement_id)`

**Protocol meaning:** accept agreement.

Only the bound counterparty may accept. Acceptance is rejected after the recovery deadline or after a decision has already been recorded.

### `expire_probe(agreement_id)`

**Protocol meaning:** execute deadline recovery.

Callable only after the recovery deadline and only while no final decision has been recorded.

R94 deterministically records the expired-refund outcome, creator consequence, creator beneficiary, and entitlement equal to the principal reference amount.

### `attest_evidence_probe(...)`

**Protocol meaning:** submit authority attestation.

Roles:

- `1` — primary authority;
- `2` — corroborating authority.

The transaction sender must exactly match the authority bound to that role. R94 also requires a direct authority transaction by rejecting nonempty call stacks.

### `get_attestation(agreement_id, role)`

Returns the stored authority attestation for the requested role.

### `bind_evidence_probe(agreement_id, generation)`

**Protocol meaning:** bind corroborated evidence.

Only an agreement participant may call it. The Core requires both authority attestations and verifies role, authority, exact generation, record/source independence, freshness, and expiry beyond the challenge window.

### `challenge_probe(agreement_id, challenge_hash)`

**Protocol meaning:** challenge the agreement evidence/decision path.

Only a participant may challenge, and only during the challenge window.

### `adjudicate_probe(...)`

**Protocol meaning:** evidence-bound GenLayer adjudication.

Parameters:

- `agreement_id`
- `policy_text`
- `authority_text`
- `primary_evidence_text`
- `corroborating_evidence_text`
- `challenge_text`

The Core verifies all committed preimages and evidence metadata before nondeterministic reasoning.

The only valid results are:

- `CREATOR`;
- `COUNTERPARTY`;
- `REPAIR`.

Validators independently evaluate the same closed result surface and require exact agreement.

`REPAIR` does not settle the agreement. It moves the record into repair-required state so a newer evidence generation can be supplied.

## Views

### `get_probe(agreement_id)`

**Protocol meaning:** get agreement.

Important final fields include `state`, `outcome_code`, `consequence_code`, `beneficiary`, `entitlement_amount`, `decision_nonce`, `decision_digest`, and `decision_recorded`.

## Error philosophy

The contract fails closed. Representative errors include:

- `AGREEMENT_NOT_FOUND`
- `AGREEMENT_EXISTS`
- `DECISION_ALREADY_RECORDED`
- `RECOVERY_DEADLINE_REACHED`
- `PARTICIPANT_ONLY`
- `COUNTERPARTY_ONLY`
- `BOUND_AUTHORITY_ONLY`
- `DIRECT_AUTHORITY_TRANSACTION_REQUIRED`
- `CORROBORATION_RECORD_NOT_INDEPENDENT`
- `CORROBORATION_SOURCE_NOT_INDEPENDENT`
- `EVIDENCE_TOO_OLD`
- `EVIDENCE_EXPIRED`
- `DECISION_REPLAY`

## Economic scope

The API records principal reference amounts and finalized entitlements.

It does not expose a token deposit, withdrawal, or transfer method in R94. Applications integrating R94 must not describe those accounting fields as proof that assets are held by the Core.

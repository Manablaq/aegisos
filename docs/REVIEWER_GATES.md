# Reviewer Gates

Status: **MANDATORY**

AegisOS cannot be called reviewer-ready until all applicable gates pass.

## Architecture

- compact Bradbury-compatible contract architecture;
- no undocumented runtime dependency;
- no critical `chain:` module loading dependency on an uncertified runtime;
- no hidden privileged adjudication path.

## Consensus

- leader produces a bounded structured decision;
- validators independently verify/reproduce the consequential decision;
- no validator that merely validates shape or JSON syntax;
- exact agreement on consequential values.

## Evidence

- authority identity binding;
- immutable/versioned evidence;
- stable evidence IDs;
- explicit freshness;
- explicit expiry;
- explicit corroboration;
- replay prevention;
- repairable evidence failures.

## Liveness

- bounded challenge period;
- bounded evidence-repair period;
- expiry/refund path;
- no indefinite locked value;
- payout failure cannot erase a finalized entitlement.

## Economic correctness

- consequence only after the required finality;
- exact beneficiary;
- exact amount;
- exact accounting;
- duplicate/replay resistance;
- recipient balance effect proven in live evidence where applicable.

## Runtime

- lint/typecheck;
- schema generation;
- deterministic unit tests;
- Direct Mode;
- adversarial/security suite;
- supported-runtime verification;
- exact deployment-payload measurement;
- Bradbury read-only admission preflight;
- live deployment finality;
- source parity.

## Release reproducibility

Evidence must preserve:

- source SHA-256;
- repository commit/tree;
- toolchain commits;
- runner pin;
- transaction IDs;
- raw relevant RPC responses before decoding;
- final transaction state;
- actual economic/state consequence.

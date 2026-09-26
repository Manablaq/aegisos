# AegisOS Architecture V1

Status: **GATE-0 CANDIDATE**

## Objective

AegisOS is a flagship GenLayer protocol centered on a stateful Core Intelligent Contract plus a stateless pure digest helper for:

- autonomous agreements;
- multi-party mandates;
- milestones;
- bounded agent authority;
- evidence-bound adjudication;
- challenges;
- repairable evidence failures;
- escrow accounting;
- finalized entitlements;
- recovery;
- replay protection;
- reputation primitives.

The implementation must remain compact enough for reliable Bradbury admission.

## Architectural rule

Feature richness will be achieved primarily through a data-driven protocol
kernel, not through dozens of bespoke public methods.

AegisOS Core is intended to contain:

1. agreement registry;
2. policy bindings;
3. milestone/state machine;
4. evidence metadata;
5. adjudication entry point;
6. decision/entitlement ledger;
7. challenge/repair state;
8. timeout/recovery state;
9. replay protection;
10. bounded reputation counters.

Product-level templates are encoded as bounded policy data rather than separate
contract implementations.

### Stateless pure digest helper

The R94 implementation splits deterministic digest construction into `AegisPureDigestHelper`. The helper has no mutable protocol state, no nondeterministic execution, no adjudication authority, no economic authority, and no upgrade role. The Core binds the helper address and supplies every digest input explicitly.

This split was Direct Mode certified and separately exercised through a real supported-runtime cross-contract path.

## No runtime module dependency

The first Bradbury release MUST NOT require:

- chain-loaded Python modules;
- child-contract factories;
- synchronous cross-IC reads for critical state;
- undocumented runtime behavior.

The stateless digest helper does not relax this rule: it is not a source of critical state. It is a deterministic pure-computation boundary whose cross-contract semantics are independently runtime-tested.

If a future Bradbury runtime is proven to support safer modularity, that can be
evaluated as a separate version.

## No admin adjudication path

There is no owner method that may:

- choose a dispute winner;
- change a live agreement outcome;
- redirect somebody else's entitlement;
- replace an evidence authority after activation;
- bypass a challenge window;
- mark an unresolved case finalized.

Any administrative surface that survives Gate 0 must be non-consequential and
explicitly documented.

## Upgrade philosophy

The target is an immutable canonical release.

Upgradeability is not assumed to be safe merely because the runtime supports it.

If temporary upgrader authority is used during pre-release validation, the
canonical release cannot be called immutable until that authority is
cryptographically and on-chain proven to be removed/frozen.

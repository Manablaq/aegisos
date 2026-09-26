# AegisOS Settlement Architecture V1

Status: **GATE-0 CANDIDATE — LIVE BRADBURY CERTIFICATION REQUIRED**

## 1. Design decision

AegisOS v1 uses two GenLayer Intelligent Contracts with sharply separated roles: the stateful AegisOS Core and a stateless pure digest helper.

The helper owns no protocol state, value, evidence authority, or adjudication authority. It deterministically computes canonical digest material for the Core.

Economic custody remains intentionally separated into a minimal EVM settlement vault. The vault is not a GenLayer Intelligent Contract and contains no AI, evidence interpretation, policy reasoning, or adjudication.

Responsibilities are deliberately separated:

### AegisOS Core Intelligent Contract

Owns:

- agreement state;
- frozen policy;
- authority bindings;
- evidence metadata;
- challenges;
- evidence repair;
- consensus adjudication;
- finalized decisions;
- decision nonces;
- reputation/accounting metadata.

### AegisOS Pure Digest Helper

Owns no mutable protocol state. It only exposes deterministic view methods used by the Core to compute evidence-pair and agreement/decision digests from explicit inputs.

The helper cannot choose an outcome, mutate an agreement, hold escrow, or authorize settlement.

### Settlement Vault

Owns only:

- escrowed GEN;
- exact escrow accounting;
- finalized beneficiary credits;
- withdrawal accounting;
- replay/idempotency protection.

The vault never decides who should receive money.

Only a finalized AegisOS decision can authorize settlement.

## 2. Why principal does not live in GenVM

Current GenLayer documentation distinguishes Intelligent Contract state from the
chain-layer ghost contract and message system.

Value-bearing child/message execution creates additional failure and recovery
semantics.

AegisOS therefore does not make economic correctness depend on a value-bearing
GenVM child message succeeding.

Principal remains in the EVM vault until an exact finalized entitlement has
been published.

## 3. Bootstrap sequence

The target deployment sequence is:

1. deploy and finalize the stateless AegisOS Pure Digest Helper;

2. deploy AegisOS Core with:
   - the finalized helper address bound in the constructor;
   - no vault bound;
   - one temporary bootstrap address;
   - all user agreement activation disabled while unbound;

3. finalize AegisOS Core deployment and obtain its canonical address;

4. deploy the Settlement Vault with:
   - AegisOS Core address as immutable controller;
   - no administrative adjudication authority;

5. call AegisOS `bind_vault(vault_address)` exactly once;

6. AegisOS verifies through the EVM interface that:
   - `vault.controller()` equals the AegisOS/ghost address;
   - the vault reports the expected protocol/domain identifier;

7. AegisOS stores the vault address;

8. AegisOS permanently clears the bootstrap address;

9. further `bind_vault` calls are impossible.

The digest helper is not an upgrader, settlement authority, evidence authority, or state source. The bootstrap address is NOT a GenVM upgrader.

No upgrader is added to the GenVM root.

The canonical AegisOS release is intended to remain code-immutable.

## 4. Funding

A funder deposits GEN directly into the Settlement Vault under a unique
agreement/escrow identifier.

Before an agreement can activate, AegisOS verifies the required funding state
through a deterministic EVM view.

Activation therefore requires the vault to contain the exact required principal.

AegisOS never treats an off-chain promise to fund as equivalent to funded
escrow.

## 5. Final decision

Consensus adjudication produces an exact bounded consequential result.

A finalized decision binds at minimum:

- agreement identifier;
- policy hash;
- evidence-set hash;
- decision version;
- consequence code;
- beneficiary;
- amount;
- decision nonce.

The Intelligent Contract persists the finalized decision before settlement
transport is considered complete.

## 6. Permissionless publication

A finalized entitlement can be published to the vault by a method conceptually
equivalent to:

`publish_entitlement(agreement_id)`

Publication is:

- permissionless;
- derived only from already-finalized AegisOS state;
- zero-value from the Intelligent Contract;
- safe to invoke repeatedly.

The method emits an external EVM message containing the exact finalized
settlement tuple.

Publication itself does not create a second adjudication.

## 7. Vault idempotency

The vault keys settlement by the finalized decision nonce / decision identifier.

For the first valid publication:

- verify caller is the immutable AegisOS controller;
- verify escrow is funded and unsettled;
- verify amount matches the escrow accounting;
- consume the escrow exactly once;
- credit the beneficiary's claimable balance;
- mark the decision identifier consumed.

For a duplicate publication containing the exact already-applied tuple:

- perform no second credit;
- return successfully or otherwise provide an idempotent no-op path.

For a duplicate decision identifier containing conflicting data:

- revert.

This distinction is mandatory.

## 8. Transport failure

A failure to publish the entitlement must NOT:

- alter the finalized AegisOS judgment;
- create a second judgment;
- redirect the beneficiary;
- destroy the escrow;
- consume the decision nonce inside the vault.

Because publication is permissionless and idempotent, the same finalized
decision can be published again later.

This provides transport recovery without re-adjudication.

## 9. Withdrawal

After the vault has credited a finalized entitlement, the beneficiary withdraws
directly from the EVM vault.

The target withdrawal implementation must use:

- pull payments;
- checks-effects-interactions;
- reentrancy protection;
- exact balance accounting.

If the final EVM transfer reverts, the whole withdrawal call must revert so the
claimable balance remains available for a later retry.

## 10. Refunds

Refunds use the same settlement primitive.

A refund is not an administrative escape hatch.

The finalized AegisOS consequence simply identifies the funder as beneficiary
for the exact refundable amount.

The same idempotency and replay rules apply.

## 11. No hidden settlement authority

The Settlement Vault must not contain an owner function capable of:

- selecting a beneficiary;
- modifying an AegisOS decision;
- draining arbitrary escrow;
- bypassing the controller;
- resetting a consumed decision nonce;
- overwriting an active escrow beneficiary.

Any emergency mechanism that can violate these properties is prohibited.

## 12. Remaining certification

This architecture is not frozen for production until all of the following pass:

- Solidity invariant tests;
- reentrancy tests;
- duplicate-publication tests;
- conflicting-replay tests;
- exact accounting tests;
- AegisOS EVM-view tests;
- EVM external-message tests;
- failed-publication recovery test;
- failed-withdrawal recovery test;
- live Bradbury controller/message proof;
- live Bradbury actual-recipient balance proof.

Studio-only success is insufficient because official GenLayer documentation
states that Studio does not fully reproduce live EVM/ghost-contract behavior.

# AegisOS Bradbury Verification

## Scope

This document records the live Bradbury Testnet identities and final state used to certify the R94 reusable AegisOS Intelligent Contract.

Date of final backend certification: **2026-09-26**.

Network:

- GenLayer Bradbury Testnet;
- chain ID `4221`;
- ConsensusMain `0x0112Bf6e83497965A5fdD6Dad1E447a6E004271D`.

## Deployed contracts

### Core

Address: `0x532de68bd897529c06803efed843d814b1744ba0`

Deployment transaction:

`0x1143f6b953dc0ac1f8a148230fbd2e60a598ba6e48658d0232e7e498d6c62133`

Source SHA-256:

`df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b`

### Stateless digest helper

Address: `0xf557028b465a6f87ae76b0f520edb2b3e6e4eec9`

Deployment transaction:

`0x3b9f31744131f207bf1fbbbb1b19d4d818c1822302d2cc91f0e9d7b6203bed64`

Source SHA-256:

`624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73`

## Live recovery agreement

Agreement ID:

`aegisos-p3h-r2-expiry-f26a9373-1143f6b9`

Creator / final beneficiary:

`0x1f87ae197af539253978d435ad45ccf28fb95024`

Principal reference amount: `1000`

Recovery deadline: `1790414086`

## Agreement creation

GenLayer transaction:

`0xded4f6c759c20a181ac5434cf1459c8099aac6ebbafcc20b019b2db236dd15de`

Final result:

- `Finalized / 7`;
- `FINISHED_WITH_RETURN / 1`.

Before expiry, state remained pristine: state `1`, generation `0`, decision nonce `0`, outcome `0`, consequence `0`, decision recorded `false`.

## Historical failed expiry and gas causality

Initial expiry EVM transaction:

`0xc7ec2d1157f6c2d3822ea936fc49e393f24b766c3b106bbd427a90473bbf7fdc`

Observed outer gas limit `912576`, gas used `871933`, receipt status `0`, and no GenLayer transaction event.

Controlled same-block replay classified the failure as:

`INSUFFICIENT_OUTER_EVM_GAS_LIMIT_CAUSALLY_REPRODUCED_AT_MINED_BLOCK_CONTEXT`

No automatic blockchain retry was performed.

## Corrected expiry

Outer EVM transaction:

`0xf3c6a525131e916ae0b9f7a9c3a22e1791158677c3c5219c620569cb7f5daf0a`

Observed:

- nonce `1360`;
- gas limit `1841016`;
- gas used `863197`;
- EVM receipt status `1`.

ConsensusMain created exactly one GenLayer transaction:

`0x96b759e96ff23c4064469fc1a3278232116b9e85e9185b43914ffa7deffb74e1`

It naturally finalized without a manual finalization transaction:

- `Finalized / 7`;
- `FINISHED_WITH_RETURN / 1`.

## Exact terminal state

| Field | Value |
| --- | --- |
| `state` | `7` |
| `outcome_code` | `3` |
| `consequence_code` | `1` |
| `beneficiary` | `0x1f87ae197af539253978d435ad45ccf28fb95024` |
| `principal_amount` | `1000` |
| `entitlement_amount` | `1000` |
| `decision_nonce` | `1` |
| `decision_recorded` | `true` |
| `accepted` | `false` |
| `challenged` | `false` |
| `decision_digest` | `53cf3938974d87d7975b2c4e1677f5b738429ffe195f8653e56621369817fda5` |

This proves the deadline-recovery path produced the exact deterministic expired-refund consequence and reached natural GenLayer finality.

## Reviewer package identity

Final backend-completion package:

- certificate SHA-256:
  `00fb72a1481f26dfa0630f230ae24366d674ea515186f220700210a259caf729`;
- archive SHA-256:
  `0fdec40c538c8b044c8d005ea64d19e8d4cf331a1cbfe1879c42ea6c345634e6`.

The package recorded exactly one corrected R3I write attempt, no second expiry attempt, no manual finalization, no appeal, no deployment during reconciliation, no Git mutation during blockchain verification, and no raw signed transaction secret in the reviewer bundle.

The archive is intentionally not committed because it is a large external reviewer artifact. Its immutable identifiers are recorded here.

## What this proof establishes

The R94 live proof establishes deployment identity, the tested reusable agreement record, deadline recovery, successful ConsensusMain admission, natural GenLayer finality, successful execution, and persistence of the exact expired-refund entitlement.

## What this proof does not establish

It does not establish token custody or asset payout transport. R94 records an entitlement; it does not expose a deposit/withdrawal token interface.

Modified source does not inherit this proof. Any contract-source change requires a new release identity and fresh live evidence.

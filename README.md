# AegisOS

**Reusable GenLayer Intelligent Contract for verifiable agreements, evidence-bound adjudication, challenge, recovery, and finalized entitlements.**

AegisOS is an Intelligent Contract protocol, not a single-purpose escrow or demo application. One deployed core can manage many independent agreements, each with its own participants, policy commitment, authority set, evidence lifecycle, challenge window, recovery deadline, and deterministic consequence.

## Status

**Bradbury Testnet live verification complete — 2026-09-26.**

Canonical release identity:

| Item | Value |
| --- | --- |
| Network | GenLayer Bradbury Testnet |
| Chain ID | `4221` |
| Core contract | `0x532de68bd897529c06803efed843d814b1744ba0` |
| Core source SHA-256 | `df7f279e651681a24fdb3b0f71079edb64ebdf45a0e5c398806804f07fb3d21b` |
| Digest helper | `0xf557028b465a6f87ae76b0f520edb2b3e6e4eec9` |
| Helper source SHA-256 | `624129618401b57c8547e6b4c4b14528fbce154a9f8e00a621596221b7864d73` |
| Corrected expiry EVM tx | `0xf3c6a525131e916ae0b9f7a9c3a22e1791158677c3c5219c620569cb7f5daf0a` |
| Corrected expiry GenLayer tx | `0x96b759e96ff23c4064469fc1a3278232116b9e85e9185b43914ffa7deffb74e1` |
| Final GenLayer status | `Finalized / 7` |
| Final execution | `FINISHED_WITH_RETURN / 1` |

The live recovery proof finalized the expected terminal record:

- state `7` — decision recorded;
- outcome `3` — expired refund;
- consequence `1` — creator entitlement;
- beneficiary `0x1f87ae197af539253978d435ad45ccf28fb95024`;
- entitlement `1000`;
- decision nonce `1`;
- decision digest `53cf3938974d87d7975b2c4e1677f5b738429ffe195f8653e56621369817fda5`.

See [Bradbury verification](docs/BRADBURY_VERIFICATION.md) for the evidence chain.

## Why AegisOS is reusable

The core stores agreements by ID in a persistent registry. Each agreement independently binds:

- creator and counterparty;
- policy hash;
- authority-set hash;
- primary and corroborating authorities;
- principal reference amount;
- challenge-window duration;
- maximum evidence age;
- recovery deadline;
- evidence generation and commitments;
- challenge state;
- final outcome, beneficiary, entitlement, nonce, and decision digest.

This makes the contract a reusable agreement kernel. New use cases are expressed through agreement data and policy commitments rather than a new contract deployment for every workflow.

## Agreement lifecycle

```text
create
  ↓
accept
  ↓
authority attestations
  ↓
bind corroborated evidence
  ↓
challenge window
  ├── no challenge
  └── challenge
       ↓
adjudicate
  ├── CREATOR
  ├── COUNTERPARTY
  └── REPAIR
       ↓
final decision / entitlement

deadline recovery:
unresolved agreement
  ↓
expire
  ↓
expired-refund decision / creator entitlement
```

The nondeterministic adjudication surface is deliberately narrow: validators agree on exactly one of `CREATOR`, `COUNTERPARTY`, or `REPAIR`. Economic/state consequences are then applied deterministically.

## Deployed R94 ABI naming

The live R94 source was certified and deployed while the runtime-boundary work still used the `*_probe` method suffix and the class name `AegisKernelBoundaryProbe`.

Those names are now **frozen ABI compatibility names for the verified deployment**. They do not mean the deployed contract is a throwaway test. Changing them would change the certified source hash and break byte-level correspondence with the Bradbury deployment.

Product semantics are:

| Deployed method | Protocol meaning |
| --- | --- |
| `create_probe` | create agreement |
| `accept_probe` | accept agreement |
| `attest_evidence_probe` | submit bound authority attestation |
| `bind_evidence_probe` | bind independent corroborated evidence |
| `challenge_probe` | challenge agreement evidence/decision path |
| `adjudicate_probe` | run evidence-bound GenLayer adjudication |
| `expire_probe` | execute deadline recovery |
| `get_probe` | read agreement |
| `get_attestation` | read authority attestation |

See [API](docs/API.md).

## Security model

AegisOS is designed to fail closed around consequential state.

The current core enforces:

- immutable agreement-level policy and authority commitments;
- sender-bound primary/corroborating authority roles;
- direct authority transaction requirement;
- independent primary and corroborating evidence records/sources;
- evidence freshness and expiry;
- exact evidence payload/content hashes;
- challenge windows;
- repair instead of settlement when exact adjudication cannot be established;
- exact consequential validator agreement;
- decision replay protection;
- bounded recovery deadlines;
- deterministic expiry recovery;
- no owner/admin verdict path.

See [Security](docs/SECURITY.md).

## Scope of the R94 release

R94 finalizes **agreement decisions and entitlement records**.

It does **not** claim that the GenVM core itself currently custodies or transfers ERC-20/native assets. `principal_amount` and `entitlement_amount` are canonical agreement/accounting fields. A payout transport or custody layer must be separately implemented and verified before AegisOS is described as token-custodial escrow.

That separation is intentional: adjudication finality should not depend on an arbitrary recipient transfer succeeding.

## Repository scope

This repository is intentionally **Intelligent-Contract-only**.

It contains:

```text
contracts/
  aegis_core.py
  aegis_digest_helper.py

docs/
  API.md
  ARCHITECTURE.md
  BRADBURY_VERIFICATION.md
  SECURITY.md

tests/
  conftest.py
  test_aegis_core_direct.py

verification/supported_runtime/
  reproducible multi-validator runtime proof

scripts/
  check_release.py
  check_supported_runtime_bundle.py

requirements-dev.txt
requirements-lock.txt
```

There is no frontend, web application, API server, database service, or off-chain product backend in this repository.

## Verification

Use Python 3.12.

```sh
python -m pip install --disable-pip-version-check --no-input -r requirements-lock.txt
python scripts/check_release.py
python scripts/check_supported_runtime_bundle.py

genvm-lint lint contracts/aegis_core.py
genvm-lint validate contracts/aegis_core.py
genvm-lint check contracts/aegis_core.py
genvm-lint typecheck contracts/aegis_core.py --strict

genvm-lint lint contracts/aegis_digest_helper.py
genvm-lint validate contracts/aegis_digest_helper.py
genvm-lint check contracts/aegis_digest_helper.py
genvm-lint typecheck contracts/aegis_digest_helper.py --strict

PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -p no:cacheprovider -q tests/test_aegis_core_direct.py
```

The supported-runtime bundle is self-contained under `verification/supported_runtime/`. It contains test-only stack witness/relay contracts used to prove runtime call-stack semantics; they are not product contracts.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API](docs/API.md)
- [Security](docs/SECURITY.md)
- [Bradbury verification](docs/BRADBURY_VERIFICATION.md)

## Release discipline

The deployed R94 contract hashes are immutable evidence identities. Any future source change—including cosmetic ABI renaming—must be treated as a new release and must not inherit R94 Bradbury verification claims without fresh deployment and finality evidence.

# GenLayer Engineering Envelope

Status: **GATE 0 — RESEARCHED, NOT YET FROZEN**

This document defines what AegisOS is allowed to assume about the target GenLayer environment.

Nothing marked unresolved may be treated as a production assumption.

## 1. Target network

Current Bradbury configuration verified from the official GenLayer Python SDK research snapshot:

- network: GenLayer Bradbury Testnet;
- GenLayer RPC: `https://rpc-bradbury.genlayer.com`;
- chain ID: `4221`;
- consensus main contract:
  `0x0112Bf6e83497965A5fdD6Dad1E447a6E004271D`.

Chain ID alone is not sufficient to identify Bradbury because another GenLayer testnet configuration has also used `4221`.

Every authorized release write must therefore verify at minimum:

1. expected RPC/network;
2. expected chain ID;
3. expected consensus contract address;
4. exact release source hash;
5. exact account nonce;
6. sufficient balance;
7. exact encoded transaction payload;
8. fresh gas/fee preflight.

## 2. Runtime compatibility rule

AegisOS MUST target features demonstrated on the actual Bradbury-compatible runtime.

A feature existing in newer GenVM source is not enough.

In particular, research found a critical version distinction:

- the frozen v0.2.16 runner line supports `py-genlayer-multi`;
- the corresponding executor parser explicitly rejects `chain:` runner IDs;
- newer GenVM development lines contain richer chain-runner / `MapFile`
  capabilities.

Therefore AegisOS MUST NOT depend on `chain:<address>:...` runtime code loading
unless Bradbury itself is separately certified to support it.

## 3. Multi-file packaging

`py-genlayer-multi` exists in the frozen v0.2.16 runner line.

That permits a ZIP contract package containing a `contract/` directory and
normal Python module imports.

However multi-file packaging does NOT, by itself, eliminate deployment payload
size. The ZIP still has to be transported as contract code.

AegisOS therefore treats multi-file packaging as a source-organization tool,
not as a deployment-size bypass.

## 4. Supported contract capabilities verified in the compatible API line

The researched runner exposes:

- `gl.Contract`;
- public view/write/payable methods;
- `TreeMap`;
- `DynArray`;
- events;
- web requests and rendering inside nondeterministic execution;
- LLM prompt execution;
- `gl.vm.run_nondet`;
- `gl.vm.run_nondet_unsafe`;
- `strict_eq`;
- comparative and non-comparative equivalence helpers;
- internal Intelligent Contract messages;
- external EVM interactions.

Use of a capability in this list still requires a project-specific runtime test.

## 5. Consensus design requirement

AegisOS will keep nondeterministic reasoning separate from deterministic
economic consequences.

The preferred adjudication pattern is:

1. deterministically load the frozen policy/evidence bindings;
2. leader independently evaluates the admissible evidence;
3. validator independently evaluates the same admissible evidence;
4. compare a small structured consequential result;
5. persist only the exact agreed consequential fields.

A validator MUST NOT merely confirm that the leader returned syntactically valid
JSON.

## 6. Consequential result

The target canonical decision surface is intentionally small:

- agreement ID;
- policy hash;
- evidence-set hash;
- decision version;
- outcome;
- consequence code;
- beneficiary;
- amount;
- decision nonce.

Open-ended explanation text is never an economic consensus field.

## 7. Finality rule

Submission is not success.

Acceptance is not final settlement.

AegisOS release evidence must distinguish:

- EVM submission;
- GenLayer transaction creation;
- consensus execution;
- accepted/decided state;
- finalization;
- successful execution result;
- actual economic/state consequence.

Consequential actions are not permitted merely because a transaction was
submitted or initially accepted.

## 8. External and internal messaging

Economic actions MUST NOT use `on="accepted"`.

Finalized messaging is the baseline for consequential actions.

Even finalized messaging must not be used in a way where an arbitrary recipient
failure can destroy liveness of the underlying agreement.

For that reason AegisOS separates final adjudicated entitlement from payout
transport.

## 9. Storage policy

On-chain storage is for canonical state and bindings, not unbounded documents.

Store:

- hashes;
- stable IDs;
- addresses;
- bounded timestamps;
- counters;
- state codes;
- bounded policy parameters;
- bounded evidence metadata;
- entitlement/accounting values.

Do not store full large evidence documents when an immutable authenticated
external record is sufficient.

## 10. Unresolved Gate-0 items

Gate 0 is NOT complete until the following are certified:

- exact native-GEN withdrawal/failure/retry semantics for the chosen payout path;
- final source-byte budget;
- final encoded deployment-payload budget;
- final outer-gas safety rule;
- exact transaction fee profiles;
- exact production toolchain commits;
- exact runtime runner pin;
- Bradbury read-only schema/admission behavior for the prototype.

Until these are closed, production implementation and deployment remain blocked.

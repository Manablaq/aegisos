# Gate-0 Research Sources

This file records implementation-sensitive sources consulted before AegisOS
production coding begins.

## Official GenLayer repositories

### genlayer-py

Research commit observed:

`dd25ef7f43e99a14b8fe42a64e01374845ad4d2d`

Relevant Bradbury configuration:

- RPC: `https://rpc-bradbury.genlayer.com`
- chain ID: `4221`
- consensus main:
  `0x0112Bf6e83497965A5fdD6Dad1E447a6E004271D`

Repository:

`https://github.com/genlayerlabs/genlayer-py`

### GenVM v0.2.16

Tag commit:

`387e1a66e920cb2dfadcdce40ab2d28da02efd1e`

Repository:

`https://github.com/genlayerlabs/genvm`

The frozen v0.2.16 line was inspected for:

- storage types;
- consensus APIs;
- messages;
- web access;
- LLM execution;
- multi-file runner support.

### GenVM executor compatibility line

Inspected executor commit:

`75e4d1fd5945aadea065f6928e60155ffca63797`

Important finding:

the parser explicitly rejects `chain:` runner IDs in that compatibility line.

Repository:

`https://github.com/genlayerlabs/genvm-executor`

### Newer GenVM development line

Inspected newer executor/runtime source separately to identify features that must
NOT be assumed to exist on Bradbury.

This distinction is intentionally preserved so AegisOS does not accidentally
target a future runtime.

### genlayer-js

Current repository source was inspected for:

- transaction gas estimation;
- gas headroom behavior;
- fee policy;
- transaction submission;
- finalization helpers.

Repository:

`https://github.com/genlayerlabs/genlayer-js`

### GenLayer testing suite

Repository:

`https://github.com/genlayerlabs/genlayer-testing-suite`

Package/version labels alone are not treated as immutable toolchain evidence.
AegisOS release tooling will pin exact commits.

## Current known GenLayer issues

Relevant open/public issue categories inspected include:

- Bradbury large-contract deployment/gas-limit behavior;
- contract-to-contract view-call/runtime behavior;
- transaction gas estimation.

Open issue status is not treated as a permanent protocol fact.

The exact target runtime is always re-probed before release.

## Internal historical engineering evidence

Prior Accord402 Bradbury work is used only as empirical engineering evidence,
not as a GenLayer specification.

It demonstrated that very large Intelligent Contract deployment payloads can be
operationally unsafe even when source logic itself is valid.

AegisOS therefore adopts a deliberately conservative source/payload budget.

# Bradbury Runtime Baseline

Status: **LIVE READ-ONLY BASELINE CAPTURED**

This document records the Bradbury environment observed by the AegisOS
Gate-0 R3-D1 live read-only probe.

It is evidence about the target network at the recorded observation point.
Dynamic quantities such as block height, gas price, and base fee are not
permanent protocol constants.

Canonical raw evidence:

`verification/bradbury/gate0-r3-d1-readonly.json`

SHA-256:

`57219cfb6d8f0f19cd1c2ec5c2b40876d8322ee694742ad5a7b4c2b6c93d3620`

## Network

Both official RPC surfaces reported:

- chain ID: `4221`;
- GenLayer RPC:
  `https://rpc-bradbury.genlayer.com`;
- underlying GenLayer Chain RPC:
  `https://rpc.testnet-chain.genlayer.com`.

The GenLayer RPC and direct chain RPC returned byte-identical deployed code for
the probed system contracts.

## Live block gas envelope

The probe observed:

- GenLayer RPC latest block gas limit: `100000000`;
- chain RPC latest block gas limit: `100000000`.

This is the block gas limit observed during R3-D1.

It is NOT an AegisOS deployment budget.

In particular, historical deployment failures involving a lower transaction
gas ceiling must not be re-described as Bradbury's block gas limit.

AegisOS deployment admission will be measured independently against the exact
encoded deployment candidate.

## Consensus Main

Address:

`0x0112Bf6e83497965A5fdD6Dad1E447a6E004271D`

Observed proxy code:

- bytes: `1159`;
- SHA-256:
  `f44fc4c62e24435d0b196912becd21e71c9464c289aa03f1c649fc9818edb9d1`.

## FeeManager

Address:

`0xF205868bf5db79d2162843742D18D0900A9E462a`

Observed proxy code:

- bytes: `1159`;
- SHA-256:
  `085cef65c48abe4c08242aa61e62134dfa8af0e16224619a5eb8da465a5f3ec0`.

Live EIP-1967 implementation:

`0x31199772507933c5ad94da28ab7b02bf9c41069c`

This exactly matches the current official Bradbury deployment artifact.

## Stable Bradbury fee surface

The live FeeManager supports:

- `GENPerTimeUnit()`;
- `storageUnitPrice()`.

At the R3-D1 observation point both returned `0`.

These values are observations, not immutable assumptions.

## v0.6 fee surface

The following newer fee-policy views reverted on both official RPC surfaces:

- `quoteGasPrice()`;
- `messageFeeParamsBudgetFloor()`.

Therefore:

`V06_FEE_VIEWS_SUPPORTED=NO`

for the Bradbury deployment observed during R3-D1.

AegisOS must not build its Bradbury release path around the v0.6 fee-policy
surface unless a later live probe proves Bradbury has been upgraded.

## Official deployment provenance

Official `genlayer-networks` revision used during Gate-0 research:

`f9a30ed9536e56255cd2d7f8579a4d5dcc81ffd0`

That revision identifies the Bradbury deployment source as:

`9c686087963551277fc2dce0354c2b1a7050b4b2`

and labels the deployment:

`v0.5:9c68608`

## Release rule

Every later AegisOS deployment authorization must re-probe the target network.

This Gate-0 baseline proves what was live during R3-D1; it does not authorize
future writes after network drift.

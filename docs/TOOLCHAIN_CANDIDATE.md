# AegisOS Toolchain Candidate

Status: **CANDIDATE — NOT YET PRODUCTION-FROZEN**

AegisOS will pin immutable revisions rather than relying only on package
version strings.

## Contract runtime

Official runner candidate:

`py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

The current official GenLayer documentation uses this exact runner hash and
documents the hash as the contract's runtime-version pin.

This same runner reference has already been exercised successfully in prior
Bradbury engineering work.

## Official documentation research revision

Repository:

`genlayerlabs/genlayer-docs`

Revision:

`1cd8e2d11f743141b441be91ed65f321139814cc`

This revision prepares and documents the Consensus v0.6 / Studio v0.123
release surface.

## Python SDK candidate

Repository:

`genlayerlabs/genlayer-py`

Revision:

`a3dc35e04898e3889cbfa855bcaf7d2664675b8f`

Reported package version:

`0.18.0`

Important properties verified at this revision:

- Bradbury chain definition;
- chain ID 4221;
- Bradbury RPC;
- Consensus v0.6 ABI;
- explicit fee-aware transaction helpers;
- fee distributions;
- message allocations;
- transaction finality/execution handling.

## Testing-suite candidate

Repository:

`genlayerlabs/genlayer-testing-suite`

Revision:

`9c09578b143905471fb0657dd53bdaf18da8e35f`

Reported package version:

`0.29.2`

At this revision it declares:

`genlayer-py>=0.18.0,<0.19.0`

which is compatible with the selected Python SDK candidate.

## Linter candidate

Repository:

`genlayerlabs/genvm-linter`

Revision:

`28450e665666300fc648dbe495110dfd0cb6a7b4`

Reported package version:

`0.11.1-rc.2`

## Pinning rule

Production requirements will use exact Git revisions.

A dependency is not considered frozen merely because:

- the package version matches;
- `main` currently contains the desired behavior;
- a newer release exists.

AegisOS will freeze this candidate only after the actual prototype passes the
complete lint/type/schema/Direct Mode/security and runtime compatibility gates.

## JavaScript SDK

The frontend toolchain is intentionally not frozen in Gate 0 R2.

Current GenLayer documentation distinguishes stable releases from Consensus
v0.6 preview/release-candidate client lines.

The browser/client SDK will be selected only when frontend integration begins,
and will be pinned separately from the contract engineering toolchain.

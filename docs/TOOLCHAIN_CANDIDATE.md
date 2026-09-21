# AegisOS Toolchain Candidate

Status: **BRADBURY-ALIGNED CANDIDATE — NOT PRODUCTION-FROZEN**

The toolchain is pinned by immutable commit, not merely by package version.

Gate-0 R3 established that the live Bradbury deployment observed by AegisOS is
not exposing the newer v0.6 fee-policy surface.

The production candidate is therefore aligned to the stable Bradbury client
family rather than assuming the v0.6 release-candidate transaction model.

## Intelligent Contract runner

Runner candidate:

`py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

This exact runner hash is also used in the current official GenLayer contract
documentation.

Runner status:

**CANDIDATE**

It is not called production-frozen until the AegisOS prototype passes the
runtime and Bradbury admission gates.

## Python

Minimum project interpreter:

**Python 3.12**

The selected Python SDK and testing candidate both require Python 3.12 or newer.

AegisOS CI will standardize on Python 3.12 for the canonical reproducible
environment unless a later certification explicitly changes it.

## GenLayer Python SDK

Repository:

`genlayerlabs/genlayer-py`

Stable release:

`v0.18.0`

Release commit:

`cf421edc0d20e567cc5a3b4da198fce61f1e579f`

Why this revision:

- it is the immutable stable v0.18.0 release commit;
- it contains the Bradbury chain definition used by the stable client family;
- unlike later v0.6 fee-aware development revisions, the transaction path does
  not require the v0.6 Bradbury fee surface that R3-D1 proved absent.

Production status:

**CANDIDATE — NOT FROZEN**

## GenLayer testing suite

Repository:

`genlayerlabs/genlayer-testing-suite`

Exact compatibility commit:

`9c09578b143905471fb0657dd53bdaf18da8e35f`

Package version reported at that commit:

`0.29.2`

This is intentionally pinned by commit rather than by the published v0.29.2
tag.

The published v0.29.2 tag resolves to an older tree whose dependency metadata
requires:

`genlayer-py>=0.13.0,<0.17.0`

which is incompatible with the selected stable `genlayer-py v0.18.0`.

The exact compatibility commit selected above instead requires:

`genlayer-py>=0.18.0,<0.19.0`

That exact dependency relationship is one reason AegisOS never treats a package
version string by itself as reproducible toolchain evidence.

The compatibility commit includes newer simulator support. AegisOS v1 must not
interpret simulator-only v0.6 fee-aware behavior as proof that the live
Bradbury v0.5 surface supports the same behavior.

Production status:

**CANDIDATE — NOT FROZEN**

## GenVM linter

Repository:

`genlayerlabs/genvm-linter`

Stable release:

`v0.11.0`

Release commit:

`928bb51c42da8ff2512d81465d3e704f599aca47`

Production status:

**CANDIDATE — NOT FROZEN**

## Official Bradbury deployment artifacts

Repository:

`genlayerlabs/genlayer-networks`

Artifact revision:

`f9a30ed9536e56255cd2d7f8579a4d5dcc81ffd0`

Bradbury consensus source revision:

`9c686087963551277fc2dce0354c2b1a7050b4b2`

Observed deployment family:

`v0.5:9c68608`

## Production freeze rule

None of these candidates becomes production-frozen merely because the
individual revisions are valid.

The complete set must still pass together:

1. clean environment installation;
2. dependency-resolution verification;
3. import/version verification;
4. GenVM lint;
5. typecheck;
6. schema extraction;
7. Direct Mode;
8. adversarial/security suite;
9. exact contract-size measurement;
10. exact encoded deployment-payload measurement;
11. Bradbury read-only admission preflight;
12. live Bradbury deployment/finality proof.

Until those gates pass:

`PRODUCTION_TOOLCHAIN_FROZEN=NO`

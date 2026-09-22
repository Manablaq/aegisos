# AegisOS Toolchain Reproducibility

Status: **REPRODUCIBLE CANDIDATE — NOT PRODUCTION-FROZEN**

Gate 0 R4 created two independent Python 3.12 virtual environments and resolved
the AegisOS GenLayer development toolchain in each.

Both environments produced the same complete 55-line `pip freeze --all`
environment byte-for-byte.

Canonical promoted lock:

`requirements-lock.txt`

SHA-256:

`14db5fb5adbf7ae14575c19f9779d7c2c996d20d44192a79e28bf601b649d20c`

## Direct GenLayer revisions

### genlayer-py

Version:

`0.18.0`

Commit:

`cf421edc0d20e567cc5a3b4da198fce61f1e579f`

### genlayer-test

Version:

`0.29.2`

Commit:

`9c09578b143905471fb0657dd53bdaf18da8e35f`

### genvm-linter

Version:

`0.11.0`

Commit:

`928bb51c42da8ff2512d81465d3e704f599aca47`

## R4 verification

Both independent environments passed:

- Python 3.12 interpreter gate;
- dependency resolution;
- `pip check`;
- exact VCS commit verification;
- package import smoke tests;
- `pytest` CLI smoke;
- `gltest` CLI smoke;
- `genvm-lint` CLI smoke.

The second environment reproduced the first environment's complete freeze
exactly.

## Executable wrapper hashes

Generated CLI wrapper hashes are not required to match across different virtual
environment paths.

Python entrypoint wrappers embed the absolute interpreter path in their shebang,
so `.venv/bin/gltest` and an equivalent `/tmp/.../bin/gltest` can differ as
files while resolving to the same package code and dependency environment.

AegisOS therefore uses:

- exact immutable upstream commits;
- exact package versions;
- complete lock parity;
- installed `direct_url.json` VCS provenance;
- runtime smoke tests;

as the relevant reproducibility evidence.

## Preserved evidence

- `requirements-lock.txt`
- `verification/toolchain/r4-r3-freeze.txt`
- `verification/toolchain/r4-r3-install-report.json`
- `verification/toolchain/r4-reproducibility.json`

The R4-R3 pip report SHA-256 is:

`74f151ca84b9f89f3e50f1fadca14a9558922baa34c377f915a91cdc53f7473e`

## Production freeze remains blocked

R4 proves that the toolchain candidate can be reproduced. Subsequent local
certification of the canonical AegisOS candidate confirms that this pinned
toolchain can execute its GenVM lint/validation, strict/basic typecheck, schema
extraction, stable ABI check, and eight Direct Mode regression proofs.

`PRODUCTION_TOOLCHAIN_FROZEN=NO`

That local result does not freeze the production toolchain and does not prove
live validator consensus or finality. Production freeze remains blocked on the
remaining release gates, including exact encoded deployment-payload
measurement, Bradbury read-only admission preflight, and live Bradbury finality
verification.

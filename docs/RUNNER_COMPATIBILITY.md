# AegisOS Runner Compatibility

Status: **LOCAL COMPATIBILITY VERIFIED — NOT PRODUCTION-FROZEN**

AegisOS Gate 0 R5 reconciled the Intelligent Contract runner against the
Bradbury-compatible GenVM `v0.2.16` runner bundle.

## Candidate

`py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## GenVM bundle

Version:

`v0.2.16`

Observed bundle SHA-256:

`4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2`

The bundle contains four `py-genlayer` runners.

The candidate above is:

- present in the `v0.2.16` bundle;
- the runner selected as the bundle's default/latest by the pinned linter;
- the same runner referenced by the pinned official GenLayer documentation.

## R5 local verification

Using the exact reproducible AegisOS toolchain, the candidate passed:

- AST/safety lint;
- SDK semantic validation;
- ABI schema extraction;
- the complete `genvm-lint check` workflow;
- Pyright typecheck with zero diagnostics.

Pyright version:

`1.1.414`

The corrected typecheck explicitly put the AegisOS virtual environment's
`bin` directory on `PATH`, because the pinned linter launches `pyright`
as a subprocess by executable name.

## Older v0.18 E2E runner

The older runner reference:

`py-genlayer:1j12s63yfjpva9ik2xgnffgrs6v44y1f52jvj9w7xvdn7qckd379`

is also physically present in the `v0.2.16` bundle.

It was not selected for AegisOS because the R5 probe did not successfully
extract the probe ABI with that runner, while the bundle-default/current-docs
runner passed the same gate.

This does not assert that the older runner is universally invalid. It means it
is not the AegisOS candidate.

## Production freeze

`PRODUCTION_RUNNER_FROZEN=NO`

Runner compatibility is now verified locally, but production freeze still
requires the actual AegisOS Intelligent Contract to pass:

1. lint;
2. semantic validation;
3. schema extraction;
4. typecheck;
5. Direct Mode regression tests;
6. adversarial consensus tests;
7. exact source/payload budget gates;
8. Bradbury read-only admission preflight;
9. live Bradbury deployment and finality verification.

The verification fixture is:

`verification/runner/runner-probe.py`

It is not production AegisOS contract code.

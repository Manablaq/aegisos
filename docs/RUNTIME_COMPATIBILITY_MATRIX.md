# AegisOS Runtime Compatibility Matrix

Status: **GATE-0 RESEARCH MATRIX**

| Capability | Gate-0 status | AegisOS rule |
| --- | --- | --- |
| Exact `py-genlayer` runner hash | Verified in current official docs | Pin exact hash |
| `TreeMap` / `DynArray` storage | Supported | Allowed with bounded schemas |
| Custom `run_nondet` | Supported | Allowed |
| Web request/render in nondeterministic execution | Supported | Allowed only with evidence policy |
| LLM execution | Supported | Allowed only inside bounded adjudication |
| External EVM view | Documented | Allowed, live Bradbury certification required |
| External EVM write message | Documented, finalization only | Allowed only through idempotent receiver |
| External message `on="accepted"` | Not supported | Prohibited |
| Internal message `on="accepted"` | Supported but appeal/replay-sensitive | Prohibited for consequences |
| Value-bearing internal child failure refund | Not automatic | Do not use for principal settlement |
| `py-genlayer-multi` packaging | Exists | Not a size bypass |
| `chain:<address>:...` module loading | Not certified on Bradbury-compatible line | Prohibited |
| Critical synchronous IC-to-IC dependency | Current runtime issue exists | Prohibited in AegisOS v1 |
| Native GenVM upgrade authority | Supported if upgraders added | Do not add upgraders |
| Default locked code with no upgraders | Supported | Required canonical release posture |
| Studio EVM-contract parity | Incomplete | Live Bradbury proof mandatory |

## Version discipline

Capabilities present in newer GenVM development source are not automatically
Bradbury capabilities.

AegisOS only promotes a feature to production-supported after one of:

1. current official Bradbury documentation explicitly binds the feature to the
   deployed environment; or
2. a reproducible live Bradbury test demonstrates the exact behavior.

## Current exclusions

AegisOS v1 must not depend on:

- chain-loaded Python implementation libraries;
- child-contract deployment to solve source-size problems;
- synchronous cross-IC state reads for critical correctness;
- accepted-stage economic messages;
- direct value-bearing internal messages for user principal settlement.

## Live Bradbury correction — Gate 0 R3

R3-D1 established that the currently observed Bradbury FeeManager is from the
stable deployment family and does not expose the newer v0.6 fee-policy views.

Accordingly:

- v0.6 fee-aware submission behavior is NOT a Bradbury v1 assumption;
- simulator support for v0.6 fee-aware calls is NOT live-network evidence;
- the stable Bradbury client path remains the baseline;
- any future Bradbury migration must be detected by a fresh read-only probe
  before release tooling changes transaction encoding.

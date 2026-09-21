# Evidence Trust Model

Status: **GATE-0 CANDIDATE**

AegisOS does not trust evidence merely because validators can fetch it.

Evidence admissibility is governed by the agreement's frozen policy.

## Authority binding

Each authority record contains bounded fields such as:

- authority ID;
- authority revision;
- role;
- identity kind;
- identity value;
- canonical origin;
- allowed evidence class.

An active agreement references the exact authority revision.

## Evidence record

Each consequential record binds:

- evidence ID;
- authority ID and revision;
- subject;
- kind;
- immutable/versioned source;
- immutable version or record identifier;
- publication time;
- observed time;
- expiry time;
- content digest;
- primary/corroborator role;
- replacement ancestry if applicable.

## Freshness

Freshness is a policy rule, not an LLM opinion.

A record outside its allowed age or expiry window is inadmissible unless the
policy explicitly defines a historical-evidence mode.

## Corroboration

High-consequence policies can require:

- at least one primary authority;
- N independent corroborating authorities;
- identity independence;
- bounded freshness differences.

Primary and corroborating records must not be counted as independent when they
resolve to the same prohibited authority identity.

## Repair

Repairable defects include only policy-approved failure classes.

Repair must preserve the immutable parts of the agreement.

A repair cannot silently modify:

- the obligation itself;
- the payout amount;
- the beneficiary rules;
- the authority trust model;
- the challenge deadline.

## Prompt-injection boundary

Delivery text, challenge text, webpages, documents, and evidence payloads are
untrusted data.

They must never be interpolated as trusted system instructions.

The adjudicator prompt must explicitly separate frozen policy from untrusted
evidence content.

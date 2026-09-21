# Escrow and Recovery Model

Status: **OPEN GATE-0 ITEM**

The economic model is intentionally not frozen until payout failure and retry
semantics are proven on the target runtime.

## Required architecture

Adjudication and payout transport are separate.

A finalized adjudication creates an immutable entitlement record.

The payout mechanism then consumes that entitlement exactly once.

## Why

Research of the consensus message path shows that finalized external messages
are processed during transaction finalization and downstream execution failure
can make the finalization operation fail.

AegisOS therefore must not make the underlying agreement's final judgment depend
on an arbitrary recipient call succeeding in that same operation.

## Required properties of the eventual withdrawal mechanism

The chosen implementation must prove:

- entitlement survives payout transport failure;
- recipient cannot claim twice;
- another user cannot redirect the entitlement;
- accounting decrements exactly once;
- retries cannot duplicate value;
- failed transport has a defined recovery path;
- contract/global accounting remains solvent;
- no administrator is required to release honest funds.

No production escrow implementation may be written until these properties are
certified for the exact target runtime.

# AegisOS Security Invariants

Status: **MANDATORY DESIGN CONSTRAINTS**

The following invariants are treated as protocol requirements.

## Consensus and consequence

1. No consequential state transition without the required validator agreement.
2. No payout or entitlement may depend on approximate agreement over amount,
   beneficiary, policy version, or outcome.
3. Consequential fields must be compared exactly.
4. Free-form model prose is never a payout field.
5. Validator logic must independently reproduce or verify the material decision.

## Evidence

6. URL possession alone is not authority.
7. Every authority is bound by stable identity and revision.
8. Every consequential evidence record is immutable or version-bound.
9. Every evidence record has a stable record/evidence ID.
10. Freshness and expiry rules are explicit.
11. Required corroboration is explicit.
12. Evidence used in one prohibited replay scope cannot silently settle another.
13. Evidence fetch/hash failures that policy permits to repair become a
    repairable state rather than an automatic terminal loss.

## Economic safety

14. No economic consequence merely on initial acceptance.
15. No duplicate settlement.
16. Every consequence has a unique decision/action nonce.
17. Accounting is conserved.
18. An entitlement cannot be redirected after finalization.
19. A failed payout transport cannot erase the underlying entitlement.
20. No value-holding state may remain locked forever.

## Authorization

21. Agreement activation freezes consequential policy parameters.
22. No administrator can replace frozen evidence authorities.
23. No administrator can manufacture a finalized verdict.
24. Agent delegation is bounded by explicit scope, amount, expiry, and permitted
    action class.
25. Delegated authority cannot delegate more authority than it owns unless the
    parent policy explicitly permits it.

## Liveness

26. Every value-holding state has at least one bounded exit.
27. Disappearing participants cannot permanently freeze unrelated funds.
28. Evidence outages have explicit repair/expiry behavior.
29. Challenge periods are finite.
30. Recovery cannot create a second economic consequence.

## Release integrity

31. Release source is content-addressed before signing.
32. Toolchain is pinned by immutable commit/hash.
33. Network identity is checked before every authorized write.
34. Deployment preflight is read-only.
35. Failed one-shot authorization is never silently reused.

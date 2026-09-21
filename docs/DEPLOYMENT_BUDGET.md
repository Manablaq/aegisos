# Deployment Budget

Status: **PROVISIONAL PROJECT SAFETY POLICY**

These numbers are AegisOS engineering budgets, not claims about formal GenLayer
protocol limits.

## Historical signal

Prior Bradbury work observed a monolithic Intelligent Contract deployment with:

- source size: 51,757 bytes;
- estimated deployment gas: approximately 40.39M;
- observed transaction gas ceiling: 16,777,216.

That class of architecture is prohibited for AegisOS.

## AegisOS provisional source budget

Before exact Bradbury prototype certification:

- preferred production source target: <= 15,000 UTF-8 bytes;
- architecture review stop: > 18,000 UTF-8 bytes.

Crossing the review stop does not mean deployment is impossible.

It means the candidate is not allowed to proceed toward signing without a new
architecture review and fresh admission measurements.

## Payload rule

Source bytes are not sufficient evidence.

For every deployment candidate record:

- exact source bytes;
- source SHA-256;
- exact encoded deployment transaction bytes;
- encoded payload size;
- exact runner dependency;
- constructor calldata;
- live gas estimate;
- current block gas limit / applicable ceiling;
- fee policy;
- sender balance;
- sender nonce;
- consensus contract address;
- network identity.

## Gas rule

No fixed gas safety percentage is frozen yet.

A numeric margin will be chosen only after the compact prototype has been
measured against current Bradbury behavior.

Until that measurement exists, production signing is blocked.

## Fail-closed deployment

Deployment tooling must refuse to sign when:

- gas estimation fails;
- network identity differs;
- nonce differs;
- source hash differs;
- payload differs;
- fee configuration differs;
- balance is insufficient;
- the candidate exceeds its certified release budget.

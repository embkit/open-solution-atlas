# ADR-0001 — Tariff arithmetic runs in a separate, governed engine

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that tariff calculation is **regulated math** — rules must be
versioned, auditable and effective-dated.

The reason this is an architecture decision rather than a configuration note is a
single observation: **a tariff change inside billing code is indistinguishable
from a bug fix in a release.** Both arrive as a deploy, both change what customers
are charged, and neither is distinguishable afterwards except by someone
remembering.

A regulated rate cannot be managed that way. It has an authority behind it, a
date it takes effect, and a requirement that customers already billed under the
old rate keep the old rate.

## Options considered

1. **Tariff as business logic inside the billing engine** — simplest to build.
   A rate change ships with a release, is indistinguishable from a fix, and
   cannot be given an effective date that a straddling cycle can respect.
2. **Tariff as a configuration table with effective dates** — better, and it
   makes versioning possible. But the arithmetic still lives in billing code, so
   a "rate change" still means a deploy when the *computation* changes, and the
   boundary is a convention rather than a component.
3. **A separate governed engine** — rule sets and their versions are governed
   artefacts with an authority, a published date and an effective range; billing
   consumes them and stamps the version it used on every charge.

## Decision

Option 3, enforced by BR-08 (versioned, auditable, effective-dated), BR-14
(tariff arithmetic is a governed input), FR-008, FR-009, FR-020, and NFR-006 as
an invariant.

The engine is governed: a rule version is a dated, published artefact with an
authority behind it. The pack deliberately encodes **no** tariff content — its job
is to make versioning, effective-dating and auditability structural so a
deployment's governed rules can be supplied.

## Consequences

- Positive: a rate change is a governed, published, effective-dated act, so it is
  attributable to a version and not to a release.
- Positive: a cycle straddling an effective date splits by evaluation
  (FR-009), so correctness is a property of the engine rather than an operator's
  care.
- Positive: the pack can be honest about what it does not know: with no tariff
  content encoded, there is nothing here to become silently wrong.
- Negative: the engine requires a governance process that billing never needed.
  Someone must own rule versions and publish them; a pack that installs the
  engine without the process produces a governed component nobody governs.
- Negative: the version stamp on every charge is a mandatory field, and a
  missing stamp is a correctness failure rather than a data-quality issue.
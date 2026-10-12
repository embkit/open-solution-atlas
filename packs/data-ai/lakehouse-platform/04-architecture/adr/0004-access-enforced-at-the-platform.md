# ADR-0004 — Classification-driven access is enforced by the platform, or it is not enforced

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that classification and access are enforced **in the
warehouse, not only in BI**.

The word doing the work is "only". A control in the BI layer is not a weaker
control; it is a control that covers one consumer out of several, and the
consumers that bypass it are not exotic — they are the ordinary ones:

- a data-science workspace or notebook;
- an export to a file, a dashboard image, or a partner feed;
- an ad-hoc query by someone holding warehouse credentials;
- a scheduled job that reads directly.

All of them are consumers of the same classified data.

## Options considered

1. **Access in the BI layer** — simplest, and every other consumer above bypasses
   it. The control covers the friendly path only.
2. **Access in both places** — the control exists twice, and the two definitions
   drift, which is the same failure as a duplicated rule elsewhere in this
   repository.
3. **Access enforced by the platform for every consumer path** — one enforcement
   point, with every consumer onboarded against the consumer contract.

## Decision

Option 3, enforced by BR-09, FR-013, FR-014, and NFR-009.

The consumer contract (`integration.md`) requires five acceptances, and the fourth
— deletion reachability — is the one that makes the control real: a consumer whose
copies the deletion pipeline cannot reach is a governance gap rather than a
convenience.

A consumer that cannot accept the platform's enforcement is **not onboarded**.
There is no exception surface, because an exception surface is where a governed
platform quietly stops being governed.

## Consequences

- Positive: one enforcement point, so a new consumer inherits the control by
  construction and control does not degrade as the number of consumers grows.
- Positive: "who read what?" is answerable from the platform's own audit trail,
  because every read went through the platform.
- Negative: consumers that historically read directly stop working, including
  data-science workspaces whose snapshots are unreachable by deletion. The pack's
  answer is that those are not onboarded, which is a real cost to real teams.
- Negative: the platform's access path becomes a dependency on every read, which
> has an availability consequence. The pack does not resolve the read-failure mode,
> but it states that failing open is not an option.
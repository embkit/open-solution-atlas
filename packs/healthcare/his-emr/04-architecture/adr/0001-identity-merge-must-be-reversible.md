# ADR-0001 — Patient identity merges must be reversible, and unmerge must propagate

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires that EMPI unmerge must be possible and audited.

The requirement reads as an operational nicety. It is not: patient identity is the
root of every clinical fact, and both directions of error are harmful.

- **A duplicate** silently splits a history — two records, two halves of one
  patient's care, and neither is complete.
- **A wrong merge** combines two lives — and this is the one that cannot be undone
  if the platform does not expose unmerge.

The mechanism of a wrong merge is usually a score threshold that fired without a
human, because the threshold was set to reduce the duplicate backlog.

## Options considered

1. **Auto-merge above a threshold** — the backlog falls, and the platform makes an
   irreversible decision about a person. The evidence is a score.
2. **Merge, no unmerge** — the merge is at least recorded, and a wrong one becomes
   permanent. This is the common implementation.
3. **Human-reviewed merge, recorded with confidence, with unmerge that
   propagates to clinical facts** — the decision is attributable, and it is
   reversible.

## Decision

Option 3, enforced by BR-04, BR-05, BR-06, FR-001 through FR-006, and NFR-003 as
an invariant.

The operative property is the second half of option 3: an unmerge must **propagate
to the clinical facts** attached to the merged profile — encounters, observations,
documents. An unmerge that stops at the profile leaves the merged profile's
clinical history asserting an identity that no longer exists.

## Consequences

- Positive: a wrong identity decision is correctable, and the record's history
  remains defensible afterwards.
- Positive: match confidence is visible to clinicians (FR-006) rather than
  hidden behind a resolved-looking patient.
- Negative: an unresolved duplicate flag is surfaced to clinicians, which is
  friction in the workflow. The pack's position is that this is correct: a
  duplicate silently resolved is worse than an ambiguity a clinician sees.
- Negative: propagating an unmerge touches the identity graph rather than a
> record, which is more expensive and more failure-prone than a profile edit.
> NFR-003 measures that propagation happens because it is the part that gets
> skipped.
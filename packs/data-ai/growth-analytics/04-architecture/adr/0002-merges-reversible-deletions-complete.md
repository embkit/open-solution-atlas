# ADR-0002 — Merges are reversible and deletions cover the join keys

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires identity merging to be reversible and deletable for privacy.

The classic growth-analytics pattern is to stitch a user across devices and
sessions into one profile. That pattern has two costs, and they are different:

- **A merge that cannot be undone.** Duplicate patients split a history; a wrong
  merge combines two lives. An identity merge that cannot be unmade is a decision
  made about a person that nobody can correct.
- **A deletion defeated by its own join keys.** A profile is deleted, but the
  events still carry the anonymous identifier the merge used — so the identity is
  reconstituted from residue.

The second is the one that usually survives review, because deleting the profile
record *looks* complete.

## Options considered

1. **Merge, without unmerge** — simplest, and it makes an irreversible decision
   about a person.
2. **Merge with unmerge, and deletion of the profile record** — fixes the first
   and leaves the second. This is the common implementation, and it is not a
   deletion.
3. **Merge with recorded join keys, unmerge that propagates, and deletion that
   covers profile, join keys and derived facts** — the mechanism matches the
   failure it is defending against.

## Decision

Option 3, enforced by BR-03, BR-04, FR-005, FR-006, FR-007, and NFR-003 and
NFR-004.

The three-part deletion is the operative rule: **profile, join keys, derived
facts.** Leaving any one of the three leaves the identity reconstructible or the
history inconsistent.

## Consequences

- Positive: an erasure request is verifiable rather than assumed, and NFR-004
  measures all three parts separately because the third is the one that gets
  skipped.
- Positive: an unmerge propagates to derived facts, so a corrected identity does
  not leave cohort memberships and funnel steps asserting the old one.
- Negative: derived-fact propagation means a merge or unmerge touches the
  identity graph, not a record. That is more expensive and more failure-prone
  than a profile edit.
- Negative: covering the join keys constrains what the merge may key on. An
  identifier that must survive deletion cannot be a permanent join key, which
> rules out some stitching strategies.
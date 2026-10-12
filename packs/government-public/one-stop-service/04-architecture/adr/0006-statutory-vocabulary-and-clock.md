# ADR-0006 — The lifecycle uses the statutory vocabulary, the clock starts at acceptance, and two notices are different steps

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires approval lifecycles to use Chinese statutory vocabulary —
受理/审查/决定/出件, 一次性告知, 限时办结. Three statements are bundled there, and
each is a separate decision.

**The vocabulary carries legal meaning.** These are not workflow statuses; they are
terms that describe legally defined acts. Using them loosely in a UI or a data
model creates a mis-description, and the mis-description is invisible because the
words look right — the same shape as the sibling workflow-bpm pack's 会签 problem.

**The clock starts at 受理, not at submission.** This one is a pack design position
rather than a citation, and it is here because the ambiguity resolves in the
flattering direction if left implicit: measuring from submission while the
obligation runs from acceptance makes every reported performance number better and
makes the obligation look met when it is not.

**一次性告知 and 补正 are different steps.** They are routinely conflated, and the
conflation is not cosmetic: 一次性告知 happens **before** acceptance and must be
complete, while 补正 happens **after** and covers missing or defective material.

## Options considered

1. **Generic workflow statuses** (submitted / in review / approved) — familiar, and
   they mis-describe every legally defined act. "Accepted" and "approved" become the
   same word, and the clock's meaning is lost with them.
2. **The statutory vocabulary, with a shared status field** — the terms are used and
   the underlying model is a generic state machine. The generic field is what
   reports, and the terms are labels.
3. **The statutory vocabulary as the model, with the clock anchored at 受理 and the
   two notices as distinct steps** — the terms are the artefact.

## Decision

Option 3, enforced by BR-06, BR-07, BR-09, FR-015 through FR-019, FR-023, FR-024,
and model constraints 3, 4 and 5.

The vocabulary is uniform across channels (FR-016), because a channel that renames
受理 has acquired a state vocabulary, and a state vocabulary is how a fork starts.

## Consequences

- Positive: the applicant sees an artefact whose name matches the legal act, and the
  clock's meaning is unambiguous because its start is recorded rather than inferred.
- Positive: an incomplete application is told once, completely, which is what
  第十八条 requires and what distinguishes it from an iterative rejection loop.
- Negative: the clock-start choice materially changes every reported number, and a
> deployment that has historically reported from submission will see its numbers
> get worse. The pack's position is that this is the honest direction and that
> NFR-010 exists to catch the older calculation persisting.
# ADR-0002 — A signed clinical document is evidence, and it is amended by addendum

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires that every amendment to a signed clinical document is an
addendum, never an in-place edit.

The reason is not that editing is inconvenient. It is that a signed note is
**evidence of what was thought at a moment in time**, and correcting it in place
destroys the evidence and the clinical record at once.

That combination is what makes the failure serious. A record that has been edited
in place cannot be defended in any later review — which is exactly when it needs
defending: after an outcome, in a complaint, in a legal proceeding.

## Options considered

1. **In-place editing with a version history** — the current text is always right
   and the history exists somewhere. The problem is that "what was thought then"
   is a reconstruction, and a reconstruction is exactly what evidence cannot be.
2. **In-place editing with no history** — the record becomes whatever it most
   recently was, and the previous content is gone.
3. **Append-only after signing: corrections are attributed, time-stamped addenda
   referencing the original; retraction marks a document never valid and keeps
   it visible** — the history is the artefact.

## Decision

Option 3, enforced by BR-07, BR-08, FR-007, FR-008, FR-009, and NFR-001 as an
invariant.

Authorship and signature are separate properties: authorship is who wrote it,
signature is the attestation that it is complete and correct (BR-07). The pack
keeps them separate because conflating them makes "signed" a word with no defined
referent — and the distinction is operationally real: an entry by a covering
clinician is signed but not authored; a dictation transcribed by a scribe is
authored but not signed.

A retraction marks the document never valid (e.g. filed on the wrong patient) and
**keeps the original visible** (BR-08) — deleting it would erase the evidence
that the error occurred.

## Consequences

- Positive: the record is defensible after the fact, which is the only moment it
  matters.
- Positive: the correction path is attributable, so "who changed this and why" is
  answered by the artefact rather than by a database diff.
- Negative: the record grows, and finding "the current truth" requires folding
  the chain. A reader sees a sequence, not a statement.
- Negative: NFR-002 (addendum rate) has no correct value. A rising rate is not a
> documentation problem — it is an authoring defect upstream, which is why the
> signal is reviewed for its direction rather than alarmed on its value.
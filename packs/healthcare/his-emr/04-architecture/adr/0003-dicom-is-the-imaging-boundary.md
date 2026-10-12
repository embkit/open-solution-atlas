# ADR-0003 — Imaging crosses into the platform as DICOM objects, and the objects are retained

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires DICOM as the imaging boundary, not ad-hoc tables.

The temptation is to normalise imaging into relational tables — patient, study,
modality, a report text field — and discard the objects once the extracted
metadata is stored. The report renders, the list view works, and everything looks
fine.

The problem is that DICOM is not a set of attributes with an image attached. It
is a mature, modality-driven object model in which the pixels, the presentation
state, the calibration, the series structure and the private tags each carry
meaning that the extraction did not capture. Decomposition is **irreversible**:
there is no path back from a table row to the object it came from.

## Options considered

1. **Metadata extraction, objects discarded** — the list view works, and every
   downstream need the modelling did not anticipate becomes impossible.
2. **Objects retained, plus a parallel relational index** — both exist, and the
   question is which one is authoritative when they disagree. In practice they
   disagree, and nobody notices for a year.
3. **Objects are the record; the platform references them and may index them for
   search, but the index is never authoritative** — one source of truth, with the
   boundary at the object.

## Decision

Option 3, enforced by BR-10, FR-013, FR-014, and NFR-008 as an invariant.

The platform stores and references DICOM objects. Indexing for search and
presentation is permitted; substituting the index for the objects is not. This is
the same pattern as the clinical/billing separation (ADR-0005) and the
raw/conformed separation in the `lakehouse-platform` sibling: one authoritative
layer, and a derived one that must never become the source of truth.

## Consequences

- Positive: a downstream need the model did not anticipate remains satisfiable
  from the objects, rather than being impossible by construction.
- Positive: the boundary is at a public standard, so exchange with RIS, PACS and
  regional platforms does not require a bespoke mapping.
- Negative: object retention has a storage cost, and the objects are subject to
  the same retention policy as the record (BR-15) rather than being expendable
  cache.
- Negative: an index that diverges from the objects is a defect rather than a
> stale-cache event, and detecting that divergence requires re-reading objects —
  which is why NFR-008 counts studies whose objects were discarded rather than
  counting index staleness.
# 02 · Non-Functional Requirements

> Measurable targets. **Numeric targets marked `(A)` are policy assumptions, not
> facts** — recorded so they can be pinned, argued and changed; their basis is in
> [`../SOURCES.md` §4](../SOURCES.md).
>
> Formulas are pinned so any party reproduces the same number. A target without a
> formula is an aspiration.
>
> `verification: unverified` — targets are pack design.

## NFR-001 — Grant completeness
- **Target**: 100%. Every data transfer has a live, purpose-matching grant.
- **Formula**: `count(transfers with a live grant) / count(transfers)`.
- **Rationale**: an invariant (BR-08). A transfer without a grant is an
  unaccountable transfer, and this is the pack's closed-loop rule.

## NFR-002 — Closed-loop traceability
- **Target**: 100% of shares walkable back to an approval.
- **Formula**: `count(shares traceable to an approval) / count(shares)`.
- **Rationale**: BR-08, FR-018. The loop is a **cycle**, not a sequence: every
  share to a grant, every grant to an approval, lineage closing to the source
  resource.

## NFR-003 — Revocation lead time
- **Target (A)**: p95 ≤ 5 minutes from revocation to access actually removed.
- **Formula**: `access_removed_ts - revocation_ts` at p95.
- **Rationale**: BR-07. The named target is the act being removed, not the record
  being written — a grant revoked but still usable is a revocation in name only.

## NFR-004 — Classification-rule coverage
- **Target**: 100% of classified datasets inherit rules derived from their grade.
- **Formula**: `count(datasets with derived rules) / count(classified datasets)`.
- **Rationale**: BR-04. A dataset with a grade but no derived rule is the
  documentation-not control case.

## NFR-005 — Classification enforcement coverage
- **Target**: 100% of reads enforce classification-derived access; 0 bypass paths.
- **Formula**: `count(consumer paths enforcing) / count(consumer paths)`.
- **Rationale**: BR-04, ADR-0004. A classification in the BI tool or in a
  consumer's own code is not enforced — a notebook is a consumer.

## NFR-006 — Catalog currency
- **Target (A)**: ≥ 95% of entries meeting their update obligation.
- **Formula**: `count(entries with current updates) / count(entries)`.
- **Rationale**: BR-02. This is the signal that lets a department demonstrate its
  duty rather than assert it.

## NFR-007 — Staleness resolution
- **Target (A)**: p95 ≤ 15 working days from staleness raised to resolved.
- **Formula**: `resolved_ts - raised_ts` at p95.
- **Rationale**: BR-10. A staleness finding with no owner and no latency is a
  report nobody reads.

## NFR-008 — Purpose-conformance measurability
- **Target (A)**: 100% of grants have a structured purpose that can be evaluated.
- **Formula**: `count(grants with structured purpose) / count(grants)`.
- **Rationale**: BR-05. A free-text purpose cannot answer "did the consumer stay
  within it?", which is the question the declared purpose exists to make
  answerable.

## NFR-009 — Grant expiry enforcement
- **Target**: 100% of grants with a duration end automatically at expiry.
- **Formula**: `count(grants expired on time) / count(grants with duration)`.
- **Rationale**: BR-07. A grant whose duration is advisory is a grant that runs
  until someone notices.

## NFR-010 — Exchange success rate
- **Target (A)**: ≥ 99% of granted exchanges complete within their window.
- **Formula**: `count(exchanges completed in window) / count(granted exchanges)`.

## NFR-011 — Channel auditability uniformity
- **Target**: 100% of channels produce the same grant and lineage record.
- **Formula**: `count(channels with uniform records) / count(declared channels)`.
- **Rationale**: BR-09. If table-to-table, file and interface differ in
  auditability, the closed loop has a hole at whichever channel is least
  instrumented.

## NFR-012 — Open-data description completeness
- **Target**: 100% of published datasets and distributions carry DCAT metadata.
- **Formula**: `count(described distributions) / count(published distributions)`.
- **Rationale**: BR-11.

## NFR-013 — Provider-side consistency
- **Target (A)**: ≥ 99% of reconciled periods show provider-held and delivered
  data consistent.
- **Formula**: `count(consistent periods) / count(reconciled periods)`.
- **Rationale**: BR-12. The provider's duty under 第十三条 is to keep shared data
  consistent with what it holds; this measures the duty rather than the
  complaints.

## Pinned formulas

| Quantity | Definition |
|---|---|
| **Live grant** | a recorded, unexpired, unrevoked grant whose purpose covers the transfer |
| **Purpose-matching transfer** | a transfer whose recorded purpose is evaluated against the grant's structured purpose |
| **Revocation completion** | access removed at the platform and at every channel the grant permitted |
| **Derived rule** | masking and access rules computed from a classification grade, not authored per dataset |
| **Closed-loop share** | a transfer that resolves to a grant, the grant to an approval, and the approval to a requester and basis |
| **Catalog currency** | an entry whose update obligation is met within its recorded period |

> ⚠️ ASSUMPTION — every `(A)` target is policy. The repository does not claim
> these come from a benchmark, a regulation, or a deployment.
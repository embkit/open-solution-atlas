# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Catalog & resource registry

### FR-001 — Catalog entry as root
- **WHEN** a resource is registered
- **THE SYSTEM SHALL** create a catalog entry linking provider, resource, classification grade, share type and consumers, and SHALL NOT permit a resource to be shared without one (BR-01)
- Traces: CAP-01, BR-01, ADR-0001

### FR-002 — Authorization references the entry, not the source
- **WHEN** a grant or approval is created
- **THE SYSTEM SHALL** reference the catalog entry, and SHALL NOT resolve a grant against a source system directly (BR-01)
- Traces: CAP-01, CAP-02, BR-01, ADR-0001

### FR-003 — Update obligation recorded
- **WHEN** a catalog entry is created or changed
- **THE SYSTEM SHALL** record the department's update obligation and its trigger events (BR-02)
- Traces: CAP-01, BR-02, ADR-0002

### FR-004 — Catalog staleness signal
- **WHEN** the currency review runs
- **THE SYSTEM SHALL** flag entries whose update obligation is unmet, and SHALL NOT present the catalog as current without that signal (BR-02)
- Traces: CAP-01, BR-02, ADR-0002

### FR-005 — Refusal records its basis
- **WHEN** a conditional request is refused
- **THE SYSTEM SHALL** record the basis, and SHALL NOT record a bare denial (BR-03)
- Traces: CAP-01, CAP-02, BR-03, ADR-0003

### FR-006 — Not-shareable entry requires a legal basis
- **WHEN** a resource is classified not-shareable
- **THE SYSTEM SHALL** require a recorded legal, regulatory, or CPC Central / State Council policy basis, and SHALL NOT permit publication without one (BR-03)
- Traces: CAP-01, BR-03, ADR-0003

## CAP-05 Classification & masking

### FR-007 — Grade drives rules
- **WHEN** a classification grade is assigned
- **THE SYSTEM SHALL** derive the masking and access rules for that grade from the policy, stated per class (BR-04)
- Traces: CAP-05, BR-04, ADR-0004

### FR-008 — Rule derivation is not per-dataset
- **WHEN** a new dataset is onboarded
- **THE SYSTEM SHALL** inherit control from its grade automatically, and SHALL NOT require a hand-granted dataset-specific rule (BR-04)
- Traces: CAP-05, BR-04, ADR-0004

### FR-009 — Grade change re-derives
- **WHEN** a grade is changed
- **THE SYSTEM SHALL** re-derive the masking and access rules, and SHALL NOT patch individual dataset rules (BR-04)
- Traces: CAP-05, BR-04, ADR-0004

### FR-010 — Masking applied at exchange
- **WHEN** data is released to a consumer
- **THE SYSTEM SHALL** apply classification-driven masking before release, and SHALL NOT rely on the consumer to mask (BR-04)
- Traces: CAP-05, CAP-04, BR-04, ADR-0004

### FR-011 — Enforcement is testable
- **WHEN** access is evaluated against a grade
- **THE SYSTEM SHALL** produce a decision that can be tested against the policy, so an unenforced grade is detectable (BR-04)
- Traces: CAP-05, CAP-07, BR-04, ADR-0004

## CAP-02 Authorization & grant lifecycle

### FR-012 — Grant records purpose, scope, duration
- **WHEN** an approval creates a grant
- **THE SYSTEM SHALL** record the consumer, the resource, the **declared purpose**, the scope and the duration, and SHALL NOT create a grant without a purpose (BR-05)
- Traces: CAP-02, BR-05, ADR-0005

### FR-013 — Purpose is checkable
- **WHEN** a grant's purpose is recorded
- **THE SYSTEM SHALL** record it as a structured attribute that can be evaluated for conformance, and SHALL NOT accept free text that cannot be checked (BR-05)
- Traces: CAP-02, CAP-10, BR-05, ADR-0005

### FR-014 — Unconditional share without negotiation
- **WHEN** a request targets an unconditional resource
- **THE SYSTEM SHALL** grant without per-consumer negotiation while still recording the share, and SHALL NOT gate it behind a conditional workflow (BR-06)
- Traces: CAP-02, BR-06

### FR-015 — Revocable grant
- **WHEN** a grant is created
- **THE SYSTEM SHALL** make it revocable, and SHALL NOT create an irrevocable one (BR-07)
- Traces: CAP-02, BR-07, ADR-0005

### FR-016 — Revocation lead time
- **WHEN** a grant is revoked
- **THE SYSTEM SHALL** actually remove the consumer's access and record the completion, and SHALL NOT treat recording as revocation (BR-07)
- Traces: CAP-02, BR-07, ADR-0005

### FR-017 — No transfer without a grant
- **WHEN** any transfer is attempted over any channel
- **THE SYSTEM SHALL** require a live, purpose-matching grant, and SHALL NOT perform the transfer without one (BR-08)
- Traces: CAP-02, CAP-04, BR-08, ADR-0005

### FR-018 — Closed loop is traceable
- **WHEN** a share occurs
- **THE SYSTEM SHALL** record the grant, the approval, the consumer and the delivered artefact, and SHALL NOT permit a share that cannot be walked back to its approval (BR-08)
- Traces: CAP-02, CAP-06, BR-08, ADR-0005

## CAP-04 Exchange channels

### FR-019 — Channels declared
- **WHEN** data is exchanged
- **THE SYSTEM SHALL** use a declared channel — table-to-table, file or interface — and SHALL NOT permit a channel outside the declared set (BR-09)
- Traces: CAP-04, BR-09

## CAP-01 / CAP-10 Governance

### FR-020 — Staleness routed
- **WHEN** a stale entry is detected
- **THE SYSTEM SHALL** route it to the provider with an owner, and SHALL NOT report staleness without one (BR-10)
- Traces: CAP-01, BR-10

### FR-021 — Open dataset description
- **WHEN** an open dataset is published
- **THE SYSTEM SHALL** describe it with W3C DCAT metadata — dataset, distribution, publisher, theme (BR-11)
- Traces: CAP-08, BR-11

### FR-022 — Every distribution described
- **WHEN** an open dataset has distributions
- **THE SYSTEM SHALL** publish each with its own DCAT distribution record, and SHALL NOT publish an undescribed form (BR-11)
- Traces: CAP-08, BR-11

### FR-023 — Two-way consistency
- **WHEN** reconciliation runs
- **THE SYSTEM SHALL** compare what the provider holds against what was delivered, and report the discrepancy to the provider (BR-12)
- Traces: CAP-10, BR-12

### FR-024 — Purpose-conformance reporting
- **WHEN** the governance review runs
- **THE SYSTEM SHALL** report usage against declared purposes, so 第十四条 conformance is an auditable question rather than an assumption (BR-05, BR-08)
- Traces: CAP-10, CAP-02, BR-05, BR-08

### FR-025 — Closed share-type vocabulary
- **WHEN** a catalog entry is created or its share type is changed
- **THE SYSTEM SHALL** accept only the three defined types — unconditional, conditional, not-shareable — and SHALL NOT permit a fourth value or one outside a governing instrument (BR-13)
- Traces: CAP-01, BR-13, ADR-0006

### FR-026 — Publication basis recorded separately
- **WHEN** a dataset is proposed for open-data publication
- **THE SYSTEM SHALL** record a publication basis distinct from the sharing grant, and SHALL NOT treat "shareable" as an implied basis for publication (BR-14)
- Traces: CAP-08, BR-14
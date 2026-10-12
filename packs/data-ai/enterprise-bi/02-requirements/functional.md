# 02 · Functional Requirements

> EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
> Stable IDs forever; each traces to a capability (`CAP-xx`), rule (`BR-xx`) and
> ADR. Acceptance criteria (AC-*) are defined at L3.
>
> `verification: unverified` — these requirements are pack design, not validated
> against a deployment.

## CAP-01 Product master (shared), CAP-02 Pricing & promotions (not in scope here)

> CAP-01/CAP-02 in the capability map describe the shared product master and the
> sibling's pricing surface. This pack's requirements start at the semantic model.

## CAP-01 Semantic model

### FR-001 — Owned, versioned metric definition
- **WHEN** a metric definition is created or changed
- **THE SYSTEM SHALL** require a named owner and a version, and SHALL NOT accept a definition without either (BR-01)
- Traces: CAP-01, BR-01, ADR-0001

### FR-002 — Single join key
- **WHEN** two metrics are used in the same artifact
- **THE SYSTEM SHALL** require them to join on one declared join key, and SHALL NOT permit comparability by name match (BR-01)
- Traces: CAP-01, BR-01, ADR-0001

### FR-003 — Version history retained
- **WHEN** a definition is revised
- **THE SYSTEM SHALL** retain the prior versions, so an artifact pinned to an older version remains interpretable (BR-01, BR-06)
- Traces: CAP-01, BR-01, BR-06

### FR-004 — Declared relationships
- **WHEN** an entity relationship is required for a join
- **THE SYSTEM SHALL** require it to be declared in the semantic model, and SHALL NOT permit joining by convention (BR-02)
- Traces: CAP-01, BR-02, ADR-0001

## CAP-03 Access control

### FR-005 — RLS/CLS in the semantic model
- **WHEN** a row- or column-level access rule is defined
- **THE SYSTEM SHALL** attach it to the semantic model, evaluated in the query context, and SHALL NOT accept a rule defined only on a dashboard (BR-03)
- Traces: CAP-03, BR-03, ADR-0002

### FR-006 — Rule evaluation for every consumer
- **WHEN** any consumer — interactive, embedded, exported or administrative — consumes data through the semantic layer
- **THE SYSTEM SHALL** evaluate the same RLS/CLS rules (BR-03, BR-10)
- Traces: CAP-03, BR-03, BR-10

### FR-007 — Rule testability
- **WHEN** an RLS/CLS rule is changed
- **THE SYSTEM SHALL** allow it to be tested in isolation and audited as a definition (BR-03)
- Traces: CAP-03, BR-03

### FR-008 — Identity context propagation
- **WHEN** a query is executed
- **THE SYSTEM SHALL** pass user identity and attributes into the query context, and SHALL NOT substitute presentation-time filtering (BR-04)
- Traces: CAP-03, BR-04, ADR-0002

### FR-009 — Uniform scoping across surfaces
- **WHEN** a user opens any query surface, including sandbox, preview, embed and admin tooling
- **THE SYSTEM SHALL** scope data by the same RLS/CLS evaluation, and SHALL NOT provide a bypass surface (BR-10)
- Traces: CAP-03, BR-10, ADR-0002

## CAP-05 Certified artifacts

### FR-010 — Artifact version pinning
- **WHEN** a certified artifact is published
- **THE SYSTEM SHALL** pin it to a model version, and SHALL NOT let a new version silently change it (BR-06)
- Traces: CAP-05, BR-06, ADR-0003

### FR-011 — Change impact report
- **WHEN** a model version is published
- **THE SYSTEM SHALL** report which artifacts pin which versions and what the change would affect, before any artifact migrates (BR-06)
- Traces: CAP-05, BR-06, ADR-0003

### FR-012 — Computed freshness
- **WHEN** an artifact is rendered
- **THE SYSTEM SHALL** compute freshness against its model's freshness contract, and SHALL NOT derive it from the last database write (BR-07)
- Traces: CAP-05, BR-07, ADR-0004

### FR-013 — Computed certification, visible without interaction
- **WHEN** an artifact is rendered
- **THE SYSTEM SHALL** derive certification from the model contract and pipeline state and display it without the user having to click (BR-07)
- Traces: CAP-05, BR-07, ADR-0004

## CAP-07 Serving, embeds & distribution

### FR-017 — Embed is a consumer
- **WHEN** a metric is embedded into another product
- **THE SYSTEM SHALL** evaluate it under the same semantic layer and the same RLS/CLS, and SHALL NOT permit an embedded surface to read outside the layer (BR-08)
- Traces: CAP-07, BR-08, ADR-0002

## CAP-06 Self-service & promotion

### FR-014 — Certified/user boundary
- **WHEN** content is created
- **THE SYSTEM SHALL** record it as user content or certified, with no third state (BR-05)
- Traces: CAP-06, BR-05, ADR-0005

### FR-015 — Promotion path
- **WHEN** user content is submitted for promotion
- **THE SYSTEM SHALL** route it through review and either publish it as certified or reject it **with a reason** (BR-05)
- Traces: CAP-06, BR-05, ADR-0005

### FR-016 — Certified attach on publication
- **WHEN** user content is published as certified
- **THE SYSTEM SHALL** attach an owner, a pinned model version and a freshness contract, without which it cannot become certified (BR-05, BR-06, BR-07)
- Traces: CAP-06, CAP-05, BR-05, BR-06, BR-07

## CAP-09 Governance, audit & lifecycle

### FR-018 — Staleness flagged with ownership
- **WHEN** the governance review runs
- **THE SYSTEM SHALL** flag artifacts pinned to superseded content as stale, and SHALL NOT silently delete them (BR-09)
- Traces: CAP-09, BR-09, ADR-0003

### FR-019 — Authoritative record for audit
- **WHEN** an audit asks why an artifact said something
- **THE SYSTEM SHALL** answer from the artifact's pinned model version, the definition versions it used, and the access records in force (BR-06, BR-07)
- Traces: CAP-09, BR-06, BR-07

## CAP-10 Platform operations

### FR-020 — Warehouse internals stay in the sibling
- **WHEN** this platform needs ingestion, storage, table-format or transform mechanics
- **THE SYSTEM SHALL** delegate to the `lakehouse-platform` sibling and SHALL NOT re-implement them (AGENTS.md)
- Traces: CAP-10
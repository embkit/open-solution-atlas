# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. No external standard is cited;
> where a rule exists because of an instrument, the instrument is named in
> `02-requirements/compliance.md` as a designation.

## The spine: the schema registry

### BR-01 — No client emits an event whose schema is not declared
*(enforced by FR-001, FR-002, ADR-0001; violated when instrumentation ships before the schema exists in the registry)*

An event arrives once. Nobody can re-ingest last quarter with a different
property name. The declare-before-emit rule is the only defence against an
unrepeatable number.

### BR-02 — Schema version travels with the event; quarantine carries a reason
*(enforced by FR-003, FR-004, ADR-0001; violated when an event is ingested without its schema version, or a validation failure is dropped without its reason)*

Three properties: every event carries its schema version; a malformed event is
quarantined **with the reason**; and exports carry the version so downstream
meaning is traceable.

> A quarantine without a reason is a bin, not a signal.

## Identity

### BR-03 — A merge is recorded, and unmerge propagates
*(enforced by FR-005, FR-006, ADR-0002; violated when an identity merge is silent, or an unmerge leaves derived facts unchanged)*

Merge and unmerge both exist and both are audited. An unmerge must propagate to
derived facts — cohort memberships, funnel steps, experiment assignments.

### BR-04 — Deletion covers profile, join keys and derived facts
*(enforced by FR-007, ADR-0002; violated when a deletion removes the profile but leaves the merge's join keys)*

The mechanism is the point: a merge joins on an anonymous or device identifier,
and that key is what re-identifies a deleted user. A deletion that leaves the
join keys is not a deletion, because the identity can be reconstituted from
residue.

> This is where the classic growth-analytics pattern breaks: the profile is
> deleted, the events still carry the anonymous identifier the merge used, and
> the identity reforms.

## Experimentation

### BR-05 — Assignment lives in the experiment engine, not the delivery system
*(enforced by FR-008, FR-009, ADR-0003; violated when assignment happens in a feature-flag service)*

If assignment lives in delivery, the ratio is unverifiable and **SRM is not
computable at all**, which makes every comparison unverifiable. A flag service
delivers; the experiment engine records.

### BR-06 — Funnels, cohorts and attribution are descriptive; only experimentation is causal
*(enforced by FR-010; violated when an analytical output is read as a causal claim)*

A capability boundary, not a caveat.

### BR-07 — Real statistics: sample size, SRM, guardrails, holdouts
*(enforced by FR-011, FR-012, FR-013, ADR-0003; violated when a result is reported as a percentage comparison without these)*

Five mechanisms, and each is stated as what its absence permits:
- **sample size** — declaring a winner on noise;
- **SRM** — an assignment bug that looks exactly like a result;
- **guardrail metrics** — trading away latency, cancellations, refunds for
  conversion;
- **holdouts** — the experimental program itself drifting;
- **novelty/primacy handling** — reading a short-term behaviour change as a
  long-term effect.

### BR-08 — The decision rule is pre-declared
*(enforced by FR-014, ADR-0003; violated when the ship/hold/kill criterion is chosen after seeing the result)*

Peeking discipline follows from this rather than being a separate warning: with
a pre-declared reading point, stopping early is a violation of the declared rule
rather than a judgement call.

## Destinations and consent

### BR-09 — Ad networks and messaging channels are destinations behind an abstraction, never the data owner
*(enforced by FR-015, FR-016, ADR-0004; violated when a destination's schema is stored as the platform's, or a destination's own numbers are used as the source of truth)*

### BR-10 — The platform owns the event model and the experiment assignment
*(enforced by FR-015; violated when a third party's versioning determines the platform's data model)*

### BR-11 — Consent is enforced at collection **and** at activation
*(enforced by FR-017, FR-018, FR-019; violated when enforcement happens at only one of the two points)*

Two specific failure modes of enforcing at one point only: with enforcement only
at **collection**, the usable purpose set grows by accretion; with enforcement
only at **activation**, a single check is treated as a general licence.

> Consent is therefore a **stateful, purpose-scoped attribute of the data**,
> checked at both boundaries, with revocation effective immediately at both.

### BR-12 — A segment is a snapshot at a point in time
*(enforced by FR-020; violated when a segment is a live view, so a long campaign silently changes membership)*

### BR-13 — Destination schema mapping lives in the abstraction
*(enforced by FR-015, FR-016; violated when the platform stores events in a destination's field names)*

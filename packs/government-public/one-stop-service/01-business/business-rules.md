# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. 国务院令第716号 and 国办发〔2025〕33号
> are quoted at article level in `00-context/regulatory-landscape.md`; no
> conformance is claimed.

## The catalogue root

### BR-01 — A 事项 has one of two statutory kinds
*(enforced by FR-001, FR-002, ADR-0001; violated when the two kinds are modelled as one undifferentiated type, or when a kind is added without an instrument)*

第四条 includes 行政权力事项 and 公共服务事项. They have different legal shapes:
only the first produces a 决定书 with review, reconsideration and appeal
consequences. A single undifferentiated item type models them wrongly.

### BR-02 — The guide is the published contract
*(enforced by FR-003, FR-004, FR-005, ADR-0002; violated when 受理条件, 办事材料 or 办理流程 is absent, or when a published guide changes silently)*

第六条 makes the three elements mandatory and requires the guide to be
**published**. An applicant is entitled to rely on it, so the guide is versioned
and a change is a dated, attributed act.

## Identity and channels

### BR-03 — Identity is the national unified service, never re-implemented
*(enforced by FR-006, FR-007, ADR-0003; violated when the platform holds a citizen identity of its own, or when a channel authenticates independently)*

第五条's 一次认证、全网通办. The platform integrates the national service and
holds no competing identity: re-implementing creates a second identity to
reconcile, and a second one to breach.

### BR-04 — A channel is a variant over the shared core
*(enforced by FR-008, FR-009, ADR-0004; violated when mini-program, POS or a new surface gains its own order model, state vocabulary or 事项 model)*

Channels differ in **input**, **identity handling** and **fulfilment source** —
never in the core objects. The failure of a fork is that the customer buys online
and the store cannot see it, and returns in-store for an online order with the
refund having no home.

## The anti-double-submission rule

### BR-05 — A field obtainable by sharing is never demanded
*(enforced by FR-010 through FR-014, ADR-0005; violated when a sharing-obtainable field is required, or when a lookup failure silently re-asks the applicant)*

第七条. Three consequences:

- every field is classified **obtainable by sharing** or not, per field;
- an obtainable field must not be a **required** input;
- a lookup failure degrades to a **permitted alternative** — never to silently
  asking again.

> Requiring a document is easy; proving it is already available is hard. A
> platform that defaults to asking looks friendlier and is non-compliant.

### BR-06 — The lifecycle uses the statutory vocabulary
*(enforced by FR-015 through FR-017, ADR-0006; violated when a generic workflow status replaces 受理/审查/决定/出件, or when the vocabulary is renamed per channel)*

The terms carry legal meaning in this domain, so using them loosely in a UI or
data model creates a mis-description of a legally defined act.

### BR-07 — 一次性告知 precedes acceptance; 补正 follows it
*(enforced by FR-018, FR-019, ADR-0006; violated when a rework request is issued without prior acceptance, or when a rejection is piecemeal)*

Two different steps with different consequences, and conflating them is how a
platform ends up rejecting an applicant repeatedly instead of once.

### BR-08 — Every cross-department call is consented and audited
*(enforced by FR-020, FR-021, FR-022; violated when a call has no recorded basis, or when a call is made without a recorded purpose)*

A call with no recorded basis is a compliance defect and, at the same time,
evidence that the platform is over-collecting.

### BR-09 — The clock starts at 受理, not at submission
*(enforced by FR-023, FR-024; violated when reported performance is measured from submission while the obligation runs from acceptance)*

A pack design position, not a citation — but recorded as a rule because it
materially changes every reported performance number, and because the ambiguity
resolves in the flattering direction if left implicit.

## Seals, licences, archive

### BR-10 — Seals and licences come from the national services, never re-implemented
*(enforced by FR-025, FR-026, FR-027, ADR-0007; violated when the platform mints a seal, defines its own licence format, or authenticates independently)*

第九条/第十条 and the Electronic Seal Administrative Measures. These are external
platform dependencies integrated through published standards; BR-14 requires the
business systems of administrative and public-service bodies to **support**
compliant seals.

### BR-11 — Archiving is electronic, and the platform's record is the archival object
*(enforced by FR-028, FR-029, ADR-0008; violated when a paper archive remains the record, or when electronic files are archived as attachments to a document management system)*

第十二条's 电子文件不再以纸质形式归档. The platform's application data model, not
the department's filing system, is the record of truth for the process.

### BR-12 — Retention is declared per class
*(enforced by FR-030; violated when one global retention period is applied to applications, documents, seals and logs)*

### BR-13 — The service portal is a consumer, not a substitute for this platform
*(enforced by FR-031; violated when the portal duplicates the 事项 model or the approval state machine)*

### BR-14 — Business systems must support compliant electronic seals
*(enforced by FR-027, CTL-04; violated when a deployment claims an exception without an owner and an expiry)*
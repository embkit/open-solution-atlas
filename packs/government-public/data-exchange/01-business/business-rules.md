# 01-business / Business Rules

> Rules are normative, stable-ID'd, and referenced (never restated) by
> requirements, ADRs and the data model. IDs are immutable once published.
>
> Format: **BR-xx — proposition** *(enforced by, violated when)*.
>
> ⚠️ ASSUMPTION — all rules are pack design. 国发〔2016〕51号 is cited as a public
> instrument; no clause-level mapping is asserted beyond the articles quoted in
> `00-context/regulatory-landscape.md`.

## The catalog

### BR-01 — The catalog entry is the root object
*(enforced by FR-001, FR-002, ADR-0001; violated when a resource is shared without a catalog entry, or when authorization references a source system rather than an entry)*

The entry links **provider, resource, classification grade and consumers**. It is
the object authorization is against, and a share that is not in the catalog is
invisible to the very process that governs it.

### BR-02 — Catalog currency is an obligation
*(enforced by FR-003, FR-004, ADR-0002; violated when a catalog entry has no staleness signal, or when an update duty has no owner)*

The 办法's 第八条 gives departments an update duty within a fixed period. The
platform's job is to make staleness visible — a catalog that cannot demonstrate
its own currency cannot demonstrate the duty.

### BR-03 — A refusal records its basis, and a not-shareable classification requires one
*(enforced by FR-005, FR-006, ADR-0003; violated when a refusal is a bare denial, or when a not-shareable entry carries no legal basis)*

第十条 provides that a not-shareable resource must have a legal, regulatory, or
CPC Central/State Council policy basis. The engineering consequence is a **field,
not a convention**: the catalog entry must storable and display that basis, and a
dropdown with no source-and-basis field cannot satisfy it.

## Classification and access

### BR-04 — Classification grade drives masking and access rules, per class
*(enforced by FR-007 through FR-011, ADR-0004; violated when a grade is recorded but not enforced, or when rules are defined per dataset rather than per class)*

The grade is a policy input. Masking and access rules are derived from it and
stated **per class**, so a new dataset inherits control automatically rather than
being hand-granted.

> A grade recorded but not enforced is documentation rather than control, and it
> is indistinguishable from none until someone tests it.

## Grants

### BR-05 — A grant records purpose, scope and duration
*(enforced by FR-012, FR-013, ADR-0005; violated when a grant records only who and what, or when the purpose is free text that cannot be checked)*

第十四条 limits a consumer to the declared purpose. The declared purpose must
therefore be a **first-class, recorded attribute of the grant** — and "did the
consumer stay within it?" must be an auditable question. A grant recording only
*who* and *what* cannot support that.

### BR-06 — An unconditional share needs no per-consumer negotiation
*(enforced by FR-014; violated when an unconditional resource is treated as conditional, gating shared data behind a workflow it does not need)*

第九条's unconditional type means available to all departments. Negotiating
per-consumer for one inverts the policy — and the 办法's framing is that sharing
is the default.

### BR-07 — A grant is revocable, and revocation is measured by its lead time
*(enforced by FR-015, FR-016, ADR-0005; violated when a grant cannot be revoked, or when revocation is recorded while access persists)*

Revocation's value is the **lead time until access is actually removed**, not the
act of recording it. A grant revoked but still usable is a revocation in name
only.

### BR-08 — No data transfer exists without a grant
*(enforced by FR-017, FR-018, ADR-0005; violated when a transfer occurs outside the grant path, or when a channel permits an ungranted read)*

`AGENTS.md`'s closed-loop rule. The loop is authorization → approval → share →
lineage as a **cycle**, not a sequence: every share traces to a grant, every grant
to an approval, and lineage closes back to the source resource.

> A transfer without a grant is a participation in the loop that cannot be
> audited, which is an unaccountable transfer by another name.

## Channels, governance, open data

### BR-09 — All exchange channels are declared and first-class
*(enforced by FR-019; violated when a channel exists outside the declared set, or when table-to-table, file and interface differ in auditability)*

Whether all three are first-class or one is primary is a recorded open question
(`README.md` #1). What is not open: a channel outside the declared set is illegal.

### BR-10 — Staleness routes to a provider
*(enforced by FR-020; violated when staleness is reported without an owner, or when a stale catalog entry is silently dropped)*

### BR-11 — Open-data metadata follows W3C DCAT
*(enforced by FR-021, FR-022; violated when an open dataset is described in an ad-hoc schema, or when a distribution is published without one)*

### BR-12 — Reconciliation is two-way
*(enforced by FR-023, BR-08; violated when reconciliation runs only platform → consumer)*

The provider's duty under 第十三条 is to keep shared data consistent with what it
holds. Reconciliation is therefore provider-side and consumer-side, and a
discrepancy is the provider's to correct — not a complaint-driven job.

### BR-13 — The share-type vocabulary is closed at three
*(enforced by FR-025, ADR-0006; violated when a fourth share type is invented, or when a share type is added without a governing instrument)*

第九条 defines three: unconditional, conditional, not-shareable. A fourth value
does not exist, and adding one — "restricted", "internal", "pending review" —
produces a share type with no defined sharing behaviour, which is how the
policy's default ("share") quietly inverts.

### BR-14 — Open-data publication basis is distinct from a sharing grant
*(enforced by FR-021, FR-026, ADR-0006; violated when publication is treated as a consequence of being shareable, or when an open dataset's basis is not recorded separately)*
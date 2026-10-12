# AGENTS.md — Omnichannel Commerce (L2)

L2 blueprint. Load in this order; respect every traceability link.

## Loading order

1. `manifest.yaml` — scope, regulatory context, maturity
2. `README.md` — scope, out-of-scope, **settled ADRs**, chapter map, variants
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` (CAP-01..10) → `processes.md` (P-01..P-08) →
   `business-rules.md` (BR-01..BR-15)
5. `02-requirements/` — functional (FR-001..FR-028) → non-functional
   (NFR-001..NFR-012 + pinned formulas) → compliance (CTL-01..CTL-08)
6. `03-domain/` — domain-model (contexts, aggregates, invariants) → glossary
   (use these terms uniformly)
7. `04-architecture/` — overview → integration (I-01..I-09, F-01..F-06) →
   security → observability, then ADR-0001..0005 (settled — do not relitigate)
8. `05-data/` — logical-data-model (10 integrity constraints) → data-dictionary

## Hard rules for expanding to L3 or implementing

- **Reserve and consume are distinct operations** (ADR-0001, BR-01): a reserve
  is reversible and requires an expiry; a consume is irreversible. A global hold
  setting is a defect, and a reservation without `expires_ts` must not exist.
- **Availability is decided in one place** (ADR-0001, NFR-002): the Inventory
  context is the only assignor. A second assignor is an oversell. Availability
  is computed (physical − holds − in-flight), never a stored field alone.
- **Pricing snapshots are immutable and record their ruleset version**
  (ADR-0002, BR-06, NFR-004): no post-capture path re-evaluates promotions. A
  re-pricing creates a **new** snapshot; no path edits an existing one. Enforce
  this in the store, not only in application code.
- **Money operations carry platform-issued idempotency keys** (ADR-0003, BR-07,
  NFR-005): the key is the platform's, not the PSP's, because the PSP's key does
  not cover POS, marketplace or batch paths. A refund is a **new** operation with
  a **new** key — never a negative charge.
- **Reversals are not inverse operations** (BR-09): returns, refunds and
  cancellations get their own states and money operations, re-reading current
  inventory and money state rather than mirroring the forward path.
- **Disposition is decided at authorisation, not receipt** (BR-12): restock or
  scrap, recorded before the physical unit arrives.
- **A channel is a variant over the shared core, never a fork** (ADR-0004,
  BR-14): channel differences are adapter configuration. An adapter that cannot
  declare input, payment path, identity handling, fulfilment sources and
  presentation is not a variant.
- **PCI scope exclusion is demonstrated per channel** (BR-10, CTL-01): hosted
  fields only; the platform holds tokens. A channel that cannot host fields is
  blocked or carries an explicit, owned, expired exception (FR-026, NFR-011).
- **External unavailability degrades the external path, never the core
  invariants** (`04-architecture/integration.md`): the single exception is fraud
  risk, which fails **closed**.
- **The ledger and order events are append-only** (BR-13, constraints 8–9):
  corrections are new entries. Reconciliation **closes** gaps; open gap age
  (NFR-009) is the metric.
- Anything environment-specific → `> ⚠️ ASSUMPTION:`; numeric targets marked
  `(A)` in `non-functional.md` are policy, not facts.
- IDs are immutable; every L3 artifact (contract, AC, task) must resolve to
  FR/NFR/CTL/ADR/BR/CAP IDs.

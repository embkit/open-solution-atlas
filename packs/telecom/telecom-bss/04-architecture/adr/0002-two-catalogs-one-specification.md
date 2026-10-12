# ADR-0002 — Two catalogs joined by a specification, never duplicated

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires the commercial product catalog and the technical/resource
catalog to be distinct models joined by a **specification**, not duplicated.

The failure of duplicating them is concrete, and it is not a tidiness concern:

- every commercial pricing change becomes a network-facing change, and vice
  versa;
- a resource-only product — wholesale, interconnection, M2M SIM — has no
  commercial representation, or acquires a fake one;
- commercial release cycles become gated on network engineering cycles.

The pressure to collapse them is constant, because keeping the specification
current is real work whose cost appears only when nothing goes wrong.

## Options considered

1. **One merged catalog** — simplest to browse, and it makes every commercial
   change a network change. Resource-only products are modelled badly or not at
   all.
2. **Two catalogs plus a mapping table** — separates the models but puts the
   translation in a table nobody owns, so it drifts silently and cannot express
   "how this is verified".
3. **Two catalogs plus a specification object** — a first-class, maintained
   artefact stating what an offering means in resource terms **and how
   realisation is verified**.

## Decision

Option 3, enforced by BR-03 (the specification is first-class), FR-002, FR-004,
and ADR-0001's boundary.

The specification is the **only permitted join** between the catalogs. No other
component infers the relationship, because an inferred relationship is a merged
catalog with extra steps.

## Consequences

- Positive: commercial changes do not require network engineering, and network
  changes do not restate commercial meaning.
- Positive: "what does this customer actually have?" is derivable from the
  specification rather than reconstructed by hand across two systems.
- Positive: an offering may map to several resource realisations (FR-004), which
  is what makes wholesale and interconnect products representable at all.
- Negative: the specification is a live, maintained artefact. A stale
  specification is worse than none, because it is trusted — so its currency
  needs a signal the pack records as a requirement rather than fixing here.
- Negative: publishing an offering now requires an attached specification
  (FR-002), which is a real gate on the commercial side. That friction is the
  point; making it optional is how duplication returns.
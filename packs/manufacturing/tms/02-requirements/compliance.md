# 02 · Compliance Controls

> Controls traced to sources in [`../SOURCES.md`](../SOURCES.md). Controls
> whose clause-level mapping is not yet cited are marked `(A)`.

| ID | Control | Traced to |
|---|---|---|
| CTL-01 | DG consignment validation against regulation data tables before dispatch; hard block on invalid classification (BR-07, FR-017) | ADR 2025 (road, intl.); JT/T 617-2018 + GB 6944-2025 (road, CN); IMDG Code 2024 incl. A42-24 (sea); IATA DGR 67th ed. 2026 (air) — as *data*, not logic |
| CTL-02 | Segregation/stowage validation from the same regulation data at consolidation & load building (BR-08, FR-018) | Same editions as CTL-01 |
| CTL-03 | Supply-chain security management framing: risk-based controls on parties, premises hand-offs, and data; documented review | ISO 28000:2022 (Ed. 2), clause-level mapping `(A)` |
| CTL-04 | Partner-facing event sharing uses EPCIS 2.0/CBV 2.0 standard vocabulary; no PII in shared event payload beyond agreed identifiers | GS1 EPCIS 2.0 / CBV 2.0 (2022-06) |
| CTL-05 | Freight invoices three-way matched with evidence trail; dispute outcomes immutable (FR-015, BR-05, BR-11) | Pack policy (auditability); no external standard claimed |
| CTL-06 | Driver/personal location data: retention limit, purpose limitation, access control | GDPR (EU 2016/679) — principles cited; article-level mapping `(A)` |
| CTL-07 | CN deployment baseline: transport-system zone security per 等保2.0 | GB/T 22239-2019 — standard level only; no article mapping `(A)` |
| CTL-08 | Incoterms® term carried verbatim on the order; system logic must not reinterpret cost/risk allocation (BR-12) | ICC Incoterms® 2020 (11 rules, in force 2020-01-01) |

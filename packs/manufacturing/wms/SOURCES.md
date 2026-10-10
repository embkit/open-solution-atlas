# SOURCES — Warehouse Management System

> Provenance ledger. Maps the pack's load-bearing claims to public, checkable
> sources; anything that could not be traced is listed in §4 and marked
> `> ⚠️ ASSUMPTION:` in the chapters.
>
> **Status: `source-checked`** (2026-10-08). Provenance: `llm-drafted`.
> Verification: `source-checked` — **not** field-verified. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).
>
> Checked against sources on 2026-10-08. This pass found **no factual errors**
> in the cited standards; it did tighten three references from "series /
> generic" to specific parts and versions (GS1 EPCIS/TDS versions, IEC 62443
> parts, ISO 9001 sub-clauses). The remaining uncited specifics are all
> **pack design or engineering budgets**, declared in §4.

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Barcode / AI data model (lot `10`, serial `21`, expiry `17`, qty, weight) — C-05, CTL-02 | GS1 | GS1 General Specifications (AI definitions) — https://ref.gs1.org/standards/ | AI list is normative; the pack uses a subset. Edition to confirm against the current release |
| License-plate / pallet & carton IDs — C-08, FR-008, CTL-02 | GS1 | SSCC, AI **(00)** — the only GS1 key for a logistic unit — https://ref.gs1.org/standards/ | Confirmed: "the SSCC is the only GS1 key that SHALL be used as the identifier of a logistic unit" |
| Location / party identification | GS1 | GLN — https://www.gs1.org/standards/id-keys/gln | |
| Canonical event vocabulary (Object/Aggregation/Transaction/Association; biz steps/dispositions) — C-30, CTL-01 | GS1 | **EPCIS 2.0.0** (ratified June 2022) + **CBV 2.0.0** — https://ref.gs1.org/standards/epcis/ | Pack uses EPCIS as *conceptual* vocabulary; external JSON/JSON-LD + REST exchange is an option (see §4) |
| RFID capture channel — NFR-014 | GS1 | **EPC Tag Data Standard (TDS) 2.3.0**; **EPC UHF Gen2 Air Interface 3.0.1** — https://ref.gs1.org/standards/ | |
| Identification & traceability, preservation, nonconforming output, record control — CTL-01/03/04/05 | ISO | ISO 9001:2015 — **8.5.2** identification & traceability, **8.5.4** preservation, **8.7** control of nonconforming outputs, **7.5** documented information — https://www.iso.org/standard/70089.html | Clause numbers confirmed against the published standard |
| ISMS controls for inventory/commercial data — CTL-06, NFR-009 | ISO/IEC | ISO/IEC 27001:2022 Annex A — A.5.15–A.5.18, A.8.2, A.8.13, A.8.15, A.8.24, A.5.33 — https://www.iso.org/standard/27001 | Shares identical clause numbering with ISO/IEC 27002:2022 |
| IT/OT zones & conduits, equipment boundary — CTL-07, NFR-012 | IEC | **IEC 62443-3-2:2020** (partitioning an IACS into zones & conduits), **IEC 62443-3-3:2013** (system security requirements), **IEC 62443-4-2:2019** (component requirements) | https://webstore.iec.ch/en/publication/30727 · /7033 · /34421 |
| Good Distribution Practice (pharma; FEFO/temp/chain-of-custody) — cold-chain variant | European Commission | EU GDP — **2013/C 343/01** | Variant-only; core encodes the *obligation* |
| Computerized systems / e-records (regulated variant) — CTL-05 | European Commission | EU GMP **Annex 11** (EudraLex Vol. 4) — https://health.ec.europa.eu/medicinal-products/eudralex_en | Variant-only |
| Electronic records / e-signatures (regulated variant) | US FDA | **21 CFR Part 11** — https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11 | Variant-only |
| Food chain traceability | ISO | ISO 22005 | Referenced (variant); edition to confirm |
| HACCP principles | Codex Alimentarius | Codex **CXC 1-1969** (General Principles of Food Hygiene, incl. HACCP) | Referenced; edition to confirm |
| CN deployment baseline | SAC (China) | **GB/T 22239-2019** 网络安全等级保护基本要求 (MLPS 2.0) | Cited at **standard level only**; no article-level mapping in this pack |
| B2B documents: DESADV/ASN, ORDERS, IFTMIN — C-06/C-16 | UNECE | UN/EDIFACT — https://unece.org/trade/uncefact | Message versions to confirm |
| B2B documents (GS1 subset of UN/EDIFACT) | GS1 | **EANCOM** — https://ref.gs1.org/standards/eancom/ | Current version 2022 (per GS1 repository) |
| B2B documents: X12 856/850 | ANSI ASC X12 | ANSI X12 **856** (Ship Notice/Manifest), **850** (Purchase Order) | Sets/versions to confirm |
| Dangerous-goods storage segregation — BR-04 | UNECE / IATA / IMO | ADR / IATA DGR / IMDG Code | Pack encodes *attributes* only (hazard class); regulation text is not embedded |

> Anything below this line that is a **number or design rule** rather than a
> citation is in §4.

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Error payload `application/problem+json` — 06-contracts conventions | IETF | RFC 9457 (Problem Details for HTTP APIs) — https://www.rfc-editor.org/rfc/rfc9457 | |
| HTTP status semantics (`409` on reservation conflict, `429`, …) — C-23, F-05 | IETF | RFC 9110 (HTTP Semantics) — https://www.rfc-editor.org/rfc/rfc9110 | Codes are standard; their *use* here is a design choice |
| Timestamps `occurred_at` vs. `recorded_at`, ISO-8601 UTC | IETF | RFC 3339 — https://www.rfc-editor.org/rfc/rfc3339 | |
| OAuth 2.0 bearer auth for the operational API | IETF | RFC 6750 — https://www.rfc-editor.org/rfc/rfc6750 | |
| OIDC SSO for human/device authN | OpenID Foundation | OpenID Connect Core 1.0 — https://openid.net/connect/ | |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Warehouse execution & inventory (task-based WMS) | openWMS.org | https://openwms.org/ | Task/stock model reference |
| Warehouse & order/inventory management | Apache OFBiz | https://ofbiz.apache.org/ | Warehouse/order/stock components |
| Inventory / warehouse management | Odoo Inventory | https://www.odoo.com/ | Inventory module as reference |
| Inventory / supply-chain management | OpenBoxes | https://openboxes.com/ | Lot/expiry-centric reference |
| Append-only / event-driven stock & task stream (ADR-0002) | Apache Kafka | https://kafka.apache.org/ | Possible SSOT/outbox substrate; not mandated |
| Authorization / SSO (CTL-06, NFR-011) | Keycloak | https://www.keycloak.org/ | OIDC/SAML reference |
| Owner-scoped row-level security (BR-13, CTL-06) | PostgreSQL | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | RLS as the isolation mechanism |
| EDI / B2B document integration (ASN/orders) | Apache Camel | https://camel.apache.org/ | EDIFACT/X12 routing patterns |
| Metrics & alerting (NFR-013) | Prometheus | https://prometheus.io/ | Observability primitives |
| Dashboards (dock/throughput KPI) | Grafana | https://grafana.com/ | Reference tooling |

## 4. Declared assumptions (not traceable to a source)

Pack policy or engineering budgets — **not facts**. Each is marked
`> ⚠️ ASSUMPTION:` at its point of use and listed in README "Open questions".

- **Scale bands & all NFR numbers** — `p95 ≤ 800 ms` scan, `≤ 10k lines` in
  `p95 ≤ 30 s` allocation, `≥ 50k SKU` / `≥ 2M` stock lines / `≥ 500M` events,
  `≥ 60`/`≥ 120` tx/s, `≥ 99.9%` availability, `RPO ≤ 5 min` / `RTO ≤ 30 min`,
  `13 mo` hot window. Engineering budgets; no benchmark or reference hardware.
  (→ `02-requirements/non-functional.md` `(A)` markers)
- **BR-01 bucket decomposition** — `on_hand = available + reserved + hold +
  qc_pending + in_transit_intra`. Pack modeling choice; no standard defines
  these buckets. (→ `01-business/business-rules.md`)
- **BR-03 putaway ranking** — fixed-bin → nearest floating → empty-bin →
  overflow with travel-distance tie-break. Heuristic; no algorithmic source.
- **BR-05 reservation lifecycle** — soft at planning, hard at release, expiry/
  cancel release; TTLs and "one hard reservation per unit" are pack rules.
- **BR-06 lot direction** — FIFO default, FEFO for food/pharma, expiry-block
  window. Default and window are pack parameters; FEFO itself is required only
  by GDP/food rules (variant).
- **BR-07 / BR-10 / BR-11 tolerances** — max splits, `tol%` variance and
  delivery tolerance, absolute caps. Parameters with no default values sourced.
- **BR-09 / BR-15 / BR-16** — ABC cadence `nA/nB/nC`, `accuracy`,
  `pick_accuracy` formulas. Defined in-pack; not derived from a cited standard.
- **BR-12 shipping completeness gate** — element list (lots/serials, VAS,
  weight, label/manifest). Pack policy.
- **SM-1..SM-6 transitions** — e.g. `DiscrepancyHold → Received`,
  `ExpiredBlocked → Quarantined`, `WaitingEquipment → Released` on device
  reject. Pack design; not required by GS1/ISO. (→ `03-domain/state-machines.md`)
- **06-contracts field details** — API paths, `Idempotency-Key` composition
  `task+step+HU+ts-window`, owner-claim rules, `409` behavior. Pack-specific.
  (→ `06-contracts/api-overview.md`)
- **Per-failure RTO/RPO & DR targets** — F-01 `15 min`, F-13 region `4 h`,
  F-03 projection rebuild `≤ 30 min`, F-08 DLQ policy. Pack proposals.
  (→ `08-quality/failure-and-dr.md`)
- **05-data/data-flow `DF-1..DF-6`** — lineage steps and the projection-rebuild
  procedure. Pack design. (→ `05-data/data-flow.md`)
- **EPCIS exchange depth** — external EPCIS XML/JSON-LD production is an L3
  option, not yet specified; the pack uses EPCIS as a conceptual vocabulary.
- **GS1 label/printer conformance (NFR-014)** — "GS1 sizing/print resolution"
  names no specific label-spec clause; to confirm, or restate as a pack rule.
- **Customs / bonded warehousing (CN)** — referenced conceptually; no citation
  in core (variant concern).
- **ADR-0001..0004** — all four are pack architectural stances; no standard
  prescribes them.

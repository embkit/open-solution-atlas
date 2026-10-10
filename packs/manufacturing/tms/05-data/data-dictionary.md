# 05 · Data Dictionary

> Core fields only; full attribute specs remain implementation material.
> Fields whose values come from cited external vocabularies are marked
> **std** with their source.

| Field | Entity(ies) | Type / domain | Source & notes |
|---|---|---|---|
| `demand_source.source_id` | demand_source | string | ERP order no. / WMS task no.; traceability spine (FR-020) |
| `incoterms_rule` | demand_source | 3-letter code (EXW…DDP, 11 rules) | **std** — ICC Incoterms® 2020 (CTL-08); consumed verbatim (BR-12) |
| `leg.state` | leg | enum | Pack state notes below (L3 = formal state machines) |
| `tender.outcome` | tender | ACCEPTED / REJECTED / TIMEOUT | Pack design (FR-009) |
| `rate_snapshot.components` | rate_snapshot | structured | linehaul, fuel basis, accessorials; immutable (BR-04) |
| `milestone_event.business_step` | milestone_event | URI/code | **std** — GS1 CBV 2.0 business steps (FR-021) |
| `milestone_event.disposition` | milestone_event | URI/code | **std** — GS1 CBV 2.0 dispositions (FR-021) |
| `milestone_event.source_ts` / `ingestion_ts` | milestone_event | timestamp (NTP-synced) | dual-timestamp rule (BR-11, NFR-011) |
| `pod.ref` | pod | string/URI | signature data or e-POD document reference (BR-06) |
| `dg_declaration.un_number` | dg_declaration | 4-digit code | **std** — UN Model Regulations family via ADR/JT/T 617/IMDG/IATA DGR tables |
| `dg_declaration.psn` | dg_declaration | string | **std** — proper shipping name (ADR 1.2 / JT/T 617.3 / IMDG 2.0 / IATA DGR 4.2) |
| `dg_declaration.class_division` | dg_declaration | class 1–9 + division | **std** — GB 6944-2025 / UN classification |
| `dg_declaration.packing_group` | dg_declaration | I / II / III / none | **std** — UN classification vocabulary |
| `regulation_edition.regime` | regulation_edition | adr / imdg / iata_dgr / jt617 / gb6944 | Edition pinning (ADR-0003, NFR-010) |
| `match_result.status` | match_result | AUTO_APPROVED / DISPUTED | Tolerance verdict (BR-05); append-only |
| `epcis_outbox.*` | epcis_outbox | EPCIS 2.0 JSON/JSON-LD | **std** — EPCIS 2.0 capture interface |

## State notes (formal state machines in [`../03-domain/state-machines.md`](../03-domain/state-machines.md))

- **Leg (plan side)**: SM-T1 — `Planned → Tendered → Accepted → Dispatched`
  with plan revisions appending, not rewriting (ADR-0005).
- **Leg (actual side)**: SM-T1 milestone stream; `Delivered` requires POD
  (BR-06).
- **Invoice**: SM-T3 — `Received → AutoApproved|Disputed → Settled`.
  No payment path without AUTO_APPROVED (FR-015).

# 00 · Regulatory Landscape

> Editions verified 2026-10-08. Full traceability in
> [`../SOURCES.md`](../SOURCES.md).

## Core (always applicable)

| Area | Instrument | Edition / status | Relevance to TMS |
|---|---|---|---|
| Transport event vocabulary | **GS1 EPCIS 2.0 / CBV 2.0** | Ratified 2022-06 | Milestone/disposition vocabulary for track-and-trace event sharing; JSON/JSON-LD + REST capture/query since 2.0 |
| Supply-chain security | **ISO 28000:2022** (Ed. 2) | Published 2022-03 | Security management system for supply chains; framing for CTL-03 |
| Trade terms | **Incoterms® 2020** (ICC) | In force 2020-01-01; 11 rules | Allocates cost/risk/obligations between seller & buyer; determines *who contracts carriage* — TMS consumes, never re-defines, the term |
| Freight message interchange | **UN/EDIFACT** IFTMIN/IFTMBF (instruction), IFTSTA/IFCSUM (status) | Message designations fixed; versions per agreement pair | Legacy/broker EDI channels for order & status exchange |
| North-American status messages | **ANSI ASC X12** 214 (shipment status), 990 (response) | Transaction sets; version per trading partner | Carrier status EDI in US trade |

## Dangerous goods (variant-relevant; validation data, not legal text)

| Mode | Instrument | Edition verified | Notes |
|---|---|---|---|
| Road (intl., UNECE) | **ADR 2025** | Amendments applicable from 2025-01-01 (UN doc. ECE/TRANS/352) | Biennial cycle: next ADR 2027 |
| Road (CN) | **JT/T 617-2018** (7 parts) + **GB 6944-2025** | JT/T 617 parts 1–7 published 2018-08-29; GB 6944-2025 effective 2025-10-01 (replaces 2012) | CN classification/consignment/loading/vehicle rules |
| Sea | **IMDG Code 2024 Edition** (incl. Amendment 42-24) | Mandatory from 2026-01-01 (adopted MSC.556(108), 2024-05) | Voluntary application allowed from 2025-01-01 |
| Air | **IATA DGR 67th edition (2026)** | In force 2026-01-01 | Annual editions; 68th ed. 2027 already published |

> The pack encodes **compliance metadata validation** against these tables
> (UN number, proper shipping name, class/division, packing group, quantity
> limits, segregation). It never reproduces regulation text as if it were
> system logic — see ADR-0003.

## Data protection & baseline security

| Area | Instrument | Notes |
|---|---|---|
| CN baseline | **GB/T 22239-2019** 等保2.0 | Cited at standard level; article-level mapping deferred (§4 assumption) |
| EU personal data | **GDPR** (EU 2016/679) | Driver/personal location data is personal data — retention & minimization apply |

## Explicitly out of pack scope

- Customs / global trade compliance (HS classification, duty calculation,
  brokerage) — candidate sibling pack.
- Immobilisation/tachograph & driver-hours legal tachograph rules — consumed
  as vehicle/driver qualification *attributes*, not enforced here.

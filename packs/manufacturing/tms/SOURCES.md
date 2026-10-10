# SOURCES — Transportation Management System

> Provenance ledger. Maps the pack's load-bearing claims to public, checkable
> sources; anything that could not be traced is listed in §4 and marked
> `> ⚠️ ASSUMPTION:` in the chapters.
>
> **Status: `source-checked`** (2026-10-09). Provenance: `llm-drafted`.
> Verification: `source-checked` — **not** field-verified. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).
>
> Checked against sources on 2026-10-09. Outcomes: (a) dangerous-goods
> editions pinned to what is actually in force (ADR 2025, IMDG 2024/A42-24
> mandatory 2026-01-01, IATA DGR 67th ed. 2026, JT/T 617-2018 + GB 6944-2025);
> (b) EPCIS pinned to 2.0/CBV 2.0 (ratified 2022-06; note the ISO/IEC
> 19987/19988 PAS adoptions of EPCIS/CBV 1.2 are **withdrawn**); (c) ISO
> 28000 pinned to the 2022 second edition; (d) Incoterms pinned to the 2020
> edition (11 rules). All numeric targets remain declared assumptions (§4).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Transport event vocabulary (milestones, dispositions) — FR-011, FR-021, CTL-04 | GS1 | **EPCIS 2.0 / CBV 2.0**, ratified 2022-06 — https://ref.gs1.org/standards/epcis/ and https://ref.gs1.org/standards/cbv/ ; implementation guideline 2.0 (2023-03) | 2.0 adds JSON/JSON-LD, REST capture/query, GS1 Digital Link. ISO/IEC 19987/19988:2017 (EPCIS/CBV 1.2 PAS) are **withdrawn** — cite the GS1 2.0 specs, not the ISO PAS |
| Supply-chain security framing — CTL-03 | ISO | **ISO 28000:2022** (Ed. 2, 2022-03), *Security and resilience — Security management systems — Requirements* — https://www.iso.org/standard/79612.html | Replaces ISO 28000:2007; Amd 1:2024 (climate) exists. Clause-level mapping is §4 |
| Trade terms consumed on orders — BR-12, CTL-08, FR-001 | ICC | **Incoterms® 2020**, 11 rules, in force 2020-01-01 — https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/ | DPU renamed from DAT in 2020; FCA A6/B6 on-board B/L provision; costs consolidated at A9/B9. The pack consumes the term; it does not interpret it |
| DG road (international) — BR-07, CTL-01/02 | UNECE | **ADR 2025** (amendments applicable from 2025-01-01), UN doc. ECE/TRANS/352 — https://unece.org/transport/dangerous-goods ; biennial cycle | Validation data only (ADR-0003). Next edition ADR 2027 |
| DG road (CN) — CTL-01 | MOT China | **JT/T 617-2018** 《危险货物道路运输规则》parts 1–7 (2018-08-29发布, 2018-12-01实施); **GB 6944-2025** 危险货物分类和品名编号 (发布 2025-03-28, 实施 2025-10-01, replaces GB 6944-2012) — https://openstd.samr.gov.cn/ | JT/T 617.3 XG1—2024 修改单 exists for part 3 |
| DG sea — CTL-01 | IMO | **IMDG Code 2024 Edition** (incl. Amendment 42-24, adopted MSC.556(108) 2024-05), **mandatory from 2026-01-01**, voluntary from 2025-01-01 — https://www.imo.org/en/publications/pages/imdg%20code.aspx | Amendment cycle 2025–2034 published |
| DG air — CTL-01 | IATA | **IATA DGR 67th edition (2026)**, in force 2026-01-01 — https://www.iata.org/en/programs/cargo/dgr/ | Annual editions; 68th ed. (2027) already published. Incorporates ICAO TI 2025–2026 |
| DG classification vocabulary (class/division, packing group, UN no., PSN) — FR-017, glossary | UN | UN *Recommendations on the Transport of Dangerous Goods — Model Regulations* (ST/SG/AC.10/3/Rev.23 per ADR 2025 definitions); GHS Rev. 10 per same definitions | Cited as the shared classification backbone of ADR/JT/T 617/IMDG/IATA |
| Freight B2B messages — FR-022, integration | UNECE | **UN/EDIFACT** trade facilitation messages: IFTMIN/IFTMBF (instruction), IFTSTA/IFCSUM (status) — https://unece.org/trade/uncefact | Message designations are stable; versions are per trading-partner agreement (§4) |
| NA carrier status messages — FR-022 | ANSI ASC X12 | **X12 214** (transportation status), **X12 990** (response to 214) — https://www.x12.org/ | Transaction-set designations; version/implementation guides per partner (§4) |
| Personal data in location tracking — CTL-06 | EU | **GDPR** (EU 2016/679) — https://gdpr-info.eu/ | Principles cited; article-level mapping §4 |
| CN deployment baseline — CTL-07 | SAC (China) | **GB/T 22239-2019** 信息安全技术 网络安全等级保护基本要求 (等保2.0) | Standard level only; no article mapping |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Clock synchronization — BR-11, NFR-011 | IETF | RFC 5905 (NTPv4) — https://www.rfc-editor.org/rfc/rfc5905 | The `skew ≤ 1 s` bound is pack policy (§4) |
| EPCIS bindings | GS1 | EPCIS 2.0 artefacts (XML, JSON-LD, CBV ontology) — https://ref.gs1.org/standards/epcis/artefacts | 2.0 canonical namespace: `https://ref.gs1.org/epcis/` |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| VRP / stop-sequencing solver (ADR-0002) | VROOM | https://vroom-project.org/ | One viable solver behind the contract; not mandated |
| Road routing engine | OSRM | https://project-osrm.org/ | Distance/time matrix source for routing |
| Routing & optimization | GraphHopper | https://www.graphhopper.com/ | Alternative engine; supports JSprit-based optimization |
| Routing API | openrouteservice | https://openrouteservice.org/ | Hosted/self-hosted alternative |
| Event streaming for the milestone spine | Apache Kafka | https://kafka.apache.org/ | Append-only substrate option (ADR-0005) |
| EDI / message routing patterns | Apache Camel | https://camel.apache.org/ | EDIFACT/X12 component patterns |
| Identity / SSO | Keycloak | https://www.keycloak.org/ | OIDC/SAML reference (cross-pack: iam-platform) |
| Policy-as-code authorization | Open Policy Agent | https://www.openpolicyagent.org/ | Optional PDP for segregation checks |
| Geocoding / map data | OpenStreetMap | https://www.openstreetmap.org/ | Reference geodata for stop coordinates |

## 4. Declared assumptions (not traceable to a source)

Pack policy or engineering budgets — **not facts**. Each is marked
`> ⚠️ ASSUMPTION:` at its point of use and listed in README "Open questions".

- **All NFR numbers** — visibility `≤ 60 s p95`, ETA `≤ 30 s p95`, tender
  `≤ 60 s p95`, match `≤ 3 s p95` / batch `≤ 1 h`, scale bands (`50k`
  shipments/day, `2M` events/day, `1k` carrier connections), retention
  `≥ 5 years`, availability `≥ 99.9 %`, skew `≤ 1 s`, observability
  thresholds. Engineering budgets; no benchmark.
- **BR-03 auto-accept** for own fleet is a configuration default, not a rule
  from any source.
- **BR-05 tolerance** (`≤ 3 % or ≤ ¥50`) — pack policy; real tolerances are
  contract-derived.
- **BR-09 capacity headroom** (`≥ 5 %`) — pack policy; legal payloads vary
  by jurisdiction/vehicle class.
- **Rate model depth** — "reference rate cards + frozen snapshot" (ADR-0004)
  is a scope decision; fuel-basis recalculation formulas are contract data,
  not pack logic.
- **Solver contract** (ADR-0002) — the problem/solution interface shape is
  pack design; no solver standard exists to trace it to.
- **State decompositions** (SM-T1..SM-T5: leg plan/actual sides, tender,
  invoice lifecycle, exception, edition) — pack design; no standard
  specifies TMS lifecycle states.
- **Bounded contexts & logical data model** — pack design; EPCIS supplies
  event vocabulary, not architecture.
- **Process flows P-01..P-06** — pack design, generalized from the scope
  stated in the brief; not normative text of any source.
- **ISO 28000 / GDPR / 等保2.0 clause-level mappings** — named at standard
  level; the specific control articles are §4 open items.
- **X12/EDIFACT version pinning** — message designations (214/990/IFTMIN/
  IFTSTA) are fixed; the version/implementation-guide pair per partner is a
  deployment input.
- **All five ADRs** — pack architectural stances. ADR-0001 is *consistent
  with* common WMS/TMS/ERP practice, ADR-0003 deliberately avoids asserting
  legal compliance (the regulations govern, the pack validates data) — none
  is mandated by a cited standard.

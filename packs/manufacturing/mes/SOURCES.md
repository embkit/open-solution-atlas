# SOURCES — Manufacturing Execution System

> Provenance ledger. Maps the pack's load-bearing claims to public, checkable
> sources; anything that could not be traced is listed in §4 and marked
> `> ⚠️ ASSUMPTION:` in the chapters.
>
> **Status: `source-checked`** (2026-10-08). Provenance: `llm-drafted`.
> Verification: `source-checked` — **not** field-verified. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).
>
> Checked against sources on 2026-10-08. Outcomes: (a) ISA-95/IEC 62264 part
> titles pinned; (b) **BR-09 (OEE) now has a real standard source — ISO
> 22400-2:2014** — where the starter ledger had recorded "no source"; (c)
> confirmed that **IEC 62264-3 explicitly does not specify genealogy**, so the
> pack's genealogy model is an extension beyond the standard, not a derivation.

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Level-3 boundary, equipment/operations hierarchy, object models (personnel/equipment/material/process) — ADR-0001, CTL-03 | ISA / IEC | ANSI/ISA-95 = **IEC 62264** — Part 1 *Models and Terminology*; Part 2 *Objects and Attributes*; Part 3 *Activity Models of Manufacturing Operations Management*; Part 4 *Objects and Attributes for MOM Integration* — https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard | Part titles confirmed; IEC 62264-2 has a 3rd edition (2026). The ISA series documents further parts beyond 1–4 |
| MOM activity decomposition underlying the pack's bounded contexts & BP-01..BP-06 — capability-map, processes | ISO/IEC | **IEC 62264-3:2016** — production / maintenance / quality / inventory operations management, each with definition management, resource management, detailed scheduling, dispatching, execution management, data collection, tracking, performance analysis — https://www.iso.org/obp/ui/#!iso:std:62264:-3:en | The pack's activity set maps onto this structure |
| **Genealogy** as a first-class capability — BR-06, CTL-01, FR-02/FR-15 | — | **Not specified by IEC 62264-3** (Annex C, "Why is genealogy not discussed?") | Honest gap: genealogy is a **pack extension**, not a standard derivation. ISO 9001 8.5.2 supplies the *obligation*, not the model |
| **OEE formula** — BR-09 (`OEE = Availability × Performance × Quality`) | ISO | **ISO 22400-2:2014**, *KPIs for manufacturing operations management — Part 2: Definitions and descriptions*: "OEE index = Availability × Effectiveness × Quality ratio", unit %, range 0–100% — https://www.iso.org/standard/53936.html | Closes the starter ledger's open item. Part 1 = Overview/concepts/terminology. 22400-2 is under revision (DIS 2nd ed.) |
| KPI elements aligned to IEC 62264 **work units** — BR-09, FR-018 | ISO | ISO 22400-2:2014 (work-unit scope) | |
| Six Big Losses / TPM origin of OEE | literature | Nakajima, S., *Introduction to TPM: Total Productive Maintenance* (Productivity Press, 1988) | Historical origin; **not** the normative definition (ISO 22400-2 is) |
| Product identification & traceability (obligation) — BR-06, CTL-01 | ISO | ISO 9001:2015 cl. **8.5.2** — https://www.iso.org/standard/70089.html | Clause number confirmed (also used in the `wms` pack) |
| ERP↔MES/control integration vocabulary ("B2MML-compatible") — NFR-008, ADR-0001 | MESA International | **B2MML** (Business To Manufacturing Markup Language), the XML realization of ISA-95 — https://www.mesa.org/ | B2MML-Common **Version 0600** is the revision cited by the OPC UA for ISA-95 companion spec; current MESA release to confirm |
| Equipment information model & companion specs — NFR-008, ADR-0003 | OPC Foundation / IEC | **IEC 62541** (OPC UA) series — Part 3 Address Space Model, Part 4 Services, Part 5 Information Model, … — https://opcfoundation.org/ ; **OPC UA for ISA-95** companion spec — https://reference.opcfoundation.org/ISA-95/ | Companion specs are per-domain; the pack says "where they exist" |
| OT/IT zoning, zones & conduits, least privilege — CTL-03, NFR-012 | IEC | **IEC 62443-3-2:2020** (zones & conduits), **62443-3-3:2013** (system security requirements), **62443-4-2:2019** (component requirements) | Same pinning as the `wms` pack |
| Electronic records / e-signatures (regulated variant) — CTL-02/04/05, BR-11 | US FDA | **21 CFR Part 11** — https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11 | Variant-only; clause-level control mapping is §4 |
| Computerised-system validation, data integrity (regulated variant) — CTL-02, BR-11 | European Commission | EU GMP **Annex 11** (EudraLex Vol. 4) — https://health.ec.europa.eu/medicinal-products/eudralex_en | Variant-only |
| ALCOA+ data-integrity framing — CTL-02 | MHRA | MHRA *'GXP' Data Integrity Guidance and Definitions* (2018) | Public regulator guidance; **exact URL to confirm** |
| CN deployment baseline — CTL-06 | SAC (China) | **GB/T 22239-2019** 信息安全技术 网络安全等级保护基本要求 (等保2.0) | Cited at **standard level only**; no article-level mapping |
| Device-history-record variant trigger (medical devices) | ISO | ISO 13485 (QMS) | Referenced only; clause mapping to confirm |
| PPAP / error-proofing variant trigger (automotive) | IATF | IATF 16949 | Referenced only; edition & clause to confirm |
| Shop-floor clock synchronization — BR-10, NFR-006 | IETF | RFC 5905 (NTPv4) — https://www.rfc-editor.org/rfc/rfc5905 | The RFC defines the protocol; the pack's `skew ≤ 1 s` bound is a design choice (§4) |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| NTP clock discipline — BR-10, NFR-006 | IETF | RFC 5905 — https://www.rfc-editor.org/rfc/rfc5905 | Numeric skew budget is a pack parameter |
| ISA-95 / IEC 62264 (see §1) | ISO/IEC | IEC 62264 series | CN national adoption as GB/T 18975 to confirm |
| OPC UA (see §1) | IEC | IEC 62541 series (Part 4 *Services* has a 4th ed., 2025) | Per-equipment companion spec list to confirm |
| Industrial MQTT namespace for OT telemetry | Eclipse Foundation | Eclipse **Sparkplug B** specification — https://sparkplug.eclipse.org/ | Cited as an option for the telemetry path, not mandated |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| MES / Industry 4.0 integration model, OPC UA + AAS | Eclipse BaSyx | https://www.eclipse.org/basyx/ | Reference for the adapter/gateway boundary (ADR-0003) |
| Industrial protocol integration (S7, Modbus, OPC UA…) | Apache PLC4X | https://plc4x.apache.org/ | Read-mostly adapter reference |
| OPC UA stack (C) | open62541 | https://open62541.org/ | Equipment-adapter building block |
| Equipment/event integration flow | Node-RED | https://nodered.org/ | Illustrative; not a control system |
| MQTT / Sparkplug B for OT telemetry | Eclipse Sparkplug | https://sparkplug.eclipse.org/ | Industrial MQTT namespace |
| MQTT broker | Eclipse Mosquitto | https://mosquitto.org/ | Transport for OT telemetry |
| Append-only event store / streaming (ADR-0002) | Apache Kafka | https://kafka.apache.org/ | One viable SSOT substrate; not mandated |
| Time-series store for equipment/OEE signals | InfluxDB | https://www.influxdata.com/ | Alternative storage for FR-017/018 signals |
| Metrics & alerting (NFR-013) | Prometheus | https://prometheus.io/ | Observability primitives |
| Dashboards / line boards visuals | Grafana | https://grafana.com/ | Reference tooling |
| Identity, RBAC, SSO (FR-008, CTL-04) | Keycloak | https://www.keycloak.org/ | OIDC/SAML reference |
| Policy-as-code authorization (RBAC/ABAC) | Open Policy Agent | https://www.openpolicyagent.org/ | Comparative to XACML-style PDP |
| Integration / EDI & adapter routing | Apache Camel | https://camel.apache.org/ | ERP/WMS/LIMS integration patterns |

## 4. Declared assumptions (not traceable to a source)

Pack policy or engineering budgets — **not facts**. Each is marked
`> ⚠️ ASSUMPTION:` at its point of use and listed in README "Open questions".

- **Scale bands & all NFR numbers** — line board `≤ 2 s p95`, station ack
  `≤ 500 ms p95`, terminal buffer `≥ 4 h`, `≤ 50 lines` / `≤ 2,000` terminals /
  `≥ 5,000 events/s`, genealogy dossier `10,000` events `≤ 5 s p95`, retention
  `≥ 5 years` / `product lifetime + 2 years`, availability `≥ 99.9 %`,
  usability `≤ 3 taps` / `≥ 10-inch`. Engineering budgets; no benchmark.
  (→ `02-requirements/non-functional.md` `(A)` markers)
- **BR-08 uncoded-downtime auto-coding** — auto-code to `UNCODED` before shift
  close and escalate. Pack policy; no external basis for the timing.
- **BR-10 dual timestamps & `skew ≤ 1 s`** — the RFC defines NTP; the numeric
  bound and the dual source/ingestion timestamp rule are pack choices.
- **Observability thresholds** — "buffer > 0 on > 5 % of stations", replication
  lag > 30 s, shift-close completeness ≥ 99 %, gap/reject-spike alerts.
- **SM-01/SM-02/SM-04 transitions & guards** — e.g. "ERP changes affect only
  CREATED orders", "QUARANTINED blocks transitions", "COMPLETED requires
  quantity reconciliation". Pack design.
- **Domain model & bounded contexts** — pack design; IEC 62264-3 supplies the
  MOM activity vocabulary but not this decomposition, and not genealogy.
- **BP-01..BP-06 process flows** — pack design (a generalized level-3 activity
  decomposition), not normative text.
- **Logical data model** — entities, keys and cardinalities are pack design;
  only the borrowed ISA-95 object vocabulary is normative.
- **CTL-02/04/05 ↔ 21 CFR Part 11 & Annex 11** — control descriptions are
  broad; the clause-level mapping is asserted, not cited.
- **CTL-06 ↔ 等保2.0** — "control mapping for the MES zone" and 数据安全法
  classification scoping are named but not clause-mapped.
- **FR-014 (SPC baseline)** — "control-chart statistics per the configured
  rules" names no rule set (e.g. Western Electric / Nelson rules); to confirm.
- **B2MML version & OPC UA companion-spec list** — "B2MML-compatible" and
  "OPC UA companion specs where they exist" are stated without pinning the
  B2MML release or the per-equipment companion-spec list.
- **ADR-0001..0004** — all four are pack architectural stances. ADR-0001
  (level-3 boundary) is *consistent with* IEC 62264-1/3, and ADR-0004 (APS
  external) is consistent with IEC 62264-3 Annex D discussing APS as adjacent
  — but neither is mandated by the standard.

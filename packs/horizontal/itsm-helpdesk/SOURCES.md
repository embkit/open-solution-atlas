# SOURCES — IT Service Desk & ITSM Platform

> Provenance ledger. Maps the pack's load-bearing claims to public,
> checkable sources; anything that could not be traced is listed in §4 and
> marked `> ⚠️ ASSUMPTION:` in the chapters.
>
> **Status: `source-checked`** (2026-10-09). Provenance: `llm-drafted`.
> Verification: `source-checked` — **not** field-verified. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).
>
> Checked against sources on 2026-10-09. Outcomes: (a) ISO/IEC 20000-1:2018
> clause numbers pinned from the published table of contents —
> **8.6.1 incident / 8.6.2 service request / 8.6.3 problem** (within 8.6
> *Resolution and fulfilment*), 8.3 relationship & agreement (SLA), 8.5
> design/build/transition, 8.7 service assurance; (b) ISO/IEC 27001:2022
> Annex A controls pinned (A.5.15/A.5.18 access, A.5.24 security-incident
> management, A.8.13 backup, A.8.15 logging, A.8.16 monitoring, A.8.32
> change management); (c) ITIL 4 kept as **licensed vocabulary** — cited by
> name, never paraphrased as fact. All numeric targets remain declared
> assumptions (§4).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Incident / service request / problem processes — FR-004..FR-012, CTL-01 | ISO/IEC | **ISO/IEC 20000-1:2018** (Ed. 3): cl. **8.6.1** incident management, **8.6.2** service request management, **8.6.3** problem management (within cl. 8.6 *Resolution and fulfilment*) — https://www.iso.org/standard/70636.html | Clause numbers from the published TOC (ISO OBP); the pack implements *outcomes*, its states/flows are pack design (§4) |
| SLA / service agreement obligations — BR-04, CTL-02, FR-001 | ISO/IEC | ISO/IEC 20000-1:2018 cl. **8.3** (relationship and agreement); 20000-2:2019 guidance | Obligation to agree & review targets; clock/pause mechanics are pack design (§4) |
| Change in transition — FR-013/FR-014, CTL-04 | ISO/IEC | ISO/IEC 20000-1:2018 cl. **8.5** (service design, build and transition) + **ISO/IEC 27001:2022 A.8.32** change management | Risk classes/CAB shapes are pack design aligned to these obligations (§4) |
| Service assurance / reporting — FR-019, BR-06 | ISO/IEC | ISO/IEC 20000-1:2018 cl. **8.7** (service assurance) | |
| Access control for agent/requester roles — BR-11, CTL-03 | ISO/IEC | **ISO/IEC 27001:2022 Annex A.5.15** (access control), **A.5.18** (access rights) | Scope-granularity interpretation `(A)` (§4) |
| Security-classified incidents on the shared backbone — CTL-06 | ISO/IEC | **ISO/IEC 27001:2022 A.5.24** (security incident management planning & preparation), A.5.25–A.5.28 family | Ticket core is IT-incident-shaped; security classification is the overlay |
| Monitoring → intake, intake health — FR-004, CTL-05 | ISO/IEC | **ISO/IEC 27001:2022 A.8.16** (monitoring activities) | |
| Audit/logging of tickets & automation — BR-07, BR-14, CTL-07 | ISO/IEC | **ISO/IEC 27001:2022 A.8.15** (logging), A.8.16 | |
| Backup of ticket records — NFR-006 | ISO/IEC | **ISO/IEC 27001:2022 A.8.13** (information backup) | |
| Incident-handling guidance (security subset) — CTL-06 | NIST | SP 800-61r2, *Computer Security Incident Handling Guide* — https://csrc.nist.gov/pubs/sp/800/61/r2/final | Guidance, not binding; r3 revision in progress as of check date |
| Practice vocabulary (incident/problem/change/continual improvement) | AXELOS/PeopleCert | **ITIL 4** — https://www.axelos.com/best-practice-solutions/itil | **Licensed framework**: practice *names* cited as vocabulary; definitions are not reproduced as pack facts (§4) |
| Email intake parsing — FR-018, BR-13 | IETF | **RFC 5322** (Internet Message Format), incl. Message-ID as thread key — https://www.rfc-editor.org/rfc/rfc5322 | |
| Channel/webhook payload authenticity — FR-018, NFR-008 | IETF | **RFC 7515** (JWS) — https://www.rfc-editor.org/rfc/rfc7515 | Signed outbound webhooks (I-08); inbound schemes are pack design (§4) |
| HTTP semantics for portal/API — NFR-001, NFR-011 | IETF | **RFC 9110** (HTTP Semantics) — https://www.rfc-editor.org/rfc/rfc9110 | Status-code usage is pack convention (§4) |
| Accessibility of the requester portal — NFR-009 | W3C | WCAG 2.1 (AA) — https://www.w3.org/TR/WCAG21/ | Same cited posture as the `personal-blog` pack |
| Requester PII retention/erasure — NFR-006, CTL-08 | EU / CN | GDPR (EU 2016/679) Arts. 5(1)(e), 17 — https://gdpr-info.eu/ ; 《个人信息保护法》(PIPL) art. 47 (删除权) | Article mapping interpretation `(A)` (§4) |
| CN deployment baseline — CTL-09 | SAC (China) | GB/T 22239-2019 等保2.0 | Standard level only; no article mapping |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| SSO for agents/requesters — NFR-008, integration I-04 | OpenID Foundation | OIDC Core 1.0 (cross-pack reference: `iam-platform`) | The pack authenticates; it never stores passwords |
| Time handling for clocks — NFR-002, FR-006 | IETF | RFC 5905 (NTPv4) for synchronization | Clock *math* is the pack fold; sync discipline is the RFC |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Helpdesk / ticketing | osTicket | https://osticket.com/ | Reference for intake/backbone shape |
| Helpdesk / ITSM | Zammad | https://zammad.com/ | Omnichannel intake reference |
| ITSM / asset & CMDB | GLPI | https://glpi-project.org/ | CMDB + inventory reference |
| Ticketing (OTRS fork) | Znuny | https://znuny.org/ | |
| ITSM (service management) | iTop (Combodo) | https://www.combodo.com/itop | Problem/change linkage reference |
| CI inventory pattern | NetBox | https://github.com/netbox-community/netbox | Registry-first CI data model inspiration |
| Alert → ticket source | Prometheus / Alertmanager | https://prometheus.io/ | I-03 reference; not a decision source |
| Open service-management process patterns | ITIL-aligned open literature / IT4IT | — | Consulted for shape only; obligations traced to §1 |

## 4. Declared assumptions (not traceable to a source)

Pack policy or engineering budgets — **not facts**. Each is marked
`> ⚠️ ASSUMPTION:` at its point of use and listed in README "Open questions".

- **All NFR numbers** — intake latencies, `99.9 %`, scale bands
  (`300 tickets/day`, `50k/year`), reporting latencies, retention
  (`≥ 3 years`), rule/clock evaluator lags, usability `≤ 3 interactions`.
- **BR-03a priority matrix** — `impact × urgency → P1..P4` values and P1
  response `≤ 15 min`; no standard publishes these numbers.
- **BR-04 pause semantics, BR-05 calendars** — ISO/IEC 20000-1 requires
  agreed SLA management, not these clock mechanics.
- **BR-08 recurrence threshold** (`3 in 30 days`) and **BR-09 emergency
  post-review window** (`≤ 5 business days`) — pack policy.
- **BR-13 channel identity rules** (header rules, allow-lists) and inbound
  webhook auth scheme — pack design; only outbound JWS is spec-pinned.
- **BR-15 auto-close silence window** (`≤ 7 days`), CSAT timing — pack
  policy.
- **SoD notes in security.md** (approver ≠ implementer) — pack
  interpretation of A.8.32/20000-1 obligations, not quoted requirements.
- **P-01..P-06 flows, SM state drafts, bounded contexts, data model** —
  pack design; the cited clauses specify outcomes, not these decompositions.
- **ITIL mapping depth** — practice names are cited vocabulary (licensed);
  no ITIL text is reproduced or claimed as a source for pack behavior.
- **CMDB discovery feed formats** (I-05/I-06) — feed schemas are
  deployment inputs.

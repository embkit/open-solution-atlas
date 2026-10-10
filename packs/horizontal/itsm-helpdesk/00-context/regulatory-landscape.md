# 00 · Regulatory Landscape

> Editions verified 2026-10-09. Full traceability in
> [`../SOURCES.md`](../SOURCES.md).

## Core (always applicable)

| Area | Instrument | Edition / status | Relevance to this pack |
|---|---|---|---|
| Service management system | **ISO/IEC 20000-1:2018** | Ed. 3, published 2018 | Clause **8.6.1 incident management**, **8.6.2 service request management**, **8.6.3 problem management** (within 8.6 *Resolution and fulfilment*); 8.3 relationship & agreement (SLA); 8.5 change in design/build/transition; 8.7 service assurance — the citable backbone this pack traces against |
| Service management guidance | **ISO/IEC 20000-2:2019** | Published 2019 | Guidance on the 20000-1 requirements; not itself certifiable |
| Information-security controls | **ISO/IEC 27001:2022** Annex A | 93 controls, 2022 | **A.5.24** security-incident management planning & preparation, **A.8.16** monitoring (alert→ticket intake), **A.8.32** change management, **A.8.13** backup (ticket data), **A.5.15/A.5.18** access control for agent roles |
| Incident-handling guidance | **NIST SP 800-61r2** (Computer Security Incident Handling Guide) | 2012; revision (r3) in progress | Optional alignment for security-classified incidents; the pack's ticket core is IT-incident-shaped, security incidents are a classification |

## Practice vocabulary (licensed — cited, not reproduced)

| Area | Instrument | Note |
|---|---|---|
| Practice names (incident/problem/change/continual improvement) | **ITIL 4** (AXELOS/PeopleCert) | Licensed framework. The pack uses practice *names* as vocabulary and does **not** paraphrase ITIL text as fact; obligations trace to ISO/IEC 20000-1 above |

## Regional / sector overlays

| Area | Instrument | Region | Note |
|---|---|---|---|
| 等保2.0 | GB/T 22239-2019 | CN | Standard level only; article-level mapping is an open assumption |
| Records/data protection | GDPR (EU 2016/679); PIPL (CN) | EU/CN | Requester PII in tickets (names, mailbox, IP in alert context) — retention & minimization apply |

## Explicitly out of pack scope

- Certification audit execution (the pack provides evidence-ready structure,
  not an audit service)
- Software-asset/license compliance and financial asset accounting
  (variant candidate)

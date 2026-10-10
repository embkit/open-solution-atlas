# 02 · Compliance Controls

> Controls traced to sources in [`../SOURCES.md`](../SOURCES.md). Clause
> numbers verified 2026-10-09; mappings still marked `(A)` where the
> pack asserts interpretation rather than quoting a requirement.

| ID | Control | Traced to |
|---|---|---|
| CTL-01 | Incident/service-request/problem outcomes implemented as separate, evidenced processes (records, roles, closure criteria) | **ISO/IEC 20000-1:2018 cl. 8.6.1 / 8.6.2 / 8.6.3** |
| CTL-02 | Service agreements & SLA definitions per service (parties, targets, review) with change-controlled calendars | **ISO/IEC 20000-1:2018 cl. 8.3** (relationship and agreement) |
| CTL-03 | Entitlement-scoped visibility (requester/agent/role/catalog scope) + least-privilege agent roles; security-classified tickets restricted | **ISO/IEC 27001:2022 A.5.15, A.5.18**; pack interpretation of scope granularity `(A)` |
| CTL-04 | Change management: RFC with risk class, assessment/approval evidence, backout, post-implementation review | **ISO/IEC 27001:2022 A.8.32**; **ISO/IEC 20000-1:2018 cl. 8.5** |
| CTL-05 | Monitoring → ticket intake with health monitoring of the intake path itself | **ISO/IEC 27001:2022 A.8.16** |
| CTL-06 | Security-incident classification on the shared backbone: plan/prepare, triage, restricted visibility, evidence preservation | **ISO/IEC 27001:2022 A.5.24** (+ A.5.25–A.5.28 family); NIST SP 800-61r2 as guidance |
| CTL-07 | Append-only, tamper-evident ticket & automation audit (who/what/when, rule version) | **ISO/IEC 27001:2022 A.8.15** (logging) & A.8.16; BR-07, BR-14 |
| CTL-08 | Requester PII minimization & retention in tickets; deletion request → payload removed, audit facts preserved | **GDPR (EU 2016/679)** Arts. 5(1)(e), 17; **PIPL** arts. 47 (删除权) — article-level mapping `(A)` |
| CTL-09 | CN deployment baseline for the ITSM zone | **GB/T 22239-2019** (等保2.0) — standard level only, no article mapping |

## Variant-deferred (declared, not core)

- Certification-audit automation (20000/27001 evidence packs)
- Regulated-sector overlays (GxP ticket handling, financial SOX change
  evidence) → variant packs
- Security-orchestration (SOAR playbooks) → integration, not core

# SOURCES — One-Stop Government Service Platform

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Electronic signature validity | PRC | 中华人民共和国电子签名法 — https://www.gov.cn/ | Name/date cited; clause mapping to confirm |
| Administrative licensing (受理/审查/决定 vocabulary) | PRC | 中华人民共和国行政许可法 — https://www.gov.cn/ | Drives approval vocabulary; clause mapping to confirm |
| Cybersecurity Law (name only) | PRC | 中华人民共和国网络安全法 — https://www.gov.cn/ | Clauses not mapped |
| Data Security Law / PIPL (names only) | PRC | 中华人民共和国数据安全法 / 个人信息保护法 — https://www.gov.cn/ | Clauses not mapped |
| CN graded protection (政务云, level-3 baseline) | — | GB/T 22239-2019 网络安全等级保护基本要求 (MLPS 2.0) | Control-item mapping to confirm |
| E-license / e-seal national standards | — | 电子证照 / 电子签章 GB/T series | Standard numbers to confirm |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| 好差评 (service-rating) mechanism | PRC State Council | 政务服务"好差评" policy — https://www.gov.cn/ | Specific document to confirm |
| 电子证照 integration contract | — | to confirm | External platform interface spec not yet identified |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Approval workflow engine | Camunda | https://camunda.com/ | BPMN engine; candidate for approval backbone |
| Identity federation (real-name) | Keycloak | https://www.keycloak.org/ | Boundary component only |

## 4. Uncited specifics to resolve

Resolved at L2 (pack design; still need external sourcing for source-checked):

- **Two item kinds** — ADR-0001 settles kind-determined result shape. Still open:
  **which items are 行政权力 vs 公共服务 in a given regime** — a legal
  determination per item, not a pack decision.
- **Guide as contract** — ADR-0002 settles versioned publication and reliance
  recording. Still open: **how far back a relied-on version must be retrievable**,
  and what an applicant is owed when a guide changes mid-application.
- **Identity** — ADR-0003 settles integration with no local credential. Still open:
  **the guest and anonymous edge cases** — which flows genuinely need no identity,
  and whether any can proceed as a guest (the pack's default is no).
- **Channels** — ADR-0004 settles variant-over-fork with five declared aspects.
  Still open: **the permitted-alternative catalogue for paid and assisted flows**
  that cannot use hosted payment fields — deliberately unspecified.
- **Anti-double-submission** — ADR-0005 settles per-field rules and a defined
  permitted alternative. Still open: **the set of permitted alternatives itself**
  — an L3 design task, and the one that decides whether the rule is enforceable in
  practice.
- **Statutory vocabulary and clock** — ADR-0006 settles vocabulary, clock start and
  the two notices. Still open: **clock pause/resume semantics and thresholds**,
  and whether auto-approval on timeout is permitted at all in a given regime.
- **Seal and licence** — ADR-0007 settles national-service integration and at-signing
  validity. Still open: **the 统一电子印章 technical standard** — the Measures
  mandate compliance with national standards but name no number; the pack names
  none either.
- **Electronic archive** — ADR-0008 settles verified completeness. Still open:
  **what a migration may not drop**, now that the application model is an archival
  object — a schema-change rule the pack requires but does not write.

Still open:

- **Retention values** — required per class by BR-12; **no period is asserted**.
- **Regional rules beyond the national instrument** — 国令第716号 is the national
  regulation; provincial and municipal implementation rules may add obligations
  this pack does not model.
- **GB/T 36901/36902/36906 clause mapping** — cited as designations; the electronic
  licence standard's clauses are not retrieved, and whether this platform's internal
  事项 catalogue should align to the 36902/36903 structure is deliberately
  undecided.
- **Cross-border destination transfer** — recorded as a pack-added designation in
  data-exchange CTL-04; not verified against an instrument here.
- **Sector data-security rules** — a sector-specific data rule may add obligations
  beyond the instruments named; not modelled here.
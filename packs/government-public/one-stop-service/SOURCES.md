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

- **事项 (service item) guide element field set** — no confirmed standard; to confirm.
- **SLA / 限时办结 durations** — no source for typical time-boxes.
- **受理 → 审查 → 决定 → 出件 state machine** — statutory vocabulary is real, but the exact transitions/guards are unverified.
- **一次性告知 / supplement-once rules** — policy-derived, no citation.
- **电子证照 standard versions & integration APIs** — to confirm.
- **MLPS level-3 control-item mapping** — to confirm.
- **Cross-region/跨层级 (省–市–区–街道) routing model** — design choice, no source.
- **好差评 mechanism definition & official source** — to confirm.

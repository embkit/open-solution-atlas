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

Resolved at L1 (now grounded in the cited regulation; details still needed at L2):

- **事项 guide element field set** — 国务院令第716号 **第六条** mandates the three
  elements (受理条件/办事材料/办理流程). The statutory minimum is now cited; the
  national 事项编码 set and any fuller metadata profile are **not** retrieved.
- **受理 → 审查 → 决定 → 出件 state machine** — the vocabulary is statutory and
  now defined in `03-domain/glossary.md` §2, with 受理/不予受理/不予批准 kept
  distinct. The exact transitions and guards remain unverified.
- **一次性告知 vs. 补正** — now defined as **distinct** terms in
  `03-domain/glossary.md` §1 (一次性告知 precedes acceptance; 补正 follows it).
  Still no citation for the once-only rule itself.
- **电子证照 standard versions** — the GB/T 36901–36906-2018 six-standard series
  is confirmed real (published 2018-11-15, effective 2019-01-01, 现行, 归口国家
  密码局). Clause-level requirements and the actual integration API are not
  retrieved; GB/T 36906 is named as the sharing-service interface.
- **MLPS level** — 等保三级 remains the pack's stated assumption (README), not a
  citation; no control-item mapping.

Still open:

- **SLA / 限时办结 durations** — no source for typical time-boxes, and the
  clock's starting point (受理 vs. submission) is an asserted design position.
- **统一电子印章 technical standard** — 国务院令第716号 第九条 mandates the
  national unified seal system but names **no standard number**, and this pack
  names none either. Establishing it is a precondition for L2.
- **事项 catalogue vs. GB/T 36902/36903** — whether the internal service-item
  catalogue should adopt the electronic-licence catalogue structure is
  deliberately undecided; they are different objects.
- **Cross-region/跨层级 (省–市–区–街道) routing model** — design choice, no source.
- **好差评 mechanism definition & official source** — to confirm.

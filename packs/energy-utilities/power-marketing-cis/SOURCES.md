# SOURCES — Power Marketing & Customer Information System

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Electricity law (name only) | PRC | 中华人民共和国电力法 — https://www.gov.cn/ | Clause mapping to confirm |
| Power supply & use regulation (name only) | PRC | 电力供应与使用条例 (国务院) — https://www.gov.cn/ | Basis for disconnection/reconnection procedure; clauses to confirm |
| Power-sector regulation & service norms | NEA | 国家能源局 — https://www.nea.gov.cn/ | 供电监管办法 / 供电服务规范 to confirm |
| Retail tariff policy | NDRC | 国家发展改革委 — https://www.ndrc.gov.cn/ | Price tables are policy-driven and change frequently; to confirm |
| CN graded protection (电力营销系统) | — | GB/T 22239-2019 网络安全等级保护基本要求 (MLPS 2.0) | Control-item mapping to confirm |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| 95598 service standard | — | to confirm | Public/industry standard reference not yet identified |
| Meter-reading / AMR data exchange | — | to confirm | Utility-specific interface spec not identified |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| — | (none confirmed) | — | No OSS reference identified for this domain yet; billing/tariff logic is utility-specific |

## 4. Uncited specifics to resolve

- **Tariff tables (居民阶梯/合表/工商业目录电价)** — exact figures are policy-driven and change frequently; no stable citable source. Treat as data, not fact.
- **估抄/补抄/零度户 exception rules & thresholds** — no source.
- **95598 service standard details** — public/industry source to confirm.
- **报装容量 (connection capacity) rules** — no source.
- **Disconnect/reconnect regulated procedure detail** — to confirm against 电力供应与使用条例 clauses.
- **Line-loss delivery / 反窃电线索 analytics thresholds** — no source.
- **Existing manifest source `http://www.dltjyy.cn/`** — provenance/authority unverified; confirm or replace.
- **Prepayment (预付费) model depth** — residential vs commercial variant; no source.
- **等保2.0 control-item mapping** — to confirm.

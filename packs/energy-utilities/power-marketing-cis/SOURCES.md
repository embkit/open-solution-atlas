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

Resolved at L2 (pack design; still need external sourcing for source-checked):

- **Tariff rules** — ADR-0001 settles versioned + effective-dated + governed
  separately from billing code. Still open: **the tariff rule content itself**,
  deliberately unencoded (see industry-brief.md §11).
- **Charge events and invoices** — ADR-0002 settles immutability, rule-version
  stamping, and regeneration-with-recorded-versions. Still open: the
  **retention period** per class, in tension with erasure (deliberately
  unresolved).
- **估抄** — ADR-0003 settles rule-bound, labelled, and reconciled. Still open:
  **the estimation method, period, and reconciliation rule** — regulatory inputs,
  not pack theses.
- **Disconnection guardrails** — ADR-0004 settles enforced-state + recorded
  evaluation. Still open: **which classes apply** — a regulatory input.
- **Interface** — BR-02 settles interface-only with no SCADA scope. Still open:
  the **contract itself** as payload shapes and state vocabulary (L3).

Still open:

- **Regulatory mapping** — 电力法 and MLPS 2.0 remain **designations only**. No
  clause-level mapping exists, per this repository's scope decision
  (see docs/citation-audit-2026-10.md §4).
- **Retention of rules, readings and approval records** — the tension with
  erasure is real; the regeneration window is a business decision.
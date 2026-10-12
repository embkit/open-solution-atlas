# SOURCES — Government Data Sharing & Exchange Platform

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Open-data catalog metadata vocabulary | W3C | DCAT v3 — https://www.w3.org/TR/vocab-dcat-3/ | Which DCAT profile/subset to adopt — to confirm |
| CN graded protection (政务云 / 政务系统) | — | GB/T 22239-2019 网络安全等级保护基本要求 (MLPS 2.0) | Article/control-level mapping to confirm |
| Data Security Law (name only) | PRC | 中华人民共和国数据安全法 — https://www.gov.cn/ | Official text via gov.cn / npc.gov.cn; clauses not mapped |
| Personal Information Protection Law (name only) | PRC | 中华人民共和国个人信息保护法 — https://www.gov.cn/ | Clauses not mapped |
| Government information-resource catalog standard | — | 政务信息资源目录体系 national standard | Standard number / clause mapping to confirm |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Regional DCAT application profile | EU / Joinup | https://joinup.ec.europa.eu/ | DCAT-AP as a comparison; CN profile to confirm |
| Exchange-channel interface specs (库表/文件/接口) | — | to confirm | No normative spec identified yet |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Open data portal / catalog & discovery | CKAN | https://ckan.org/ | Public-dataset publication reference |
| Metadata & lineage | Apache Atlas | https://atlas.apache.org/ | |
| Metadata platform | OpenMetadata | https://open-metadata.org/ | |
| Metadata platform | DataHub | https://datahubproject.io/ | |

## 4. Uncited specifics to resolve

Resolved at L2 (pack design; still need external sourcing for source-checked):

- **Catalog as root** — ADR-0001 settles entry-as-unit and no-source-system
  authorization. Still open: **the resource description vocabulary** — what a
  esource_ref may describe, and how granular it is relative to a table or a
  field.
- **Catalog currency** — ADR-0002 settles a measured obligation with owner
  routing. Still open: **whether an over-obligation entry blocks sharing** — the
  pack chose reporting over blocking and recorded the trade.
- **Refusal basis** — ADR-0003 settles a required basis field. Still open: **the
  structure of a legal basis** — how a citation to a 法律/行政法规/政策 is recorded
  so it is checkable rather than a string.
- **Grade-driven rules** — ADR-0004 settles derivation with no overrides. Still
  open: **the grade → rule mapping itself** — needs GB/T 43697-2024 confirmed at
  clause level.
- **Structured purpose** — ADR-0005 settles structure over free text. Still open:
  **the structure that covers the purposes actually in use** — the L3 design task.
- **Closed share types and open data** — ADR-0006 settles the closed vocabulary
  and the separate regime. Still open: **whether open data is core or a sibling
  pack** (open question #3).

Still open:

- **Regulatory mapping** — 国发〔2016〕51号 is quoted at article level (第八/九/十/
  十三/十四条) against the State Council Gazette and re-checked for currency in
  the 2026-10 audit, but later **provincial and municipal implementation rules may
  add obligations this pack does not model**. MLPS 2.0, 《数据安全法》, GB/T 43697
  and GDPR/PIPL remain **designations only** — no clause-level mapping exists, per
  this repository's scope decision (see docs/citation-audit-2026-10.md §4).
- **GB/T 21063 clause mapping** — cited as a designation; the clause-level mapping
  to this platform's catalog model is a precondition for source-checked.
- **《政务信息资源目录编制指南》** — named as a designation only, because its text
  has not been retrieved.
- **Federated vs. centralized nodes** — open question #2; the pack does not assume
  an answer.
- **Channel composition** — open question #1; whether all three are first-class is
  undecided.
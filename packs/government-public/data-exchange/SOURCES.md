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

- **Catalog (资源目录) metadata field set** — no confirmed national-standard field list; to confirm.
- **Data classification/grading (分级分类) levels & masking rules per class** — no source; jurisdiction- and policy-specific.
- **Exchange channel composition** — whether 库表/文件/接口 are all first-class or one is primary with adapters is a design choice.
- **National/provincial exchange hierarchy** — single-tenant vs federated nodes is an open question; no source.
- **Approval/grant lifecycle & revocation rules** — workflow states and revocation semantics uncited.
- **Desensitization depth** — centralized rules engine vs per-channel policy is a design choice.
- **DCAT profile choice** — which government DCAT subset applies — to confirm.
- **Law obligations cited by name only** — 数据安全法/PIPL are referenced without clause mapping; pending.

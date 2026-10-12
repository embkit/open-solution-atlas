# 01-business / Capability Map

```
01-business / capability-map.md — Government Data Sharing & Exchange Platform (L1)

┌─ 01 Catalog & resource registry ──────────────────────────────────────┐
│  registration · 挂接 · metadata · share type · classification · 目录编制 │
└──────────────────────────────────────────────────────────────────────┘
┌─ 02 Authorization & grant lifecycle ──────────────────────────────────┐
│  request · purpose capture · approval · grant · amend · suspend · revoke│
└──────────────────────────────────────────────────────────────────────┘
┌─ 03 Exchange channels ────────────────────────────────────────────────┐
│  库表 · 文件 · 接口 · scheduling · batching · incremental · retry        │
└──────────────────────────────────────────────────────────────────────┘
┌─ 04 Classification & masking ─────────────────────────────────────────┐
│  grade assignment · per-class rules · desensitization · policy engine  │
└──────────────────────────────────────────────────────────────────────┘
┌─ 05 Lineage & attribution ────────────────────────────────────────────┐
│  source → grant → consumer → artefact · who/what/why/when · replay      │
└──────────────────────────────────────────────────────────────────────┘
┌─ 06 Quality & reconciliation ──────────────────────────────────────────┐
│  source↔platform↔consumer consistency · freshness · 疑义/错误校核       │
└──────────────────────────────────────────────────────────────────────┘
┌─ 07 Usage monitoring & audit ─────────────────────────────────────────┐
│  purpose conformance · statistics · reports · evidence for supervision │
└──────────────────────────────────────────────────────────────────────┘
┌─ 08 Open-data publication ────────────────────────────────────────────┐
│  dataset selection · DCAT metadata · desensitization · portal feed     │
└──────────────────────────────────────────────────────────────────────┘
┌─ 09 Identity, org & department context ──────────────────────────────┐
│  department identity · role · delegation · service accounts           │
└──────────────────────────────────────────────────────────────────────┘
┌─ 10 Platform operations & security compliance ───────────────────────┐
│  availability · 等保 controls · incident · capacity · upgrade          │
└──────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **CAP-01** | **Catalog & resource registry** | what exists, who owns it, and on what terms it may be shared | the root object linking provider, resource, classification and consumers (`AGENTS.md`) |
| **CAP-02** | **Authorization & grant lifecycle** | whether a transfer may occur, and can it be stopped | request → purpose → approval → grant → revoke; a grant is revocable by design |
| **CAP-03** | **Exchange channels** | how data physically moves | 库表/文件/接口; whether all are first-class is an open question (`README.md` #1) |
| **CAP-04** | **Classification & masking** | what protection applies to this data, enforced where | grade → rule, enforced at exchange time |
| **CAP-05** | **Lineage & attribution** | for any transfer, who authorized it, why, and what moved | the closing half of the audited loop |
| **CAP-06** | **Quality & reconciliation** | whether delivered data matches what the provider holds | 第十三条 makes this a provider obligation |
| **CAP-07** | **Usage monitoring & audit** | whether consumers stayed within their declared purpose | 第十四条 makes purpose-bound use a duty |
| **CAP-08** | **Open-data publication** | how public datasets are produced and described | DCAT-modelled; a different regime, not a subset |
| **CAP-09** | **Identity, org & department context** | who is acting, on whose behalf | department identity, roles, delegation, service accounts |
| **CAP-10** | **Operations & security compliance** | is the platform itself controlled and available | 等保 controls, incident response, capacity |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 01 Catalog | deciding whether a share is approved — that is 02 |
| 02 Authorization | deciding *what* the data is — that is 01 |
| 03 Exchange | deciding whether a transfer is permitted — it executes a grant |
| 04 Classification | deciding the grade — that is the provider and the classification officer |
| 05 Lineage | making the decision lawful — it records, so the decision can be examined |
| 06 Quality | fixing the source data — it reports, the provider corrects (第十三条) |
| 07 Usage monitoring | adjudicating misuse — it surfaces, supervision adjudicates |
| 08 Open data | setting the legal basis for publication — it publishes what is approved |
| 09 Identity | departmental authority — it identifies, it does not confer rights |
| 10 Operations | business policy about data — it runs the platform |

> The most common failure in this class of system is a capability quietly
> absorbing its neighbour: masking done in the BI tool rather than the platform,
> purpose recorded as a free-text note rather than a grant attribute, or
> reconciliation run only when a consumer complains. Each boundary above is a
> checkable statement.

## 3. Level-1 priorities

Complete for discussion, incomplete for estimation; silent on relative
difficulty because that needs a reference deployment.

> ⚠️ ASSUMPTION: capabilities **01 (catalog)**, **02 (grants)** and **05
> (lineage/attribution)** are named first because `AGENTS.md` treats the
> authorization → approval → share → lineage loop as the platform's defining
> requirement. This is an editorial ordering, not an evidence-backed
> criticality claim.

## 4. Out of scope for the whole platform

- Citizen-facing service delivery (the `one-stop-service` pack) — the platform
  supplies data to it via published interfaces.
- The business systems that own the source data.
- Analytics/BI built on shared data (the `data-ai` packs).
- 政务云 and network infrastructure — the hosting substrate.
- The organisation's data-governance **policy** — the platform enforces
  decisions, it does not make them.

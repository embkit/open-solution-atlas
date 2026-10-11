# 00-context / Industry Brief — Government Data Sharing & Exchange Platform

## 1. What this system is in the value chain

Government services run on data that departments hold and rarely agree on. A
**政务数据共享交换平台** (government data sharing & exchange platform) is the
horizontal system that moves data between departments **only when authorised**,
and makes every movement attributable.

It is the **substrate**, not the front door. The citizen-facing portal
(一网通办, the sibling `one-stop-service` pack) is one of its consumers, and so
are internal approval systems, credit systems and analytics:

```
  provider departments                     consumer departments
  --------------------                     ---------------------
  公安局 (population)                      市场监管局 / 医保 / 人社 / 税务
  市场监管局 (legal persons)  ┌────────┐    一网通办 portal (citizen-facing)
  自然资源 (geo)      ───────▶│ SHARING│◀──────  analytics & 决策支持
  人社 / 医保         ───────▶│ & EXCH │        公共数据开放门户 (open data)
  电子证照库          ───────▶│ PLATFORM│
                            └────────┘
                                 │
                     catalog · grants · lineage · quality
                     classification · masking · audit
```

The defining problem is **authorized, traceable sharing**: no data transfer
exists without a recorded, revocable grant, and every share is attributable
(`AGENTS.md`). A platform that technically moves data without recording *why*
has failed its core requirement, however good the throughput is.

## 2. The governing principle: share by default

《政务信息资源共享管理暂行办法》(国发〔2016〕51号) sets the domain's
constitutional rule:

> 以共享为原则，不共享为例外；需求导向、无偿使用；统一标准、统筹建设；
> 建立机制、保障安全。

Two operational consequences follow, and they shape everything else:

1. **Sharing is the default; refusal is the exception that must be
   justified.** The same办法第十条 provides that resources classified as
   **不予共享** (not shareable) must have a **legal, regulatory, or CPC
   Central/State Council policy basis**. So "不予共享" is a claim that carries
   a citation obligation, not a preference.
2. **Sharing is free of charge between departments.** The business model of a
   commercial data exchange simply does not apply.

## 3. The three share types — the pack's central classification

《办法》第九条 divides government information resources into three share
types:

| Share type | 中文 | Definition (per 第九条) | Platform consequence |
|---|---|---|---|
| **Unconditional** | 无条件共享 | available to **all** 政务部门 | no per-consumer grant needed; still recorded |
| **Conditional** | 有条件共享 | available to **related** departments, or only partially | requires an approval workflow and a grant |
| **Not shareable** | 不予共享 | not appropriate to share | must cite a legal/regulatory/policy basis (第十条) |

> ⚠️ ASSUMPTION: the pack treats share type as a **property of the catalog
> entry** that drives workflow behaviour, not as a free-text label. This is the
> pack's design position; 第九条 defines the types but not the system.

同一《办法》第十条 also names the **basic information resources** — population
(人口信息), legal persons (法人单位), natural resources and geospatial
(自然资源和空间地理信息), electronic licences/certificates (电子证照) — whose
**basic fields** must be shared unconditionally. These are the high-volume,
high-sensitivity backbone the platform is usually built for first.

## 4. Core flows (L1 view)

1. **Register** — a provider registers a data resource in the catalog
   (资源目录) with metadata, share type, classification grade and owner.
2. **Request** — a consumer department requests access, stating purpose,
   scope and duration (第十四条: use is limited to the declared purpose).
3. **Approve** — for conditional resources, the provider (and where policy
   requires, the platform authority) approves. The grant is recorded.
4. **Exchange** — data moves over a channel: table-to-table (库表), file, or
   API (接口). Scheduling, batching and incremental exchange apply.
5. **Consume & log** — the consumer uses the data within the declared purpose;
   usage is logged.
6. **Monitor & reconcile** — quality, freshness and consistency between what a
   provider holds and what was delivered (第十三条: the provider must ensure
   the shared data matches what it holds).
7. **Revoke & review** — grants expire or are revoked; usage is auditable
   throughout.

## 5. Why this system is unusually hard to get right

- **The loop must be closed.** Authorization → approval → share → lineage is a
  *cycle*, not a sequence (`AGENTS.md`). A grant that is never revoked, a share
  with no grant, or lineage that stops at "an API was called" each break it.
- **Refusal needs a citation.** 第十条 means the platform must be able to store
  and display *the legal basis* for a 不予共享 classification. A dropdown with
  no source field cannot do that.
- **The catalog is the root object.** It links provider, resource,
  classification and consumers (`AGENTS.md`). Without it, authorization has
  nothing to authorize *against*.
- **Classification must drive enforcement.** 分级分类 determines masking and
  access rules; if classification is metadata-for-reporting rather than
  policy-for-enforcement, the control does not exist.
- **Cross-department authority is political, not technical.** "谁经手，谁使用,
  谁管理，谁负责" (第十四条) assigns responsibility in a way that no system can
  implement on its own — the platform can only make the responsibility
  *visible and enforced*.
- **Open data has different rules.** Publishing to the public is not the same
  as sharing with another department: the metadata model (DCAT), the consent
  basis and the desensitization bar are all different.

## 6. Defining quality metrics

L1 frames intent; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Catalog coverage & freshness | is the catalog a reliable map of what exists |
| Grant completeness (% shares with a valid, unexpired grant) | whether the "no transfer without a grant" rule holds |
| Exchange success & latency (per channel) | whether the plumbing works |
| Reconciliation variance (provider vs. consumer) | whether delivered data matches the source |
| Revocation lead time (request → access actually removed) | whether revocation is real |
| Usage-purpose conformance (% usage matching declared purpose) | whether 第十四条 is observable at all |
| Desensitization pass rate | whether classification-driven masking works |
| Open-data publication currency | whether the open-data front is maintained |

## 7. Public materials anchoring the model

**Statutory / policy (cited by document and 文号):**

- **《政务信息资源共享管理暂行办法》** (国发〔2016〕51号, 2016-09-05 印发) —
  the domain's basis: the share-by-default principle, the three share types
  (第九条), the citation obligation for 不予共享 and the basic information
  resources (第十条), and the provider/consumer responsibility rules
  (第十三/十四条). Full text reachable at
  http://www.cac.gov.cn/2016-09/21/c_1119596700.htm and mirrored on Wikisource.
- **《政务信息资源目录编制指南》** — the companion document referenced by
  第八条 for how departmental catalogs are compiled and maintained
  (15 working days update duty). **Not yet retrieved; designation only.**

**Standards (verified reachable):**

- **W3C DCAT 3** — https://www.w3.org/TR/vocab-dcat-3/ — the vocabulary for
  open-data catalog metadata.
- **GB/T 21063《政务信息资源目录体系》** — the national standard for the
  government information resource *catalog system*; accessible via the national
  standards information platform (https://openstd.samr.gov.cn/bzgk/gb/std_list?p.p2=GB/T%2021063).
  Clause-level mapping still to be confirmed.

**Other instruments in scope (designations stated; clause mapping at L2):**

- **GB/T 22239-2019**《网络安全等级保护基本要求》 — graded-protection baseline.
- **GB/T 43697-2024**《数据安全技术 数据分类分级规则》 — the classification and
  grading method behind the pack's classification-driven policy.
- **《中华人民共和国数据安全法》** (2021-09-01 施行).
- **《中华人民共和国个人信息保护法》** (2021-11-01 施行) — personal
  information handling; relevant to 人口/医保/自然人 data.

> ⚠️ ASSUMPTION: the platform is assumed to be a **single-tenant
> municipal/provincial node** with the possibility of federated nodes; whether
> the core is federated or centralized is an explicit open question
> (`README.md` #2) and the pack does not assume an answer.

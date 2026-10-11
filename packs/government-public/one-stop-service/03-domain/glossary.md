# 03-domain / Glossary

> **Purpose of this file at L1.** `AGENTS.md` requires approval lifecycles to use
> **Chinese statutory vocabulary** (受理/审查/决定/出件, 一次性告知, 限时办结)
> rather than generic workflow words. Those terms carry legal meaning in this
> domain, so they are defined here explicitly and used verbatim throughout the
> pack. A term defined here has exactly one meaning; no synonyms are introduced
> later.
>
> `Source` records the basis: **[REG]** 国务院令第716号 (cited), **[STD]** a
> national standard (cited), **[PACK]** this pack's definition, **[CONV]** an
> industry convention with no single standard.

## 1. The catalogue root

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Service item (事项)** | 政务服务事项 | The unit of government service a citizen or enterprise applies for. **The catalogue root**: it determines the guide, form, materials, routing, deadline and result. | [REG] 第四条 |
| **Administrative power item** | 行政权力事项 | A 事项 where an administrative power is exercised and a formal 决定 is issued — with review, reconsideration and appeal consequences. | [REG] 第四条 |
| **Public service item** | 公共服务事项 | A 事项 that delivers a service rather than exercising an administrative power. No 决定书 in the same sense. | [REG] 第四条 |
| **Service guide (办事指南)** | 办事指南 | The published statement of a 事项: **受理条件, 办事材料, 办理流程**, plus what the applicant needs to know. Published on the platform. | [REG] 第六条 |
| **Acceptance condition (受理条件)** | 受理条件 | The conditions under which an application is 受理. Because it is declared, the material list is derivable from it rather than maintained separately. | [REG] 第六条; [PACK] for the derivation claim |
| **Materials (办事材料)** | 办事材料 | The documents and data an applicant must supply. Each material must be classified **obtainable by sharing** or not. | [REG] 第六条/第七条 |
| **Item code** | 事项编码 | The standardised identifier of a 事项, required for cross-region interoperability and supervision statistics. | [PACK] (national code set not retrieved — see SOURCES) |
| **Case (办件)** | 办件 | One submitted instance of a 事项 by one applicant. The unit tracked, timed and archived. | [PACK] |
| **One-thing (一件事)** | 一件事 | Several 事项 and procedures that a citizen experiences as one affair, delivered as one integrated journey while each decision remains with its own authority. | [CONV] |
| **Supplement request (补正)** | 补正 | The agency's request for missing or defective material, after 受理. Distinct from **一次性告知**, which happens *before* acceptance. | [PACK] |
| **Once-only notification (一次性告知)** | 一次性告知 | Where an application cannot be 受理, the agency must notify the applicant **once**, completely, of everything that is missing — not reject piecemeal. | [PACK] (standard practice; the regulation mandates the published guide, not this term) |
| **Time-limited completion (限时办结)** | 限时办结 | The commitment that a 事项 concludes within a declared time limit. A service commitment, and a measurement obligation. | [REG] 第六条 (办理流程/时限 published) |
| **Result (出件)** | 出件 | Issuing the outcome of a decided 事项 to the applicant, with the decision document or licence. | [PACK] |
| **Rating (好差评)** | 好差评 | The applicant's post-service evaluation of the handling — the feedback channel closing the loop. | [CONV] |

## 2. The approval lifecycle

`AGENTS.md` requires these statutory terms. Their order and their legal
distinctions are the point — a generic "approved/rejected" workflow loses them.

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Accept (受理)** | 受理 | The agency formally takes the application into process. **Acceptance is not approval** — it starts the clock and the statutory duties. | [PACK] |
| **Examine (审查)** | 审查 | Substantive review of the application against the conditions. May result in 补正. | [PACK] |
| **Decide (决定)** | 决定 | The agency's formal outcome: 同意/批准, 不予批准/不予许可, or another disposition defined by the 事项. Issued by the authority that holds the legal power. | [PACK] |
| **Issue (出件)** | 出件 | Delivery of the decided result to the applicant. | [PACK] |
| **Not accepted** | 不予受理 | Where the application fails the 受理条件. The agency then owes a **一次性告知** listing everything missing, once. | [PACK] |
| **Not approved** | 不予批准 | A decision after 受理 and 审查 that refuses the application on the merits. **Not** the same as 不予受理 — it carries different consequences for the applicant. | [PACK] |
| **Reconsideration / review** | 行政复议 / 诉讼 | The applicant's statutory routes against a 决定. **Out of the platform's scope to decide**, but the platform must preserve the record that such a route exists and when it was notified. | [REG] 第四条 (行政权力事项 distinction); [PACK] for the preservation duty |
| **Deadline clock** | 办结时限 | The timer on a 办件, measured per 事项 and paused/resumed per policy. Starts at 受理, not at submission. | [PACK] |
| **Withdrawal** | 撤回 | The applicant retracting a submitted 办件 before a decision. | [PACK] |

> ⚠️ ASSUMPTION: the pack treats 受理 → 审查 → 决定 → 出件 as the canonical
> lifecycle and states that the **deadline clock starts at 受理**. That starting
> point materially changes reported performance, and it is a design position
> this pack asserts — it is not quoted from the regulation. L2 must confirm it
> against the applicable procedural rules for each 事项 type.

## 3. Identity, data and verification

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Unified authentication** | 统一身份认证 | The national authentication service providing 一次认证、全网通办. **Integrated, never re-implemented.** | [REG] 第五条; `AGENTS.md` |
| **Legal representative** | 法定代表人 | The person who may act for an enterprise. | [PACK] |
| **Authorised agent** | 委托代理人 | A person acting for an applicant under authorisation; requires recorded authorised consent. | [PACK] |
| **Shared-data verification** | 共享数据核验 | Confirming applicant facts from another authority's data instead of demanding them. Each call **consented and audited** (`AGENTS.md`). | [REG] 第七条 (the duty); [PACK] (the mechanism) |
| **Obtainable by sharing** | 可共享获取 | A field or material the agency can obtain through data sharing, and therefore **must not** be demanded. A **per-field classification**, not a per-form guess. | [REG] 第七条; [PACK] for the field-level mechanism |
| **Pre-fill** | 数据预填 | Populating a form from shared data so the applicant confirms rather than types. | [PACK] |
| **Degradation path** | 降级路径 | What happens when a shared-data lookup fails. It must **not** silently convert into asking the applicant — that is a 第七条 violation. | [PACK] (derived from 第七条) |

## 4. Electronic artefacts

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Electronic signature** | 电子签名 | Data contained in or attached to a data message, used to identify the signer's identity and indicate recognition of its content. | [REG] 第十五条 |
| **Electronic seal (电子印章)** | 电子印章 | A seal generated using trusted cryptography as an identity marker, rendered as electronic graphic data. From the **national unified seal system**. **Same legal effect as a physical seal.** | [REG] 第九条/第十五条 |
| **Electronic licence (电子证照)** | 电子证照 | A licence, certificate or similar electronic document formed, transmitted and stored by electronic equipment. **Same legal effect as a paper licence**; may be used as the basis for handling a 事项. | [REG] 第十条/第十一条/第十五条 |
| **Standard layout document** | 标准版式文档格式 | The prescribed document format for 电子证照 (typically OFD-family). | [REG] 第十条 |
| **Licence annotation (加注件)** | 加注件 | An addendum attached to a licence recording a change or annotation. | [STD] GB/T 36901-2018 architecture (电子证照资源库: 证照库, 管理信息和加注件) |
| **Mutual recognition** | 互信互认 | Cross-region and cross-department acceptance of the same 电子证照 without re-submission. | [REG] 第十条 |
| **Electronic file** | 电子文件 | A file formed during the exercise of official duties, managed and archived electronically. | [REG] 第十二条 |
| **Electronic archive** | 电子档案 | An electronic file with evidential, reference and preservation value, archived. **Same legal effect as a paper archive.** | [REG] 第十二条/第十五条 |
| **Reliable e-signature** | 可靠的电子签名 | A signature meeting the Electronic Signature Law's conditions; same effect as handwritten signature or seal. Referenced by 国务院令第716号 but **not defined in it**. | [REG] (cross-reference); definition in 《电子签名法》 — see SOURCES |

## 5. Supplied by external platforms — never re-implemented

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **National integrated platform** | 全国一体化在线政务服务平台 | The national platform; the system this one integrates with. | [REG] 第四条 |
| **Unified seal system** | 国家统一电子印章系统 | The national service issuing seals. | [REG] 第九条 |
| **E-licence sharing service** | 电子证照共享服务系统 | The national service providing licence catalogue, sharing and mutual recognition. | [REG] 第十条 |
| **Government data sharing platform** | 政务数据共享交换平台 | The data substrate (`data-exchange` pack) that makes 第七条 satisfiable. | [PACK]; §7 of 国发〔2016〕51号 for the share-by-default basis |
| **Integration dependency** | 集成依赖 | A capability consumed through a published interface because re-implementing it is both non-compliant and a security liability (`AGENTS.md`). | [PACK] |

## 6. Supervision and feedback

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Pre/in/post supervision** | 事前事中事后监管 | Supervision before, during and after the process; a stated requirement of 国发〔2022〕5号 for 政务服务. | [PACK] (cited to 国发〔2022〕5号) |
| **Complaint** | 投诉 | An applicant's challenge to handling; routed, not adjudicated by the platform. | [CONV] |
| **Approval-outcome record** | 决定记录 | The immutable record of who decided what, when, on what basis, with which seal. The platform's core evidential artefact. | [PACK] |

## 7. Conventions

- **"must not"** marks a rule whose violation is a defect — e.g. data
  obtainable by sharing must not be demanded; a seal must not be minted
  locally.
- **Bilingual terms**: Chinese is authoritative for the 政务 lifecycle and
  licence vocabulary, because these terms are **statutory**; English for general
  platform terms.
- **No synonyms**: this pack uses **一次性告知** and **补正** as **distinct**
  terms and never interchanges them; **不予受理** and **不予批准** likewise;
  it uses **办件** (not "ticket"/"order") and **事项** (not "service"/"item"
  interchangeably).
# 00-context / Regulatory Landscape

> Obligations stated at instrument level with their engineering consequence.
> Where an article-level mapping is unverified, it is marked — per the pack
> standard §5. `verification: unverified`; this is not compliance advice.

## 1. Instruments in scope

| Instrument | Jurisdiction | What it governs here |
|---|---|---|
| **《政务信息资源共享管理暂行办法》** (国发〔2016〕51号, 2016-09-05 印发) | CN | The share-by-default principle; the three share types; the citation obligation for non-shareable resources; provider/consumer responsibility |
| **《政务信息资源目录编制指南》** | CN | How departmental resource catalogs are compiled and maintained (designation; text not yet retrieved) |
| **GB/T 21063《政务信息资源目录体系》** | CN | The national standard for the catalog system that carries the catalog |
| **GB/T 22239-2019《网络安全等级保护基本要求》** | CN | Graded-protection (等保/MLPS 2.0) baseline |
| **GB/T 43697-2024《数据安全技术 数据分类分级规则》** | CN | The method behind classification and grading |
| **《中华人民共和国数据安全法》** (2021-09-01 施行) | CN | Data-handling duties; classification grading; risk management |
| **《中华人民共和国个人信息保护法》** (2021-11-01 施行) | CN | Personal information handling; consent basis; deletion rights |
| **W3C DCAT 3** | Global (industry) | Metadata vocabulary for open-data catalogs |

## 2. What the 国发〔2016〕51号 办法 actually requires

The operative clauses were read from the published text and are quoted at the
level a builder can act on.

**The governing principle.** 以共享为原则，不共享为例外；需求导向、无偿使用；
统一标准、统筹建设；建立机制、保障安全.

> Engineering consequence: the platform's default path must be **share**.
> Every configuration that makes sharing harder than withholding inverts the
> policy and is a defect, not a preference.

**第九条 — the three share types.**

| Type | 中文 | The 办法's wording (condensed) |
|---|---|---|
| Unconditional share | 无条件共享 | may be provided for use by **all** 政务部门 |
| Conditional share | 有条件共享 | may be provided to **related** departments, or only partly to all |
| Not shareable | 不予共享 | not appropriate to provide to other 政务部门 |

**第十条 — refusal requires a basis.** A resource listed as 不予共享 must have
a **法律、行政法规或党中央、国务院政策依据**.

> Engineering consequence: the catalog entry for a non-shareable resource must
> carry a **reference to that basis**, and the platform must be able to show it.
> A share-type dropdown without a source-and-basis field cannot satisfy this.

**第十条 — basic information resources.** 人口信息、法人单位信息、自然资源和
空间地理信息、电子证照信息 and similar basic resources have **basic fields**
that departments commonly need; these must be shared **unconditionally**,
under an integrate-and-co-build principle, with data managed centrally or via
platform access.

> Engineering consequence: the platform must treat a named set of resources as
> unconditionally shareable by *class*, not by per-consumer negotiation. This
> is the highest-volume, highest-sensitivity traffic and the reason the platform
> exists.

**第八条 — catalog currency.** Departments compile and maintain their resource
catalogs per the《政务信息资源目录编制指南》 and must update them **within 15
working days** of a relevant law/regulation change or a change in
administrative function.

> Engineering consequence: catalog freshness is a **compliance clock**, not a
> hygiene metric. A catalog with no staleness signal cannot demonstrate this.

**第十三条 / 第十四条 — responsibility on both sides.**

- 提供部门: 谁主管，谁提供，谁负责 — must maintain and update data, and ensure
  the shared data is **consistent with what the department itself holds**.
- 使用部门: 谁经手，谁使用，谁管理，谁负责 — may use shared data **only for the
  declared purpose**, must not pass it to third parties directly or in altered
  form, and must not use it for other purposes.

> Engineering consequence: **purpose-limited use is an obligation**, so the
> declared purpose must be a first-class, recorded attribute of the grant — and
> "did the consumer stay within it?" must be an auditable question. A grant
> that records *who* and *what* but not *why* cannot support this.

> ⚠️ ASSUMPTION: the article numbers above are quoted from the published text
> of 国发〔2016〕51号 (full text reachable at
> http://www.cac.gov.cn/2016-09/21/c_1119596700.htm and mirrored on Wikisource).
> Re-verify against the authoritative source before relying on them in a
> compliance argument. Later provincial/municipal implementation rules may add
> obligations this pack does not model.

## 3. The classification obligation

数据安全法 requires data classification grading; GB/T 43697-2024 supplies the
method; GB/T 21063 supplies the catalog framework in which the classification
is recorded.

> Engineering consequence (`AGENTS.md`): classification must **drive** masking
> and access-control rules, stated per class. If classification is recorded but
> not enforced, the platform has documentation rather than control.

> ⚠️ ASSUMPTION: the mapping from a classification grade to a concrete masking
> or access rule is **not specified** at L1. The pack defines the requirement
> (grade → rule) and leaves the rule set to L2 with the standard's clause
> mapping confirmed.

## 4. Personal information

PIPL governs personal information handling: lawful basis, purpose limitation,
minimum necessary, and the right to deletion. In this platform's context the
personal data of citizens moves between departments for public-service
purposes, which is exactly the case where a declared purpose and a lawful basis
matter most.

> Engineering consequence: the grant must record not only the consumer's
> declared purpose but the **legal basis** for inter-departmental use, and
> deletion must propagate across exchanged copies, caches, logs and derived
> datasets.

## 5. Graded protection (等保)

GB/T 22239-2019 sets the baseline controls for the platform itself. The
grading level is assigned externally; this pack requires the level to be a
**declared platform property** rather than an assumption, because it determines
which controls are mandatory.

> ⚠️ ASSUMPTION: this pack does **not** claim a grading level or map specific
> controls. Which GB/T 22239-2019 control set applies is an L2 compliance-chapter
> task requiring the assigned level.

## 6. Open data is a different regime

Publishing to the public (公共数据开放) is governed by different instruments
than inter-departmental sharing, and its metadata follows **W3C DCAT 3**.

> The pack models both, but does not assume open-data obligations are a
> subset of sharing obligations. Whether the open-data portal is core to this
> platform or a sibling pack is an explicit open question (`README.md` #3).

## 7. What would make this pack `source-checked`

1. Retrieve and cite《政务信息资源目录编制指南》.
2. Map GB/T 21063 catalog elements to this platform's catalog model.
3. Map GB/T 43697-2024 grades to concrete masking/access rules.
4. Map the assigned 等保 level to GB/T 22239-2019 controls.
5. Identify the regional implementation rules (省级/市级办法) that add
   obligations beyond 国发〔2016〕51号.

Until those close, `verification` stays `unverified` and this file's claims are
framing, not compliance advice.

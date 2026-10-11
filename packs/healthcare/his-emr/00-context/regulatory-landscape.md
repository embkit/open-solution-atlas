# 00-context / Regulatory Landscape

> Obligations are stated at the level a builder can act on, each with its
> engineering consequence, quoting the instrument. Where a mapping is unverified
> it is marked rather than asserted — per the pack standard §5.
> `verification: unverified`; **not** compliance advice.

> ⚠️ **Read this first — a citation hazard.** 《中华人民共和国网络安全法》was
> **amended on 2025-10-28 and the amendment took effect 2026-01-01**, with the
> law **renumbered and re-promulgated** ("对条文顺序作相应调整，重新公布").
> Article numbers from the 2016–2025 text are stale. For example the graded-
> protection duties were **第二十一条** in the old text and are **第二十三条**
> in the current one. **This pack uses the current numbering and cites no
> 网络安全法 article by number** where the operative provision is reproduced
> above from the amendment decision itself. Official text of the amendment:
> http://www.npc.gov.cn/c2/c30834/202510/t20251028_449048.html

## 1. Instruments in scope

| Instrument | Jurisdiction | Status | What it governs here |
|---|---|---|---|
| **《网络数据安全管理条例》** (国务院令第790号) | CN | effective 2025-01-01 | Network-data processing generally; personal information, important data, cross-border transfer, audit |
| **《网络安全法》** (as amended 2025-10-28) | CN | amended, effective 2026-01-01 | Graded protection duties; incident reporting; legal liability |
| **《数据安全法》** (2021-09-01 施行) | CN | in force | Classification and grading; important data; risk management |
| **《个人信息保护法》** (2021-11-01 施行) | CN | in force | Lawful basis, **sensitive** personal information, separate consent, rights, audit |
| **《医疗卫生机构网络安全管理办法》** (国卫规划发〔2022〕29号) | CN | in force | Sector network-security management: grading, self-inspection, data lifecycle |
| **《医疗卫生机构数据安全和个人信息保护管理办法（试行）》** (国卫规划发〔2026〕6号) | CN | 2026-02-14 印发即施行 | **The current sector data rule** — classification, lifecycle, prohibitions, PI protection |
| **GB/T 22239-2019**《网络安全等级保护基本要求》 | CN | in force | Graded-protection control baseline |
| **HIPAA** (US) | US | in force | Named in the manifest; **no clause mapping made here** |

## 2. 《网络数据安全管理条例》(国令第790号) — retrieved full text

Passed by the State Council's 40th executive meeting on 2024-08-30, signed
2024-09-24, promulgated 2024-09-30, **effective 2025-01-01**. Full text at
https://www.gov.cn/zhengce/content/202409/content_6977766.htm

**第九条 — graded protection is the floor, not the whole of it.** A network-data
processor must, **on the basis of** graded protection, add data-security
protection: establish management systems; adopt encryption, backup, access
control and authentication; protect data against tampering, destruction, leakage
and unauthorised use; and bear **主体责任**.

> Engineering consequence: 等保 compliance is the **starting point**. A system
> that passes grading but has no access control over its own clinical store has
> not met 第九条.

**第十二条 — providing or entrusting personal information or important data
requires a contract and a record.** The processor must agree purpose, method,
scope and security obligations with the recipient, **supervise** performance of
those obligations, and keep the **provision/entrustment records for at least
3 years**.

> Engineering consequence: any outbound data flow — to a research platform, a
> regional exchange, a vendor — needs a recorded agreement **and a ≥3-year
> record**, plus a mechanism to supervise the recipient. This is a dated,
> auditable obligation, not a policy aspiration.

**第二十二条 — separate consent for sensitive personal information.** Processing
**医疗健康** (medical and health), biometric, religious-belief, specific-identity,
financial-account or location-tracked sensitive personal information requires the
individual's **separate consent (单独同意)**; consent must not be obtained
through misleading, fraudulent or coercive means, must not exceed the consented
purpose/method/type/retention, and must be **re-obtained** when those change.

> Engineering consequence: consent is a **versioned, purpose-scoped object**. A
> consent record that cannot answer "what exactly did they consent to, under
> which version of which purpose" does not satisfy this article.

**第二十四条 — deletion and anonymisation.** Where information must be deleted
or is technically hard to delete, the processor must at minimum **stop all
processing other than storage and necessary security protection**.

> Engineering consequence: deletion has a defined **degraded state** the system
> must be able to reach. A hard-delete-only design will fail when deletion is
> technically impossible, which is exactly when it matters.

**第二十七条 — periodic compliance audit.** Processors must **regularly**, by
themselves or a professional body, audit their own compliance.

> Engineering consequence: audit is a **recurring scheduled capability** with
> evidence output, not an ad-hoc review.

**第二十八条 — scale threshold.** A processor handling **personal information
of 10 million or more people** must additionally comply with the provisions
addressed to handlers of important data (第三十条, 第三十二条).

> Engineering consequence: this is a **threshold the platform can cross without
> warning**. Usage volume monitoring must surface the crossing, because the
> obligations change at it.

**第六十二条(四) — important data defined**: data of a specific field, group,
region or reaching a certain precision and scale whose tampering, destruction,
leakage or unauthorised acquisition/use could directly harm national security,
economic operation, social stability, or **public health and safety**.

## 3. 《医疗卫生机构数据安全和个人信息保护管理办法（试行）》(国卫规划发〔2026〕6号)

Issued 2026-02-14 by 国家卫生健康委、公安部、国家互联网信息办公室、
国家中医药管理局、国家疾病预防控制局, in seven chapters, effective on
promulgation. **This is the most directly applicable instrument for this pack**
and the one a 2026-era implementation should start from.

> ⚠️ ASSUMPTION: the 文号, issuing bodies, date and chapter structure above are
> consistent across multiple independent secondary sources, but **the official
> 国家卫生健康委 text was not retrieved** from this environment. Article-level
> quotations below should be re-verified against the official notice before a
> compliance argument. The obligations are nevertheless recorded, because they
> are directly load-bearing for this pack.

Provisions that shape the system, as reported:

- **Classification into three tiers**: 核心数据 (core data), 重要数据
  (important data) and 一般数据 (general data). Where tiers are processed
  together and cannot be protected separately, **the highest tier's protection
  applies**.
- **Full lifecycle coverage**: 收集、存储、使用、加工、传输、提供、公开、删除 —
  the data-security lifecycle is explicitly seven-stage, and every stage carries
  obligations.
- **Escalating graded protection**: institutions storing and processing
  **重要数据** must meet **等保三级及以上**; those handling **核心数据** that are
  also critical information infrastructure must additionally apply CII
  protection requirements on top of graded protection.
- **Accountability structure**: the institution bears **主体责任**; a leadership
  group chaired by the principal must meet at least annually; the principal is
  the 第一责任人 and the deputy is the 直接责任人; the three-parties principle
  谁主管谁负责、谁运营谁负责、谁使用谁负责 applies.
- **Annual risk assessment** for institutions processing important data, with
  identification and reporting of important data to the health administration.
- **Prohibitions (十项禁止)**: no unlawful collection; no unlawful storage;
  no unlawful transmission (**不得通过微信、网盘、社交软件传输核心数据、重要数据和敏感数据**); no unlawful cross-border provision; no违规 use; no unauthorised processing by construction/operations staff; no provision without approval; no arbitrary disclosure; no disposal of equipment without data erasure; **no concealment of a data-security incident**.
- **AI constraint (第二十八条)**: where an institution uses **AI and other new
  technologies** to process patient records and other personal information, it
  **must ensure personal-information security**.

> That last provision is the direct regulatory hook for this repository's L3
> "agent-ready" objective in the healthcare domain: an AI feature over the
> clinical record is not an optional add-on but a regulated activity.

- **Entrusted processing (第二十七条)**: a prior personal-information protection
  impact assessment, plus an entrustment agreement and confidentiality
  agreement, with the entrusted party bound to the agreed scope.
- **Compliance audit (第二十六条)**: regular personal-information protection
  compliance audit, aligned to the personal-information compliance-audit
  measures.

## 4. 《医疗卫生机构网络安全管理办法》(国卫规划发〔2022〕29号)

Issued 2022 by 国家卫生健康委、国家中医药局、国家疾控局. Official text:
https://www.nhc.gov.cn/wjw/c100175/202208/1d611703ecd6458fb7b6b816d3feff3b.shtml

> ⚠️ Note: this URL returned **HTTP 412** (anti-bot precondition) to an automated
> request from this environment — the same situation as `iso.org` returning 403.
> The page exists; it simply refuses scripted clients. No clause-level quotation
> is made on the strength of an unretrieved page.

Provisions reported consistently from multiple secondary sources:

- Institutions determine their protection level by **function, service scope,
  service objects and data processed**, report for approval, then file, assess
  and remediate; **level 3 or 4 networks require an annual graded-protection
  assessment** by an accredited body.
- New networks must pass a **security test before going live**; new
  informatisation projects must budget **at least 5% of total project budget**
  for network security.
- **Annual self-inspection** including document verification, vulnerability
  scanning and penetration testing; **annual data-security risk assessment**.
- Data lifecycle management covering 收集、存储、传输、处理、使用、交换、销毁,
  with **domestic storage** and security assessment for any outbound transfer.

> Engineering consequence: the 5% budget and the pre-launch test are
> **project-governance obligations** that surface in procurement, not in code —
> but a platform that cannot produce the evidence (test reports, assessment
  reports, remediation records) cannot satisfy them either.

## 5. HIPAA (US)

Named in the manifest as a US privacy reference. The HHS page
(https://www.hhs.gov/hipaa/index.html) did not respond to an automated probe
from this environment, so **this pack makes no clause-level HIPAA claim**. For a
US deployment this is a blocking gap before `source-checked`.

## 6. What would make this pack `source-checked`

1. Retrieve the **official text of 国卫规划发〔2026〕6号** and quote it at article
   level — it is currently sourced from secondary summaries.
2. Retrieve the official text of **国卫规划发〔2022〕29号** and quote the
   assessment/testing cadence articles directly.
3. Map the assigned **等保 level** to GB/T 22239-2019 control clauses.
4. Retrieve **HIPAA** provisions and decide whether a US regional profile is in
   scope for this pack.
5. Retrieve the **national 重要数据目录** relevant to healthcare, once published
   in a form that binds medical institutions.
6. Confirm **ICD / ICD-11** versions and any national adaptation in use.

Until those close, `verification` stays `unverified` and this file is framing,
not compliance advice.
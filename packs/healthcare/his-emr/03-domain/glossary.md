# 03-domain / Glossary

> A term defined here has exactly one meaning across this pack; no synonyms are
> introduced later. `Source` records the basis: **[FHIR]** the HL7 FHIR resource
> model (cited), **[DICOM]** the DICOM standard, **[REG]** 《网络数据安全管理
> 条例》(国令第790号, cited), **[M2026]** 国卫规划发〔2026〕6号 (designation
> confirmed, text not retrieved), **[PACK]** this pack's definition,
> **[CONV]** an industry convention.

## 1. Identity

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **EMPI / enterprise master patient index** | 企事业主索引 / 主索引 | The institution's authoritative patient identity, resolving the many identifiers a patient presents with to one internal identity. | [PACK] |
| **MPI (matching)** | 主索引匹配 | The probabilistic process of deciding whether two identifier sets belong to the same person. | [CONV] |
| **Duplicate** | 重复档案 | Two or more EMPI records that in fact describe one person. | [PACK] |
| **Merge** | 合并 | Uniting two EMPI records under one identity, **preserving both prior identities** and recording what was merged. | [PACK] |
| **Unmerge** | 拆分 | Reversing a merge, restoring the pre-merge identities. `AGENTS.md` requires it to be **possible and audited**; a platform that merges but cannot unmerge has made an irreversible decision about a person. | [PACK] |
| **Reconciliation** | 主索引核对 | The human-reviewed process of resolving suspected duplicates and incorrect merges. | [CONV] |
| **Match confidence** | 匹配置信度 | The score and its uncertainty for a proposed match. Must be **visible**, not hidden behind a boolean. | [PACK] |
| **Demographics** | 人口学信息 | Identity attributes: name, date of birth, sex/gender, contact, identifiers. Not the clinical record. | [FHIR] Patient |

## 2. Encounter and care context

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Encounter** | 就诊 / 诊疗活动 | An interaction between a patient and a provider with a defined start and end. The context most clinical facts attach to. | [FHIR] Encounter |
| **Episode of care** | 诊疗阶段 | A clinically coherent grouping of one or more encounters. | [CONV] |
| **Admission** | 入院 | Creation of an inpatient encounter. | [CONV] |
| **Discharge** | 出院 | Conclusion of an encounter with a departure disposition. | [CONV] |
| **Visit** | 门诊就诊 | An outpatient encounter. | [CONV] |
| **Care context** | 诊疗场景 | Where the patient is and under whose care — ward, clinic, ICU, theatre. Decides which staff may access. | [PACK] |
| **ADT** | 入院/转科/出院登记 | Admission, Discharge, Transfer messaging — the HL7 message family for encounter lifecycle. | [PACK] |
| **Attending / responsible clinician** | 主治/主管医师 | The clinician currently responsible for the patient in a care context; the basis of much access control. | [PACK] |

## 3. Clinical data

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Clinical record** | 临床病历 | The record of what happened to the patient: observations, diagnoses, procedures, notes, orders, results. **Authoritative for clinical facts.** | [PACK] (separation law per `AGENTS.md`) |
| **Observation** | 观察/体征 | A measurement or simple assertion about a patient (vital sign, lab value, "smoker"). | [FHIR] Observation |
| **Condition** | 诊断/病症 | A clinical determination about the patient's condition. | [FHIR] Condition |
| **Procedure** | 诊疗操作 | Something done to the patient. | [FHIR] Procedure |
| **Medication request** | 医嘱 / 处方申请 | The instruction to dispense and administer a medication. | [FHIR] MedicationRequest |
| **Diagnostic report** | 诊断报告 | A clinician's interpretation of an investigation. | [FHIR] DiagnosticReport |
| **Document reference** | 文档引用 | A pointer to a clinical document (note, report, consent) held in its own repository. | [FHIR] DocumentReference |
| **Order** | 申请/医嘱 | An instruction to a service (lab, imaging, pharmacy). | [FHIR] (ServiceRequest / MedicationRequest family) |
| **CPOE** | 计算机化医嘱录入 | Clinician entry of orders directly into the system rather than on paper. | [CONV] |
| **Closed loop** | 闭环 | An order that reaches a result, a disposition, and a review — the measure that orders do not dangle. | [CONV] |
| **LIS / RIS / PACS** | 检验/放射/PACS | The laboratory, radiology and imaging archive systems respectively. | [CONV] |
| **DICOM boundary** | DICOM 边界 | Imaging crosses into the platform as DICOM objects rather than being decomposed into tables. `AGENTS.md` requires this. | [DICOM]; `AGENTS.md` |

## 4. Signed content and amendment

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Signed document** | 已签署文书 | A clinical document that has been authenticated by its author, and thereafter **never edited in place**. | [PACK] |
| **Addendum** | 补录 / 附录 | An attributed, time-stamped correction referencing the original document. The **only** permitted form of amendment to signed content (`AGENTS.md`). | [PACK] |
| **Retraction** | 作废 | Marking a document as never valid (e.g. filed on the wrong patient) — distinct from amendment; the original stays visible. | [PACK] |
| **Authorship vs. signature** | 署名与签署 | Authorship = who wrote it. Signature = attestation it is complete and correct. The pack keeps them **separate**, because conflating them makes "signed" a word with no defined referent. | [PACK] |
| **Note** | 病程记录 | The running clinical narrative for an encounter. | [CONV] |
| **Discharge summary** | 出院小结 | The document concluding an inpatient episode. | [CONV] |

## 5. Coding, terminology and the two truths

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Coding** | 编码 | Assigning diagnosis/procedure codes to what happened. | [CONV] |
| **Code system + version** | 编码体系与版本 | The terminology *and its release* a code was recorded against. `AGENTS.md` requires it on every coded fact. | [PACK] |
| **Versioned terminology service** | 版本化术语服务 | The component that maps codes across versions, auditable and re-runnable. `AGENTS.md` requires terminology mapping to be a **service**, not a lookup table baked in at implementation. | [PACK] |
| **Retired code** | 废止代码 | A code withdrawn upstream and still present in stored records — the mechanism of silent rot. | [PACK] |
| **Re-mapping** | 重新映射 | Repointing historical records at a successor code. A migration **with clinical risk**, not a lookup. | [PACK] |
| **DRG / DIP** | 疾病诊断相关分组 / 按病种分值付费 | Payment grouping. Consumes the coded record; never modifies it. | [CONV] |
| **Billing record** | 收费/结算记录 | The record of what is owed and why. **Authoritative for charges; separate from and never editing the clinical record** (`AGENTS.md`). | [PACK] |
| **Charge** | 收费项目 | A billable item derived from the encounter. | [CONV] |
| **Clinical/billing divergence** | 临床与收费差异 | Where the two records disagree. Expected; must be **explained**, never resolved by editing the clinical record. | [PACK] |

## 6. Privacy, consent and access

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Sensitive personal information** | 敏感个人信息 | Personal information whose processing carries elevated risk; **medical and health information (医疗健康) is explicitly listed**, along with biometric, religious-belief, specific-identity, financial-account and location data. | [REG] 第二十二条 |
| **Separate consent** | 单独同意 | Consent obtained **specifically and distinctly** for processing sensitive personal information, required in addition to general consent. | [REG] 第二十二条 |
| **Consent record** | 同意记录 | The versioned record of what was consented to, for which purpose, scope and retention. Must support re-consent when purpose/method/type/retention change. | [REG] 第二十二条; [PACK] for versioning |
| **Sensitive-care relationship** | 诊疗关系 | The patient–provider relationship that is the lawful basis for accessing the clinical record. | [PACK] |
| **Break-glass access** | 紧急访问 | Emergency access exceeding normal authorisation, **logged, justified, and reviewed afterwards**. Exceptional by definition; a rising rate means the normal path is broken. | [PACK] |
| **Purpose limitation** | 目的限定 | Data obtained for care must not be reused for research, marketing, training or analytics without a separate basis. | [REG] 第二十二条(4) |
| **Classification tier (CN)** | 数据分类分级 | **核心数据 / 重要数据 / 一般数据**. Where tiers cannot be protected separately, the **highest** tier's protection applies. | [M2026] |
| **Important data** | 重要数据 | Data whose tampering, destruction, leakage or unauthorised use could directly harm national security, economic operation, social stability, or **public health and safety**. | [REG] 第六十二条(四) |
| **Degraded-deletion state** | 降级删除态 | Where deletion is technically impossible, the minimum state: **stop all processing except storage and necessary security protection**. | [REG] 第二十四条 |
| **Entrustment (委托处理)** | 委托处理 | Processing by another party on the institution's behalf, requiring a prior impact assessment, an entrustment agreement and a confidentiality agreement, with records kept **≥3 years**. | [REG] 第十二条; [M2026] 第二十七条 |
| **Disclosure control** | 披露控制 | Limiting what is released to a requester — the control that stops an aggregate from re-identifying a patient. | [CONV] |

## 7. Audit, retention and AI

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Access audit** | 访问审计 | Who accessed which patient's data, when, and under what authority. The evidence base for every privacy obligation. | [PACK] |
| **Retention class** | 数据类别保存期限 | Retention defined **per data class**, not globally (`AGENTS.md`). | [PACK] |
| **Compliance audit (PI)** | 个人信息保护合规审计 | Regular audit of personal-information processing compliance, aligned to the applicable audit measures. | [M2026] 第二十六条; [REG] 第二十七条 |
| **Annual risk assessment** | 年度风险评估 | Yearly assessment of data-processing risk; required for institutions processing important data, with reporting. | [M2026]; [REG] 第三十三条 |
| **AI over the clinical record** | 病历人工智能处理 | Processing patient records and personal information with AI or other new technologies. The sector rule requires that **personal-information security be ensured** (第二十八条) — making this a **regulated activity**, not a feature. | [M2026] 第二十八条 |
| **Threshold crossing** | 阈值跨越 | Crossing **10 million** persons' personal information, above which 重要数据-handler obligations also apply. A scale the platform may reach without warning. | [REG] 第二十八条 |

## 8. Conventions

- **"must not"** marks a rule whose violation is a defect — the clinical record
  must not be edited to fit a code or a charge; signed content must not be
  edited in place; unmerge must not be impossible.
- **Bilingual terms**: Chinese is authoritative for the 病历 and 收费
  vocabulary and for regulatory terms; English for FHIR resource concepts.
- **No synonyms**: this pack distinguishes **merge** / **unmerge**, **amendment
  (addendum)** / **retraction**, **authentorship** / **signature**, and
  **clinical record** / **billing record**, and never uses one word for two of
  them.
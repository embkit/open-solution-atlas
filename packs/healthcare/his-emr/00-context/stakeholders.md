# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **Hospital / medical institution** (医疗卫生机构) | Operates the platform; holds **主体责任** for data security and personal information protection | Owner/operator; accountable to the health administration |
| **Hospital leadership group** (网络安全和信息化工作领导小组) | Chaired by the principal; the 第一责任人 / 直接责任人 structure | Governance authority over data and security |
| **Health information department** (信息科) | Builds and operates HIS/EMR | Operates the platform; no clinical authority |
| **Clinical departments** (临床科室) | Produce the clinical record; decide clinical content | Primary authors of the clinical record |
| **Medical records / medical affairs** (病案科) | Coding, DRG/DIP, completeness, archives | Owns the coded record; consumes both truths |
| **Pharmacy** (药剂科) | Dispensing, medication safety | Consumes and reports against CPOE orders |
| **Nursing** (护理部) | Nursing documentation, execution records | Author and executor of care records |
| **Finance / billing** (财务/收费处) | Charges, settlement, cost | Consumes the encounter; **never modifies the clinical record** |
| **Medical insurance function** (医保办) | 医保 settlement, compliance, interface | Consumer/assessor; separate record |
| **Laboratory (LIS)** | Specimen, analysis, results | Upstream result producer |
| **Radiology / imaging (RIS/PACS)** | Imaging acquisition, interpretation | Upstream producer; DICOM boundary |
| **Public health / CDC interface** (疾控/公卫) | Notifiable disease reporting, registries | Downstream statutory consumer |
| **Regional health information platform** (区域健康信息平台) | Cross-institution exchange | Exchange peer |
| **Health administration / regulator** (卫生健康行政部门) | Supervision, inspection, grading | External regulator; assigns 等保 level |
| **Cybersecurity / privacy function** | Access control, audit, retention, incident response | Constrains every capability |
| **Research / biobank** | Secondary use of clinical data | Downstream consumer under distinct rules |
| **Patients / public** | The data subject | Rights holder; the reason consent exists |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Registration clerk | 挂号员 | create registration, resolve EMPI, flag suspected duplicates |
| Physician / clinician | 医师 | author orders and notes, sign documents, add addenda |
| Nurse | 护士 | document care, record execution/vital signs |
| Pharmacist | 药师 | review and dispense, check interactions |
| Imaging radiologist | 影像诊断医师 | read studies, issue DiagnosticReport |
| Lab technologist | 检验技师 | produce and validate results |
| Medical record coder | 病案编码员 | assign ICD/procedure codes with code system + version |
| Medical affairs / DRG-DIP manager | 病案/医保管理人员 | completeness, coding audit, payment grouping |
| Billing clerk | 收费员 | charge, refund, reconcile — from the billing record only |
| Insurance specialist | 医保专员 | settlement, compliance checks, interface operation |
| Privacy officer / 数据安全负责人 | 数据安全负责人 | classification, important-data identification, risk assessment |
| Compliance auditor | 个人信息保护合规审计员 | periodic audit (per the sector rules) |
| HIM administrator | 系统管理员 | operate accounts and configuration; **no** clinical content authority |
| Security administrator | 安全管理员 | security configuration; separate from system administration |
| Break-glass approver | 紧急访问审批人 | authorise and review emergency access |
| Patient / proxy | 患者/代理人 | exercise information rights; consent |

### Non-human actors

| Actor | Note |
|---|---|
| **EMPI / MPI service** | patient identity resolution; **merge and unmerge, audited** (`AGENTS.md`) |
| **Clinical data store** | the record of clinical truth; append + addendum, no in-place edit of signed content |
| **Document/signature service** | authorship, signing, and addendum linkage |
| **Terminology service** | versioned ICD/LOINC/SNOMED mapping (`AGENTS.md`) |
| **Coding service** | assigns codes with system + version; feeds medical records |
| **Billing engine** | derives charges **from** the encounter; **writes only to the billing record** |
| **Order/compute engine (CPOE)** | orders, checks, results linkage |
| **DICOM/PACS gateway** | the imaging boundary |
| **LIS/RIS interfaces** | HL7 v2.x messaging in most deployments |
| **Consent & disclosure manager** | separate consent for sensitive information; disclosure control |
| **Audit trail service** | who accessed what, when, under what authority |
| **Data classification service** | 核心/重要/一般 classification driving differentiated protection |
| **AI/algorithm service** | L3 surface — governed by explicit constraint, never a free-text model over records |

## 3. External / upstream-downstream systems as actors

- **Regional health information platform** — cross-institution exchange.
- **National health information interconnect** — where one exists in the deployment.
- **Medical insurance (医保) settlement platform** — a **separate** record boundary.
- **Public health reporting systems** — statutory reporting.
- **Laboratory and imaging systems** — LIS/RIS/PACS.
- **Pharmacy automation** — dispensing and cabinets.
- **Blood bank, ICU devices, bedside monitors** — device-generated clinical data.
- **Payment gateway** — administrative fee collection.
- **Research platforms / biobanks** — secondary use, under distinct rules.
- **Identity provider / staff directory** — staff authentication.
- **Security monitoring / SIEM** — consumes audit and security telemetry.
- **Backup, archive and disaster recovery** — availability and evidentiary retention.

## 4. Actor goals (top)

- **Clinician**: record once, at the point of care, without the system
  interrupting care; and correct an earlier note without fear of destroying it.
- **Patient**: know who has looked at their record, and see a correction rather
  than a silent change.
- **Coding / medical affairs**: codes that reflect what happened, with the
  terminology version recorded so a future remap is possible.
- **Billing**: a settlement that stands up to audit — achieved by deriving from
  the encounter, never by editing it.
- **Privacy officer**: know where every copy of a record lives, who can reach
  it, and prove that access was authorised.
- **Information department**: keep the platform available during care, and keep
  the clinical and billing records genuinely separate under pressure.
- **Researcher**: access to de-identified or consented data without the
  research becoming an uncontrolled disclosure channel.
- **Regulator**: evidence that grading, retention, and important-data handling
  match what was declared.

> ⚠️ ASSUMPTION: the pack assumes the **clinical record is authoritative for
> clinical facts** and the **billing record is authoritative for charges**. Where
> the two conflict on a coverage question, the billing record decides what is
> owed and the clinical record decides what happened. This is the reading of
> `AGENTS.md`'s separation law, not a quoted rule.
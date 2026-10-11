# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **IT / platform team** (企业 IT) | Runs the engine, forms, integrations, upgrades | Owns/operates the platform |
| **Business process owner** (流程负责人) | Owns a process definition and its rules end to end | Requests changes; approves process versions |
| **Office administration / 办公室** | Governs 公文, 文号, templates, archive & retention | Content authority rather than platform authority |
| **HR / organization master** (人力资源) | Authoritative source for org structure, positions, employment state | Feeds org/reporting-line changes into participant resolution |
| **Finance** (财务) | Expense/reimbursement/payment rules; controls | Downstream consumer; defines rule-heavy flows |
| **Legal / compliance** (法务合规) | Contract templates, seal use, records obligations | Defines what must be retained and provable |
| **Internal audit** (内审) | Evidence of control execution | Read-only consumer of the audit trail |
| **Records / archive authority** (档案管理) | Retention schedule, 归档, disposal | Consumes completed records |
| **Information security** (信息安全) | Access control, grading compliance (等保), log integrity | Consumes telemetry; sets control requirements |
| **Line-of-business system owners** (业务系统负责人) | The systems a flow calls into | Upstream/downstream integration counterparties |
| **Regulators / external auditors** (监管与外部审计) | Statutory inspection | Read-only evidence; cannot touch the platform |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Applicant | 申请人 | author & submit a form, attach evidence, withdraw before approval |
| Assignee / approver | 办理人/审批人 | claim or receive a task, approve, reject, return for rework, comment |
| Countersigner | 会签人 | act jointly with peers in one countersign (会签) group |
| Process owner | 流程负责人 | define & version the process, set gateways, SLA and escalation, publish |
| Form designer | 表单设计者 | author form schema, validation, conditional visibility |
| Org / role administrator | 组织角色管理员 | maintain org units, positions, role-to-permission mappings |
| Delegate / agent | 代办人/代理人 | act on another participant's behalf within a bounded scope and time window |
| Transferrer / re-router | 转办人 | hand a task to another participant, with the transfer recorded |
| Office administrator | 公文管理员 | manage 文号 allocation, templates, 核稿/签发 routing, archive rules |
| Seal custodian | 印章管理员 | authorize and log seal/signature application; never self-approve its own use |
| Auditor | 审计员 | read-only access to instances, event trails and documents |
| Operations administrator | 运维管理员 | manage the engine, jobs, integrations; no business-rule authority |
| Process analyst / miner | 流程分析师 | export and analyse event logs (read-only) |

### Non-human actors

| Actor | Note |
|---|---|
| **Workflow engine** | creates instances, evaluates definitions, spawns tasks, drives timers |
| **Form engine** | resolves schema, applies validation and conditional visibility |
| **Rule/decision service** | evaluates approval conditions (candidate: DMN) |
| **Integration connector** | calls downstream systems; must be idempotent |
| **Job scheduler** | timers, reminders, escalation sweeps, retention jobs |
| **Identity provider (IAM)** | authenticates participants; supplies group/role claims |
| **Document/content repository** | stores documents & metadata (candidate interface: CMIS) |
| **Notification gateway** | todo/reminder/escalation delivery |
| **Signature / seal service** | applies and verifies electronic signatures & seals |

## 3. External / upstream-downstream systems as actors

- **HR / organization master** — employees, org tree, reporting lines, positions.
- **Identity provider** — authentication, group membership, role claims.
- **Finance systems** — expense/payment posting; often the "real" system of record.
- **ERP / procurement / asset systems** — call targets and data providers.
- **Document / content repository** — the store behind documents & records.
- **Electronic signature & seal service** — a regulated dependency; see `regulatory-landscape.md`.
- **Notification channels** — in-app todo, email, IM, SMS.
- **SIEM / log platform** — consumes audit & operational telemetry.
- **Archive / records system** — long-term retention, 归档, disposal.

## 4. Actor goals (top)

- **Applicant**: submit once, know exactly where it is and who is holding it,
  never lose an attachment.
- **Approver**: see the request and its evidence in one place, decide quickly,
  and never be asked to approve something outside their authority.
- **Process owner**: change a routing rule without a release, and see the
  effect on in-flight instances *before* it takes effect.
- **Office administrator**: issue a 公文 with a controlled 文号, and prove the
  sequence was never duplicated or skipped.
- **Auditor**: reconstruct any instance's full history — who did what, when,
  on what basis, and what the document looked like at each step.
- **Operations administrator**: keep the engine available and observable
  without being able to alter approval outcomes.
- **Security officer**: demonstrate that access to instances is granted by
  role and business scope, and that the audit trail cannot be edited by
  anyone, including administrators.

> ⚠️ ASSUMPTION: the pack assumes participants resolve **by role and business
> scope, never by hard-coded user name**, and that HR is the authoritative
> source for both. A deployment that hard-codes approvers into process
> definitions is treated as a defect, not a shortcut — this is a design
> position, not a citation.

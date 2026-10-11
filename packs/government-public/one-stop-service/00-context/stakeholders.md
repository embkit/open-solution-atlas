# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **政务服务管理机构 / 政务服务中心** (government service authority) | Owns the platform, the service catalogue, service standards | Operates and governs the platform |
| **Department / 政务部门** (service provider) | Delivers 事项, publishes 办事指南, decides outcomes | Upstream provider; each owns its own 事项 and decisions |
| **Departmental back-office** (机关内部审批) | Performs 受理/审查/决定 | Acts on behalf of the department, through the platform |
| **National / provincial platform authority** (国家/省级统筹) | Coordinates the integrated platform, standards, inter-region integration | Governs above the department |
| **Public security / 市场监管 / 税务 / 人社** (data-source authorities) | Hold the shared data the platform verifies against | Data sources via the `data-exchange` pack |
| **Identity & authentication authority** (统一身份认证) | Provides the national unified authentication service | **External platform dependency** — integrated, never re-implemented |
| **Electronic seal authority** (统一电子印章) | Issues seals from the national unified seal system | **External platform dependency** (`AGENTS.md`) |
| **E-licence service operator** (电子证照共享服务) | Runs the licence catalogue, sharing and mutual recognition | **External platform dependency**, GB/T 369xx interfaces |
| **Archives authority** (档案部门) | Receives electronic archives, sets archival requirements | Downstream recipient (第十二条) |
| **Payment / treasury** (支付与财政) | Administrative fee collection | Integration party |
| **Supervision / 监管** (supervision) | Pre-, in- and post-event supervision of the process | Consumes process data |
| **Personal information protection** (个人信息保护) | Lawful basis, minimisation, consent, deletion | Constrains every data call |
| **Public / press / researchers** | Oversight of the published guide and outcomes | Read-only consumers of the portal |
| **Legacy system vendors** (存量系统承建方) | Operate departmental systems that must integrate | Integration counterparties (国发〔2022〕5号) |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Applicant — natural person | 个人办事人 | search 事项, read 办事指南, authenticate, submit, track, sign, pay, rate |
| Applicant — legal representative / agent | 法定代表人 / 委托代理人 | act for an enterprise; requires authorised consent |
| 受理 staff | 受理人员 | perform 受理 or issue **一次性告知** |
| 审查 staff | 审查人员 | perform substantive review; may request 补正 |
| 决定 maker | 决定人员 | issue the decision (批准/不予批准/其他决定) |
| 出件 & archive staff | 出件归档人员 | issue the result, apply the seal, archive the electronic file |
| Service catalogue manager | 事项管理员 | create and maintain 事项 and publish 办事指南 |
| Guide editor | 办事指南编辑 | maintain 受理条件/办事材料/办理流程 — the published contract |
| Materials/forms designer | 表单与材料配置 | configure forms and the material list, flag data-shared fields |
| Fee administrator | 收费管理员 | configure 收费项目 where applicable |
| Feedback handler | 好差评处理人 | receive and respond to ratings and complaints |
| Supervisor | 监督人员 | read process and outcome data for 事前事中事后监管 |
| Auditor / inspector | 审计监督人员 | read-only evidence: decisions, seals, archives |
| Platform operator | 平台运维 | run the platform; **no** authority over approval outcomes |
| Personal information handler | 个人信息处理者 | responsible for lawful processing of applicant data |

### Non-human actors

| Actor | Note |
|---|---|
| **事项 catalogue service** | the root object; drives forms, materials, routing, deadlines (`AGENTS.md`) |
| **Guide publication service** | publishes the 办事指南 — the applicant-facing contract (第六条) |
| **Unified identity client** | calls the national authentication service; never a local re-implementation |
| **Shared-data verifier** | resolves applicant identity/attributes from the `data-exchange` pack, with **consent + audit** on every call (`AGENTS.md`) |
| **Form & pre-fill engine** | pre-fills from shared data and flags which fields must never be demanded (第七条) |
| **Approval/workflow engine** | 受理 → 审查 → 决定 → 出件 with 限时办结 timers |
| **一次性告知 composer** | assembles the complete list of missing items, once |
| **Payment client** | administrative fee settlement |
| **E-seal client** | applies a seal from the national unified system (第九条) |
| **E-licence client** | produces/consumes electronic licences via GB/T 36906 interfaces |
| **Archive client** | electronic filing per 第十二条 |
| **Rating & feedback service** | 好差评 collection and response |
| **Notification** | 办件进度/证照到期/政策资讯 reminders |
| **Supervision feed** | publishes process data to supervision systems |

## 3. External / upstream-downstream systems as actors

- **National integrated online platform** (全国一体化在线政务服务平台) — the
  system this platform integrates with, per 第四条 and 国发〔2022〕5号.
- **Unified identity service** (全国统一身份认证) — 一次认证、全网通办 (第五条).
- **Unified electronic seal system** (国家统一电子印章系统) — 第九条.
- **Electronic licence sharing service** (电子证照共享服务系统) — 第十条.
- **Government data sharing platform** — the `data-exchange` sibling pack; the
  source of everything 第七条 requires the platform to stop asking for.
- **Departmental business systems** — where 事项 processing actually lives.
- **Archive management system** — 第十二条.
- **Financial / treasury systems** — fee collection.
- **Supervision platforms** — 监管 consumers.
- **Authentication for staff** — internal government identity for back-office.
- **OFD / 版式 document services** — the standard layout document format
  referenced for 电子证照 (第十条) and electronic files.

## 4. Actor goals (top)

- **Applicant**: submit once, know exactly where it is, not be sent to another
  department, and not be asked for a document the government already has.
- **受理 staff**: a complete submission at the first pass, so 一次性告知 is the
  exception rather than the routine.
- **决定 maker**: see the full file including shared-data verification, and
  make the decision within 限时办结 without re-reading paper.
- **Service catalogue manager**: a 办事指南 that is **true**, because it is
  published and relied upon.
- **Department head**: 一件事 handled end to end without losing sight of which
  decision is legally theirs.
- **Platform operator**: integrate legacy departmental systems without
  re-implementing national services.
- **Personal information handler**: every cross-department call consented and
  auditable, and nothing collected twice.
- **Supervisor**: evidence that decisions were made on time, within authority,
  and on verified data.

> ⚠️ ASSUMPTION: the pack treats **一次认证、全网通办** as the identity model —
> the applicant authenticates once against the national unified service and the
> platform does not maintain an independent citizen identity. This follows
> 第五条; the boundary between "the platform's account" and "the national
> identity" is an L2 integration question, not specified here.
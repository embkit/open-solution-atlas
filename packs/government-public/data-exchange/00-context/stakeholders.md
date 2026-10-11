# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **Platform authority** (平台管理/主管部门) | Owns the platform, the catalog standard, and cross-department policy | Operates and governs the platform |
| **Data providers / 提供部门** | Register resources, publish metadata, keep data fresh and consistent, approve access | Upstream; "谁主管，谁提供，谁负责" (国发〔2016〕51号 第十三条) |
| **Data consumers / 使用部门** | Request access with a declared purpose, use it only for that purpose | Downstream; "谁经手，谁使用，谁管理，谁负责" (第十四条) |
| **Basic-resource库牵头部门** (人口/法人/地理/电子证照) | Build and maintain the basic information resource bases | Highest-value providers; basic fields are unconditionally shareable |
| **Catalog management office** (目录管理) | Compile and maintain the resource catalog, supervise its currency | Owns the root object |
| **Network & security authority** (网信/安全主管部门) | MLPS grading, security review, incident response | Sets control requirements; audits |
| **Privacy / personal information protection** (个人信息保护) | PIPL obligations, consent basis, erasure requests | Consumes classification; drives deletion handling |
| **Open-data office** (公共数据开放) | Public dataset publication, open-data portal content | Consumer of the same platform, different rules |
| **Service portal operators** (一网通办运营) | Citizen-facing services that consume shared data | Consumer via published interfaces (`AGENTS.md`) |
| **Legal / policy affairs** (法制/政策) | The legal basis for 不予共享 and conditional sharing | Supplies citations the platform must be able to store |
| **Internal audit / supervisory** (审计与监督) | Evidence of control execution and lawful use | Read-only consumer of grants, logs and lineage |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Resource registrar (provider side) | 资源登记人 | register a resource, declare share type, classification grade, owner |
| Resource owner | 资源负责人 | accountable for one resource's metadata, freshness and quality |
| Access requester | 访问申请人 | request access, state purpose, scope, duration |
| Access approver | 审批人 | approve/deny a conditional request; approves within delegated authority |
| Grant administrator | 授权管理员 | issue, amend, suspend and revoke grants |
| Catalog editor | 目录编辑 | maintain catalog entries and metadata within a department |
| Catalog supervisor | 目录审核/管理者 | review and publish entries; enforce catalog standards |
| Exchange channel operator | 交换运维 | operate 库表/文件/接口 channels, schedules, retries |
| Classification officer | 分类分级专员 | assign and review classification grades; drives masking policy |
| Masking/policy administrator | 脱敏策略管理员 | define desensitization rules per classification class |
| Usage auditor | 使用审计员 | read-only review of grants, usage logs and lineage |
| Open-data publisher | 开放数据发布者 | publish datasets to the open-data portal with DCAT metadata |
| Platform operator | 平台运维 | run the platform and its components; **no** business-rule authority |

### Non-human actors

| Actor | Note |
|---|---|
| **Catalog service** | the root object linking provider, resource, classification, consumers (`AGENTS.md`) |
| **Authorization engine** | decides whether a transfer may occur, given a grant |
| **Exchange channels** | 库表 / 文件 / 接口 adapters; each with its own failure semantics |
| **Scheduler** | batching, incremental exchange windows, retries |
| **Lineage recorder** | source → grant → consumer → delivered artefact |
| **Quality/reconciliation job** | provider-held vs. consumer-delivered comparison |
| **Masking engine** | applies classification-driven desensitization at exchange time |
| **Audit log store** | append-only record of grants, transfers and usage |
| **Identity provider** | authenticates departmental users; supplies org/department claims |
| **Seal/signature service** | where agreements or approval records are signed |

## 3. External / upstream-downstream systems as actors

- **Departmental business systems** — the true owners of the source data.
- **Basic information resource bases** — population, legal person, geospatial,
  electronic licence.
- **Identity provider / 政务统一身份认证** — authentication and org attributes.
- **一网通办 service portal** — a consumer via published interfaces.
- **Credit / social-governance systems** — consumers of regulated data.
- **公共数据开放门户** — the open-data front.
- **MLPS security management platform** — graded-protection reporting and
  monitoring.
- **保密 / 密码管理设施** — where classified data is in scope.
- **Supervisory and audit systems** — external recipients of evidence.

## 4. Actor goals (top)

- **Provider department**: publish once, keep control, and never be blamed for
  data a consumer misused — with responsibility boundaries that are visible
  rather than argued after the fact.
- **Consumer department**: get the data within a usable time, with a clear
  statement of what may be done with it — and *stop* re-collecting from citizens
  what the platform can supply.
- **Approver**: an unambiguous request with a declared purpose, so approval is
  a defensible act rather than a formality.
- **Catalog office**: a catalog that is current enough to be trusted as the
  map of what exists.
- **Auditor**: for any transfer, reconstruct which grant authorized it, what
  the consumer declared, and what actually moved.
- **Security authority**: demonstrate classification-driven enforcement, not
  classification-as-documentation.
- **Citizen (indirectly)**: not be asked to submit the same document twice.

> ⚠️ ASSUMPTION: the pack assumes responsibility boundaries follow the two
> 《办法》 principles quoted in the first table. Those principles are cited,
> but **how a platform encodes them** (e.g. whether a consumer's declared
> purpose is machine-checkable) is this pack's design problem and is not
> specified at L1.

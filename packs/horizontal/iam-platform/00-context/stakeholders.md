# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| Enterprise IT / IAM team (企业 IT) | Operates the IdP, policy and directories | Owns/operates the platform |
| HR / People operations (人力资源) | Source of truth for workforce identity & employment state | HRIS feeds joiner/mover/leaver events |
| Security operations (SOC 安全运营) | Monitors authentication/authorization anomalies, responds | Consumes audit/telemetry; feeds risk signals |
| Compliance / internal audit (合规审计) | Evidence of access control, reviews, SoD | Read-only evidence; campaign oversight |
| Business application owners (应用负责人) | Define the resources & roles they protect | Register apps, consume tokens, connect PEPs |
| SaaS / vendor management (SaaS 管理) | Onboard external apps, manage subscriptions | SCIM targets, federation partners |
| MDM / endpoint (终端管理) | Manages devices & certificates | Device identity signal; certificate issuance |
| Partners / B2B counterparties (合作方) | Federate identity for shared services | Trust relationship; attribute exchange |
| Regulators / auditors (监管与审计) | e.g. MLPS/GDPR/ISO auditors | Read-only evidence, reports |
| End users — employees (员工) | Access work resources | Authenticate, request/approve access |
| End users — customers (客户) | Access customer-facing services | Register, authenticate, manage consent |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| End user | 最终用户 | authenticate, self-manage authenticators, request access, review own access |
| Customer (CIAM) | 客户 | self-register, manage profile & consent, reset credentials |
| Approver / resource owner | 审批人/资源负责人 | approve/deny access requests, attest entitlement membership |
| Reviewer / certifier | 评审人 | perform access review/certification decisions for a campaign |
| IAM administrator | IAM 管理员 | manage identity model, apps, policy templates, provisioning connections |
| Policy author | 策略作者 | author/maintain authorization policies and role-permission mappings |
| Privileged operator | 特权操作员 | request & use JIT elevation for admin tasks within time window |
| Security analyst (SOC) | 安全分析师 | monitor auth/decision events, investigate anomalies, force revocation |
| Auditor | 审计员 | read-only access to audit trail, campaigns, decisions |
| Help-desk / service desk | 服务台 | identity proofing-assisted reset, unlock, MFA re-enrollment within policy |
| Service / workload account owner | 服务账号负责人 | own machine identities and their credential rotation policy |
| Provisioning connector (SCIM client) | 供给连接器 | non-human actor: push identities to downstream apps |
| Resource service (PEP) | 资源服务（策略执行点） | non-human actor: request decisions, enforce & report |

## 3. External / upstream-downstream systems as actors

- **HRIS** (Workday/SAP-SuccessFactors-class, referenced generically) —
  authoritative workforce master; emits joiner/mover/leaver events.
- **Directory services** (LDAP/AD-style) — enterprise directory; upstream or
  downstream depending on deployment archetype.
- **SaaS applications & internal applications** — RPs/SPs that delegate login
  and (for SaaS) consume SCIM provisioning.
- **Resource services / APIs / microservices** — PEPs calling the PDP.
- **SIEM / SOC** — consumes audit and authentication/decision telemetry.
- **MDM / PKI** — device posture and certificate/smart-card issuance.
- **Notification / SMS / email gateways** — MFA codes, security notifications,
  consent receipts.
- **Key management / HSM** — signing keys for tokens, SAML assertions, secrets.
- **ITSM / ticketing** — access requests can originate here; provisioning
  status flows back.

## 4. Actor goals (top)

- Employee: log in once, on any device, with a fast, phishing-resistant
  method; never lose access they legitimately need.
- Customer: sign up and log in frictionlessly; control their own data/consent.
- Approver: see a clear, risk-annotated request; approve once, confidently.
- Security analyst: detect and revoke compromised credentials/sessions fast;
  understand exactly what a subject could reach.
- Auditor: reconstruct any authentication or authorization decision exactly
  (who, what, when, on what basis, result).
- IAM administrator: change the identity/policy model without code changes,
  and prove the change is safe and reversible.
- Application owner: onboard an app in minutes; consume identity as a
  service, not re-implement it.

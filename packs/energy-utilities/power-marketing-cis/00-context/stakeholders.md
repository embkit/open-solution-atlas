# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **Marketing / customer service department** (营销/客户服务) | Owns the CIS and the customer lifecycle | Operates the platform |
| **Metering & data collection** (计量与采集) | Meter assets, collection, reading accuracy | Upstream of the bill |
| **Tariff / pricing function** (电价管理) | Interprets and applies regulated tariffs | Governs the tariff engine's inputs |
| **Billing & accounting** (电费核算) | Invoicing, adjustment, revenue | Consumes readings and tariff results |
| **95598 call centre** (95598 客服中心) | Hotline intake, case handling, dispatch | Highest-volume customer surface |
| **Field service operations** (现场运维) | Meter installation, reading, disconnect/reconnect execution | Executes work orders |
| **Distribution network operations** (配网运营) | Network state, outages, restoration | Upstream through the interface |
| **Payment / treasury channels** (收费渠道) | Collection, reconciliation | Downstream of billing |
| **Government / regulator supervision** (政府与监管) | Tariff approval, service standards, complaint handling | External authority |
| **Legal / compliance** | Disconnection rules, customer rights | Authority over guardrails |
| **Information security** | Customer data, metering data, 等保 compliance | Constrains every capability |
| **Revenue audit** (收入审计) | Evidence of correct billing and adjustments | Read-only consumer of the approval trail |
| **Large & industrial customers** (大客户) | Contracts, settlement, special arrangements | A customer class with different flows |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Customer | 客户 | the subject of the bill |
| Service-hall agent | 营业厅受理员 | onboarding, contract, payment intake |
| 95598 agent | 客服坐席 | case intake, status communication, dispatch request |
| Meter reader (field) | 抄表员 | collect readings; record exceptions |
| Metering technician | 计量技术员 | verify, calibrate, replace meters |
| Tariff administrator | 电价管理员 | publish tariff rule versions with effective dates |
| Billing operator | 电费核算员 | run cycles; inspect exceptions |
| Adjustment approver | 调整审批人 | approve billed corrections |
| Disconnection / reconnection operator | 停复电操作员 | execute only within guardrails |
| Payment reconciler | 收费对账员 | reconcile channels against ledger |
| Work-order dispatcher | 工单派发员 | route field work |
| Outage communicator | 停电信息发布员 | outage-linked customer notification |
| Auditor | 审计员 | read-only evidence of rules, approvals, reads |
| Platform administrator | 平台管理员 | run the platform; **no** tariff or approval authority |

### Non-human actors

| Actor | Note |
|---|---|
| **Meter data collection (AMR/AMI)** | automated reading ingestion |
| **Reading exception engine** | flags missing/out-of-range/history-inconsistent readings |
| **估抄 rule service** | applies estimation only by rule, and labels the result |
| **Tariff engine** | effective-dated, versioned, auditable regulated arithmetic |
| **Billing engine** | produces the bill with its rule version recorded |
| **Adjustment workflow** | approval-required money correction |
| **Payment & reconciliation service** | channels, allocation, mismatch detection |
| **95598 case service** | intake, linking to account/meter, dispatch |
| **Work-order service** | field dispatch and completion feedback |
| **Guardrail policy service** | evaluates disconnect eligibility, notice, timing |
| **Distribution interface adapter** | interface-only; no SCADA scope |
| **Audit & retention service** | the evidence trail rules, approvals and readings |

## 3. External / upstream-downstream systems as actors

- **Distribution automation / SCADA / OMS** — reached **only** through the
  interface (`AGENTS.md`).
- **AMI / smart meter network** — automated collection.
- **Payment channels** — banks, third-party, retail agents.
- **Government service platforms** — where the utility reports or publishes.
- **Outage communication channels** — SMS, app, portal.
- **Treasury / accounting** — revenue and settlement.
- **Regulatory reporting systems** — statutory reporting obligations.
- **SMS / notification gateways** — notices, including pre-disconnection.
- **Tax / e-invoicing services** — where the jurisdiction requires them.

## 4. Actor goals (top)

- **Customer**: a bill I can understand, that matches my meter, with any
  estimate clearly marked, and never a disconnection I should have been exempt
  from.
- **Metering**: readings collected accurately, exceptions surfaced, and an
  estimate never silently substituted.
- **Tariff administrator**: a rule version takes effect on its date, on every
  bill it should apply to, and on no bill it should not.
- **Billing**: a cycle that closes on time, with exceptions resolved by rule
  rather than by operator judgement.
- **95598**: the customer's real situation visible — meter, reading history,
  outages, payments — without a transfer.
- **Adjustment approver**: an approval that is quick enough to be used and
  complete enough to defend.
- **Field operator**: an instruction that carries its guardrails, so a
  disconnection the rules forbid cannot be executed.
- **Auditor**: "why is this bill this amount?" answered from the record, in one
  query.

> ⚠️ ASSUMPTION: the pack assumes the tariff engine is a **separate, governed**
> component rather than business logic inside the billing engine. This is the
  structural consequence of "regulated math" and is a design position, not a
  citation.
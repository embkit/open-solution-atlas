# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **Commercial / product management** (产品经营) | Defines offerings, pricing, eligibility, promotions | Owns the commercial catalog |
| **BSS engineering** (BSS 研发) | Builds and operates the commercial layer | Owns BSS domains |
| **OSS / network engineering** (OSS/网络) | Builds and operates fulfillment, assurance | Owns OSS domains; the BSS/OSS contract |
| **Network operations (NOC)** (网络运维) | Keeps the network real | Downstream of resource orders |
| **Revenue management** (收入管理) | Billing accuracy, invoicing, credit | Consumes charge events; owns reconciliation |
| **Finance / accounting** (财务) | Receivables, revenue recognition, inter-company | Downstream of invoices |
| **Collections** (欠费追缴) | Dunning, recovery, disconnection policy | Consumes receivables |
| **Customer care / retail** (客服与营业) | Orders, assurance, complaints | Consumes everything; the customer-facing edge |
| **Wholesale / interconnection** (国际化与批发) | Roaming, interconnect settlement | Consumer of settlement-facing data |
| **Regulators & numbering authorities** (监管机构与码号管理) | Numbering, portability, reporting obligations | External authority over resources and reporting |
| **Legal / privacy** (法务与隐私) | Subscriber data retention and erasure | Authority over retention & erasure |
| **Security** | Access, CDR confidentiality, fraud | Constrains every capability |
| **Retail partners / resellers** (渠道与代理商) | Sell through channels | Consumers of the commercial catalog |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Product / catalog manager | 产品目录管理员 | define commercial offerings, prices, eligibility; publish |
| Pricing & rating analyst | 定价分析师 | rating rules, charge plans, adjustments |
| Order orchestrator (system) | 订单编排器 | decompose and orchestrate orders across domains |
| Fallout / exception analyst | 异常处理员 | diagnose and re-drive failed decomposition steps |
| Provisioning / activation engineer | 激活工程师 | fulfill resource orders, report status |
| Number/code inventory administrator | 码号管理员 | allocate, reserve, release numbers and codes |
| Billing operator | 计费操作员 | run bill cycles, inspect and correct via new events |
| Collections agent | 催缴员 | dunning actions, payment allocation, disconnection workflows |
| Customer care agent | 客服代表 | order capture, assurance, complaint handling |
| Revenue assurance analyst | 收入保障分析师 | reconcile order ↔ charge ↔ inventory |
| Trouble-ticket / assurance operator | 故障单处理员 | handle network-facing issues; tie resource state to commercial |
| Interconnect settlement analyst | 结算管理员 | wholesale and roaming settlement |
| Subscriber / customer | 用户/客户 | the subject of everything commercial |
| Platform administrator | 平台管理员 | run the platforms; **no** authority over catalog or pricing |
| Privacy operator | 隐私运营 | enforce retention and erasure per data class |

### Non-human actors

| Actor | Note |
|---|---|
| **Commercial product catalog** | commercial offerings, prices, eligibility — the commercial truth |
| **Technical/resource catalog** | logical/physical resources, topology, activation paths |
| **Specification** (the join) | maps a commercial offering to its resource realisation and its verification |
| **Order orchestrator** | decomposes CO → SO → RO, manages partial failure |
| **Rating engine** | emits charge events — immutable once emitted |
| **Billing/invoicing engine** | cycles, aggregation, adjustments, credits |
| **Receivables & dunning engine** | ageing, allocation, recovery, disconnection |
| **Number/code inventory service** | allocation and release of a finite, regulated resource |
| **CRM / trouble-ticket system** | care and assurance, tied back to the service instance |
| **Fault management / assurance system** | resource-state signal feeding both OSS and billing |
| **Interconnect settlement system** | wholesale and roaming settlement |
| **Revenue assurance / reconciliation engine** | the two-way order↔charge↔inventory reconciliation |
| **Event bus** | the only sanctioned cross-domain coupling surface |

## 3. External / upstream-downstream systems as actors

- **Network elements / controllers** — the actual service realisation.
- **ITU-T and numbering-authority interfaces** — portability, number ranges.
- **Subscriber-facing channels** — retail, digital, partner.
- **Finance & accounting systems** — invoicing downstream.
- **Tax authorities** — invoice, tax, statistical reporting.
- **Partner/reseller systems** — channel integration.
- **Fraud management platform** — CDR and order-level fraud signal.
- **Data platform / warehouse** — heavy CDR analytics, downstream of this suite.
- **Identity / subscriber identity module** — authentication and authority.

## 4. Actor goals (top)

- **Product manager**: launch an offering without a network-engineering project
  per price change.
- **Order orchestrator operator**: know exactly where a chain broke, and
  re-drive it without duplicating a charge.
- **Revenue assurance**: detect usage with no customer, and activation with no
  charge.
- **Collections**: recover without disconnecting the wrong person, and without
  disputes that outnumber recoveries.
- **Customer care**: tell a customer what they actually have, in commercial
  terms, while the network is half-broken.
- **Business/Finance**: regenerate a historical invoice from its events.
- **Regulator-facing**: produce the required reports from the system's record
  rather than from a side spreadsheet.
- **OSS**: accept a resource order that means the same thing the commercial side
  meant.

> ⚠️ ASSUMPTION: the pack assumes the **event bus is the only sanctioned
> cross-domain coupling surface**. Direct domain-to-domain calls may exist but
  each one must be declared as a contract — this is a design position consistent
  with the ODA adoption, not a citation.
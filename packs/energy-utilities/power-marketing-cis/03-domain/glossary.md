# 03-domain / Glossary

> A term defined here has exactly one meaning across this pack; no synonyms are
> introduced later. `Source` records the basis: **[AGENTS]** this pack's
> `AGENTS.md` design position, **[PACK]** this pack's definition, **[CONV]** an
> industry convention with no single standard.

## 1. Customer and service objects

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Customer** | 客户 | The party supplied. The subject of rights, not the billing object. | [PACK] |
| **Account** | 账户 | The billing relationship through which charges are made and payments applied. | [CONV] |
| **Service point** | 供电点/计量点 | The physical point of supply. Distinct from the customer and from the account. | [PACK] |
| **Meter** | 电能表 | The measuring device at a service point. | [CONV] |
| **Customer class** | 客户类别 | Residential / industrial / commercial / agricultural / large — determines applicable tariff and rules. | [PACK] |

## 2. Metering and reading

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Reading** | 抄表 | The metered value at a point in time, with its collection method. | [CONV] |
| **Collection method** | 采集方式 | Automated (AMR/AMI) or field reading. Recorded with the reading. | [PACK] |
| **Reading exception** | 抄表异常 | A reading that is missing, out of range, or inconsistent with history. An exception to be resolved, not smoothed. | [AGENTS] |
| **估抄** | 估抄 | Estimation of an unobtainable reading, produced **only by a defined rule** and **labelled as an estimate** on the bill. | [AGENTS] |
| **Silent estimate (anti-pattern)** | 静默估抄 | An estimate substituted without a rule or without a visible label. Produces a bill that is arithmetically correct and factually unfounded — unfalsifiable by the customer, unprovable by the utility. | [AGENTS] |
| **Estimate reconciliation** | 估抄复核 | Correcting the estimate against the next actual reading, as a defined process. | [PACK] |
| **Cycle-straddling** | 跨期 | A billing period covering a tariff, meter or service change — must be split by evaluation, not approximated. | [PACK] |

## 3. Tariff — regulated math

`AGENTS.md`: versioned, auditable, effective-dated. These are the properties the
whole engine exists to provide.

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Tariff rule** | 电价规则 | A governed rule producing charges. A **governed input**, never a platform decision. | [AGENTS] |
| **Rule version** | 规则版本 | One dated revision of a tariff rule set, with an authority behind it. | [AGENTS] |
| **Effective-dating** | 生效日期 | The date a rule version applies from. A cycle straddling the date applies each version over its own period. | [AGENTS] |
| **Auditable arithmetic** | 可审计计算 | Every figure on a bill is re-derivable from readings, rule version and the rule itself. | [AGENTS] |
| **Tariff engine (separate component)** | 独立的电价引擎 | The engine is governed and separate from billing logic — because a tariff change hidden in a release is indistinguishable from a bug fix. | [PACK] |
| **Bill-stored rule version** | 账单记录规则版本 | The rule version a bill was computed under, recorded on the bill so it is reproducible years later. | [PACK] |
| **Regulated math (not pricing)** | 受管制计算（非定价） | The distinction from a commercial pricing engine: a commercial price is a decision the platform implements; a regulated tariff is arithmetic the platform must not improve upon. | [PACK] |

## 4. Billing, adjustment and money

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Bill / invoice** | 电费账单 | The customer-facing assertion of amount owed, with its rule version and reading basis. | [CONV] |
| **Adjustment** | 退补/调整 | A correction to a billed amount. An **approved, attributed act**, not an edit — the original bill remains. | [AGENTS] |
| **Approval workflow** | 审批流程 | The required act by a party with authority, recorded, before an adjustment takes effect. | [AGENTS] |
| **Recompute, never edit** | 重算不改写 | The shared rule across this repo's finance-facing packs: a financial assertion once made is not rewritten. | [PACK] |
| **Charge traceability** | 费用可追溯 | Every amount traces to a reading, through a rule version. | [AGENTS] |
| **Payment allocation** | 收费分摊 | Applying a payment to outstanding charges, by rule. | [CONV] |
| **Reconciliation** | 对账 | Money and energy reconciled to readings — the basis of resolvable disputes and passable audits. | [AGENTS] |

## 5. Disconnect / reconnect

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Disconnection** | 停电/销户停电 | Withdrawing supply under arrears or policy. A **regulated act**, not a collections switch. | [AGENTS] |
| **Guardrail** | 护栏 | A regulated condition that must hold before the act: eligibility, notice, timing. | [AGENTS] |
| **Eligibility class** | 禁停类别 | Regulated classes exempt from disconnection (e.g. medical need, vulnerable customers). **Enforced by the process**, not remembered by the operator. | [AGENTS]/[PACK] |
| **Notice period** | 通知期限 | The required advance notice before the act, through a defined channel. | [AGENTS] |
| **Restricted period** | 限制时段 | Periods when disconnection is not permitted (season, time of day). | [AGENTS] |
| **Operator memory (anti-pattern)** | 依赖操作员记忆（反模式） | Guardrails held as configuration someone may overlook. A guardrail not evaluated by the process is not a guardrail. | [PACK] |
| **Reconnection** | 复电 | Restoring supply after arrears clearance, also through a defined and auditable process. | [CONV] |

## 6. Service and the interface boundary

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **95598 case** | 95598 工单/案件 | A customer service request, linked to account, meter and outage context. | [CONV] |
| **Work order** | 现场工单 | A dispatch instruction for field work, with completion feedback. | [CONV] |
| **Distribution interface** | 配网接口 | The seam to distribution/OMS/SCADA systems. | [AGENTS] |
| **Interface-only (no SCADA scope)** | 仅接口（不含 SCADA） | The marketing/CIS system does not reach into real-time control. The two worlds have incompatible failure semantics. | [AGENTS] |
| **Seam** | 接缝 | The explicit, contractual boundary where commercial and operational meet. Vague seams are how control obligations migrate into a commercial system. | [PACK] |

## 7. Conventions

- **"must not"** marks a rule whose violation is a defect — an estimate must not
  be substituted without a rule and a visible label; a tariff rule must not be
  changed as part of a release; a disconnection must not proceed past an
  unmet guardrail; the interface must not extend into SCADA.
- **No synonyms**: this pack uses **reading** vs **estimate** as distinct
  objects with distinct labels; **tariff rule** (governed input) vs **bill
  computation** (what the platform does with it); **adjustment** (approved
  correction) vs **edit** (forbidden).
- The shared "recompute, never edit" rule appears across this repository:
  `telecom-bss` charge events, `omnichannel-commerce` money operations, and this
  pack's adjustments.
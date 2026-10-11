# 03-domain / Glossary

> A term defined here has exactly one meaning across this pack; no synonyms are
> introduced later. `Source` records the basis: **[ODA]** TM Forum Open Digital
> Architecture vocabulary (adopted, not claimed), **[TMF]** TMF Open API family
> (adopted, not claimed), **[AGENTS]** this pack's `AGENTS.md` design position,
> **[PACK]** this pack's definition, **[CONV]** an industry convention.

## 1. The two sides and the boundary

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **BSS** | 业务支撑系统 | The commercial layer: sell, price, bill, collect, support. The system of *what we sold and what we owe*. | [AGENTS] |
| **OSS** | 运营支撑系统 | The fulfillment and assurance layer: *is the service real right now*. | [AGENTS] |
| **BSS/OSS boundary** | BSS/OSS 边界 | The integration contract between them, expressed through the **specification**. Must never blur. | [AGENTS] |
| **Blurred boundary** | 边界模糊化 | Letting BSS speak network or OSS speak price. The failure that turns every later reconciliation into bespoke work. | [PACK] |

## 2. Catalogs and the specification

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Commercial product catalog** | 商业产品目录 | The commercial truth: what is offered, at what price, to whom, under what eligibility. | [AGENTS] |
| **Technical / resource catalog** | 技术与资源目录 | What must actually exist on the network to make an offering real. | [AGENTS] |
| **Specification** | 规格说明 | The object joining the two: what a commercial offering means **in resource terms, and how it is verified**. First-class, not a mapping table. | [AGENTS] |
| **Product offering** | 产品提供物 | A sellable combination of a commercial product and its specification. | [ODA]/[CONV] |
| **Price plan** | 资费计划 | Commercial pricing attached to an offering. A change here is **never** a network-facing change. | [PACK] |
| **Eligibility rule** | 资格规则 | Who may buy, and under what preconditions. | [CONV] |
| **Resource realisation** | 资源实现 | One of the N technical ways an offering becomes real. An offering may map to several. | [PACK] |
| **Duplication (anti-pattern)** | 目录重复 | Modelling the two catalogs as one. The pressure is constant, because keeping the specification current is real work; the cost appears when nothing goes wrong. | [PACK] |

## 3. Orders and orchestration

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Customer order (CO)** | 客户订单 | The commercial request from a customer, at offering level. | [CONV] |
| **Service order (SO)** | 业务订单 | The decomposition step naming the service instances involved. | [CONV] |
| **Resource order (RO)** | 资源订单 | The step naming the network resources to reserve or activate. | [CONV] |
| **Order decomposition** | 订单分解 | CO → SO → RO, per service, per domain. | [AGENTS] |
| **End-to-end traceability** | 端到端可追溯 | The chain is walkable in **both** directions: CO→RO to diagnose failure, invoice→CO to attribute charge, RO→inventory to confirm enactment. | [AGENTS] |
| **Orchestration** | 编排 | Driving a decomposed order across domains, handling partial failure. | [CONV] |
| **Partial failure** | 部分失败 | A decomposition that completed some domains and not others. Cannot be a simple rollback; a stateful problem. | [PACK] |
| **Fallout** | 异常落项 | An order step that stopped. The **diagnosable** unit, not a retry queue. | [PACK] |
| **Re-drive** | 重新驱动 | Restarting a fallout step without duplicating a charge or an activation. | [PACK] |
| **Order-to-activation** | 订单到激活 | The commercial commitment becoming network reality — tracked, not assumed. | [PACK] |

## 4. Money: rating, charges and billing

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Rating** | 计费 | Turning usage and recurring events into charge events. | [CONV] |
| **Charge event** | 计费事件 | One immutable assertion that money is owed. **Never edited after emission.** | [AGENTS] |
| **Recompute, not edit** | 重算不改写 | Correcting a charge is a new event and, if the customer was already told, an adjustment/credit — never an in-place change. | [AGENTS] |
| **Adjustment / credit** | 调整/冲抵 | A new financial event correcting a prior one. The prior event remains, and remains reproducible. | [PACK] |
| **Bill cycle** | 账期 | The period over which charges aggregate into an invoice. | [CONV] |
| **Invoice regeneration** | 发票重算 | Rebuilding a historical invoice from the events that produced it, with the pricing that applied. A hard requirement, not a nice property. | [PACK] |
| **Dunning** | 欠费催缴 | Ageing an unpaid invoice through contact, restriction and disconnection. | [CONV] |
| **Payment allocation** | 支付分摊 | Applying a payment to invoices, oldest-first or by policy. | [CONV] |
| **Collections** | 催收 | Recovery actions on aged receivables. | [CONV] |
| **Interconnect settlement** | 互联结算 | Wholesale and roaming settlement between operators. A distinct money stream from retail billing. | [CONV] |

## 5. Numbers, resources, reconciliation

| Term |  | Definition | Source |
|---|---|---|---|
| **Logical resource** | 逻辑资源 | The service-layer view of what must exist. | [ODA]/[PACK] |
| **Physical resource** | 物理资源 | The network-element-layer view of what exists. | [ODA]/[PACK] |
| **Activation path** | 激活路径 | The concrete sequence realising an offering, including failures and alternatives. | [PACK] |
| **Number / code inventory** | 码号资源库存 | The pool of numbers, codes and ranges — a finite, externally regulated resource. | [PACK] |
| **Allocation / release** | 分配/释放 | Assigning and recovering a number. Release is the scarce capability: unreleased numbers are silent leakage. | [PACK] |
| **Fragmentation** | 碎片化 | Allocated-but-unusable numbers caused by release policy failures. A waste metric. | [PACK] |
| **Portability** | 携号转网 | Moving a number between operators or services, under external rules. | [CONV] |
| **Two-way reconciliation** | 双向对账 | Charge events reconciled against **both** the order (attributable to what was bought) and the inventory (usage belongs to someone). | [AGENTS] |
| **One-way reconciliation** | 单向对账 | Order→invoice only. Produces systems that bill correctly and are **blind to leakage**. | [PACK] |
| **Usage with no customer** | 无主使用 | Consumption attributed to no subscriber. Only the inventory side detects it. | [PACK] |
| **Activation with no charge** | 无费激活 | A resource realised but not charged. Only the order side detects it. | [PACK] |

## 6. Care, assurance and privacy

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Trouble ticket** | 故障单 | A care-side issue, tied to a service instance and thus to the commercial relationship. | [CONV] |
| **Service instance** | 服务实例 | The realisation of one offering for one customer — the object care and rating both refer to. | [PACK] |
| **Assurance** | 保障 | The activity of keeping the service real: monitor, detect, fix, report back. | [CONV] |
| **Retention class** | 保留类别 | A declared retention and erasure policy attached to a data class (CDR, location/usage, customer master, invoice, care history), not a global setting. | [AGENTS] |
| **Generation window** | 生成/再生窗口 | The period over which a historical record (e.g. an invoice) can be regenerated from events. In tension with erasure; the mechanism resolving it is per-class policy. | [PACK] |
| **CDR (call data record)** | 通话详单 | High-volume, quasi-static usage records; the highest-volume retention class. | [CONV] |
| **Subscriber** | 用户 | The person the data is about — the privacy subject, distinct from the customer (the commercial counterparty). | [PACK] |

## 7. Conventions

- **"must not"** marks a rule whose violation is a defect — a charge event must
  not be edited; the two catalogs must not be merged into one; the BSS/OSS
  boundary must not blur; a released number must not remain allocated.
- **No synonyms**: this pack uses **charge event** for the immutable financial
  assertion and **invoice** for the aggregated artefact; **service order** and
  **resource order** for the two decomposition levels, never "order" alone;
  **logical/physical resource** for the technical catalog's two views.
- **Vocabulary adoption, not conformance.** ODA and TMF Open API names are
  adopted as this pack's vocabulary; nothing here claims conformity to a
  maturity level or an API version.
# 03-domain / Glossary

> A term defined here has exactly one meaning across this pack; no synonyms are
> introduced later. `Source` records the basis: **[AGENTS]** this pack's
> `AGENTS.md` design position, **[PACK]** this pack's definition, **[CONV]** an
> industry convention with no single standard, **[PCI]** PCI Security Standards
> (a designation, no clause cited).

## 1. Products and channels

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Product master / PIM** | 商品主数据 | The single description of what is sold, from which all channels read. | [PACK] |
| **Channel variant** | 渠道变体 | A channel-specific attribute or behaviour, expressed as **configuration** over the shared master. | [AGENTS] |
| **Channel fork (anti-pattern)** | 渠道分叉 | A channel that gains its own order, inventory or pricing model. Produces orders invisible to other channels. | [PACK] |
| **Marketplace** | 第三方平台 | An external marketplace the merchant sells through — another channel, with its own rules. | [CONV] |
| **Listing feed** | 刊登数据流 | The outbound projection of the master to a marketplace. | [CONV] |
| **SKU** | 最小存货单位 | The sellable unit of a product. | [CONV] |
| **Taxonomy** | 分类体系 | The category structure channels expose. Shared, not re-keyed. | [PACK] |

## 2. Pricing and promotions

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Price list** | 价格表 | Prices by product, channel, currency and audience. | [CONV] |
| **Promotion rule** | 促销规则 | A stated condition yielding a discount contribution, with eligibility. | [CONV] |
| **Stacking / exclusivity** | 叠加与互斥 | Whether promotions may combine. The articulation of this is the product. | [PACK] |
| **Pricing snapshot** | 价格快照 | The frozen result of evaluating promotions at capture: product prices, the rules applied, each rule's contribution, per-line totals, and the **ruleset version** that produced it. | [AGENTS] |
| **Recompute after capture (anti-pattern)** | 捕获后重算 | Re-evaluating promotions after the order was captured. A promotion the customer can lose while paying. | [AGENTS] |
| **Ruleset version** | 规则集版本 | The identifier of the promotion rule set used, recorded in the snapshot so a past order is reproducible. | [PACK] |
| **Displayed price** | 展示价 | What the customer was shown. A **record**, not a rendering. | [PACK] |

## 3. Cart, checkout, payment

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Cart** | 购物车 | The customer's priced intention, with a hold policy per line. | [CONV] |
| **Hold policy** | 库存占用策略 | Per-product: reserve at add-to-cart, at confirmation, at capture, or at fulfilment — with expiry for reversible holds. | [AGENTS] |
| **Reserve** | 预留 | A reversible deduction. Must expire or be released cleanly if never paid. | [PACK] |
| **Consume** | 消耗 | An irreversible deduction. The item is committed to a shipment. | [PACK] |
| **Checkout** | 结算 | Capture of shipping, identity and payment intent. | [CONV] |
| **PSP-hosted fields** | 托管支付字段 | Payment inputs rendered by the payment service provider, so card data never enters the platform's processes. The architecture that carries PCI scope exclusion. | [AGENTS] |
| **Tokenisation** | 令牌化 | Replacing card data with a reference usable for future operations. | [PCI] |
| **PCI scope exclusion** | 支付合规范围排除 | A claim that the core is out of card-data scope — must be **demonstrated**, evidenced, not asserted. | [AGENTS]/[PCI] |
| **Idempotency key** | 幂等键 | A platform-issued key on every money operation, so a retry collapses instead of double-charging. The PSP's own key is not sufficient — it does not cover a POS or marketplace path. | [AGENTS] |
| **Capture** | 请款 | Moving an authorised amount into a settled one. | [CONV] |
| **Refund** | 退款 | Its **own** money operation with its own idempotency key — not a negative charge. | [AGENTS]/[PACK] |
| **Reconciliation spec** | 对账规格 | A stated expectation of money and inventory movement, plus the procedure that **closes** the gap. A spec, not a report. | [AGENTS] |

## 4. Inventory

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Availability** | 可用库存 | What may be sold — a function of physical stock, holds, reservations and in-flight orders. | [PACK] |
| **Oversell** | 超卖 | Selling what is not there. `AGENTS.md`'s cardinal sin; the pack exists to prevent it across channels. | [AGENTS] |
| **Negative inventory** | 负库存 | The persistent state that results from an oversell that was not corrected. | [PACK] |
| **Inventory count / adjustment** | 盘点与调整 | The physical-vs-system reconciliation and its corrections. | [CONV] |
| **Cross-channel deduction** | 跨渠道扣减 | An order whose fulfilment crosses channels (buy online, pick up in store) must be deducted **once, in one place**. | [PACK] |
| **Reservation expiry** | 预留过期 | The automatic release of a reversible hold, so abandoned carts stop locking stock. | [PACK] |
| **Atomically scarce resource** | 原子性稀缺资源 | The reason inventory is hard: two customers, two channels, one last item, and the failure only reproduces under load. | [PACK] |

## 5. Order lifecycle

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Order** | 订单 | The stateful commitment object every downstream capability reads. | [CONV] |
| **Order state machine** | 订单状态机 | The definitions of states and transitions, exposed **identically at every channel**. A load-bearing decision, not a workflow. | [AGENTS] |
| **Paid but not accepted** | 已付未受理 | The money-taken, fulfilment-not-started state. Must be reachable and resolvable. | [PACK] |
| **Accepted but stock gone** | 已受理未到货 | A cancellation and possibly a refund owed. | [PACK] |
| **Cancellation** | 取消 | Terminating an order before fulfilment, with the refund path determined. | [PACK] |
| **Return / RMA** | 退货/退货授权 | Post-fulfilment reversal: authorise, receive, restock or scrap. | [CONV] |
| **Restock vs. scrap** | 重新入库 vs. 报废 | The two dispositions of a returned unit — the one that returns it to availability, the one that does not. | [PACK] |
| **Partial fulfilment** | 部分履约 | Some lines shipped, some cancelled, some refunded. The state where ambiguity causes customer-facing harm. | [PACK] |
| **Ambiguous state (anti-pattern)** | 模糊状态 | A state whose meaning differs by channel. Produces customer-facing consequences, not log lines. | [PACK] |

## 6. Post-sale reversals and the ledger

| Term | 中文 | Definition | Source |
|---|---|---|---|
| **Ledger** | 账本 | The append-only record of money and inventory movements, from which figures are derived and disputes resolved. | [PACK] |
| **Reversal** | 冲正 | Undoing a commitment through its own state transitions and money operations — never by mirroring the forward path. | [AGENTS]/[PACK] |
| **Inverse operation (anti-pattern)** | 逆操作（反模式） | Treating a refund as a negative charge or a return as a negative shipment. Fails when the target has moved on. | [PACK] |
| **Dispute / chargeback** | 拒付/争议 | A cardholder-initiated reversal, feeding the same ledger as a refund. | [CONV] |
| **Reconciliation gap** | 对账差异 | The difference between expected and actual. Its **age** is the metric: a gap that stays open is a defect, not a report. | [PACK] |
| **Idempotent retry** | 幂等重试 | Repeating an operation under the same key, collapsing to one effect. The normal path, not an error path. | [AGENTS] |

## 7. Conventions

- **"must not"** marks a rule whose violation is a defect — promotions must not
  recompute after capture; money operations must not proceed without a
  platform-issued key; a channel must not fork the core; a return must not be
  modelled as a negative shipment.
- **No synonyms**: this pack uses **reserve** vs **consume** as distinct
  inventory semantics, **snapshot** vs **recompute** as distinct pricing
  behaviours, and **refund** vs **chargeback** as distinct money operations.
- This pack shares its reproducibility discipline with its siblings:
  `growth-analytics` requires a versioned schema so history is interpretable,
  and `telecom-bss` requires immutable charge events. The same rule appears here
  as the pricing snapshot and the append-only ledger.
# 00-context / Stakeholders

## 1. Organizations

| Organization | Responsibility | System relationship |
|---|---|---|
| **Merchandising / product management** (商品) | Owns the catalog, prices, attach, lifecycle | Owns the product master |
| **Pricing & promotions** (价格与促销) | Owns promotional rules and eligibility | Author of the ruleset the snapshot evaluates |
| **Commerce platform engineering** (交易平台研发) | Builds cart, checkout, order, fulfilment | Owns the platform core |
| **Inventory / supply chain** (库存与供应链) | Owns physical stock, counts, replenishment | Upstream truth for the scarce resource |
| **Payments / treasury** (支付) | PSP relationships, capture, refunds, settlement | Consumes the payments abstraction |
| **Fraud & risk** (风控) | Risk scoring, chargebacks, blocking | Consumes order/checkout signals |
| **Customer service** (客服) | Order queries, cancellations, refunds, disputes | Highest-volume consumer of the state machine |
| **Logistics / fulfilment** (履约) | Routing, shipment, pickup, returns logistics | Downstream consumer of the order |
| **Channel owners** (渠道运营) | Own each surface: web, mini-program, POS, marketplace | Supply channel variants |
| **Finance / accounting** (财务) | Revenue recognition, settlement, reconciliation | Consumes money and inventory ledgers |
| **Security & compliance** (安全合规) | PCI scope, personal data, audit | Constrains every capability |
| **Marketplace operators** (平台方) | External marketplaces the merchant sells through | Another channel, with its own rules |
| **Card schemes / PSPs** (支付机构) | The money movement and the hosted fields | Integration counterparties |

## 2. Roles (application actors)

| Role (EN) | 中文 | Key permissions / tasks |
|---|---|---|
| Merchant / catalog manager | 商品运营 | define products, attributes, media, taxonomy |
| Pricing analyst | 定价分析 | set prices, define promotion rules and eligibility |
| Promotion operator | 促销运营 | schedule and tune campaigns; never edit a captured snapshot |
| Inventory planner | 库存计划 | set hold policies, replenish, write off, count |
| Checkout operator | 收银员 | complete in-store checkout on POS |
| Fulfilment operator | 履约操作员 | pick, pack, ship; route to store or carrier |
| Returns operator | 退货操作员 | authorise, receive, restock or scrap |
| Customer-service agent | 客服 | modify orders within policy; issue refunds under idempotency keys |
| Finance / settlement analyst | 结算分析 | run and close reconciliation |
| Fraud analyst | 风控分析 | review risk flags, release or block |
| Security / PCI compliance officer | 安全合规 | maintain scope evidence and assessment readiness |
| Channel manager | 渠道管理员 | configure channels as variants, not forks |
| Customer | 客户 | the buyer; the person whose money and promise are at stake |
| Store associate | 店员 | assists, sells, and returns in-store |

### Non-human actors

| Actor | Note |
|---|---|
| **Product master / PIM** | the shared catalog; channel attributes are variants of it |
| **Pricing & promotion engine** | evaluates rules into a **snapshot**; never recomputes after capture |
| **Cart & checkout service** | prices, reserves per policy, captures payment intent |
| **Payments abstraction** | PSP-hosted fields, tokenisation, idempotency keys |
| **Inventory service** | the scarce resource: reserve, consume, release, count |
| **Order orchestration** | drives fulfilment, reversals and post-sale |
| **Fulfilment & routing** | shipment, pickup, delivery, cross-channel routing |
| **Fraud / risk service** | scoring and blocking, consumed at checkout |
| **Reconciliation engine** | closes money and inventory gaps per spec |
| **Idempotency key service** | issues and deduplicates keys for money operations |
| **Channel adapters** | mini-program, POS, marketplace — variants of one core |
| **Event bus / ledger** | the append-only record money and inventory are derived from |

## 3. External / upstream-downstream systems as actors

- **PSPs and payment instruments** — hosted fields, authorisation, capture,
  refund. The boundary PCI scope is demonstrated against.
- **Carriers and logistics providers** — label, ship, track, return.
- **ERP / accounting** — inventory postings and revenue.
- **Marketplaces** — order feed, catalogue feed, inventory feed, settlement.
- **Tax engines** — price-inclusive vs. exclusive, by jurisdiction.
- **Identity / customer master** — who the buyer is across channels.
- **Loyalty / CRM** — downstream consumers of orders.
- **Card schemes / dispute networks** — chargebacks and representments.
- **Product data pools / GS1** — channel data exchange.
- **Warehouse management** — physical execution.

## 4. Actor goals (top)

- **Customer**: the price I was shown is the price I pay; the thing I bought
  exists; I can see my order from any channel; a return works.
- **Merchandising**: publish a product once and reach every channel, without
  re-keying attributes per channel.
- **Pricing**: change a promotion without altering what captured orders mean.
- **Inventory**: never sell what is not there, and never hold stock a customer
  abandoned.
- **Payments**: charge exactly once, refund exactly once, and know when the two
  ledgers disagree.
- **Customer service**: know what state an order is in, and undo it safely
  without a second refund.
- **Fraud**: block before capture, not after the shipment.
- **Security / PCI**: demonstrate, not assert, that card data never entered the
  core.
- **Channel owner**: add a channel as a configuration, not a fork.

> ⚠️ ASSUMPTION: the pack assumes **one product master shared by all channels**
  and **one inventory pool** — either can be per-channel in a real deployment,
  but the moment it is, "one number, one price, one promise" stops being the
  platform's property and becomes a policy the deployment must declare.
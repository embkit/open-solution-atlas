# Solution Taxonomy v1

The taxonomy is the shelf map of the library. It is deliberately organized by
**industry domain first, capability second** — because in regulated industries
the compliance environment and business semantics shape the entire solution.

Every pack maps to exactly one `domain` and one `subdomain`. Cross-cutting
systems that serve every industry live under `horizontal`.

Legend: 🟣 planned · 🟡 in progress (L1) · 🔵 L2 · 🟢 L3 agent-ready · ⚫ L4 proven

> Maturity here means **completeness**, not trustworthiness. Every pack also
> declares `provenance` and `verification` in its manifest; today all packs are
> `llm-drafted` / `unverified`. See
> [pack-standard §8](pack-standard.v1.md#8-provenance--verification).

## finance — 金融（暂缓征集：银行类系统）

> **Collection note (2026-10):** banking-specific subdomains — core banking,
> bank risk, bank regulatory reporting, bank payments/clearing — are
> **currently not collected** due to maintainer conflict-of-interest
> avoidance. The domain remains reserved for clearly non-bank systems:
> insurance core, generic third-party fintech tooling, open-source financial
> infrastructure patterns. Packs touching regulated finance require extra
> review and public-source-only citations.

| Subdomain | Example packs |
|---|---|
| Insurance 保险 | policy admin, claims, rating/reinsurance |
| Generic fintech infrastructure | non-bank payment abstraction, open-source ledger patterns, personal finance tooling |
| Wealth (non-bank distribution) | fund/wealth distribution platforms not operated by a deposit institution |

## energy-utilities — 能源电力

| Subdomain | Example packs |
|---|---|
| Grid operations 电网运行 | (IT-side) outage management, grid asset analytics |
| Power marketing 电力营销 | metering, billing/电费, customer service, 95598-class service hubs |
| Energy data 能源数据 | smart meter data platforms, consumption analytics |
| New energy 新能源 | distributed resource management, charging networks |

## government-public — 政务公共

| Subdomain | Example packs |
|---|---|
| Government services 政务服务 | 一网通办 / one-stop service portals, approval workflows, electronic licensing |
| Data exchange 数据共享 | government data sharing & exchange platforms, open data portals |
| Smart city 智慧城市 | city operation centers, urban governance grids |
| Public safety & justice 公共安全司法 | case management, command & dispatch |
| Taxation & public finance 税务财政 | tax administration, electronic invoices, budget management |

## telecom — 通信
BSS/OSS, billing & rating, customer/order management, network inventory.

## healthcare — 医疗健康
HIS/EMR, hospital operations, insurance settlement/医保, pharmacy, regional
health platforms, medical data governance.

## manufacturing — 制造工业
ERP, MES/MOM, supply chain & procurement, WMS/TMS logistics, quality
management, PLM, asset management/EAM.

| Subdomain | Example packs |
|---|---|
| MES/MOM 制造执行 | work orders, shop-floor execution, genealogy, quality, OEE (ISA-95) |
| Logistics/WMS 仓储物流 | WMS, TMS, inbound/outbound, automation boundary |
| Enterprise planning | ERP, procurement, cost (planned) |
| Quality & PLM | QMS, product lifecycle (planned) |

## retail-commerce — 零售电商
Commerce platforms, inventory & order management, POS/omnichannel, membership
& loyalty, marketplace operations.

| Subdomain | Example packs |
|---|---|
| Commerce platform | omnichannel commerce & order/fulfillment, PIM, promotion, loyalty |
| Marketplace 平台电商 | multi-merchant marketplace, merchant ops, settlement (planned) |
| Retail operations | store/POS operations, replenishment (planned) |

## data-ai — 数据与智能平台

| Subdomain | Example packs |
|---|---|
| BI & analytics | enterprise reporting, self-service BI, semantic layer, dashboards |
| Data platforms | data warehouse/lakehouse, data mid-platform/数据中台, data governance & catalog |
| Growth & marketing analytics | growth analysis, attribution, experimentation/A-B, CDP, marketing automation |
| AI/ML platforms | feature platforms, model lifecycle/MLOps, recommendation systems (planned) |

## horizontal — 通用能力（跨行业）

| Subdomain | Example packs |
|---|---|
| Identity & access | IAM/SSO, organization & permission models, customer IAM |
| Content & publishing | personal blog/CMS, headless CMS, documentation portals |
| Collaboration | OA, workflow/BPM, knowledge bases, document management |
| Service management | IT service desk/ITSM, helpdesk, CRM/contact-center ticketing |
| Finance ops | expense, invoicing, payroll (planned) |
| Platform engineering | multi-tenant SaaS base, notification, file, scheduling platforms |

## Contribution to the taxonomy

The taxonomy evolves by pull request. Adding a subdomain requires: (1) evidence
that at least two distinct real-world systems fit it, (2) a one-paragraph
boundary definition against neighboring subdomains, (3) at least one pack
proposal referencing it.

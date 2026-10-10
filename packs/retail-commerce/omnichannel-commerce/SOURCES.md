# SOURCES — Omnichannel Commerce & Order Platform

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Card-data handling / PCI scope (default: never touch card data) | PCI SSC | PCI DSS (v4.0) — https://www.pcisecuritystandards.org/ | Self-assessment type (e.g. SAQ A) and eligibility to confirm against the current DSS |
| Product identification (SKU/SPU, barcodes) | GS1 | GS1 Standards (GTIN, GLN) — https://www.gs1.org/standards | Mapping of SKU/SPU to GTIN to confirm |
| Currency codes (pricing, settlement) | ISO | ISO 4217 — https://www.iso.org/iso-4217-currency-codes.html | |
| Date/time (order timestamps, delivery promise) | ISO | ISO 8601 — https://www.iso.org/iso-8601-date-and-time-format.html | |
| CN e-commerce obligations (returns, disclosures) | — | 中华人民共和国电子商务法 (2019) | Article-level mapping (e.g. 7-day 无理由退货) to confirm |
| CN personal information (membership/consent) | — | 中华人民共和国个人信息保护法 (PIPL, 2021) | Article-level mapping to confirm |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Idempotent money/write operations over HTTP | IETF | RFC 9110 (HTTP Semantics: idempotency, status codes) — https://www.rfc-editor.org/rfc/rfc9110 | Idempotency-Key convention itself is not an RFC |
| Payment/PSP callback authenticity | IETF | RFC 7515 (JWS) / RFC 7519 (JWT) — https://www.rfc-editor.org/rfc/rfc7519 | Candidate mechanism; not yet specified |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Commerce core (cart/checkout/order) | Medusa | https://medusajs.com/ | Headless commerce reference |
| Commerce core | Saleor | https://saleor.io/ | |
| Commerce core | Spree Commerce | https://spreecommerce.org/ | |
| Commerce suite (PIM/OMS-ish) | Odoo | https://www.odoo.com/ | Broad ERP/commerce reference |
| Commerce platform | Adobe Commerce (Magento Open Source) | https://business.adobe.com/products/magento/magento-commerce.html | |
| Catalog search / faceting | Apache Solr | https://solr.apache.org/ | |
| Catalog search | Elasticsearch | https://www.elastic.co/ | |
| Event backbone (order ↔ inventory ↔ payment) | Apache Kafka | https://kafka.apache.org/ | Eventing pattern reference |
| Identity for member/membership | Keycloak | https://www.keycloak.org/ | Plugs into the IAM pack |
| Sibling pack (warehouse internals) | (internal) | packs/manufacturing/wms | Referenced, not owned here |

## 4. Uncited specifics to resolve

- **Inventory deduction semantics** — reservation saga vs. Redis-based deduction is an explicit open question (Open questions #1); "overselling is the cardinal sin" is a stated principle, not a sourced guarantee.
- **Order state machine** — states/transitions for order ↔ inventory ↔ payment are declared load-bearing (AGENTS.md) but not yet enumerated; no source.
- **Idempotency keys & reconciliation** — "every money operation needs idempotency keys and reconciliation specs" (AGENTS.md) has no key format, scope, or reconciliation window defined.
- **PCI scope demonstration** — "PSP-hosted fields, out of core" is asserted; the applicable SAQ category and eligibility criteria are not cited and must be confirmed against PCI DSS v4.0.
- **Promotion engine** — coupons, stacking, priority, and budget/quota rules have no rule DSL, precedence model, or source; simulation fidelity is an open question (#3).
- **Pricing snapshot** — "promotions evaluated on a pricing snapshot, never recomputed" is a design stance; the snapshot contents and freeze point are undefined.
- **Delivery promise** — warehouse/store routing and delivery-promise computation have no algorithm or SLA basis stated.
- **Membership / loyalty** — levels, points, rights mechanics are unordered and uncited; consent handling must align with PIPL (article-level mapping pending).
- **Settlement / reconciliation** — GMV and settlement figures are named but the reconciliation rules, cutoff, and discrepancy handling are unspecified.
- **Channel variants** — mini-program/POS treated as variants; the shared order-core boundary and any channel-specific constraints are not yet defined.
- **SKU/SPU ↔ GTIN** — product identification is modeled as SKU/SPU; the relationship to GS1 identifiers is not specified.

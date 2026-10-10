# Solution Pack Index

> ⚠️ **Trust status — read before using any pack.**
> Every pack here is **`provenance: llm-drafted`**, and **none has been
> validated in a real deployment**. Verification levels are **not** uniform:
> `iam-platform`, `itsm-helpdesk`, `personal-blog`, `wms`, `mes` and `tms`
> are `source-checked` (their
> load-bearing claims are traced to public sources in their `SOURCES.md`);
> all other packs are currently `unverified`. The maturity column below
> measures **completeness only** — it is not an endorsement. Always read a
> pack's `manifest.yaml` and
> `SOURCES.md` before trusting a specific claim. Two orthogonal axes apply
> (see [`../docs/pack-standard.v1.md` §8](../docs/pack-standard.v1.md)):
>
> - **Maturity** — how complete the pack is: 🟣 planned · 🟡 L1 brief ·
>   🔵 L2 blueprint · 🟢 L3 agent-ready · ⚫ L4 proven
> - **Verification** — how strong the external evidence is: ⛔ `unverified` ·
>   📑 `source-checked` · 👤 `practitioner-reviewed` · ✅ `field-proven`

All packs live here, organized by the taxonomy in
[`../docs/taxonomy.md`](../docs/taxonomy.md).

| Pack | Domain | Maturity | Verification | Summary |
|---|---|---|---|---|
| [personal-blog](./horizontal/personal-blog/) | horizontal / content-publishing | 🟢 L3 | 📑 source-checked | Personal blog & content publishing — agent-ready reference pack (static-public, Webmention, ownership-first) |
| [iam-platform](./horizontal/iam-platform/) | horizontal / identity-access | 🟢 L3 | 📑 source-checked | Enterprise IAM/SSO (identity foundation) — JML lifecycle, OIDC/OAuth2/SAML2/SCIM2, RBAC+ABAC PDP, MFA/WebAuthn, JIT privileged access, auditable decisions |
| [workflow-bpm](./horizontal/workflow-bpm/) | horizontal / collaboration | 🟡 L1 | ⛔ unverified | Workflow/BPM & OA approval platform — BPMN engine, forms, 会签/加签, 公文/电子签章 |
| [itsm-helpdesk](./horizontal/itsm-helpdesk/) | horizontal / service-management | 🔵 L2 | 📑 source-checked | IT service desk/ITSM — incident/problem/change, SLA clocks, CMDB, service catalog |
| [omnichannel-commerce](./retail-commerce/omnichannel-commerce/) | retail-commerce / commerce-platform | 🟡 L1 | ⛔ unverified | Omnichannel commerce — PIM, checkout, OMS, inventory, promotions, loyalty, after-sales |
| [mes](./manufacturing/mes/) | manufacturing / mes-mom | 🟢 L3 | 📑 source-checked | Manufacturing execution (ISA-95) — work orders, event-sourced execution, genealogy, quality gates, formula-exact OEE |
| [wms](./manufacturing/wms/) | manufacturing / logistics-wms | 🟢 L3 | 📑 source-checked | Warehouse management — event-sourced stock, atomic reservation/no-oversell, directed putaway, FIFO/FEFO waves, cycle count, task-based WCS boundary |
| [tms](./manufacturing/tms/) | manufacturing / logistics-wms | 🟢 L3 | 📑 source-checked | Transportation management — transport orders, carrier/rate, load planning, tender/dispatch, in-transit tracking, three-way freight settlement |
| [telecom-bss](./telecom/telecom-bss/) | telecom / bss-oss | 🟡 L1 | ⛔ unverified | Telecom BSS/OSS — customer & product catalog, order-to-activation orchestration, rating/billing, dunning, ticketing, number/resource inventory |
| [his-emr](./healthcare/his-emr/) | healthcare / his-emr | 🟡 L1 | ⛔ unverified | Hospital IS & EMR — EMPI, registration/outpatient/inpatient, CPOE & EMR, LIS/RIS boundary, pharmacy, insurance settlement |
| [mlops-platform](./data-ai/mlops-platform/) | data-ai / ml-platforms | 🟡 L1 | ⛔ unverified | MLOps & model lifecycle — feature store, experiment tracking, model registry, training pipelines, serving, drift monitoring, lineage |
| [one-stop-service](./government-public/one-stop-service/) | government-public / government-services | 🟡 L1 | ⛔ unverified | 政务一网通办 — service catalog, online application, cross-department verification, approval, e-license |
| [data-exchange](./government-public/data-exchange/) | government-public / data-exchange | 🟡 L1 | ⛔ unverified | 政务数据共享交换 — catalog & mounting, authorization/approval, exchange channels (table/file/API), lineage & quality, open-data portal |
| [power-marketing-cis](./energy-utilities/power-marketing-cis/) | energy-utilities / power-marketing | 🟡 L1 | ⛔ unverified | Power marketing/CIS — metering, regulated billing, payment, 业扩报装, 95598 service orders |
| [enterprise-bi](./data-ai/enterprise-bi/) | data-ai / bi-analytics | 🟡 L1 | ⛔ unverified | Enterprise BI — metric governance, semantic layer, dashboards, self-service, RLS |
| [growth-analytics](./data-ai/growth-analytics/) | data-ai / growth-marketing | 🟡 L1 | ⛔ unverified | Growth analytics & experimentation — event governance, funnels, A/B testing, cohorts, CDP activation |
| [lakehouse-platform](./data-ai/lakehouse-platform/) | data-ai / data-platform | 🟡 L1 | ⛔ unverified | Warehouse & lakehouse — ingestion, layered modeling, DQ, catalog/lineage, governance |

## Collection policy notes

- **Banking-specific systems (core banking, bank risk, bank regulatory
  reporting) are not currently collected** — maintainer conflict-of-interest
  avoidance. Generic non-bank fintech and insurance packs may be added later
  under a clearly scoped subdomain.
- Next promotions to L2/L3 are chosen by contributor availability; see
  [`../docs/roadmap.md`](../docs/roadmap.md).

To propose a new pack, open an issue using the pack proposal template and read
[`../CONTRIBUTING.md`](../CONTRIBUTING.md).

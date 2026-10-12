# SOURCES — Growth Analytics & Experimentation Platform

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Privacy regime — EU | EU | GDPR (EU 2016/679) — https://gdpr-info.eu/ | Consent, data-subject rights, residency |
| Privacy regime — CN | National People's Congress | 中华人民共和国个人信息保护法 (PIPL, 2021) | Article numbers to confirm; no URL cited |
| Advertising/messaging content rules — CN | National People's Congress | 中华人民共和国广告法 (Advertising Law) | Referenced for messaging content; article numbers to confirm |
| Consent signalling (optional) | IAB Europe | Transparency & Consent Framework (TCF) | Only if TCF interop is claimed; version/URL to confirm |
| Data quality vocabulary (event schemas) | — | No standard cited for the event schema registry | Schema-registry conventions to be sourced at L2 |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Event streaming transport | Apache (open source, not RFC) | See §3 | No RFC-level transport is mandated by the pack |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Product analytics & experiments | PostHog | https://posthog.com/ | Event capture, funnels, flags, A/B |
| Feature flags / experimentation | GrowthBook | https://www.growthbook.io/ | Experiment platform reference |
| Feature management / flags | Unleash | https://www.getunleash.io/ | |
| Feature flags | Flagsmith | https://flagsmith.com/ | |
| Flag/experimentation standard API | OpenFeature (CNCF) | https://openfeature.dev/ | Vendor-neutral flag API |
| Event collection / behavioral data platform | Snowplow | https://snowplow.io/ | Event tracking pipeline reference |
| Event streaming | Apache Kafka | https://kafka.apache.org/ | ODS ingestion |
| Analytics DB / OLAP | ClickHouse | https://clickhouse.com/ | Funnel/retention computation |
| Analytics DB / OLAP | Apache Druid | https://druid.apache.org/ | |
| Data integration / ELT | Airbyte | https://airbyte.io/ | Activation/destination sync |
| BI / self-service | Apache Superset | https://superset.apache.org/ | PM-facing reports |

## 4. Uncited specifics to resolve

Resolved at L2 (pack design; still need external sourcing for source-checked):

- **Event schema governance** — ADR-0001 settles declare-before-emit, validated
  on ingestion, reason-bearing quarantine, version on export. Still open: the
  **schema language and compatibility rules** (add/rename/remove semantics).
- **Identity merge / delete** — ADR-0002 settles recorded reversible merges with
  propagation, and the three-part deletion. Still open: **whether derived
  aggregates must be recomputed** after an erasure — undecided and in tension
  with experiment validity.
- **Experimentation statistics** — ADR-0003 settles assignment location and
  pre-declared decision rules. Still open: **a normative method text** for
  sample size, SRM, guardrails, holdouts and peeking discipline. The pack cites
  none; this is a precondition for verifiable experiment requirements.
- **Destinations** — ADR-0004 settles abstraction-not-ownership and
  reports-as-reconciliation-input. Still open: the **transfer property
  semantics** (CTL-04), which this pack added beyond the manifest's designations.
- **Segments** — BR-12 settles snapshot-not-live-view. Still open: the
  **re-resolution policy** for long-lived campaigns.

Still open:

- **Regulatory mapping** — PIPL and GDPR remain **designations only**. No
  clause-level mapping exists, per this repository's scope decision
  (see docs/citation-audit-2026-10.md §4).
- **Cross-border destination requirements** — recorded as a pack-added
  designation (CTL-04), not verified against any instrument.
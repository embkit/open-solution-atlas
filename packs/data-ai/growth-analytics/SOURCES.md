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

- **Statistical engine** — "sample size, power, SRM detection, guardrails, sequential vs. fixed-horizon tests" (open question #3) is named but no reference is given; a statistics source (e.g. a standard experiment-analysis method) must be cited at L2.
- **Attribution models** — "rule + multi-touch patterns" is listed with no defined model set (first/last touch, linear, position, Markov, etc.) and no source.
- **Identity graph** — "anonymous → login ID linking" and "merge/deletion" are asserted; merging/unmerging rules and reversibility have no cited basis (open question #1).
- **Consent enforcement** — "consent state enforced at collection and at activation" is stated with no defined enforcement point or consent-state model citation.
- **Aggregated reporting thresholds** — "aggregated reporting thresholds" for privacy is mentioned with no numeric minimum or source.
- **Retention / data residency** — behavioral-event retention and residency rules are asserted from PIPL/GDPR but no article-level mapping or period is given.
- **Experiment metrics / guardrails** — "LTV/RFM", "frequency caps and suppression" are named without definitions or sources.
- **Advertising-law constraint** — 广告法 content rules for messaging are referenced without article numbers; confirm the specific clauses.
- **L1 breadth** — no requirements/NFR/model chapters yet; no numeric targets or event-schema fields exist to audit. The items above are the load-bearing claims to source when L2 is written.

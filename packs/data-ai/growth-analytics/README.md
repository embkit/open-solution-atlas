# Growth Analytics & Experimentation Platform / 增长分析与实验平台

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
| Domain | data-ai / growth-marketing-analytics |
| Stack stance | Vendor-neutral |
| Regulatory context | PIPL/GDPR — behavioral events are personal-data adjacent; consent, minimal collection, data residency; 广告法 constraints on messaging content |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The data loop that product and growth teams actually run: event tracking
governance, user/device identity stitching, funnel/retention/cohort analysis,
attribution, A/B and multivariate experimentation with statistical rigor,
user segmentation, and message orchestration (push/in-app/email) with
experiment-consistent exposure logging. Designed B2C-scale and privacy-first
by default.

## In scope

- Tracking plan governance: event schema registry, naming conventions,
  SDK/server events, validation & quality monitoring, plan versioning
- Identity: anonymous → login ID linking, identity graph rules, user merge/
  deletion (privacy operations), consent state propagation
- Analytics: event streams → ODS → marts; funnels, retention curves,
  LTV/RFM, path analysis, attribution models (rule + multi-touch patterns)
- Experimentation: feature-flag delivery, traffic splitting, exposure
  logging, guardrail metrics, sample-size/power, sequential vs. fixed-horizon
  tests, SRM detection, holdouts
- Segmentation & activation: cohort builder → sync to messaging/CDP
  destinations with frequency caps and suppression
- Privacy: consent-aware collection, data minimization, deletion pipeline,
  aggregated reporting thresholds
- Self-service for PMs: metric builder, report templates, anomaly alerts

## Out of scope (explicitly)

- Marketing campaign buying/ad-network optimization (integrates, not owns)
- General warehouse platform (sibling pack)
- Recommendation model training (MLOps pack candidate; activation
  integrations included)

## Open questions

1. Identity graph depth: explicit vs. deterministic-only default.
2. Online feature serving excluded — boundary statement at L2.
3. Statistical engine: spec the tests and assumptions (variance, multiple
   comparisons) platform-agnostically.

## Maturity roadmap

- [x] L1 — Brief
- [ ] L2 — Blueprint
- [ ] L3 — Agent-ready
- [ ] L4 — Proven

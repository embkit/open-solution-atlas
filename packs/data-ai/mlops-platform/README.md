# MLOps & Model Lifecycle Platform / 机器学习工程与模型生命周期平台（MLOps）

| | |
|---|---|
| Maturity | 🟡 L1 — Brief (target L3) |
| Domain | data-ai / ml-platforms |
| Stack stance | Vendor-neutral |
| Regulatory context | NIST AI RMF; ISO/IEC 42001 (AI management system); explainability/audit expectations for models |

> ⚠️ **DRAFT — not field-verified.** Provenance: `llm-drafted` · Verification: `unverified`.
> Drafted with LLM assistance from public standards; **not** validated in a real
> deployment. Treat specific claims as hypotheses until [`SOURCES.md`](./SOURCES.md)
> and independent review raise the verification level (see standard §8).

## What this pack covers

The engineering backbone for the ML model lifecycle: shared feature
definitions, experiment tracking, model registration and versioning, training
pipeline orchestration, deployment and inference serving, runtime monitoring
with drift detection, and the lineage that makes a prediction reproducible and
auditable. The defining problem is **dual versioning and reproducibility** — a
served model must be pinned to the exact code, data, and feature versions it
was trained on, and its behavior must stay under monitoring after release.

## In scope

- Feature platform: feature registry/definitions, offline/online store,
  point-in-time correctness, training/serving consistency
- Experiment tracking: runs, parameters, metrics, artifacts, comparison
- Model registry: model versions, stages (candidate/production/archived),
  metadata, approval gates
- Training pipelines: orchestration, scheduled/triggered runs, environment and
  dependency capture, reproducibility manifests
- Deployment & serving: batch scoring and online inference, canary/shadow,
  rollback, endpoint governance
- Monitoring: prediction and feature drift, data quality, performance decay,
  alerting, feedback capture
- Governance: lineage, approval workflow, model cards/documentation, access
  control, audit trail
- Reproducibility: dataset/feature/model lineage from a served prediction back
  to source data and code

## Out of scope (explicitly)

- Data warehouse/lakehouse pipelines themselves (sibling data-platform packs;
  MLOps consumes governed data)
- BI dashboards and analytics (sibling enterprise-BI pack)
- Recommendation/search application logic (candidate downstream pack)
- GPU cluster provisioning / infrastructure-as-code (integration substrate)

## Open questions

1. Feature store: build the offline/online dual-store in core, or integrate an
   existing store behind an interface?
2. Serving architecture: core inference runtime vs. a boundary to operator
   serving stacks (KServe/Triton-class)?
3. Where the human-in-the-loop approval gate for production promotion lives.
4. Depth of automated drift response: alert-only vs. auto-retrain policy.

## Maturity roadmap

- [x] L1 — Brief
  - [x] Industry brief with sources (`00-context/industry-brief.md`)
  - [x] Regulatory landscape (`00-context/regulatory-landscape.md`)
  - [x] Stakeholder list (`00-context/stakeholders.md`)
  - [x] Level-1 capability map (`01-business/capability-map.md`)
  - [x] Glossary seeded (`03-domain/glossary.md`)
- [ ] L2 — Blueprint
  - [ ] Business processes / rules (`01-business/`) — promotion, rollback, retirement
  - [ ] Functional requirements (`02-requirements/`) with stable IDs
  - [ ] NFR catalog (`02-requirements/non-functional.md`)
  - [ ] Compliance controls traced to `regulatory-landscape.md`
  - [ ] Domain model incl. bounded contexts (`03-domain/domain-model.md`)
  - [ ] Architecture views + ≥3 ADRs (`04-architecture/`)
  - [ ] Logical data model + data dictionary (`05-data/`)
- [ ] L3 — Agent-ready
- [ ] L4 — Proven

### Blocking L2

1. **The binding's full component list** — `AGENTS.md` names code commit, data
   snapshot and feature definitions as the minimum, but a real deployment pins
   more (hyperparameters, framework version, seeds, environment). What the
   binding must contain is a versioned decision, not a default.
2. **Retention vs. erasure** — rollback and retraining require snapshots to be
   retained; data-protection obligations require training data to support
   erasure of a specific individual. Deliberately unresolved in this pack;
   needs a stated regeneration window.
3. **Risk-tier taxonomy** — the pack requires a declared tier field but does not
   define the tier set, per the scope decision that no framework clause was
   verified.

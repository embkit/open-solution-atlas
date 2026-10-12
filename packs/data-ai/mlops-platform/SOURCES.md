# SOURCES — MLOps & Model Lifecycle Platform

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| AI risk management process (govern, map, measure, manage) | NIST | AI RMF 1.0 (NIST AI 100-1) — https://www.nist.gov/itl/ai-risk-management-framework | |
| AI management system requirements | ISO/IEC | ISO/IEC 42001:2023 — https://www.iso.org/ | Catalogue page to confirm |
| AI regulatory obligations (EU) | EU | Regulation (EU) 2024/1689 (AI Act) — https://eur-lex.europa.eu/eli/reg/2024/1689/oj | Risk-class applicability to confirm |
| Model documentation (model cards) | arXiv | Model Cards for Model Reporting — https://arxiv.org/abs/1810.03993 | |
| Dataset documentation | arXiv | Datasheets for Datasets — https://arxiv.org/abs/1803.09010 | |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Model interchange format | ONNX | https://onnx.ai/ | Optional; framework-specific formats also valid |
| Lineage event model | OpenLineage | https://openlineage.io/ | Open specification; adoption at L2 to confirm |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Experiment tracking / model registry | MLflow | https://mlflow.org/ | |
| Feature store (offline/online, point-in-time) | Feast | https://feast.dev/ | |
| Training pipeline orchestration | Kubeflow | https://www.kubeflow.org/ | |
| Model serving | KServe | https://kserve.github.io/website/ | |
| Data quality / validation | Great Expectations | https://greatexpectations.io/ | |
| Data & pipeline versioning | DVC | https://dvc.org/ | |
| Drift detection | Evidently | https://www.evidentlyai.com/ | |
| Lineage collection | OpenLineage | https://openlineage.io/ | Framework-agnostic lineage |

## 4. Uncited specifics to resolve

Resolved at L2 (pack design; still need external sourcing for source-checked):

- **Dual versioning / the binding** — ADR-0001 settles unit + queryable, with
  the triple stated as the **minimum**. Still open: **which additional
  components a deployment pins** — a versioned decision the pack names but does
  not make.
- **The registry gate and approval** — ADR-0002 settles single gate, named-party
  approval and rollback-as-selection. Still open: the **approval evidence
  checklist** — BR-02 requires sliced evaluation, but the set of evidence types
  is not enumerated.
- **Lineage** — ADR-0003 settles query-with-an-answer and NFR-009's latency.
  Still open: the **sampling policy** for traces, unstated and in tension with
  privacy (security.md §3).
- **Sliced evaluation** — ADR-0004 settles declared predicates presented at
  approval. Still open: **which segments are declared** — pack design, and
  slicing on protected attributes raises questions the pack does not answer.
- **Point-in-time features** — ADR-0005 settles as-of semantics and
  replay-equals-training. Still open: **how non-point-in-time objects are
  modelled** — the pack notes they must be a different kind of object and does
  not define it.
- **Drift** — BR-07/BR-08 settle live-traffic plus four-kind classification.
  Still open: the **statistical method** for each kind — deliberately
  unspecified.
- **Retention** — BR-11 fixes that bindings are retained while servable; the
  **window** is in tension with erasure over training data and is deliberately
  unresolved.

Still open:

- **Governance frameworks** — NIST AI RMF and ISO/IEC 42001 are adopted as
  governance **shape and vocabulary**, per AGENTS.md. No clause was verified,
  no conformity is claimed, and the EU AI Act's risk-tier taxonomy was not
  reproduced. Establishing these is a precondition for source-checked.
- **Regulatory mapping** — the EU AI Act, GDPR and PIPL remain designations
  only, per this repository's scope decision
  (see docs/citation-audit-2026-10.md §4).
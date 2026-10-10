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

- **Dual versioning binding** — pinning a served model to an immutable combination of code commit + data snapshot + feature definitions is a design assertion; no standard mandates this exact binding/queryability.
- **Drift detection thresholds & response** — no numeric thresholds given; alert-only vs auto-retrain policy is an open question.
- **Production promotion approval gate** — where the human-in-the-loop gate lives is unresolved; no source.
- **"Lineage answers why this prediction end-to-end"** — aspirational depth; uniformity across pipelines unverified.
- **Feature store: build vs integrate** — open design choice, no source.
- **Serving runtime: in-core vs KServe/Triton boundary** — design choice, no source.
- **No measurable NFRs exist at L1** — any future latency/throughput/availability targets are unverified until stated with evidence.

# AGENTS.md — MLOps Platform (L1)

L1 brief. At L2: enforce dual versioning — every served model version is
pinned to an immutable combination of code commit, data snapshot, and feature
definitions, and that binding is queryable; training/serving feature skew is a
first-class correctness concern (point-in-time features); the model registry
is the single gate to production with an explicit approval record; drift
detection runs on live traffic and its results are auditable; lineage must
answer "why this prediction" end-to-end; governance follows NIST AI RMF and
ISO/IEC 42001 (risk management and documentation), never ad-hoc policy.

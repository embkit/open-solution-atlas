# AGENTS.md — Warehouse/Lakehouse (L1)

L1 brief. At L2: layers and contracts are the architecture (raw immutable →
conformed → marts); every load idempotent and reprocessable by partition;
data-quality gates distinguish blocking vs. warning; lineage covers
source-field → mart-column; classification/access enforced in the warehouse,
not only in BI; GDPR/PIPL deletion needs an operational pipeline; cloud vs.
信创 differences isolated to variants.

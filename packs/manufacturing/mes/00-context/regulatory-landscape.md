# 00 · Regulatory Landscape

MES sits under model standards and, in regulated industries, under binding
electronic-record regulations. Controls derived here are traced in
`02-requirements/compliance.md` as `CTL-*`.

| Regime | Type | Obligations affecting design |
|---|---|---|
| ISA-95 / IEC 62264 | model standard | level-3 scope, object models (personnel/equipment/material/process), integration vocabulary (B2MML) |
| ISO 9001:2015 cl. 8.5.2 | QMS standard | identification and traceability of output through production and service provision |
| IEC 62443 series | security standard | zones & conduits, network segmentation, least privilege for industrial control environments |
| FDA 21 CFR Part 11 | regulation (US; regulated variant) | e-records: audit trail, e-signatures, copy fidelity, retention |
| EU GMP Annex 11 (EudraLex Vol. 4) | regulation (EU; regulated variant) | computerized-system validation; data integrity (ALCOA+) |
| 网络安全法 / 数据安全法 / 等保2.0 (GB/T 22239-2019) | law & baseline (CN deployment) | classified protection, industrial data management, logging & audit |
| — ⚠️ 网络安全法 as amended 2025-10-28, effective **2026-01-01**, **renumbered** (see `docs/citation-audit-2026-10.md`). No article number is cited here. | — | — |

## Variant triggers (regulated variants must be declared before use)

- **Medical devices** (ISO 13485; FDA QMSR/21 CFR 820): device history record
  per serialized unit; signature at each record step.
- **Pharma / biotech** (EU GMP Annex 11; cGMP): electronic batch record with
  review-by-exception; ALCOA+ data integrity across the event store.
- **Automotive** (IATF 16949): PPAP-linked traceability, error-proofing
  (poka-yoke) records.

## What is explicitly *not* required here

- MES does not certify product quality (QMS/LIMS authority); it supplies the
  execution evidence.
- Safety instrumented systems (SIS) and machine interlocks are never
  implemented in this pack (ADR-0003).

# 00-context / Regulatory Landscape

> Obligations are stated at instrument level with the engineering consequence
> made explicit. Where clause mapping is unverified it is marked, per the pack
> standard §5. `verification: unverified` — nothing here is compliance advice.

## 1. Instruments in scope

| Instrument | Jurisdiction | What it governs here |
|---|---|---|
| **《中华人民共和国数据安全法》** (2021-09-01 施行) | CN | Data classification grading, risk management, and protection duties for data activities |
| **《中华人民共和国个人信息保护法》** (2021-11-01 施行) | CN | Personal-information handling rules; the right to deletion that the erasure pipeline must satisfy |
| **GB/T 22239-2019《网络安全等级保护基本要求》** | CN | Graded-protection (等保/MLPS 2.0) baseline controls |
| **GB/T 43697-2024《数据安全技术 数据分类分级规则》** | CN | How to classify and grade data — the method behind the platform's classification |
| **GDPR (EU 2016/679)** | EU | Where EU-resident personal data is in scope; erasure, purpose limitation, records of processing |

## 2. The classification obligation, and why it drives the architecture

The CN data-security framework requires data to be **classified and graded**,
and protection measures to be applied according to grade. GB/T 43697-2024 gives
the classification method; 《数据安全法》 supplies the obligation.

> Engineering consequence: classification is not a document. If classification
> is enforced only in the BI layer, every other consumer — a notebook, a data
> scientist, an export, a downstream platform — bypasses it. The pack therefore
> requires access control **in the platform** (`AGENTS.md`), with
> classification as metadata that drives policy rather than as a label.

> ⚠️ ASSUMPTION: the clause-level obligations of GB/T 43697-2024 and
> 《数据安全法》 are **not** mapped here. The standard is cited by designation
> with a verified public access point; the specific clauses and grading
> outcomes are to be confirmed at L2 when the compliance-controls chapter is
> written. Confirming them is a precondition for `source-checked`.

## 3. The deletion obligation, and why it is a pipeline

《个人信息保护法》 gives data subjects the right to deletion in defined
circumstances; GDPR Article 17 imposes the equivalent right with its own
conditions. Neither is satisfiable by a manual procedure across a lakehouse:

| Where the data lives | Deletion implication |
|---|---|
| Raw layer | append-only and immutable — a deletion cannot be an UPDATE |
| Conformed layer | reprocessed; a deleted subject must not reappear on reprocess |
| Marts / aggregates | derived values may embed personal data without a row to delete |
| Exports and extracts | copies outside the platform, often unmanaged |
| Logs, caches, snapshots | time-travel means the "deleted" row still exists in a snapshot |
| ML training sets | features derived from the subject may persist |

> Engineering consequence: **erasure is an operational pipeline** with
> propagation, verification and an auditable completion record (`AGENTS.md`).
> A platform whose only erasure answer is "ask the BI admin" does not meet the
> obligation, however good its access control is.

> ⚠️ ASSUMPTION: how erasure interacts with immutability is a genuine design
> tension and this pack does **not** resolve it at L1. Candidate approaches
> (crypto-shredding of keyed columns, logical tombstones honoured by every
> reader, snapshot expiry windows) are L2/L3 decisions requiring specific legal
> advice. Stating a preference now would be inventing certainty.

## 4. Records, reporting and retention

Statutory and internal reporting obligations mean platform outputs become
records with retention duties. Two consequences:

- **Reproducibility is a compliance property.** Retaining raw data and
  transforms makes "recompute the figure we reported last quarter" possible;
  discarding raw makes the reported number unreproducible.
- **Retention is a conflict, not a setting.** Longer retention aids
  reproducibility and audit; shorter retention aids minimisation and erasure.
> ⚠️ ASSUMPTION: this pack does not choose a retention policy. The conflict is
> resolved per dataset class by the governance council, with legal input.

## 5. Residency and transfer

Data-residency and cross-border transfer rules can constrain where the
platform runs and how data moves. This is increasingly jurisdiction-specific
and fast-moving, so the pack does not encode it; it requires residency to be a
declared platform property rather than an accident of a vendor's region list.

## 6. Regional profiles

| Profile | Distinguishing obligations |
|---|---|
| **CN** | 数据安全法 classification duties; 个人信息保护法 deletion; 等保 grading; GB/T 43697 method |
| **EU / GDPR** | erasure and purpose limitation; records of processing; transfer restrictions |
| **Other** | to be profiled if requested |

> The pack is not a compliance document. A deployment must have its obligations
> determined for its own jurisdictions and grading by a qualified party.

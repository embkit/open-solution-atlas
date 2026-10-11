# 00-context / Industry Brief — Enterprise Data Warehouse & Lakehouse Platform

## 1. What this system is in the value chain

An enterprise accumulates data in dozens of systems that were never designed to
agree with each other. A **data platform** is the horizontal system that turns
that pile into something answerable: it ingests, integrates, curates, and serves
data so that reports, analytics and machine learning describe *one* version of
the truth.

It sits between every producing system and every consuming system, and its
whole value is that neither side has to know about the other:

```
   source systems                    consumers
   -------------                     ---------
   OLTP databases / ERP / CRM        BI & dashboards
   application logs / events         data science / ML
   SaaS & partner feeds               operational apps
   IoT / OT telemetry                 regulatory & statutory reporting
   files / object storage             data products & APIs
            │                                ▲
            ▼                                │
   ┌────────────────────────────────────────┴─────────────────────┐
   │  DATA PLATFORM                                                │
   │                                                                │
   │  ingest ──▶ store (raw, immutable) ──▶ conform ──▶ serve      │
   │             │                            │                    │
   │             └── catalog & metadata ◀──────┘                    │
   │             └── quality gates ── lineage ── access control      │
   └────────────────────────────────────────────────────────────────┘
```

The pack models the platform as a **pipeline plus a contract layer**, not as a
product: the layers and the contracts between them are the architecture
(`AGENTS.md`).

## 2. The layering that this pack treats as architecture

| Layer | Contents | Mutability |
|---|---|---|
| **Raw / bronze** | as-landed source data, one record type per source | **immutable, append-only** — never edited |
| **Conformed / silver** | deduplicated, typed, validated, joined on canonical keys | reprocessable; corrected by reprocessing, never by UPDATE |
| **Marts / gold** | business-shaped aggregates for a specific consumption | derived from conformed; disposable and rebuildable |

> The layering is a **contract**, not a folder scheme. Raw is immutable so any
> downstream result can always be recomputed from scratch; conformed is the
> only place where source-specific mess is resolved once, for everyone. A
> platform that lets a mart read raw, or that allows in-place edits, has
> broken the property that makes reprocessing possible.

## 3. The central tension: storage has decoupled from compute

The category was reshaped by open table formats that put a transactional
table abstraction **on top of cheap object storage**:

| Format | Project | Notable design emphasis |
|---|---|---|
| **Apache Iceberg** | Apache Iceberg (https://iceberg.apache.org/) | open table format with hidden partitioning and partition evolution |
| **Delta Lake** | Delta Lake (https://delta.io/) | transaction log and optimistic concurrency on object storage |
| **Apache Hudi** | Apache Hudi (https://hudi.apache.org/) | record-level upserts and incremental processing |

> ⚠️ ASSUMPTION: this pack names these three because they are the widely
> adopted open table formats, **not** because the pack has compared them. A
> format choice is an architectural decision that belongs in a `variants/`
> overlay at L2/L3 with actual criteria — this pack stays neutral, which is
> what `stack_stance: stack-agnostic` commits to.

Consequences the platform must handle regardless of format choice:

- **Time travel and snapshots** — every read sees a consistent snapshot;
  reprocessing is "read the snapshot, write a new one", not "mutate rows".
- **Schema evolution** — adding, renaming and deleting columns must not break
  existing readers.
- **Small-file and compaction pressure** — streaming writes create many small
  files; compaction is a scheduled correctness-adjacent job, not housekeeping.
- **Partition reprocessing** — "reload last Tuesday" must be a first-class,
  safe operation (`AGENTS.md`).

## 4. Core flows (L1 view)

1. **Ingest** — pull/push from sources into raw; batch, micro-batch or
   streaming; at-least-once with idempotent landing.
2. **Profile & validate** — measure quality on arrival; route violations to
   blocking or warning paths (`AGENTS.md`: the two are *different*).
3. **Conform** — deduplicate, standardise types and keys, resolve slowly
   changing references.
4. **Curate & model** — build marts against declared contracts.
5. **Serve** — BI, ML feature extraction, APIs, exports; enforce access
   control at the platform, not only in the BI tool (`AGENTS.md`).
6. **Observe** — freshness, volume, quality, cost, lineage health.
7. **Govern** — classification, retention, and *operational* deletion
   (`AGENTS.md`: GDPR/PIPL erasure is a pipeline, not a ticket).

## 5. Why this system is unusually hard to get right

- **Downstream trust is the product.** One silent type coercion or late-arriving
  duplicate destroys confidence in every number built on it, and confidence is
  restored slower than it was lost.
- **"Reprocessable" is a design property, not a feature.** It requires
  immutable raw, deterministic transforms, and stable partition keys — all
  three decided at the start and expensive to retrofit.
- **Lineage that stops at the table is useless.** "Which dashboard number is
  wrong?" is answered only by lineage down to the **source field → mart
  column** level (`AGENTS.md`), which is field-level graph construction, not
  table-level documentation.
- **Access control belongs to the platform.** Classification enforced only in
  the BI layer means every other consumer bypasses it (`AGENTS.md`).
- **Deletion is an operational pipeline.** A legal right to erasure cannot be
  satisfied by a manual runbook across raw, conformed, marts, caches, exports,
  logs and ML training sets.
- **Cost is a correctness concern.** A recompute that is technically correct
  and financially ruinous will be skipped, which is how teams end up trusting
  stale data.

## 6. Defining quality metrics

L1 frames intent only; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Data freshness (per contract) | how current is each mart, and is it within contract |
| Pipeline success rate & MTTR | reliability of delivery and speed of repair |
| Quality-gate pass rate by dataset | whether upstream producers or the platform is the problem |
| Reprocess time for a full partition | whether recovery from a logic bug is bounded |
| Lineage coverage (% fields with resolved upstream) | whether "why is this number wrong" is answerable |
| Access-control coverage (% classified datasets with enforced policy) | whether governance is real or aspirational |
| Erasure SLA (request → verified removal) | whether deletion is an operational capability |
| Cost per served query / per job | whether scaling is sustainable |

## 7. Public materials anchoring the model

> The pack's own rule is *cite or qualify*. Everything below is either a
> verified public artefact or explicitly flagged.

**Verified (probed, HTTP 200):**

- **Apache Iceberg** — https://iceberg.apache.org/ — open table format spec.
- **Delta Lake** — https://delta.io/ — open table format spec.
- **Apache Hudi** — https://hudi.apache.org/ — open table format spec.
- **GB/T 43697-2024《数据安全技术 数据分类分级规则》** — the CN data
  classification and grading rules referenced by the manifest; standard
  accessible via the national standards information platform
  (https://openstd.samr.gov.cn/bzgk/gb/std_list?p.p2=GB/T%2043697).
  Clause-level mapping still to be confirmed.

**Statutes (designations stated, text to be quoted at L2):**

- **《中华人民共和国数据安全法》** (2021-09-01 施行) — data classification
  grading and risk-management obligations.
- **《中华人民共和国个人信息保护法》** (2021-11-01 施行) — personal
  information handling, including the right to deletion that the erasure
  pipeline must satisfy.
- **GB/T 22239-2019**《网络安全等级保护基本要求》 — graded-protection
  baseline.

**Named but deliberately not claimed:**

- **DAMA-DMBOK** — the industry reference model for data management
  (architecture, modelling, quality, governance functions). Named as
  vocabulary; a stable public URL could not be verified, so it is recorded
  here rather than as a manifest source.
- **ISO/IEC data-governance and data-quality standards** — designations such as
  ISO/IEC 38505-1 and ISO/IEC 25012 are widely referenced in this domain, but
  the catalog numbers **could not be verified from this environment** and an
  earlier draft of this manifest cited an ISO number that appears not to
  exist. They are therefore recorded as candidates in `SOURCES.md`, not as
  citations. Confirming them is a precondition for `source-checked`.

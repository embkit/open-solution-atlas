# Personal Blog & Content Publishing / 个人博客与内容发布系统

| | |
|---|---|
| Maturity | **L3 — Agent-ready** |
| Domain | horizontal / content-publishing |
| Stack stance | Vendor-neutral |
| Why this pack exists | The smallest end-to-end pack, used to validate the standard and tooling on a system everyone understands |

> **AI agents / coding agents**: start at [`AGENTS.md`](./AGENTS.md).
> **Humans**: read chapters in numeric order; begin with
> [`00-context/industry-brief.md`](./00-context/industry-brief.md).

> 📑 **SOURCE-CHECKED — not field-verified.** Provenance: `llm-drafted` ·
> Verification: `source-checked` (2026-10-09). Every load-bearing claim is
> traced to a public source in [`SOURCES.md`](./SOURCES.md); unsourced
> numeric targets and design choices are marked `⚠️ ASSUMPTION` at their
> point of use. **Not** validated in a real deployment — practitioner review
> pending (see standard §8).

## What this pack covers

A self-owned publishing system for an individual creator: write in a durable
authoring format (Markdown), organize posts with tags and drafts, publish with
SEO-friendly URLs and feeds (RSS/Atom, sitemap), moderate comments or
Webmentions, and own the content with full export. Covers both statically
generated and dynamically rendered deployment styles.

## In scope

- Authoring: Markdown-first editing, drafts, preview, media library
- Organization: taxonomy (tags/categories/series), archives, search
- Publishing: scheduled publish, canonical URLs, RSS/Atom feed, sitemap, SEO
  metadata, OpenGraph
- Interaction: comments moderation or Webmention/ActivityPub federation
- Ownership: full content export/backup, migration path to another engine
- Operations: analytics without intrusive tracking, spam defense, TLS

## Out of scope (explicitly)

- Multi-tenant SaaS blogging platforms (a separate pack candidate)
- Editorial workflow for large newsrooms (roles, embargoes, multi-reviewer)
- Real-time collaborative editing

## Why a "simple" system still deserves a full pack

It demonstrates the full L3 chain — requirements, domain model, API contracts,
acceptance criteria, delivery task map — in days rather than months, which makes
it the test bed for the pack standard itself.

## Open questions

1. ActivityPub federation: resolved as a future **variant**, not core — core
   stays Webmention/POSSE-shaped (ADR-0003).
2. Comments: resolved — Webmention default; native comments optional and
   off-by-default (FR-015, T-23). Third-party comment SaaS is excluded
   (privacy-by-default).

## Maturity roadmap

- [x] L1 — Brief
- [x] L2 — Blueprint
- [x] L3 — Agent-ready (18 FRs, 15 NFRs, 10 controls, 4 ADRs, 24 tracked tasks)
- [ ] L4 — Proven (next: minimal reference implementation + validation report)

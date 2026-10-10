# Roadmap

## Phase 0 — Foundation (now)

- [x] Project mission, positioning, license
- [x] Solution Pack Standard v1 draft
- [x] Taxonomy v1
- [x] Pack template + review checklist
- [x] First exemplar pack to validate the standard:
  - [x] `horizontal/personal-blog` — **L3 agent-ready** (proves L3 end-to-end:
    18 FRs / 15 NFRs / 10 controls / 4 ADRs / OpenAPI 3.1 / 24 tasks)
- [x] `manufacturing/mes` — **L2 blueprint** (21 FRs / 13 NFRs / 6 controls /
  4 ADRs; validates the standard on a complex OT-adjacent domain)
- [x] `manufacturing/wms` — **L3 agent-ready** (28 FRs / 14 NFRs / 7 controls /
  4 ADRs; C-01..31 contracts + OpenAPI 3.1 / AC-001..028 & AC-N01..14 /
  T-01..38 task map; event-sourced stock, reservation/no-oversell, WCS
  task boundary)
- [x] `horizontal/iam-platform` — **L2 blueprint** (24 FRs / 14 NFRs /
  7 controls / 4 ADRs; identity foundation: OIDC/OAuth2/SAML2/SCIM2,
  RBAC+ABAC PDP, JIT privileged access)
- [x] `manufacturing/tms` — **L1→L3** (22 FRs / 13 NFRs / 8 controls /
  5 ADRs / C-01..26 / AC-001..022 / T-01..32; dangerous-goods editions
  pinned: ADR 2025, IMDG 2024 A42-24, IATA DGR 67, JT/T 617 + GB 6944-2025)
- [x] `manufacturing/mes` — promoted **L2→L3** (24 contracts / AC-001..022 /
  SM-01..05 / F-01..06 data-flows / T-01..30)
- [x] Initial cross-industry L1 collection (12 briefs; see packs/README.md)
  — 17 packs total across 7 domains
- [x] **Trust & governance layer (dual-axis standard §8)** — manifest schema,
  `tools/validate-packs.py` + `tools/check-links.py`, GitHub Actions CI,
  practitioner-review issue template, verification decay rules
- [x] Pack template completed to full L3 skeleton (smoke-tested vs. validator)
- [x] Repo facade: root README trust section (EN/zh-CN), CHANGELOG
- [ ] Community review of the standard; publish v1.0

> **Collection scope note:** banking-specific systems are not collected for
> now (maintainer conflict-of-interest avoidance). See taxonomy finance note.

## Phase 1 — The core shelf

Target: ~12 packs across the taxonomy, at least 3 at L3.
**Status: shelf target met (17 packs, 5× L3: personal-blog, iam-platform,
wms, mes, tms; 1× L2: itsm-helpdesk); remaining work is depth, not breadth.**

- [x] Manufacturing: MES, WMS, TMS (all L3, source-checked)
- [x] Horizontal: IAM (L3), personal-blog (L3, source-checked)
- [x] Horizontal: ITSM service desk → L2 + source-checked
- [ ] Horizontal: workflow/BPM (OA) → L2 + source-checked
- [ ] Government: one-stop government service platform → L2
- [ ] Energy: power marketing/CIS → L2
- [ ] Retail: omnichannel commerce → L2
- [ ] Data & AI: enterprise BI, growth analytics, warehouse/lakehouse → L2

### Known debt (machine-visible)

11 L1 packs are 4-file briefs lacking the §6 L1 checklist chapters
(`00-context/*`, capability map, glossary) — `tools/validate-packs.py`
emits 55 warnings for them; each lands with that pack's promotion to L2.

`verification` distribution (checked 2026-10-09): **6 source-checked**
(iam-platform, itsm-helpdesk, personal-blog, wms, mes, tms), 11 unverified,
**0 practitioner-reviewed, 0 field-proven** — rungs 3–4 require named humans
and real deployments, which is a community/field task, not an editorial one.

## Phase 2 — Tooling & quality gates

- [x] `packlint` core: manifest schema validation, level checklists,
  verification-ladder honesty, banner rules, relative-link check, OpenAPI
  parseability, translation honesty (runs in CI)
- [x] `packlint` advanced: ID cross-reference checking (`tools/check-ids.py` —
  dangling FR/NFR/CTL/BR/AC/ADR/SM/CAP/BC references fail CI; cross-pack refs
  reported as info)
- [x] Tooling tests (`tests/`, pytest; runs in CI)
- [x] External citation-link probe (`check-links.py --check-external`, CI job)
- [ ] Glossary consistency checking (deferred: needs a term registry first)
- [ ] Agent consumption guides: Spec Kit, BMAD-METHOD, Kiro, Claude Code, Codex
- [x] Pack registry index — **searchable static site** (`tools/build-site.py`
  → GitHub Pages), with full-text search, facet filters and a link self-check
- [ ] Bilingual (EN/zh-CN) parity tracking — `translations: []` across the
  shelf today (key assets are bilingual; full translation is incremental)

## Phase 3 — Proven packs & ecosystem

- L4 packs with linked open-source reference implementations
- Variant overlays for major stacks (cloud-native, domestic/信创)
- Maintainer governance: domain maintainers per industry, review rotation
- Teaching track: how to read/write a pack, used with architecture curricula

## Non-goals (explicit)

- This repository does **not** ship production code frameworks (references to
  implementations are linked, not vendored).
- It does not favor or sell any cloud vendor.
- It does not host confidential or client-derived material — ever.

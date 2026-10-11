# Changelog

All notable changes to Open Solution Atlas. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions are repository-wide
releases (individual packs carry their own `version` in `manifest.yaml`).

## [Unreleased]

### Fixed — repository hygiene (outsider-facing)

- `.github/ISSUE_TEMPLATE/config.yml`: both `contact_links` pointed at
  `github.com/USERNAME/...` — placeholders left over from the pre-rename push.
  With `blank_issues_enabled: false`, an outsider had **no route at all** to ask
  a question. Links now point at `embkit/...`, GitHub Discussions, the online
  catalog, and the taxonomy.
- GitHub **Discussions** and **private vulnerability reporting** are now
  enabled. `SECURITY.md` already told readers to use the latter, but the
  feature was off — the file described a route that did not exist.
- `SECURITY.md` names a fallback contact ([@ebk-slm](https://github.com/ebk-slm))
  instead of "no named maintainers, contact route pending", which contradicted
  the very next sentence.
- `LICENSE` now holds the CC BY-SA 4.0 text and a new `LICENSE-MIT` holds the
  MIT text. The previous single `LICENSE` mixed both in prose, so GitHub
  detected `NOASSERTION` — no license badge, and license scanners could not
  classify the repository. READMEs updated to point at both files.
- `.github/CODEOWNERS` was 100% comments; it now routes every path to the
  actual maintainer, with `require_code_owner_reviews` explicitly off and the
  reason documented (single maintainer ⇒ code-owner approval would block
  everything, since an author cannot approve their own PR).
- `MAINTAINERS.md` records the repository maintainer that already existed in
  fact, and states plainly that the verification ladder above rung 2 is empty.
- `CONTRIBUTING.md` promised "one domain reviewer and one architecture
  reviewer" while branch protection required zero approvals. It now states the
  enforced rule (one approving review) and the intent separately.
- Repository **topics** (15) and the **homepage link** (`embkit.github.io/...`)
  were both empty, so the catalog had no entry point from the repo page and the
  project was undiscoverable in GitHub search.

### Added — searchable site
- `tools/build-site.py` — generates the static catalog into `_site/`: a
  searchable index page, a page per pack and per document, Mermaid rendering,
  and a **link self-check that fails the build** on any broken internal link.
- `tools/site-assets/{style.css,app.js}` — site theme and client-side search
  (Fuse.js over `search-index.json`) with facet filtering; progressive
  enhancement means the catalog is fully browsable without JavaScript.
- `.github/workflows/pages.yml` — publishes the site to GitHub Pages on every
  push to `main`.
- `tests/test_build_site.py` — 8 tests covering URL mapping, link rewriting,
  Markdown/Mermaid rendering and the internal-link checker.
- `requirements.txt`: `Markdown` added as a tool dependency.

### Added — trust & governance
- `docs/pack-standard.v1.md` §8: dual-axis trust model (`maturity` ×
  `verification`), verification ladder, no-self-escalation rules, decay
  mechanics (§8.3 rules 1–7).
- `schemas/pack-manifest.schema.json` — field-level manifest schema.
- `tools/validate-packs.py` — machine enforcement of level checklists,
  verification-ladder honesty, banner rules, ADR counts, OpenAPI parseability,
  translation honesty, staleness warning.
- `tools/check-links.py` — repository-wide relative Markdown link check, plus
  an informational `--check-external` probe over cited URLs.
- `tools/check-ids.py` — **ID cross-reference check** (the roadmap's
  "packlint advanced"): dangling FR/NFR/CTL/BR/AC/ADR/SM/CAP/BC references
  fail CI; cross-pack references are reported as info.
- `tests/` — pytest suite covering all three tools (`python -m pytest tests/`).
- `requirements.txt` / `requirements-dev.txt` — pinned tool dependencies.
- `.github/workflows/ci.yml` — validate + ID check + link check + tests on
  every PR; non-blocking external-link probe job.
- `.github/ISSUE_TEMPLATE/practitioner-review.yml` — the rung-3 review
  workflow feeding `verified_by`.
- `.gitignore`, `MAINTAINERS.md`, `.github/CODEOWNERS` (placeholder until real
  handles exist).

### Added — packs
- `manufacturing/wms` — L3, source-checked.
- `manufacturing/mes` — L2→L3, source-checked (ISO 22400-2 traced for OEE;
  genealogy honestly declared a pack extension over IEC 62264-3).
- `manufacturing/tms` — L1→L2→L3, source-checked (ADR 2025 / IMDG 2024
  A42-24 / IATA DGR 67 / JT-T 617 + GB 6944-2025 edition-pinned; EPCIS
  1.2 ISO/PAS citations corrected to GS1 EPCIS/CBV 2.0).
- `horizontal/iam-platform` — L2→**L3**, source-checked (SP 800-63-3→63-4,
  ISO 27002 clause corrections; contracts C-01..C-24, AC-001..025, T-01..T-32).
- `horizontal/itsm-helpdesk` — L1→**L2**, source-checked (ISO/IEC 20000-1:2018
  cl. 8.3/8.5/8.6.1-3/8.7 and ISO/IEC 27001:2022 Annex A controls pinned; ITIL 4
  kept as licensed vocabulary only; SM-S1..S3 state machines).
- `horizontal/personal-blog` — **source-checked** (LCP 2.5 s traced to Core
  Web Vitals; EN 301 549 pinned to v3.2.1; PIPL / 17 U.S.C. §512(c) / ICP
  国务院令第292号 art. 4 cited at instrument level).

### Fixed
- `packs/manufacturing/wms`: `BR-08b/c/d` were referenced but never defined —
  the scan control points now carry stable sub-IDs (`BR-08a`..`BR-08d`)
  (found by the new `check-ids.py`).
- `packs/manufacturing/mes`: process references corrected `P-01..P-06` →
  `BP-01..BP-06` to match the defined process headings.
- `packs/horizontal/itsm-helpdesk`: `SM-T1/SM-T2` renamed to `SM-S1/SM-S2`
  (collided with `manufacturing/tms`) and formally defined.
- 17 pack manifests declared `translations: [zh-CN]` with no translation
  file — corrected to `[]`; the validator now rejects the false claim.

### Changed
- `templates/pack-template` completed to a full L3 skeleton; smoke-tested
  against the validator.
- `docs/pack-standard.v1.md` §5: `translations` semantics pinned (a locale
  requires `README.<locale>.md` or `translations/<locale>/`); §3/§6: optional
  chapters declared; checklists bound to `tools/validate-packs.py`.
- Fixed 17 broken `pack-standard` links in pack `SOURCES.md` files
  (one directory short).

## [0.1.0] — 2026-10-08

Initial repository state: pack standard draft, taxonomy, roadmap, 17-pack
shelf (1× L3, 1× L2, 15× L1 at that point), contribution guides, issue/PR
templates, dual license (CC BY-SA 4.0 content / MIT code).

# Changelog

All notable changes to Open Solution Atlas. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions are repository-wide
releases (individual packs carry their own `version` in `manifest.yaml`).

## [0.3.0] — 2026-10-14

Twelve packs contributed rules, requirements and NFRs to a machine-readable
index for the first time; six packs gained the integrity constraints they had
been missing; each pack gained four prompts assembled from its own decisions and
a first hand-written demo; and the site's visual layer was rebuilt as technical
drawing after review found it matched the commonest tells of a generated page.
`validate-packs.py` still reports 0 errors and 0 warnings, `check-ids.py`
reports 0 errors with 1821 distinct ID definitions, and 139 tests pass.

### Added — the packs became machine-readable

- `tools/pack_index.py` — extracts every pack's capabilities, rules,
  requirements, NFRs, controls, ADRs, integrity constraints and bounded
  contexts into a typed index, emitted as `_site/data/pack-index.json`. It
  parses **all** conventions the corpus uses — `### BR-01 — Proposition`,
  `**BR-01 Name**` under a `## Topic`, and a five-column table; heading-anchored
  EARS and a single inline `- **FR-001** WHEN …` bullet.
- **Extraction quality is reported per section** — structured / prose-only /
  absent — because a parser that returns `[]` for a shape it does not know
  would report *zero rules* for a pack that has fifteen, and a page built on
  that would state a falsehood about the corpus. Six packs had no integrity
  constraint table; that is now a dashed badge rather than an empty table.
- `url_for` delegates to `pack_index.doc_url`, so the URL mapping lives in
  exactly one place; a test asserts the two agree on the corpus.
- 125 capabilities, 234 rules, 394 requirements, 221 NFRs, 84 controls, 86 ADRs.

### Added — the structured spec panel

- Every pack overview page carries a radio-based **document view / structured
  view** toggle, server-rendered so it is complete with JavaScript disabled.
- Eight section groups with their real counts, trace chips linking to the row
  each identifier names, and a store-enforcement badge on constraints the data
  model claims are enforced in the store.
- The store flag is **derived, not asserted**: it is parsed out of the sentence
  in each `05-data/logical-data-model.md` that names which numbered constraints
  are store-enforced — flattened first, because the sentence is routinely wrapped
  mid-phrase at the source's line width, and a regex over the raw text never
  sees the phrase it is looking for.

### Added — prompt bundles, 256 files

- `tools/prompts.py` assembles four prompts per pack from that pack's own
  records: **implement** (capabilities, rule propositions, decisions taken,
  store-enforced constraints, measurable targets with formulas), **adr** (one
  decision, what depends on it, **and what was ruled out**), **test** (one rule,
  the requirements that enforce it, the targets that measure it), and
  **context** (the pack's chapters, for a model that needs the source).
- The `adr` prompt's rejected-options section is the part that matters: 78 of
  the 86 ADRs across the corpus yield the alternatives they rejected, and a
  prompt carrying only the winner lets a model re-derive the loser.
- Every prompt states the repository's honesty conditions — `verification:
  unverified`, no claimed conformance, `(A)` markers are policy rather than
  measurement, recorded gaps stay gaps. A prompt that omits them gets an
  implementation that invents them.
- Copy buttons are an enhancement: every prompt is a real `.md` file, so with
  JavaScript disabled the action is a link that opens and a textarea that
  selects.

### Added — the first interactive demo

- `packs/horizontal/workflow-bpm/10-demo/` — an approval-vocabulary lab,
  hand-written and self-contained (inline styles, inline script, no external
  asset and no network request), because a demo that depends on the site's
  stylesheet cannot be opened on its own.
- It fails correctly: 会签 without a declared completion policy records
  `FR-013`, `NFR-007` and constraint 7 as sev-1, and the two completion policies
  the pack leaves open are presented as decisions the user must make rather than
  as defaults.
- **Drift is guarded.** `10-demo/demo.json` declares which pack IDs the demo
  demonstrates, and `tools/check-ids.py` validates them: a demo still
  demonstrating `ADR-0004` after that ADR was renumbered fails the build.

### Fixed — six packs with no integrity constraints

- `iam-platform`, `itsm-helpdesk`, `personal-blog`, `mes`, `tms`, `wms` gained
  numbered constraint tables, 86 constraints in total, each naming the `BR-`/`FR-`
  identifiers it enforces and each file closing with the sentence that records
  which are enforced in the store.
- The constraints are drawn from each pack's own rules rather than from a shared
  template: `wms` gets "no bucket goes negative" and "the projection equals the
  fold of its event log" because its ADR-0002 is an append-only event store,
  while `personal-blog` gets "no anonymous write path reaches public content"
  because on a static site the failure is a page that stays wrong until the next
  build.
- Corpus totals: constraints 118 → 204, of which 114 are claimed
  store-enforced; extraction quality for constraints is now 17/17 structured.

### Changed — the site reads as engineering drawings

- The palette was a warm cream ground (`#fbfaf7`) with a terracotta accent
  (`#b45309`) — one of the commonest tells of a generated page, appearing
  regardless of subject — alongside identical rounded cards with the same soft
  shadow, ALL-CAPS labels, big-number stat tiles and separator-joined meta
  strings. Rebuilt as technical drawing: vellum `#edeede`, ink `#1c1f1d`,
  ink-soft `#5b625c`, draft blue `#2a5580`, revision red `#a32020`.
- **Red means violated and nothing else.** No third accent: a green "all clear"
  and an ochre "policy" were both cut.
- **Monospace is the primary voice** for every machine-read element — identifier,
  formula, target, count, label — with sans for prose only, never both inside one
  element. A drawing is annotated in one lettering style.
- The catalog is a register: one ruled row per pack, three aligned columns, no
  containers. No `border-radius` and no `box-shadow` anywhere; hierarchy comes
  from line weight and column alignment.
- Two rule weights, separated deliberately: `--rule` (1.91:1) separates rows,
  where adjacent content already carries its own leading; `--rule-strong`
  (3.16:1) borders anything a person must recognise as a control, clearing WCAG
  1.4.11's 3:1. Holding both to 3:1 would make the sheet heavy; holding both to
  1.4:1 would make the controls indistinguishable from the page.
- The demo's palette was aligned to the same system, and its passing state
  changed from green to quiet ink: a second semantic colour for the passing case
  would train a reader to skim past the states that matter.

### Fixed — defects found by tooling rather than by reading

- **A ReDoS.** The clause recovering which numbered constraints a data model
  claims are store-enforced used nested quantifiers over a digit run, which
  backtrack exponentially. CodeQL flagged it; it is now a negated character
  class, and a 3000-nine input completes in under a millisecond where the
  previous form did not finish. The docstring records why the expression must
  stay a character class.
- **The build output was discovered as repository content.** The CI
  compatibility job builds into `_compat_site` before it tests, and the emitted
  prompt bundles are Markdown, so `discover_markdown()` — which excluded build
  output by name — treated the previous build's `prompts/*.md` as content and
  the site contained a copy of itself. Excluded by leading underscore now; the
  job's exact sequence is a test, because the failure was invisible to every
  other test.
- **`check-links.py`** walked `_site/` for the same reason and reported 161
  broken links that are not broken on the site.
- **`--vellum` contained a Cyrillic `е`** inside its hex value, so every
  `color: var(--vellum)` resolved as an invalid colour and the selected view
  toggle rendered near-black text on a blue ground.
- **The catalog's auto-placed grid** put the Chinese title in the middle column,
  because `card-sum` forced a full-width second line; the card now has three
  explicit columns.
- **The demo's action handlers** appended to the event log but never redrew the
  state panel, so clicking `delegate` produced no visible change.

### Added — tests

- `tests/test_pack_index.py` (22), `tests/test_prompts.py` (14),
  `tests/test_demo_layer.py` (11), `tests/test_design_tokens.py` (10).
- `tests/test_design_tokens.py` computes contrast for both colour schemes,
  asserts the control floor separately from the structural one, and forbids
  `border-radius`, `box-shadow` and `text-transform: uppercase` by name. It
  caught two leftovers in its author's own first draft.
- Suite: 65 → 139 tests.

### Added — skills

- `.opencode/skills/frontend-design` and `.opencode/skills/webapp-testing`,
  installed from `anthropics/skills` under their original licenses and kept
  project-local so they are shared with the repository. Playwright and Chromium
  were installed outside the repository; the toolchain remains Python-only.

### Deliberately not done

- **`verification` above `unverified`** — unchanged, and `practitioner-reviewed`
  and `field-proven` remain 0. Rung 3 needs a named human.
- **Conformance claims** — ODA/TMF, BPMN 2.0, GB/T and the EU AI Act remain
  vocabulary and shape only.
- **The other 16 demos** — the first is the reference implementation for the
  pattern; each remaining pack's is a separate unit of work.

## [0.2.0] — 2026-10-13

Twelve packs raised to L2, eleven completed at L1, and the tooling that found
what review missed. 86 ADRs, 148 business rules, 342 functional requirements,
139 NFRs across the shelf. `validate-packs.py` reports **0 errors and 0
warnings** — the §6 checklist debt carried since the initial import is cleared.

### Added — L1 checklist completed (11 packs)

`validate-packs.py` emitted 55 warnings for the §6 L1 chapters that eleven packs
lacked. All eleven now carry the five required chapters:

- `horizontal/workflow-bpm` · `data-ai/lakehouse-platform` ·
  `government-public/data-exchange` · `government-public/one-stop-service` ·
  `healthcare/his-emr` · `data-ai/enterprise-bi` · `data-ai/growth-analytics` ·
  `telecom/telecom-bss` · `data-ai/mlops-platform` ·
  `energy-utilities/power-marketing-cis` · `retail-commerce/omnichannel-commerce`

Each pack's regulatory landscape states what an instrument **forces the software
to do**, rather than quoting it — per this repository's scope decision that legal
accuracy matters only where it changes a design decision.

### Added — L2 Blueprint (12 packs)

Twelve packs raised from L1 to L2, each with a domain model, architecture views,
a logical data model with store-enforced integrity constraints, and 4–8 ADRs
covering the load-bearing decisions:

| Pack | ADRs | The decision the pack exists to make |
|---|---|---|
| `one-stop-service` | 8 | the anti-double-submission rule is **per field**, and its failure mode is the system being helpful |
| `his-emr` | 7 | a signed document is **evidence**; clinical and billing records have a **one-way** dependency |
| `workflow-bpm` | 6 | the Chinese approval vocabulary is **defined here**, because BPMN 2.0 does not define it |
| `data-exchange` | 6 | a classification grade **derives** rules per class; a dataset-scoped override is illegal |
| `telecom-bss` | 5 | tariff arithmetic is a **governed input**, never a platform decision |
| `lakehouse-platform` | 6 | layers **are** contracts, and deletion reaches caches, snapshots and derived ML data |
| `mlops-platform` | 5 | feature store exists for **point-in-time correctness**; a replay equals training values is the test for skew |
| `omnichannel-commerce` | 5 | inventory deduction is a **business bet** tabled per product, not a global setting |
| `enterprise-bi` | 5 | the metric definition is the core object, and the **join key** is the mechanism of comparability |
| `growth-analytics` | 4 | an event arrives once, so schema governance is a **write-time** control |
| `power-marketing-cis` | 4 | tariff calculation is regulated math; a rate change inside billing code is indistinguishable from a bug fix |
| `data-exchange` | 6 | no data transfer exists without a recorded, revocable, **purpose-matching** grant |

### Added — tooling that found what review missed

- **`tools/check-ids.py` in-pack gap detection.** A missing ID was previously
  classified by asking every pack whether that ID was defined *anywhere*, which
  made a collision silently green: a pack defining `ADR-1..4` and citing
  `ADR-5` was reported as an INFO because an unrelated pack also defined an
  `ADR-5`. References into a pack's **own** numbering sequence (within +2 of its
  maximum) are now in-pack gap errors. This caught **five** real defects across
  the L2 batch — dangling references in `omnichannel-commerce`, `telecom-bss`,
  `mlops-platform` and `data-exchange` — each of which had reached a commit
  before being caught by other means.
- `tests/test_check_ids.py`: 4 new tests covering both directions (a collision
  no longer masking a local gap; a genuinely distant cross-pack reference still
  an INFO) plus the helper directly. Suite: 62 → 65 tests.

### Fixed — citations that could not be verified

- `packs/data-ai/lakehouse-platform`: the manifest's only pack-level source was
  `iso.org/standard/56737.html`, for which **no ISO/IEC standard with that
  number could be found**. Removed rather than propagated, and the finding
  recorded in `SOURCES.md` with the follow-up action, so the next person to
  promote the pack inherits the investigation rather than the fabricated
  reference.
- `packs/government-public/data-exchange`: the gov.cn policy URL guessed in the
  original manifest 404'd. Replaced with the published text of 国发〔2016〕51号
  from the State Council Gazette.
- `docs/citation-audit-2026-10.md` — a repository-wide audit of whether the
  cited instruments are still in force, prompted by discovering that
  **《网络安全法》was amended on 2025-10-28 and renumbered** (effective
  2026-01-01): the graded-protection duties moved from Article 21 to Article 23,
  so every pre-2026 article number is stale. The audit records that the
  repository had never cited an article number of that law, so no historical
  content was wrong — but the hazard is live for any future citation, and the
  warning is now carried in the packs that name the law.
- The audit also states the **limits of the method**, which matter more than
  the findings: the national standards search endpoint returns HTTP 200 for a
  standard number that does not exist, so reachability is not existence — and
  anti-bot 403/412 responses prove neither existence nor absence.

### Changed — pack template

`templates/pack-template` gained the conventions the L2 packs actually use,
rather than only the file layout: settled-ADR tables, chapter maps, the load
order in the order traceability flows, and hard rules learned rather than
copied (settled ADRs are not relitigated; IDs are immutable; invariants are
distinguished from service levels; a rule is stated by what it prevents).

### Fixed — legal content that was wrong or unavailable

- `国办发〔2025〕33号《电子印章管理办法》` retrieved in full. Its Article 27 —
  business systems of administrative and public-service bodies **shall support**
  compliant electronic seals — turns a mandate into an obligation on the
  `one-stop-service` platform's own architecture, and was previously recorded
  as an open question with no answer available.
- 国务院令第716号's article numbers and dates were verified against the
  Ministry of Justice's National Administrative Regulations Database rather
  than asserted from memory.
- GB/T 36901–36906-2018 (electronic licence, six standards) confirmed real
  against the national standards platform — published 2018-11-15, effective
  2019-01-01, in force.

### Deliberately not done

- **`verification` above `source-checked`** — `practitioner-reviewed` and
  `field-proven` both remain 0. Rung 3 requires `verified_by` entries naming a
  human, which no agent can supply.
- **Conformance claims** — ODA/TMF, BPMN 2.0, NIST AI RMF, ISO/IEC 42001 and
  the EU AI Act are all adopted as **vocabulary and shape**, with no maturity
  level, API version or clause claimed.
- **Retention values, tariff content, estimation methods, seal primitives** —
  each is recorded as a gap with the requirement stated, rather than filled
  with plausible content.
- **Currency tracking** — per the repository's scope decision, no instrument is
  re-verified for amendments after drafting.

### Fixed — repository hygiene & the outsider-facing surface

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
- `LICENSE` — one file mixing CC BY-SA and MIT in prose. GitHub detected
  NOASSERTION, so the repo showed no license badge and license scanners could
  not classify it. Split into `LICENSE` (the canonical CC BY-SA 4.0 legal text,
  verbatim from the official legalcode so licenceer recognises it — a
  hand-condensed version did *not*) and `LICENSE-MIT`; READMEs point at both.
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

## [0.1.0] — 2026-10-10

Initial repository state: pack standard draft, taxonomy, roadmap, 17-pack
shelf (1× L3, 1× L2, 15× L1 at that point), contribution guides, issue/PR
templates, dual license (CC BY-SA 4.0 content / MIT code).

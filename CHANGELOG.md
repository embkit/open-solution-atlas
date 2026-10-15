# Changelog

All notable changes to Open Solution Atlas. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions are repository-wide
releases (individual packs carry their own `version` in `manifest.yaml`).

## [Unreleased]

### Fixed — the front end, page by page

A pass over the built site that opened every page *type* and measured it, rather
than reading the stylesheet. Eight defects were on every page of the site, and
three of them were accessibility failures axe-core had been reporting all along:

| defect | scope | how it showed |
|---|---|---|
| `--sticky-top: var(--sticky-top)` — a self-reference, invalid at computed-value time, so `top` fell back to `auto` | every page | neither the pack sidebar nor the contents rail ever stuck |
| `.navmenu { display: none }` was the *desktop* default | every page | Catalog, Standard, Taxonomy and Roadmap were reachable on a phone and on no desktop, tablet or laptop at any width |
| nothing ever set `aria-current="page"` | every page | the primary nav's active-pill rule was dead code |
| the generated directory index: a raw slug as the `<h1>`, a flat `<ul>` of file names, no page gutter | ~300 pages | the page you land on when you open a design-system folder |
| the article `<h1>` had no rule | every chapter and doc page | it fell through to the browser's own 2em heading |
| no `scroll-margin` anywhere | every page | a contents link put its heading *under* the sticky titlebar |
| `li a { text-decoration: underline }` was unscoped | every page | the pack sidebar and the contents rail were underlined like body copy, against the rule's own comment |
| the catalog wrote "packs" in the server HTML and "solutions" in the script | the catalog | the count changed word on load |

The chapter pages had their own two, both serious and both on all 590 of them:

- **The contents rail was invalid markup.** `render_toc` emitted the nested
  `<ul>` as a *sibling* of its parent `<li>`; a `<ul>` may contain `li`,
  `script` or `template` and nothing else, so axe reported `list`.
- **Its links were 16px tall**, under WCAG 2.2 AA's 24px minimum target
  (`target-size`, 14 nodes per page). They are 26px blocks now.

Four more were layout, and each had a cause worth naming:

- **A chapter's rail was a block above the article.** `.view-doc` had no rule at
  all, so the rail took the main column's full width *and* its own height — 512px
  on a chapter with a dozen headings — pushing the text down by that much and
  leaving the 579px prose column 300px short of the 880px box it sat in. It is a
  two-column reading layout now, and below 900px the rail is dropped rather than
  stacked, because capped it becomes a 287px box that swallows the reader's first
  upward swipe above the article.
- **The pack sidebar had no inner scroll**, so an L3 pack's 1381px nav lost its
  last third off the bottom of the screen.
- **`nav_tree` was not the disclosure its docstring described.** The comment
  claimed the groups "render as `<details>` … below 760px the same markup becomes
  collapsible"; it emitted `<div>`s, and on a phone the 40-chapter sidebar filled
  the viewport before the `<h1>`. The groups are `<details>` now, with the current
  one `open`, and desktop reveals them all through `::details-content` — a closed
  `<details>` keeps its contents out of the box in the UA's own machinery, which
  an author `display` cannot override.
- **`404.html`'s hero sat outside `.wrap`**, so its panel was the full viewport
  width while the catalog's identical panel was 1180px.

**The generated directory pages are a designed surface now** — the build gives
every output directory an index so that a link to `…/docs/` resolves, and there
are roughly three hundred of them. Each gets the page's own gutter and measure, a
breadcrumb back through the path, the raw path as a subtitle, and one card per
entry in the catalog's card language, with the entry count taken from the
directory rather than asserted.

**One more was not layout at all.** §2.1's rule is that Latin and figures come
from a neutral grotesque, but its literal order puts four CJK faces ahead of
`-apple-system` and `Segoe UI` — and CSS matches a family per *character*, so on a
machine without Inter the first family owning U+2019 is `Microsoft YaHei`. Measured
in the browser: the apostrophe in `pack's` advanced 11.64px that way and 2.77px
with a Latin face first, and every Latin glyph and the cards' `tabular-nums`
figures came from the CJK font too. The same rule, in an order that holds without
Inter installed; Inter stays first, so a machine that has it is unaffected.

Also fixed: the pack and plain pages had no `.wrap` (so the breadcrumb and pack
header sat flush against the viewport edge while the grid below them was inset);
the overview rendered the title and its metadata twice; a duplicate mermaid
`<script>` on overview pages with a diagram; and `app.js` was not loaded on
chapter pages at all, which is why the rail could not mark the section being read.

### Added — the contents rail marks where you are

The rail now sets `aria-current="location"` on the section the reader is in — the
last heading that has passed under the sticky titlebar — recalculated on scroll
and coalesced into one frame. It is progressive enhancement: without the script
every link still works, and the rail is absent below 900px, where the CSS is
asked rather than a duplicated breakpoint.

### Added — a guard for the font rule

`test_latin_faces_precede_the_cjk_faces` asserts §2.1's *rule* (a Latin face
precedes every CJK face in `--sans`) rather than its literal string, so a future
font swap cannot quietly reintroduce the fallback above. The category-colour
guard is now read from the token block instead of a `--cat-` prefix match, which
had been calling `.diricon`'s use of `--cat-box` — the icon container's *size*,
not a colour — a leak of the category palette.

### Added — every pack has a demo: 17 of 17

The demo layer is complete. Each one is hand-written for its pack — there is no
shared engine — and each exists to make one rule's *failure mode* clickable rather
than to display the pack.

What they share is the point of them: **a violation path and the permitted repair,
both asserted.** A demo whose failure path is decorative teaches the wrong thing,
so `tools/demo-harness/demo_check.js` asserts that the invariant panel lights up on
the action that breaks a rule *and clears* on the action that fixes it.

The recurring shape is a person under pressure taking the step that looks like
helping:

| pack | the step the reader is invited to take |
|---|---|
| `wms` | "fix the quantity" — a wrong *fact* is reversed by a compensating event, a wrong *projection* is rebuilt from the stream; neither is an UPDATE |
| `his-emr` | correcting a signed clinical document in place, under billing pressure |
| `enterprise-bi` | declaring your own dashboard certified; an artifact silently following `latest` |
| `iam-platform` | "grant it permanently", "override the conflict this once", a local password for an SSO user |
| `mes` | skipping the predecessor, the inspection gate, the genealogy |
| `tms` | "the truck leaves, the POD can follow" |
| `telecom-bss` | "the rule changed last month, just recompute it" |
| `power-marketing-cis` | "estimate a number and bill it", "cut the power now" |
| `lakehouse-platform` | "just re-run it" |
| `growth-analytics` | "looks good, ship it to everyone" |
| `mlops-platform` | "hot-patch it" |
| `itsm-helpdesk` | "close it and backfill later", "raise it as P1" |
| `personal-blog` | renaming after publication, unpublishing as a 404 |
| `omnichannel-commerce` | "just retry it", "roll this order back" |

Fourteen were written in this cycle. Every demo is one self-contained file that
opens from a `file://` URL, carries the byte-identical token block, and is
light-only — a test enforces each of those.

### Fixed — two defects in the demo harness, both of which made it too weak

- The stub **minted a node for any id a demo asked for**, so a demo that wrote to
  an undeclared `#log` passed here and threw on load in a real browser. It now
  registers the ids the HTML declares and returns null for the rest.
- **`clickAll` stopped at the first screen**, so "every button is clickable" was a
  claim about the initial state of a progressive demo.

### Changed — the demo kit's hardcode exemption is scoped, and colour is not in it

`lint_hardcodes.py` reported 694 values across the demos, every one of them a px
metric of the component kit — which each demo must carry verbatim, because a demo
has to be a single file. The region is marked with the tool's own escape hatch and
the reason is written into each file. A colour is **not** covered: a hex or an
`rgba()` outside the token block is a second palette starting, so that is checked
separately, per demo, by a test.

### Added — the site speaks both languages, and a reader can choose

The chrome was half English and half Chinese *in the same header*: an English
nav above a Chinese spec panel, "复制提示词" beside "Requirement". Not a
translation gap — a missing layer. There is one now.

`tools/i18n.py` is the vocabulary: ~130 keys, each with an `en` and a `zh`
value, covering nav, buttons, panel labels, empty states, copy feedback. The
build renders one of them (the new `--lang en|zh` reaches every template, not
only `<html lang>`), and `assets/i18n.js` — generated from the same catalog, so
the two halves cannot drift — renders the other when the reader clicks the
switch in the titlebar. The choice is stored and the browser's language decides
it on a first visit; `<html lang>` follows, down to `zh-CN`.

What is *not* translated is pack prose, and that is deliberate: a pack's
regulatory landscape is authored content, and half of it is bilingual on purpose
(《网络安全法》, 会签). Content already carries its own `lang` attribute. The
switch changes chrome; the demos stay in their pack's domain, because a demo of
a Chinese one-stop service hall *is* a Chinese page.

Every string is split around the markup it sits next to — a key holds plain
text, never a `<code>` element — and each language carries its own punctuation
and spacing, so an English comma does not become a space before a Chinese one.
Three tests hold the invariants: no key may be half-translated, no markup may
hide inside a value, and the English build must contain no Chinese chrome at
all.

### Fixed — the view switch was welded to the panel below it

`.vs-lab` is an inline-flex box, and its bottom margin never reached the line
box it was drawn in: the label's bottom edge and `.shell`'s top edge were the
same coordinate, so "文档视图 / 结构视图" sat flush against the sidebar card
with nothing between them. The margin belongs on the label, and it is there now
— 16px, measured.

### Deliberately not done

- `practitioner-reviewed` and `field-proven` remain 0. Both need a named human.
- The remaining packs' controls and capabilities stay structured at 13/17. The
  structured view is what exposed the gap; filling it is content work.

`verification` unchanged: a demo encodes the pack's design and proves nothing about
the pack's correctness.

## [0.4.0] — 2026-10-14

The catalog became EmbKit's shop window, and building it then found what the shop
window had been hiding: a page with no gutter, a demo that died on load, a trust
note that was a flex container, and a second palette that no audit was looking
at. Three interactive demos ship. Three is not seventeen.

### Changed — the catalog adopts the product's theme

The site had its own visual identity, which is the failure the UI contract names
outright: several surfaces on several palettes. Rebuilt on the contract's
tokens, vendored at `docs/embkit-ui-contract.md`.

- **Brand is indigo `#4F46E5` and nothing else.** The contract marks the hue
  LOCKED; the former `#635bff` is gone and a test asserts it does not return.
- **Neutrals are cold.** The contract says it twice — "不要引入暖灰，会和 indigo
  打架" — so there is no warm grey anywhere, and a test asserts blue ≥ red on
  every neutral.
- **Radius and elevation are used, and they are the contract's.** Six radius
  steps and the four cool-blue shadows. The previous pass had removed both, on
  the advice of a skill this repository's own standard forbids.
- **Spacing sits on the 4/8/12/16/20/24/28/32 scale**; §5 forbids stray values
  by name, and a test rejects off-scale spacing and radius tokens.
- **The register became the contract's §7.4 category card**: a four-column grid
  whose first row is an icon on a `--primary`-family tint beside a large
  tabular number. The number is real rather than decorative — it is how much
  machine-readable content the pack carries. Category colours appear on the
  icon's stroke and its tint and nowhere else, which a test enforces.
- **The pack page became §4.2's three-part sidebar** (220px, `--surface` on a
  `--page` ground — the lightness difference the contract calls the key to the
  page's layering) plus §4.3's main column. Both views live inside `main`, so
  the navigation survives the view switch; replacing the whole shell, as the
  first attempt did, hid the nav exactly when the reader was deepest in the
  material.
- **The catalog hero is §9's marketing frame** — the indigo wash with its light
  banding, a two-part headline with the second half in `--primary`, and a
  sub-line joined with `·` as §9 specifies.
- An empty result is §7.8's empty state — icon, title, what happened, and a way
  out — rather than a bare "no data".
- The demos carry the same tokens, byte-identical, because they inline them in
  order to open on their own; a test compares their `:root` blocks so a second
  palette cannot start there.

### Added — house skills, and one removed

- `.opencode/skill/{redesign,design-review,a11y-audit}` — the skills EmbKit's
  contract names for this work, copied project-local so they travel with the
  repository.
- **Removed `.opencode/skills/frontend-design`.** The contract's last line is
  explicit: *"但**不要**装 Anthropic 的 `frontend-design`——该 skill 明文禁止
  「紫渐变」，会试图改掉我们 LOCKED 的 indigo 品牌色"*. It had been installed
  and its guidance drove the previous redesign, which is why that pass chose a
  warm ground, removed every radius and shadow, and invented an accent colour.
- `tools/site_icons.py` — a hand-drawn icon set and the §1.4 category palette.
  The contract requires Lucide at stroke 2 / round caps / 24 viewBox and, for a
  repository that takes no runtime dependency, explicitly permits a hand-drawn
  set meeting that spec.

### Added — the second demo, and its test scaffolding

- `packs/government-public/one-stop-service/10-demo/` — the anti-double-
  submission lab. Where the first demo lets you walk a vocabulary, this one
  lets you violate a rule, because Article 7 is violated by the natural
  direction of the system rather than by a defect. Demanding an obtainable
  field lights `FR-011` and `NFR-001`; a failed lookup with no permitted
  alternative lights `FR-013`; an empty exemption reason lights `NFR-003`.
- The demo controls carry `data-action` / `data-field`, so a test names the
  control it means instead of relying on label text and render order.
- Shared test scaffolding for the demos (`demo_stub.js`, `demo_check.js`), and
  it fixed two defects that had been reporting success: the harness registered
  a button only when it was appended to a known container, so a demo building
  its controls inside generated wrappers registered none — "every button is
  clickable" was a true statement about an empty set; and `prompt` was placed
  on `document` when the demo calls the bare global.

### Fixed

- **The vendored scripts lost their SRI integrity hash** during the catalog
  rewrite. The build already fails if a vendored file's bytes change, so the
  attribute is the browser-side half of the same check; a test caught its
  absence.
- The empty state was drawn even when the catalog had results, because
  `display: flex` outranks the `hidden` attribute.
- Chapter slugs wrapped to three lines inside the contract's fixed 36px nav
  row; they truncate to one line now.

### Changed — one theme, not two

Dark mode is gone. It was **derived** from the contract's navy rather than
transcribed from §1, which made it the one part of the theme with no source of
truth — and it cost more than it gave. Inline code rendered at **1.49:1** in
dark, and the audit meant to catch it graded the *light* palette, because dark
was driven by `@media (prefers-color-scheme: dark)` while the kit's
`axe_audit.mjs --dark` sets `data-theme="dark"`.

The contract does not mention a dark theme at all, so removing it is not a
deviation from anything: it is one palette to get right instead of two.
`color-scheme: light` is pinned in the stylesheet, so a reader whose OS prefers
dark does not get this sheet with the browser's own inverted form controls and
scrollbars. A test asserts there is no second palette anywhere, in the site or
in the demos.

### Fixed — what the kit's verifiers found, run against this site

`scripts/lint_hardcodes.py`, `lint_taste.py`, `axe_audit.mjs` and the `verify_*`
family are the house tooling, and the contract names two of them as its
acceptance method. Running them replaced guessing with findings, and every one
below is a defect that reading the stylesheet had not revealed.

- **123 hardcoded values** → now `OK: no hardcoded values found`. The fix names
  the numbers rather than inlining fewer of them: a component-metrics block, and
  off-scale literals (6px, 10px, 13.5px) snapped onto §5's scale.
- **110 nodes below 4.5:1** — tertiary text on `--page`, `--surface-2` and
  `--surface-3`, not on the `--surface` where the contract's value was checked.
- **Two unlabelled form elements** (critical): the inline prompt's textarea and
  the demo's completion-policy select had no accessible name.
- **Links inside text blocks** are underlined, so they do not rely on colour.
- **`node_modules` was discovered as content**, which put a dependency's READMEs
  on the site and broke the link checker on a file inside a package.

### Fixed — what a real browser found that the suite did not

Serving the built site and reading it found four defects that the published
site, the test suite and the audits had all passed.

- **The catalog had no page gutter.** `render_catalog` never wrapped its body in
  `.wrap`, the container that carries the measure and the gutter, so the first
  facet label was clipped at x=0 and the hero and trust note sat against the
  viewport edge. Their own padding made everything *look* inset, which is why a
  screenshot had not exposed it either.
- **The trust note was a flex container.** It is a sentence with inline `code`
  and `strong` in it, and flex blockified those children and put a gap before the
  punctuation, so it read as fragments.
- **The anti-double-submission demo threw on load**: its script wrote to a `#log`
  the page never declared. The harness passed it because the stub minted a node
  for any id asked for — a stub that answers every question is not a test.
- **Identifiers in the demos' tables no longer wrap** (`FR-018` was splitting
  after the hyphen, which stops it reading as an identifier).

### Added — the demo harness moved into the repository

`tools/demo-harness/`, run by `tests/test_demo_harness.py` so CI runs it. It was
a scratch-directory script, which is how a demo that dies on load could ship: the
check that should have caught it was not reproducible by anyone else. The stub
now registers the ids the HTML declares and returns **null** for the rest, which
is what a browser does.

### Added — the third demo

`packs/government-public/data-exchange/10-demo/` — the closed-loop sharing lab.
Authorization → approval → share → lineage is a **cycle**, and breaking it
anywhere produces the same thing: a transfer nobody can attribute. A transfer
with no grant lights `BR-08` and `FR-018`; a purpose-mismatched transfer is the
subtler case, because a grant that exists but does not cover this transfer's
purpose is not a grant for it; and a revocation recorded while access persists
lights `BR-07`, because revocation's value is the lead time until access is
actually removed.

### Deliberately not done

- **Fourteen demos.** A demo has to demonstrate the pack's own rule rather than a
  generic interaction, so they are written one at a time and each takes the shape
  of the invariant it exists to show. `wms` is next.
- **Dark mode is removed rather than fixed.** It was the only part of the theme
  derived instead of transcribed, and it shipped a contrast failure the audit
  could not see. Reverting it is the fix; adding it back would need a source of
  truth in the contract first, and there is none.
- `practitioner-reviewed` and `field-proven` remain 0. Both need a named human.
- The remaining packs' controls and capabilities stay structured at 13/17 — the
  structured view is what showed the gaps, and filling them is content work
  rather than tooling.

`verification` unchanged: this changes how the content is presented, not what
any pack claims. 161 tests, ruff clean, 0 broken links.

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

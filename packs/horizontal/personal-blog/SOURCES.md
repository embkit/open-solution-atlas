# SOURCES — Personal Blog & Content Publishing

> Provenance ledger. Maps load-bearing claims to public, checkable sources;
> anything that could not be traced is listed in §4 and marked
> `> ⚠️ ASSUMPTION:` in the chapters.
>
> **Status: `source-checked`** (2026-10-09). Provenance: `llm-drafted`.
> Verification: `source-checked` — **not** field-verified. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).
>
> Checked against sources on 2026-10-09. Outcomes: (a) LCP ≤ 2.5 s traced to
> Core Web Vitals guidance (the pack's CLS ≤ 0.05 is stricter than the
> published 0.1 and stays an assumption); (b) EN 301 549 pinned to the
> harmonised v3.2.1 (2021-08-18); (c) ICP filing and DMCA safe-harbor notes
> given instrument-level citations; (d) PIPL pinned to the 2021 act.
> All remaining numeric targets remain declared assumptions (§4).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Markdown authoring format (BR-02, NFR-011) | CommonMark | CommonMark Spec — https://spec.commonmark.org/ | Specifies syntax; does not mandate an editor/autosave behavior |
| Webmention receive/verify/send (BR-09, FR-013/FR-014, AC-013/AC-014) | W3C | Webmention (W3C Recommendation, 2017) — https://www.w3.org/TR/webmention/ | Idempotency by `(source, target)` is a pack rule, not required by the spec |
| Microformats2 markup for mentions/replies | Microformats | microformats2 — https://microformats.org/wiki/microformats2 | |
| Federation protocol (future variant, ADR-0003) | W3C | ActivityPub (W3C Recommendation) — https://www.w3.org/TR/activitypub/ | Deferred to a variant, not core |
| RSS 2.0 feed (FR-011, NFR-010, AC-011) | RSS Advisory Board | RSS 2.0 Specification — https://www.rssboard.org/rss-specification | |
| Feed validation (AC-011) | W3C | W3C Feed Validator — https://validator.w3.org/feed/ | Tool, not a normative spec |
| Sitemap (FR-012, AC-012) | sitemaps.org | Sitemap protocol — https://www.sitemaps.org/protocol.html | |
| Social/canonical preview metadata (FR-012) | Open Graph | The Open Graph protocol — https://ogp.me/ | |
| JSON-LD `Article` structured data (AC-012) | schema.org | schema.org/Article — https://schema.org/Article | |
| Optional alternative feed | JSON Feed | JSON Feed 1.1 — https://www.jsonfeed.org/version/1.1/ | Not required by the pack |
| Publisher push notification (optional) | W3C | WebSub — https://www.w3.org/TR/websub/ | |
| Accessibility of public pages (NFR-009, BR-10, CTL) | W3C | WCAG 2.1 — https://www.w3.org/TR/WCAG21/ ; non-text content obligation: SC **1.1.1** (Level A); pack targets Level AA | Level AA identified in the pack |
| Accessibility procurement (public-sector reach) | ETSI/CEN/CENELEC | **EN 301 549 v3.2.1**, harmonised under EU Web Accessibility Directive 2021-08-18 — https://digital-strategy.ec.europa.eu/en/policies/web-accessibility-directive-standards-and-harmonisation | v2.1.2 (2018) superseded; clause-level mapping remains §4 |
| Load-performance threshold (NFR-001, AC-N01) | Google web.dev | **Core Web Vitals**: LCP ≤ 2.5 s, CLS ≤ 0.1 ("good" thresholds; ≥75 % of visits) — https://web.dev/vitals/ | Pack adopts LCP 2.5 s from this guidance; pack's CLS ≤ 0.05 is **stricter** than 0.1 → §4 assumption; TTFB ≤ 200 ms has no CWV source → §4 |
| Privacy regime (CTL-001…) | EU | GDPR (EU 2016/679) — https://gdpr-info.eu/ | |
| Privacy regime (CCPA/CPRA) | California AG | https://oag.ca.gov/privacy/ccpa | |
| Privacy regime (CN) | National People's Congress | 《中华人民共和国个人信息保护法》(PIPL) — adopted 2021-08-30, in force 2021-11-01; legality bases **art. 13**, individual rights **arts. 44–50** | URL via NPC; article numbers cited at article level |
| Copyright / takedown contact (regulatory note) | US Congress | **17 U.S.C. §512(c)** (hosting safe harbor; §512(c)(3) notification, §512(g) counter-notification) | Statute cited at subsection level |
| CN hosting note (regulatory-landscape) | State Council (China) | 《互联网信息服务管理办法》(国务院令第292号, 2011修订) **art. 4** — 非经营性互联网信息服务实行备案制度 (ICP 备案) | Instrument-level citation; enforcement practice varies |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Atom feed (FR-011, NFR-010, AC-011) | IETF | RFC 4287 (Atom Syndication Format) — https://www.rfc-editor.org/rfc/rfc4287 | |
| AtomPub (optional publishing API) | IETF | RFC 5023 — https://www.rfc-editor.org/rfc/rfc5023 | |
| HTTP status semantics for BR-06/AC-003/AC-010/AC-015 (301, 410, 415, 413, 429) | IETF | RFC 9110 (HTTP Semantics) — https://www.rfc-editor.org/rfc/rfc9110 | Codes are standard; the pack's use of them is a design choice |
| CDN caching semantics (NFR-001, NFR-003) | IETF | RFC 9111 (HTTP Caching) — https://www.rfc-editor.org/rfc/rfc9111 | |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Static-site generation (ADR-0001/0002) | Hugo | https://gohugo.io/ | Reference for static-first build/deploy |
| Static-site generation | Eleventy (11ty) | https://www.11ty.dev/ | |
| Static-site generation | Astro | https://astro.build/ | |
| Static-site generation | Jekyll | https://jekyllrb.com/ | |
| Dynamic CMS alternative | WordPress | https://wordpress.org/ | Contrasts static-first stance |
| Dynamic CMS alternative | Ghost | https://ghost.org/ | |
| Client-side search (FR-007, AC-007) | Pagefind | https://pagefind.app/ | Pack requires no-network search |
| Client-side search | Lunr.js | https://lunrjs.com/ | |
| Webmention endpoint (FR-013) | webmention.io | https://webmention.io/ | |
| POSSE / bridging (ADR-0003) | Bridgy | https://brid.gy/ | |
| ActivityPub reference (variant) | Mastodon | https://joinmastodon.org/ | |
| LCP/CLS measurement (AC-N01) | Chrome Lighthouse | https://developer.chrome.com/docs/lighthouse/overview/ | |
| Structured-data validation (AC-012) | schema.org Validator | https://validator.schema.org/ | |
| IndieWeb patterns (ADR-0003) | IndieWeb | https://indieweb.org/ | Community, not a normative body |

## 4. Uncited specifics to resolve

- **NFR-001 / AC-N01** — `TTFB ≤ 200 ms (CDN hit)` and `CLS ≤ 0.05` are
  internal targets: TTFB has no Core Web Vitals source, and CLS 0.05 is
  stricter than the published 0.1 good-threshold (LCP 2.5 s *is* sourced —
  see §1 Core Web Vitals row).
- **NFR-002 / AC-001 / AC-002** — editor autosave `≤ 1 s p95`, preview render `≤ 300 ms for 20k-word` posts, autosave fires within `5 s`. No benchmark or source; adopt as design targets.
- **NFR-003 / AC-N03** — "no capacity planning needed to 1 M requests/day" and "sustains 100× traffic spike". Capacity claim, unvalidated; depends entirely on chosen CDN/hosting.
- **NFR-004 / NFR-006** — `99.9 %/month` availability, publish latency `≤ 60 s`. Arbitrary targets with no contracting/source basis.
- **NFR-005 / AC-N04** — content-loss window `≤ 5 min`, mirrored to `≥ 2 locations`, weekly restore drill. Backup figures are pack policy, not sourced.
- **NFR-008** — "no stored reader IPs beyond 24 h". Retention period is a policy choice; contradicts nothing, but EU guidance treats IPs as personal data (see regulatory-landscape); confirm against a specific regime.
- **NFR-014 / AC-N05** — production cost `≤ 5 USD/month` at baseline. Pricing-dependent (free-tier changes); not verifiable as a constant.
- **BR-03 / BR-05** — slug `max 80 chars`, `max 8 tags` per post. Internal hygiene limits with no external basis.
- **BR-10 / AC-003** — mandatory non-empty alt text; `6 MB PNG → 413`, non-image upload `→ 415`. The size/type limits are arbitrary; alt text requirement is WCAG-derived (2.1 AA §1.1.1) but the enforcement boundary is a pack choice.
- **AC-007** — search `≤ 300 ms on a 500-post index` on an undefined "reference device". Benchmark undefined and unmeasured.
- **AC-011** — feed exposes "only the latest 20 posts". Common practice, not a spec requirement; the number 20 is arbitrary.
- **Observability SLOs** — "publish-to-visible ≤ 120 s at ≤ 500 posts", "webmention visible within 5 min", "3 failed attempts → alert", "backups stale > 36 h". Invented operational thresholds; no source.
- **NFR-010 / NFR-012** — "current + previous major" browsers, `320 px–2560 px`, single-command deploy, `≤ 30 min` from zero to site. Support-matrix and onboarding claims are unverified.
- **EN 301 549 / WCAG / privacy clause-level mappings** — instruments and
  versions are pinned (§1); the specific clause → pack-control mappings
  remain to be written before any compliance claim is made.
- **ICP 备案 & DMCA practice** — instrument-level citations are in §1;
  jurisdiction-specific application guidance is deployment work, not pack
  content.

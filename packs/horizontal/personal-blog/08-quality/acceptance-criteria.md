# 08 · Acceptance Criteria

Each AC is a falsifiable test statement mapped to a requirement. This is the
definition of "done" for an L3 pack; a coding agent must be able to verify
each by automated test or an explicitly marked manual check.

## Authoring & revisions

- **AC-001** (FR-001): Given a Markdown edit, preview output for headings,
  code blocks, lists, quotes and embedded images is byte-identical in
  structure to the published page render.
- **AC-002** (FR-002): Autosave fires within 5 s of edit idle; closing and
  reopening the editor restores the exact last-saved text; every save creates
  a revision row; restoring revision n creates revision n+1 (history never
  mutates).
- **AC-003** (FR-003): Upload of a non-image type → 415; 6 MB PNG → 413;
  valid JPEG without alt cannot be embedded into a post that is then
  published (publish blocked, FR-004 list mentions the specific image).
- **AC-004** (FR-004): Post missing title/slug/tags/summary/license → publish
  returns 422 listing every missing field; with all fields present → 202
  release job.

## Organization

- **AC-005** (FR-005): Tags ` Python `, `python`, `PYTHON` collapse to one
  normalized tag; a 9th tag is rejected; `/tags/<name>/` page exists for
  every used tag and lists posts newest-first with correct counts.
- **AC-006** (FR-006): Year/month archive pages enumerate exactly the posts
  whose `published_at` falls in the window; drafts never appear.
- **AC-007** (FR-007): Search for a word present in a published post returns
  it within 300 ms on a 500-post index on the reference device; a word only
  in a draft returns nothing; no network request is emitted (verified via
  network panel).

## Publishing & URLs

- **AC-008** (FR-008): Publish returns DEPLOYED; post page, tag page, home,
  RSS and Atom all contain the new post; interrupting promotion mid-way
  leaves the previous site fully serving (inject failure → no mixed state).
- **AC-009** (FR-009): A post scheduled T publishes by T+60 s; with builder
  failing 3 times the author receives an alert and the post is not public.
- **AC-010** (FR-010): Changing a published post's slug creates a working
  301 old→new and updates internal links; unpublishing yields 410 at the
  original URL; neither action produces a bare 404.

## Distribution

- **AC-011** (FR-011): RSS and Atom validate against their official
  validators; editing a post updates the existing item (same GUID) rather
  than adding a duplicate; only the latest 20 posts appear.
- **AC-012** (FR-012): Sitemap contains exactly all published URLs, excludes
  drafts/410s; each post has canonical, OG/Twitter tags and JSON-LD
  `Article`; structured-data validator reports zero errors.

## Interaction

- **AC-013** (FR-013): POST with malformed target → 400, nothing stored;
  target unknown → 400; source that does not link back → stored REJECTED;
  valid reply → 202 then PENDING; repeat send with same source updates the
  same row (no duplicate).
- **AC-014** (FR-014): Approval shows the mention on the post after rebuild;
  raw `<script>` in source HTML is absent from rendered output; blocked
  source is auto-rejected on subsequent sends.
- **AC-015** (FR-015) [if enabled]: 5 rapid comments from one IP → 429;
  valid comment stays invisible until approved; disabled post → 403.

## Insight & ownership

- **AC-016** (FR-016): Default deployment makes zero third-party requests on
  reader page load (network audit); analytics responses contain no IP and
  cannot identify a reader across days.
- **AC-017** (FR-017): Export bundle contains every post, revision, media
  binary, tag, redirect and approved mention, plus `manifest.json`; contains
  no IPs or access logs; SHA-256 list verifies all media.
- **AC-018** (FR-018): Restore the bundle into an empty installation;
  100 % of previously published URLs serve identical content; feeds and
  redirects work.

## NFR gates

- **AC-N01** Lighthouse on representative post (mobile, throttled 4G): LCP
  ≤ 2.5 s, CLS ≤ 0.05, a11y ≥ 95; CDN-hit TTFB ≤ 200 ms (NFR-001).
- **AC-N02** Kill the authoring service for 24 h: public pages and feeds
  remain 200 throughout; admin shows degraded mode (NFR-004).
- **AC-N03** 100× baseline request rate for 1 h via load generator against
  CDN target: error rate 0, no autoscaling of origin (NFR-003).
- **AC-N04** Weekly backup restore drill completes and content checksum
  matches (NFR-005, CTL-010).
- **AC-N05** Monthly cost for baseline profile fits the documented ≤ 5 USD
  model (billing review; manual).

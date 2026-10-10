# 02 · Functional Requirements

EARS notation: `WHEN <trigger> THE SYSTEM SHALL <response>`.
Stable IDs forever; each traces to a capability (`CAP-xx`) and acceptance
criteria (`AC-xxx` in 08-quality).

## CAP-01 Authoring

### FR-001 — Markdown editor with preview
- **WHEN** the author edits a post body in Markdown
- **THE SYSTEM SHALL** render a live preview using the same renderer and
  styles as published pages
- **AND SHALL** preserve raw Markdown as the stored form
- Priority: Must · Traces: CAP-01.1 · Acceptance: AC-001

### FR-002 — Autosave & revisions
- **WHEN** the author pauses typing for 5 s or closes the session
- **THE SYSTEM SHALL** persist the draft automatically without a save action
- **AND SHALL** retain a revision history with timestamps, allowing restore
  of any prior revision
- **AND SHALL** show the author the last-saved state explicitly
- Priority: Must · CAP-01.2 · AC-002

### FR-003 — Media library
- **WHEN** the author uploads an image
- **THE SYSTEM SHALL** validate type (image/* allowlist) and size (≤ 5 MB)
- **AND SHALL** reject uploads failing validation with a specific error
- **AND SHALL** require alt text (or an explicit "decorative" flag) before
  the image may be embedded into a post targeted for publishing
- Priority: Must · CAP-01.3 · AC-003

### FR-004 — Post metadata
- **THE SYSTEM SHALL** enforce metadata completeness (title, slug, tags,
  summary, license) before a post can transition to PUBLISHED
- and block the transition listing every missing/invalid field.
- Priority: Must · CAP-01.4 · AC-004

## CAP-02 Organization

### FR-005 — Taxonomy
- **WHEN** tags are assigned
- **THE SYSTEM SHALL** normalize them per BR-05, reject more than 8 per post,
  and generate a paginated index page per tag/category/series.
- Must · CAP-02.1/02.2 · AC-005

### FR-006 — Archive navigation
- **THE SYSTEM SHALL** generate year/month archive pages and a global archive
  listing in reverse chronological order.
- Must · CAP-02.2 · AC-006

### FR-007 — Site search
- **WHEN** a reader enters a query on the site
- **THE SYSTEM SHALL** return matching published posts via a client-side
  index, with no server round-trip and no third-party service.
- Should · CAP-02.3 · AC-007

## CAP-03 Publishing

### FR-008 — Publish/unpublish
- **WHEN** the author publishes a complete post
- **THE SYSTEM SHALL** build and deploy the post page, affected index pages,
  feed and sitemap atomically (a deploy is all-or-new; never a mixed state).
- Must · CAP-03.1/03.4 · AC-008

### FR-009 — Scheduled publishing
- **WHEN** a post is set to PUBLISHED with a future `published_at`
- **THE SYSTEM SHALL** perform the publish within 60 s of the scheduled time
- **AND SHALL** retry on failure and alert the author after 3 failed attempts.
- Should · CAP-03.2 · AC-009

### FR-010 — URL governance
- **WHEN** a published post's slug is changed or merged
- **THE SYSTEM SHALL** create a `301` redirect from old to new URL; on
  unpublish it SHALL serve `410 Gone`; no published URL SHALL ever return a
  bare 404 due to an authoring action.
- Must · CAP-03.3 · AC-010

## CAP-04 Distribution

### FR-011 — Feed
- **THE SYSTEM SHALL** publish a valid RSS 2.0 **and** Atom 1.0 feed of the
  latest 20 posts, with stable GUIDs per BR-08, correct `updated` semantics,
  and full-content optional flag.
- Must · CAP-04.1 · AC-011

### FR-012 — SEO artifacts
- **THE SYSTEM SHALL** emit XML sitemap, robots.txt, canonical links,
  OpenGraph/Twitter Card metadata, and JSON-LD `Article` for every post.
- Must · CAP-04.2 · AC-012

## CAP-05 Interaction

### FR-013 — Receive Webmention
- **WHEN** an HTTP POST with `source` and `target` arrives at the Webmention
  endpoint
- **THE SYSTEM SHALL** accept only syntactically valid pairs whose target is a
  real post URL, fetch the source, verify it links back to the target,
  classify the mention, store it as PENDING, and respond 202.
- Must · CAP-05.1 · AC-013

### FR-014 — Moderation
- **THE SYSTEM SHALL** provide a single-author queue listing pending
  mentions/comments with source snippet, type, target, and received time;
  approve/reject/block actions; approved mentions render sanitized HTML only.
- Must · CAP-05.2 · AC-014

### FR-015 — Native comments (optional)
- **WHEN** enabled per post
- **THE SYSTEM SHALL** accept name + URL (no email required) + Markdown
  comment, apply rate limiting and spam scoring, and hold for moderation.
- Could · CAP-05.3 · AC-015

## CAP-06 Insight

### FR-016 — Privacy-preserving analytics
- **THE SYSTEM SHALL** aggregate page views without cookies, without
  cross-site identifiers, and without sending reader IPs to third parties;
  the author sees views/uniques (coarse), referrers, top posts.
- Should · CAP-06.1 · AC-016

## CAP-07 Ownership

### FR-017 — Full export
- **WHEN** the author triggers export
- **THE SYSTEM SHALL** produce a single archive: posts (Markdown +
  frontmatter), media, taxonomy, redirects, approved mentions, and a manifest
  with format version — excluding access logs and reader IPs.
- Must · CAP-07.1 · AC-017

### FR-018 — Restore / migration
- **THE SYSTEM SHALL** restore an export into a clean installation,
  reconstructing identical URLs and content.
- Must · CAP-07.2/07.3 · AC-018

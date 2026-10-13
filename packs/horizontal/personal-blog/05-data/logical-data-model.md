# 05 · Logical Data Model

Two stores by design (ADR-0002): the **content repository** (Git tree,
system of record for publishing) and the **operational store** (derived and
ephemeral). Logical entities, physical-neutral.

## ER view (logical)

```mermaid
erDiagram
    POST ||--o{ REVISION : has
    POST }o--o{ TAG : classified
    POST }o--o| SERIES : belongs
    POST ||--o{ POST_MEDIA : embeds
    MEDIA_ASSET ||--o{ POST_MEDIA : referenced
    POST ||--o{ MENTION : receives
    POST ||--o{ COMMENT : receives
    POST ||--o{ REDIRECT : "guards old URL"
    RELEASE }o--o{ POST : includes
    MENTION }o--o| MODERATION_ACTION : audited
    COMMENT }o--o| MODERATION_ACTION : audited
```

## Table-level entities (operational store)

| Entity | Key | Notable attributes | Notes |
|---|---|---|---|
| post_metadata | post_id (uuid) | slug (unique), status, published_at, canonical_url, license_id, repo_path | projection of repo frontmatter; rebuilt on sync |
| revision | (post_id, rev_no) | commit_sha, created_at, note | mirrors Git history; append-only |
| tag | tag_id | name_norm, display_name | normalization per BR-05 |
| post_tag | (post_id, tag_id) | — | ≤ 8 per post enforced |
| series / series_entry | series_id / (series_id, position, post_id) | title | ordered |
| media_asset | media_id | sha256, content_type, bytes, alt_text, decorative, storage_key | dedup by sha256 |
| post_media | (post_id, media_id, position) | — | embed order |
| mention | mention_id | source_url (UK with target), target_post_id, type, status, content_safe, received_at, verified_at | idempotency key (source,target) |
| comment | comment_id | post_id, name, url, body_md, body_safe, spam_score, status | optional feature |
| moderation_action | id | target_type, target_id, action, actor, at, reason | audit append-log |
| redirect | from_path (PK) | to_url, kind (301/410), created_at, reason | no chains/loops |
| release | release_id | commit_sha, artifact_prefix, status, created_at, deployed_at | atomic promotion record |
| schedule | post_id, run_at | last_attempt, attempts, alert_sent | scheduler state |
| audit_log | id | actor, action, entity, at, detail_json | append-only (CTL-010) |
| analytics_hourly | hour, path | views, unique_coarse, referrer_class | **aggregated only**; no raw rows, no IPs |

## Content repository layout (system of record)

```
content/
├── posts/YYYY/MM/<slug>/
│   ├── post.md            # frontmatter + Markdown body
│   └── media/…            # or shared media pool with hash names
├── series/<slug>.yaml
├── tags.yaml              # display names / renames map
├── redirects.yaml
├── licenses/
└── site.config.yaml
```

## Classification & retention

| Data | Class | Retention |
|---|---|---|
| Posts/revisions/media | owned content | indefinite, exported |
| Approved mentions/comments | third-party contributed, public | until target post unpublished or deletion request (CTL-003); included in export |
| Pending/rejected mentions | interaction metadata | 90 days then purge |
| Reader IP / raw logs | personal data | ≤ 24 h, scrubbed at edge (NFR-008) |
| Analytics | derived aggregate | 24 months hourly, then monthly rollups |
| Audit log | operational | ≥ 2 years |

## Integrity constraints (normative)

Constraints the model must enforce. They are numbered and stable, and each
names the `BR-`/`FR-` identifier it enforces. The closing sentence records
which are enforced **in the store** rather than in application code — a claim
the pack makes about itself, not a verified property, since application
discipline is exactly what a later change bypasses.

| # | Constraint | Enforces |
|---|---|---|
| 1 | A post has exactly one `canonical_url` row; a second one is illegal | BR-01, ADR-0001 |
| 2 | `title`, `slug`, `author`, `created_at`, `license` are NOT NULL at first publish | BR-02 |
| 3 | `slug` matches lowercase-ASCII kebab-case, is ≤ 80 chars, and is unique across every post **including retired ones** | BR-03 |
| 4 | `slug` is immutable once the post is published; an edit after publish is rejected | BR-04 |
| 5 | Tags are stored normalised (trimmed, case-folded per language), and a post carries at most the configured tag count | BR-05 |
| 6 | Unpublishing writes a `410` rule; renaming or merging writes a `301`. No public URL is ever silently dropped | BR-06 |
| 7 | A post is publicly visible iff `status = PUBLISHED AND published_at <= now`; no render, search or feed path may bypass this predicate | BR-07 |
| 8 | A feed item's GUID is the canonical URL and never changes; an edit updates the item, never its GUID | BR-08 |
| 9 | A webmention is unique on `(source_url, target_url)`; a duplicate updates state rather than inserting | BR-09, ADR-0003 |
| 10 | An image inside published content carries non-empty `alt`; a decorative image carries the decorative marker | BR-10 |
| 11 | No anonymous write path reaches public content: a publish requires an authenticated author identity | BR-11 |
| 12 | A third-party request (font, analytics, embed) is declared and recorded, or the build fails | BR-12 |
| 13 | An export includes received webmentions and **never** includes reader IP addresses or raw logs | BR-13 |
| 14 | A draft is excluded from sitemap, feeds, the search index and the public build, by predicate rather than by filter | BR-14, ADR-0004 |
| 15 | A `REDIRECT` row is append-only and never targets a draft | BR-06 |

> Constraints 1, 3, 7, 9 and 11 are **enforced in the store**, not in
> application code. A second canonical URL, a colliding slug, a render path
> that bypasses the visibility predicate, a duplicated webmention, or an
> anonymous write reaching the public tree is a defect regardless of what
> application discipline promises — on a static site the failure is a page
> that stays wrong until the next build, and nobody sees it happen.

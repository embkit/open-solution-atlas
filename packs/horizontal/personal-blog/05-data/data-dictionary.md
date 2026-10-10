# 05 · Data Dictionary (core fields)

## post metadata

| Field | Type | Constraints | Meaning |
|---|---|---|---|
| post_id | uuid | PK | internal stable id |
| slug | string | `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤ 80, unique | URL component; immutable post-publish (BR-04) |
| title | string | 1–150 chars | display title |
| summary | string | ≤ 300 chars | feed/card/meta description source |
| status | enum | DRAFT/SCHEDULED/PUBLISHED/UNPUBLISHED | SM-01 |
| published_at | timestamptz | null for drafts; ≤ now gates visibility (BR-07) | feed/order key |
| canonical_url | url | unique, https | GUID source for feeds (BR-08) |
| license_id | enum/ref | required at publish | per-post license (CTL-005) |
| repo_path | path | exists in repo | link to SSOT |
| og_image_ref | media_id? | square ≥1200px recommended | social card |

## media_asset

| Field | Type | Constraints |
|---|---|---|
| sha256 | hex(64) | dedup key |
| content_type | enum | image/png, image/jpeg, image/webp, image/gif, image/svg+xml (sanitized SVG only) |
| bytes | int | ≤ 5,242,880 (FR-003) |
| alt_text | string? | required unless decorative=true (BR-10) |
| width,height | int | populated by inspection |

## mention

| Field | Type | Constraints |
|---|---|---|
| source_url | url | http(s), length ≤ 2048 |
| target_post_id | fk | must exist at ingestion (FR-013) |
| type | enum | REPLY/LIKE/REPOST/BOOKMARK/MENTION |
| status | enum | PENDING/APPROVED/REJECTED/BLOCKED |
| content_safe | html | sanitizer output only; raw source never stored beyond job lifetime |
| uk(source_url,target_post_id) | unique | BR-009 |

## redirect

| Field | Constraints |
|---|---|
| from_path | root-relative, unique; must not equal an existing live path |
| to_url | required for 301; ignored for 410 |
| kind | 301 (moved/merged) / 410 (gone) |

## release

| Field | Constraints |
|---|---|
| commit_sha | the exact content tree built |
| status | BUILDING/READY/DEPLOYED/FAILED (SM-02) |
| artifact_prefix | immutable storage location |

## Timestamps

All times UTC; rendering converts to author-specified display timezone for
scheduling UI only. `published_at` is the sole public ordering key;
`updated_at` triggers `atom:updated` without changing GUID.

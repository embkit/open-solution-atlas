# 06 · API Overview

Two surfaces:

1. **Management API** (`/api/v1`, authenticated, author-only) — content,
   media, scheduling, moderation, redirects, export.
2. **Public ingestion endpoints** (unauthenticated, untrusted, hardened) —
   Webmention, optional comment.

Everything else the public consumes is a **static artifact**, not an API:
`/index.html`, `/posts/<slug>/`, `/feed.xml` (RSS 2.0), `/atom.xml`,
`/sitemap.xml`, `/robots.txt`, `/search-index.json` (lazy-loaded).

## Inventory

| Contract | Method/path | Auth | Purpose | Requirement |
|---|---|---|---|---|
| C-01 | `GET /api/v1/posts` | bearer | list posts incl. drafts w/ filters | FR-001 |
| C-02 | `POST /api/v1/posts` | bearer | create draft | FR-001 |
| C-03 | `GET/PATCH/DELETE /api/v1/posts/{id}` | bearer | read / autosave update / delete draft only | FR-001/002 |
| C-04 | `POST /api/v1/posts/{id}/revisions` | bearer | snapshot revision | FR-002 |
| C-05 | `POST /api/v1/posts/{id}/publish` | bearer | publish now (validates gates) | FR-004/008 |
| C-06 | `POST /api/v1/posts/{id}/schedule` | bearer | set/change scheduled time | FR-009 |
| C-07 | `POST /api/v1/posts/{id}/unpublish` | bearer | 410 transition | FR-010 |
| C-08 | `POST /api/v1/media` | bearer (multipart) | image upload w/ alt requirements | FR-003 |
| C-09 | `GET/PUT /api/v1/tags`, series, categories | bearer | taxonomy management | FR-005 |
| C-10 | `CRUD /api/v1/redirects` | bearer | 301/410 governance | FR-010 |
| C-11 | `GET /api/v1/mentions` | bearer | moderation queue | FR-014 |
| C-12 | `POST /api/v1/mentions/{id}:approve|:reject|:block` | bearer | moderation actions | FR-014 |
| C-13 | `POST /api/v1/export` | bearer | create ExportBundle job | FR-017 |
| C-14 | `POST /webmention` | none, form-encoded | W3C Webmention receiver | FR-013 |
| C-15 | `POST /posts/{slug}/comments` | none, rate-limited | optional native comment | FR-015 |
| C-16 | `GET /api/v1/releases`, `/releases/{id}` | bearer | release/observability | NFR-013/015 |

Conventions: bearer token (short-lived, OIDC-issued); JSON; ISO-8601 UTC;
idempotency key header on publish/schedule/export; errors as RFC 9457
problem+json; all mutations append audit rows.

Full OpenAPI 3.1 contract: [`api/openapi.yaml`](./api/openapi.yaml).

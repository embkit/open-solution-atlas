# 03 · Domain Model

## Bounded contexts

| Context | Responsibility | Owns |
|---|---|---|
| **Authoring** | Drafts, revisions, media, metadata editing | Post (draft), Revision, MediaAsset |
| **Publishing** | Build, release, URL governance, scheduling | Release, Redirect, Post (published projection) |
| **Catalog** | Taxonomy, indexes, search index | Tag, Series, SearchIndex |
| **Syndication** | Feeds, sitemap, SEO artifacts | FeedItem (projection), SitemapEntry |
| **Interaction** | Webmentions, comments, moderation, spam | Mention, Comment, ModerationAction |
| **Insight** | Aggregated, anonymous analytics | PageViewEvent → aggregated stats only |
| **Ownership** | Export/restore of everything above | ExportBundle |

Interaction and Insight never feed back into Authoring content; they are
downstream-only contexts (prevents reader data from leaking into exports of
content beyond approved mentions, BR-13).

## Core aggregates

### Post (aggregate root)

```
Post
├── identity: id (uuid), slug (unique, immutable post-publish)
├── content: title, summary, bodyMarkdown, bodyHtml (rendered projection)
├── classification: Tag[*], Category?, Series? (+ position)
├── media: MediaAsset[*] (ordered embeds, each alt-text or decorative flag)
├── licensing: licenseId
├── lifecycle: status, createdAt, publishedAt?, updatedAt, revisedAt
├── seo: canonicalUrl, ogImage?, metaDescription?
└── invariants (enforced by aggregate, not by UI)
    • DRAFT may be deleted; PUBLISHED may only be unpublished (410), never hard-deleted silently
    • slug change while PUBLISHED is legal only together with a Redirect (301)
    • publish requires metadata completeness (FR-004) and image a11y (FR-003)
    • visible to public ⇔ status=PUBLISHED ∧ publishedAt ≤ now (BR-07)
```

### Revision
`(postId, revisionNo, snapshotMarkdown+frontmatter, author, createdAt,
note?)` — append-only; restore creates a **new** revision, never rewinds.

### MediaAsset
`id, originalFilename, contentType (allowlist), bytes (≤5MB), sha256,
altText|null, decorative:bool, storageKey, width, height`. The sha256
deduplicates identical binaries while embeds may carry different alt text.

### Release
`id, contentTree hash, includedPostIds[], feedVersion, sitemapVersion,
status (BUILDING|READY|DEPLOYED|FAILED), createdAt, deployedAt?`.
Atomic unit of publication (NFR-015): a Release is what readers see, all or
nothing.

### Redirect
`fromPath, toPostId|toUrl, type (301|410), createdAt, reason`. Managed
invariant: no chain (redirects resolve in one hop), no loops.

### Mention (Webmention)
`id, sourceUrl, targetPostId, type (REPLY|LIKE|REPOST|BOOKMARK|MENTION),
authorName?, authorUrl?, contentHtml (sanitized), receivedAt,
verifiedAt?, status (PENDING|APPROVED|REJECTED|BLOCKED)`.
Idempotency key: unique `(sourceUrl, targetPostId)` (BR-09).

### Comment (optional aggregate)
mirrors Mention with `name, url?, markdownBody, htmlSanitized, spamScore`.

## Relationships (logical ER)

```
Post 1──* Revision
Post *──* Tag          (normalized; post max 8)
Post ?──1 Series       (ordered position within series)
Post 1──* MediaAsset   (via ordered embeds)
Post 1──* Mention      (only verified ones approved)
Post 1──* Comment      (when native comments enabled)
Post 1──* FeedItem     (projection, GUID = canonicalUrl)
Release *──* Post      (posts included in a published tree)
Post 1──? Redirect     (when slug retired/merged)
```

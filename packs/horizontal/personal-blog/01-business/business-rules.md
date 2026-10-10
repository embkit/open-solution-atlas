# 01 · Business Rules

| ID | Rule | Rationale |
|---|---|---|
| BR-01 | Every published post has exactly one canonical URL; `https`, trailing-slash policy fixed site-wide | SEO + link stability |
| BR-02 | Every post has: title, slug, author, created date, published date, license; body in Markdown | Required metadata completeness |
| BR-03 | Slug = lowercase ASCII kebab-case, max 80 chars; unique across all posts including unpublished | URL safety, collision avoidance |
| BR-04 | Before first publish slug is editable; after first publish it is immutable except via explicit redirect action | Existing links must never 404 silently |
| BR-05 | Tags are normalized (trim, lowercase fold per language) before storage; max 8 tags per post | Taxonomy hygiene |
| BR-06 | Unpublishing serves `410 Gone`; renaming/merging creates a `301`; no URL is ever left dangling silently | Reader/crawler contract |
| BR-07 | A post is publicly visible iff status = PUBLISHED and `published_at <= now` | Schedule semantics |
| BR-08 | Feed items keep a stable GUID = canonical URL; edits update the item, never duplicate it | RSS reader behavior |
| BR-09 | Webmentions are idempotent by `(source, target)`; duplicates update state | Network retries are normal |
| BR-10 | Images in published content must carry non-empty alt text; decorative images explicitly marked | WCAG 2.1 AA |
| BR-11 | No anonymous write path reaches public content: publish needs the author identity; comments/mentions need verification + moderation | Spam/defacement defense |
| BR-12 | All third-party requests (fonts, analytics, syndication embeds) are declared in the privacy page; default deployment emits none without consent | Privacy-by-default |
| BR-13 | Export must include received Webmentions; export never includes IP addresses or raw access logs | Ownership without leaking readers |
| BR-14 | Drafts are never included in sitemap, feeds, search index, or public builds | Leak prevention |

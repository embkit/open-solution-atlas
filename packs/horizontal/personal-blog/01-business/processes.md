# 01 · Core Business Processes

## BP-01 Publish an article (end-to-end)

```
author creates draft (CAP-01.1)
   │  autosave each edit (CAP-01.2)
   ▼
author attaches media, sets tags/slug/summary/license (CAP-01.3/01.4, CAP-02.1)
   │
   ▼
preview ──不满意──▶ edit loop
   │ satisfied
   ▼
publish now ──or── schedule for future time (CAP-03.1/03.2)
   │
   ▼
build static artifacts → deploy → CDN invalidate (CAP-03.4)
   │
   ├──▶ feed/sitemap regenerated (CAP-04.1/04.2)
   └──▶ optional: author manually syndicates canonical link (CAP-04.3)
```

- A draft's slug may change freely; **after first publish the slug is
  immutable** — renames require an explicit redirect (rule BR-06).
- Scheduled posts publish within a declared tolerance (see NFR-006), not at
  exact second precision.

## BP-02 Receive and display a response (Webmention)

```
external site posts a response linking to a post
   │  sends Webmention(source, target) to endpoint (CAP-05.1)
   ▼
validate target exists locally; fetch source; verify link-back exists
   │ fail ──▶ reject (4xx), no state persisted
   ▼
classify type (reply / like / repost / bookmark) + store as PENDING
   │
   ▼
moderation queue (CAP-05.2) ──reject──▶ discarded + sender blocked option
   │ approve
   ▼
published mention appears under target post; spam never rendered
```

Duplicate Webmentions for the same `(source, target)` update the existing
record rather than creating a new one (idempotency, BR-09).

## BP-03 Edit or retract published content

```
author edits published post → new revision (CAP-01.2)
   │  republish rebuilds page; feeds contain updated content with same GUID
   ▼
author unpublishes → URL returns 410 Gone with explanation page
   │  (deletion) or 301 redirect (merge/rename) (CAP-03.3, BR-07)
   ▼
search index, sitemap, feeds all consistent with current state
```

## BP-04 Reader discovery & return

```
reader lands from search/referral → post page (SEO metadata, canonical)
   ├──▶ navigates tag/archive/series (CAP-02.1/02.2)
   ├──▶ uses site search (CAP-02.3)
   └──▶ subscribes RSS (CAP-04.1) → reader polls feed → sees new post
```

## BP-05 Exit / migration (ownership exercise)

```
author triggers full export (CAP-07.1)
   ▼
zip/tar: Markdown files + frontmatter + media + taxonomy + mentions
   │  open formats only; readable without this software
   ▶
restore into a fresh install or a different engine
```

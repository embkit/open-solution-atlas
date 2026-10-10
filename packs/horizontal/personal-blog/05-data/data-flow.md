# 05 · Data Flow

## DF-1 Authoring → Public (write path)

```
editor autosave (≤1s)
   ├──▶ staging workspace (unsaved buffer, debounce 5s)
   └────commit──▶ content repo (new revision row + sha)
                        │
   publish action ──────┴──▶ release job:
                                  1. sync repo at commit
                                  2. validate frontmatter, links, a11y, feed schema
                                  3. render pages, indexes, feed, sitemap, search index
                                  4. upload artifacts to prefix/<sha>
                                  5. atomic pointer promotion → current=<sha>
                                  6. CDN purge (post, indexes, feed, sitemap)
                                  7. mark release DEPLOYED; else FAILED, old current intact
```

## DF-2 Read path

```
request ─▶ CDN ──hit──▶ artifact (no origin, no logs beyond edge aggregate)
              └─miss─▶ object storage (immutable prefix) ──▶ cache fill
Drafts exist nowhere on this path (BR-14): builder excludes them.
```

## DF-3 Ingestion path (mentions)

```
endpoint ─▶ job queue ─▶ egress-fetch source ─▶ parse+verify ─▶ sanitize
   ─▶ operational store (PENDING) ─▶ moderation ─▶ approved rows included
in next release rebuild of the target post page.
```
Mentions rendered at **build time** into static HTML — the public site still
has no runtime DB dependency.

## DF-4 Scheduling

```
cron/function (1 min) ─▶ due schedules (run_at ≤ now, post SCHEDULED)
   ─▶ invoke same publish pipeline ─▶ attempts++ ─▶ 3 fails ⇒ alert (FR-009)
```

## DF-5 Backup & export

```
content repo ──mirror──▶ remote git (continuous)
operational DB ──snapshot──▶ encrypted off-region bucket (daily, 30-day retention)
                            └─ restore test weekly (drill, see 08-quality/failure-and-dr.md)
export action ─▶ repo archive + mentions/comments/redirects/taxonomy (JSON/CSV)
                 + manifest.json(format version) = ExportBundle (no IPs/logs — BR-13)
```

## Consistency rules

1. Feed GUID ⇒ canonical URL (never reused).
2. Sitemap, search index, tag pages, post page are all generated in the same
   Release — cross-artifact disagreement is impossible by construction.
3. Redirect table is evaluated by builder and by edge config; 410/301 exist
   even at CDN layer, so removed pages never fall through to 404 (BR-06).

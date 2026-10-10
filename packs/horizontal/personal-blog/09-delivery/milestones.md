# 09 · Milestones

Incremental, each independently demonstrable. Scope is the Must/Should rows
of the capability map; Could items deferred.

| M | Name | Outcome (demonstrable) | Exits when |
|---|---|---|---|
| M0 | Skeleton & pipeline | repo layout, content repo sync, builder renders a hello post to storage with atomic pointer promotion | one deploy promotes; rollback works; AC-008 basic |
| M1 | Authoring core | admin SPA + content API: drafts, autosave, revisions, media upload w/ validation & alt gate | AC-001..004 |
| M2 | Publishing & URLs | publish/unpublish/schedule, redirect table (301/410), feed+sitemap+SEO, tag/archive pages | AC-005/006/008/009/010/011/012 |
| M3 | Reader experience + search | public theme meeting E-01/02, lazy static search index, a11y gates | AC-007, AC-N01 |
| M4 | Interaction | Webmention endpoint + verify + moderation queue; rebuild on approve | AC-013/014 (comments deferred) |
| M5 | Observability & security hardening | security headers/CSP, CVE scan, probes, alerts, rate limits; SSRF/XSS corpora in CI | NFR-007 gates, AC-N02 |
| M6 | Ownership & DR | export/restore, backup snapshots, restore drill, cost model verified | AC-017/018, AC-N04/05 |
| M7 | Optional: comments, POSSE bridge | feature-flagged native comments; syndication link helper | AC-015 |

Dependencies: M1→M2; M0→all; M4 needs M2 release pipeline; M3 can parallel M4.

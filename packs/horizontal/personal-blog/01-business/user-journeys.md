# 01 · User Journeys

## J-01 Author: "finish and publish tonight's draft"

1. Open editor; draft list shows last-edited first with autosave status.
2. Write Markdown; live preview matches published typography.
3. Upload two images; system forces alt-text entry (a11y rule BR-10).
4. Add tags `python` and `testing`; accept suggested slug; mark summary.
5. Hit preview → check mobile layout.
6. Publish. Success screen shows the canonical URL and a "copy syndication
   link" button. Feed and sitemap updated automatically.
7. Close laptop. Nothing else to operate.

**Pain points this journey must avoid**: lost drafts, surprise URL changes,
"works on my machine" preview differences, forgotten manual deployment.

## J-02 Author: "publish while I'm on holiday"

Schedule the post for Tuesday 08:00 local. The system publishes without the
author being online; on failure it retries and notifies via the configured
outbound channel (e.g. email/webhook); the post never appears half-built.

## J-03 Reader: "read, verify, come back"

1. Arrive from a search engine on a 3-year-old post; page loads fast on a
   phone over a poor connection.
2. Reader notices publish **and last-revised** dates; sees the content
   license at the bottom.
3. Browses the `testing` tag, finds related posts in the same series.
4. Subscribes via RSS — no account, no email wall.

## J-04 Reader: "reply from my own blog"

Reader writes a response post on their own site, sends a Webmention. Their
reply appears under the article only after verification + moderation. No
account on the author's site is ever created.

## J-05 Author: "leave this platform"

One action exports the entire site in open formats into a single archive;
after restore elsewhere, URLs can be preserved (slugs and structure are
deterministic). This journey is the guarantee behind the project's promise;
it must be tested like a feature, not documented as an aspiration.

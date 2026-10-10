# 07 · Experience — Key Flows

This is not visual design; it specifies interaction contracts that any
implementation must honor.

## E-01 Reader — post page (public)

**Information order**: title → (publish date · last-revised date · reading
time) → content → license → tags/series nav → mentions/comments → post nav.
- Typography: system font stack; measure ≤ 72 chars; respects
  `prefers-reduced-motion` and dark-mode system preference.
- Images lazy-load with intrinsic dimensions (no layout shift, CLS = 0 target).
- No newsletter wall, no consent modal in default deployment.

## E-02 Reader — discovery

- Header persistent: Home, Tags, Archive, Search, RSS.
- Search opens a field that lazy-loads `search-index.json` on first focus;
  results update as the reader types (≥ 2 chars); Esc closes; keyboard
  navigable. No request ever leaves the origin.
- Tag/category/series pages: title, post count, paginated list; empty state
  for a tag with zero published posts never exists (builder doesn't emit it).

## E-03 Author — editor

Two-pane (Markdown / live preview), collapse to single-pane preview tab on
narrow screens.
- **Persistent status pill**: `Saved 12:04:31` / `Saving…` / `Offline —
  changes will sync`. Never ambiguous (FR-002).
- Publish button disabled with a tooltip listing missing fields until
  publish gates pass (FR-004): exact list, not generic "please complete".
- Schedule control: timezone-pinned date/time; confirmation line restates
  the absolute UTC moment.
- Dangerous actions (unpublish, slug change, draft delete) require typed
  confirmation; slug change dialog **previews the 301** that will be created.

## E-04 Author — media

- Drag/drop + paste images into editor; upload progress per file.
- Alt-text prompt is **blocking before publish**, with a one-click
  "mark as decorative" alternative; existing images missing alt surface in a
  pre-publish checklist.

## E-05 Author — moderation queue

- Columns/filter: Pending / Approved / Rejected / Blocked; each row: source
  site, verified link-back status, mention type chip, target post, received
  time, sanitized excerpt.
- One-key approve (a) / reject (r); block-source is deliberately two-step.
- Empty state: "No pending mentions — incoming responses are verified
  automatically."
- Approving enqueues a rebuild; the UI states which post page will update.

## E-06 States that must be designed

| Situation | Required user-visible behavior |
|---|---|
| Build failed after publish | Author sees red release with log link; public site still on previous release; clear "retry" |
| Scheduled post missed (3 fails) | Banner + alert email; post remains SCHEDULED, nothing half-published |
| Reader hits an old URL | 301 silent redirect for moves; styled 410 page with "this post was removed" + archive link |
| Webmention endpoint abused | Silent 429 for abusers; author sees summarized rate-limit activity, not noise |
| Reader on JS-disabled browser | Full content, archives, feeds, search form degraded to a note pointing to tags; core reading never requires JS |

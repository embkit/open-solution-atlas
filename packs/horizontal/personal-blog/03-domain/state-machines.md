# 03 · State Machines

## SM-01 Post lifecycle

```
                 ┌─────────┐
   create ──────▶│  DRAFT  │◀──────────────┐
                 └────┬────┘               │
          edit/autosave│              restore revision
                 ┌─────▼──────┐      (creates new revision)
                 │ SCHEDULED  │
                 └─────┬──────┘
            publish now│ scheduler fires (FR-009)
                 ┌─────▼──────┐  unpublish   ┌────────────┐
                 │ PUBLISHED  │─────────────▶│  UNPUBLISHED│
                 └─────┬──────┘              └──────┬──────┘
        edit published │ creates revision+rebuild   │ republish
                       └──────────────▶ republished  │
                                                 ◀──┘
```

Guard rules:
- DRAFT/SCHEDULED → PUBLISHED: metadata completeness (FR-004) + alt-text
  (FR-003) + build success.
- PUBLISHED → UNPUBLISHED: emits a Release that serves 410 at the URL.
- UNPUBLISHED → PUBLISHED: same URL reactivates (no new slug unless author
  creates a redirect).
- No transition may produce a state where feeds/index disagree with pages
  (Release atomicity, NFR-015).

## SM-02 Release lifecycle

```
BUILDING ──build+tests ok──▶ READY ──deploy ok──▶ DEPLOYED (immutable)
   │                          │
   └──failure──▶ FAILED       └──deploy fail──▶ FAILED ──retry──▶ BUILDING
```
- FAILED never replaces the currently DEPLOYED release; readers keep the
  previous complete site.
- Each Release records content-tree hash; deploys are reproducible.

## SM-03 Mention lifecycle

```
incoming HTTP ──syntactic/SSRF checks fail──▶ REJECTED (4xx, nothing stored)
      │ pass
      ▼
  PENDING (stored, 202)
      │ fetch source + verify link-back fails ──▶ REJECTED
      │ pass (typed)
      ▼
  VERIFIED-PENDING-MODERATION
      ├── author approve ──▶ APPROVED  (rendered, sanitized)
      ├── author reject  ──▶ REJECTED
      └── author block source ──▶ BLOCKED (future sends auto-rejected)
```
Re-delivery of an existing `(source,target)` updates the record in place
(BR-09) and resets moderation only when verified content changed.

## SM-04 Revision append-log

`revision n` —(edit/save)→ `revision n+1` (never updates/removes prior).
"Restore" = create revision n+2 with an older snapshot.

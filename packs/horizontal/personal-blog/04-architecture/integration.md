# 04 · Integration

## Integration inventory

| # | Counterparty | Protocol | Direction | Data | Frequency |
|---|---|---|---|---|---|
| I-01 | Content Git remote (hosted or self-hosted) | HTTPS / SSH git | both | Markdown tree, media, config | on every save/publish; also valid manual channel |
| I-02 | Object storage / static host | S3-compatible API | out | Release artifacts | per Release |
| I-03 | CDN purge API | HTTPS REST | out | invalidation paths/wildcards | per Release |
| I-04 | External Webmention senders | HTTP `POST` (form-encoded) | in | source, target URLs | event-driven |
| I-05 | Source pages of mentions | HTTP `GET`, egress | out | HTML fetch for link verification | per inbound mention |
| I-06 | Feed readers / crawlers | HTTP `GET` XML | out | RSS/Atom, sitemap | poll-driven |
| I-07 | Auth provider (optional delegated login) | OAuth 2.0 / OIDC | both | author identity only | login |
| I-08 | Alert channel | SMTP or webhook | out | schedule/build failures | on failure |
| I-09 | Syndication targets (optional) | their APIs/manual | out | canonical link only | manual (POSSE) |

## Contract rules

- **Inbound is untrusted by definition** (I-04/I-05): schema validation,
  size caps, egress SSRF allowlist (no private IP ranges, no cloud metadata
  endpoints), redirect-follow limits, timeout ≤ 5 s.
- **Outbound release path is idempotent**: upload to a versioned prefix keyed
  by content hash; promotion is a single pointer/metadata swap; retries are
  safe (NFR-015).
- **No reader-data leaves the system** except explicit, enabled-by-opt-in
  integrations (tracking manifest, CTL-002).
- **External APIs degrade, never block publishing**: I-03/I-08/I-09 failure
  must not roll back a successful Release; they queue and alert.

## Data flow for a mention (detailed)

```
POST /webmention ──▶ validate form ──▶ enqueue job (202 immediately)
                                              │
                            fetch source (egress allowlist, UA declared)
                                              │
                 parse HTML (sandboxed) ──▶ find <a href=target>
                      │ absent/unreachable ──▶ mark REJECTED
                      ▼ present
            classify microformats (h-entry): reply/like/repost/bookmark
                      ▼
            store PENDING (sanitized excerpt) ──▶ moderation queue
```

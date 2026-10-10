# 04 · Observability

The operator is a single person who may not look for months: observability
must be **push-based and boring**. No dashboards to watch.

## Signals

| Layer | Signal | Where | Action threshold |
|---|---|---|---|
| Builder | build result, duration, warnings (broken links, a11y violations) | build log + persisted per Release | any failure = red status on admin home; a11y/link failures block deploy |
| Deploy | promotion success, CDN purge result | release record + I-03 log | purge failure queues retry + alert; never rolls back release |
| Scheduler | scheduled posts due vs published | job log each minute | 3 failed attempts → alert channel (FR-009) |
| Webmention ingest | received, verified, rejected counts; verification latency | service log, daily digest mail (opt-in) | none blocking; backlog > 1 h surfaces in admin |
| Public site | external uptime probe (GET homepage + newest post) every 5 min from ≥2 regions | third-party probe | 2 consecutive failures → alert |
| Edge security | auth failures, rate-limit trips, sanitizer rejects | service log | bursts summarized; no reader-facing detail |
| Backups | last snapshot timestamp + restore-test result | weekly summary | stale > 36 h or failed restore test → alert |

## SLOs (author-facing, not contractual)

- Public availability 99.9 %/month (NFR-004).
- Publish-to-visible ≤ 120 s (build + deploy + cache) at ≤ 500 posts.
- Webmention accepted → visible after approval within 5 min processing time
  (moderation latency is human and unmeasured by SLO).

## Privacy of telemetry itself

- Operational logs contain no reader IPs after 24 h; log scrubbing happens at
  the edge, not in batch later.
- No APM/RUM third party in the default deployment.

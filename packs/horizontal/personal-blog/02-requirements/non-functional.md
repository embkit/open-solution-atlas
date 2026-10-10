# 02 · Non-Functional Requirements

Targets assume the standard context: single author, ≤ 500 posts, ≤ 10 GB
media, ≤ 50 k visits/month with link-driven spikes up to 100× hourly mean.

| ID | Category | Requirement (measurable) |
|---|---|---|
| NFR-001 | Performance — public | Post page LCP ≤ 2.5 s on 4G mobile; TTFB ≤ 200 ms (CDN cache hit); fully static, zero origin dependency on cache hit |
| NFR-002 | Performance — authoring | Editor autosave completion ≤ 1 s p95; preview render ≤ 300 ms for 20 k-word posts |
| NFR-003 | Scalability | Sustains a 100× traffic spike with no degradation because the public tier is a CDN-served static artifact set; no capacity planning needed to 1 M requests/day |
| NFR-004 | Availability | Public site monthly availability ≥ 99.9 % excluding declared hosting windows; authoring/management plane best-effort single-node (downtime never affects already-published content) |
| NFR-005 | Durability | Content loss window ≤ 5 min: every save is written to durable storage; complete content mirrored to ≥ 2 locations (working store + versioned backup) |
| NFR-006 | Scheduling accuracy | Publish latency vs. `published_at` ≤ 60 s under normal operation (see FR-009) |
| NFR-007 | Security | No public write surface except Webmention/comment endpoints; management API requires strong auth (MFA-capable); all inbound untrusted HTML sanitized; A+ TLS configuration; dependency CVE scan in build |
| NFR-008 | Privacy | Default deployment: no third-party requests, no non-essential cookies, no stored reader IPs beyond 24 h; analytics aggregated/anonymized (supports CTL-001) |
| NFR-009 | Accessibility | All public pages meet WCAG 2.1 AA; automated a11y checks run in build and fail on violations |
| NFR-010 | Compatibility | Public pages: current + previous major of Chrome/Firefox/Safari/Edge; responsive 320 px–2560 px; feed validates against RSS 2.0 & Atom 1.0 validators |
| NFR-011 | Portability | 100 % of content exportable in open formats (Markdown, JSON, media originals); no proprietary binary format anywhere on the content path |
| NFR-012 | Maintainability | Deploy via single command; ≤ 30 min from zero to working personal site for a technical author; security updates merge via bot PRs and need no manual server surgery |
| NFR-013 | Observability | Build/deploy success/failure visible; weekly backup verification result visible; public uptime check from external probe (see 04-architecture/observability.md) |
| NFR-014 | Cost | Production hosting cost ≤ 5 USD/month at baseline traffic (object storage + CDN free tiers are typical) |
| NFR-015 | Build correctness | Every deploy is reproducible and atomic: readers see either the previous complete site or the new complete site; feed/post/index versions never mix |

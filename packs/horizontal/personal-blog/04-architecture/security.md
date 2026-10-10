# 04 · Security

## Trust boundaries & threat model

Assets worth protecting, in priority order:
1. Author identity / publishing rights (defacement risk)
2. Reader safety (XSS via mentions/comments; privacy)
3. Content durability (integrity/availability of writing)
4. Operational credentials

| Threat | Mitigation |
|---|---|
| Account takeover → malicious publish | OAuth/OIDC to a trusted IdP (or strong password + TOTP MFA), short-lived tokens, session revoke; single identity; admin UI hosted on a separate `/admin` origin with IP allowlist option |
| Stored XSS from Webmentions/ comments | Server-side allowlist sanitizer on ingest; render only approved HTML; `rel="nofollow noopener ugc"`; CSP with no inline scripts on public pages |
| SSRF via Webmention source fetch | Egress allowlist; block RFC1918/link-local/metadata IPs (169.254.169.254); DNS-rebinding guard; cap response 2 MB; no cookies/credentials on fetch |
| Spam flood | Per-IP & per-source rate limits, adaptive throttle, moderation-by-default, optional proof-of-work/honeypot on comment form |
| Media upload abuse | Authn required; type allowlist + magic-byte sniff; size cap; content-disposition isolation; serve user media from a cookieless asset origin |
| Supply-chain on build | Pinned lockfiles; CVE scan fails build (NFR-007); signed/immutable release artifacts; builder has no production credentials beyond write-scoped storage token |
| Content tampering | Releases keyed by Git commit hash; pointer promotion is the only mutation; audit log (CTL-010); repo itself is signed/protected-branch |
| TLS misconfiguration | HSTS preload, modern TLS only, A+ target; automatic certificate renewal with expiry alerting |
| Enumeration/scraping of reader traces | No reader accounts; IPs retained ≤ 24 h; analytics aggregated; privacy page generated from manifest |

## Security headers (public pages)

```
Content-Security-Policy: default-src 'self'; img-src 'self' https:; style-src 'self';
                         script-src 'self'; frame-ancestors 'none'; base-uri 'none'
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```
(Exact policy is version-controlled; third-party scripts exist only when an
explicit tracking-manifest entry exists — CTL-002.)

## Backup & secrets

- Secrets never in the content repo; injected at runtime.
- DB snapshots encrypted; restore tested monthly (see failure-and-dr.md).

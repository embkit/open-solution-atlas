# 08 · Test Strategy

## Levels & coverage targets

| Level | What | Tooling character | Gate |
|---|---|---|---|
| Unit | domain rules (slug, BR-03/04/05; post invariants; mention idempotency; redirect loop/chain detection; sanitizer) | fast, no I/O | ≥ 90 % line coverage on domain + sanitizer |
| Contract | OpenAPI conformance of management & ingestion endpoints | schema-validated requests/responses; RFC 9457 error shape | every endpoint |
| Integration | repo→builder→release→storage promotion; scheduler; mention verify pipeline | ephemeral storage + git fixture repos | happy path + each failure injection |
| Build-time | broken internal links, missing alt, a11y axe rules, feed/sitemap validity, JSON-LD validation | builder plugins | **any violation fails the release** |
| E2E | publish journey (E-03), reader journey (E-01/02), moderation (E-05), export/restore (J-05) | browser automation against staging | full AC list above |
| Performance | AC-N01 Lighthouse in CI on reference pages; AC-N03 spike test quarterly | — | regression tracked, not noisy per-commit |
| Security | dependency CVE scan, CSP/header test, XSS payload corpus through mention path, SSRF corpus (169.254.169.254, localhost, DNS-rebind) | SAST + payload corpora | high/Critical CVE = build red |
| Property | invariants across random operation sequences: no bare 404 after slug ops; feed GUID stability; releases never observed mixed | property-based | 1,000 sequences nightly |

## Test data

- Synthetic fixture corpus: 520 posts, 9 tags, 2 series, 1,300 media assets,
  40 mentions incl. malicious payloads, 6 redirects. No real reader data.
- Time-dependent tests use a controllable clock for scheduling/feed windows.

## Environments & promotion

```
PR → lint + unit + contract + build-time checks
staging (every main merge) → integration + E2E + security + Lighthouse
release tag → same suite + restore drill (monthly minimum)
```

## Manual checks (explicitly marked)

- AC-N05 cost model review.
- Reader-side feel on a low-end Android device per release candidate.

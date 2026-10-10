# 09 · Agent-Executable Task Map

Tasks are sized for one focused agent change each, with a verification hook.
IDs `T-xx`; each maps to milestone and requirement IDs. Execute milestone by
milestone; do not skip verification hooks.

## M0 — Skeleton & pipeline

- **T-01** Define content-repo format & sync: frontmatter schema, repo
  watcher/poll, projection into post_metadata. Verify: fixture repo
  round-trips. [FR-001]
- **T-02** Build engine: Markdown render with fixed renderer shared by
  preview; page/index/feed/sitemap generators behind one build entrypoint.
  Verify: snapshot output. [AC-001, AC-011/012]
- **T-03** Artifact publisher: hash-prefixed upload, current-release pointer,
  purge. Verify: inject mid-promote failure → old site intact. [AC-008,
  NFR-015]
- **T-04** Release records + rollback command. Verify: rollback serves prior
  release within 5 min. [F-04]

## M1 — Authoring core

- **T-05** Admin SPA shell + OIDC/bearer session on isolated admin origin.
  Verify: unauthenticated API calls 401. [NFR-007]
- **T-06** Posts CRUD with EARS-aligned validation, slug rules BR-03.
  Verify: contract tests vs OpenAPI. [FR-001/004]
- **T-07** Autosave staging + revision append-log + restore-as-new-revision.
  Verify: AC-002 property tests. [FR-002]
- **T-08** Media upload: type magic-byte sniff, size cap, sha dedup, alt/
  decorative gate, asset origin + CSP. Verify: AC-003 + XSS-as-svg corpus.
  [FR-003, CTL-008]
- **T-09** Pre-publish gate endpoint returning exact missing-field/image
  list. Verify: AC-004. [FR-004, BR-10]

## M2 — Publishing & URLs

- **T-10** Publish/unpublish state machine service with guards. Verify: all
  SM-01 transitions incl. illegal ones rejected. [FR-008/010]
- **T-11** Scheduler worker (1-min tick, attempts, alerts, idempotent run).
  Verify: clock-controlled tests AC-009.
- **T-12** Redirect service: builder + edge rules, loop/chain detection,
  410 pages. Verify: AC-010 property suite. [BR-06]
- **T-13** RSS/Atom + sitemap + canonical/OG/JSON-LD emitters and validators
  as build gates. Verify: AC-011/012.
- **T-14** Taxonomy normalize/dedup/max-8 + index pages. Verify: AC-005/006.

## M3 — Reader experience + search

- **T-15** Public theme implementing E-01/02 incl. reduced-motion/dark,
  no-JS reading, security headers. Verify: axe + header tests, AC-N01.
  [NFR-009]
- **T-16** Static search index generator + in-browser search UI. Verify:
  AC-007 incl. drafts excluded and no-network assertion. [ADR-0004]

## M4 — Interaction

- **T-17** Webmention receiver: form validation, queue, SSRF-safe fetcher,
  microformat classifier, idempotent store. Verify: AC-013 + SSRF corpus.
- **T-18** Sanitizer + moderation endpoints + queue UI + rebuild trigger.
  Verify: AC-014 XSS corpus. [CTL-008]

## M5 — Observability & security

- **T-19** Build gates: link checker, a11y, CVE, feed/JSON-LD. Verify: gates
  fail on seeded defects.
- **T-20** Uptime probes, alert channel, admin release status, weekly
  backup-verification summary. Verify: chaos drill AC-N02. [F-01..F-09]

## M6 — Ownership & DR

- **T-21** ExportBundle job + restore flow. Verify: AC-017/018 in empty
  environment.
- **T-22** Snapshot scheduling, off-region copy, drill scripts + documented
  runbook. Verify: monthly drill AC-N04.

## M7 — Optional

- **T-23** Feature-flagged comments: rate limit, honeypot/POW, spam scoring,
  same moderation queue. Verify: AC-015.
- **T-24** POSSE link helper (manual-first). Verify: syndication metadata
  present; no automated third-party calls by default. [BR-12]

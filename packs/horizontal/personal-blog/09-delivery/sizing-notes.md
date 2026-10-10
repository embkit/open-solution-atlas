# 09 · Sizing, Effort & Risk

## Reference build profile

- 1 full-stack developer comfortable with static tooling + one thin service;
  L3 spec → running production-grade site ≈ 4–6 focused weeks (M0–M6),
  dominated by hardening (M4/M5) and export/DR (M6), not page rendering.
- With multiple coding agents against this pack, implementation of the
  tracked tasks is expected to compress to days; the non-compressible work is
  review gates, security validation, and real-provider setup.

## Team shape options

| Shape | Notes |
|---|---|
| Solo technical author | reference case; choose managed storage/CDN/OIDC to avoid ops |
| Dev + reviewer | recommended minimum for a public deployment; reviewer owns
security & AC verification |
| Multi-agent build | T-02/T-03 first (contracts for everything else); parallelize
M3/M4; serialize all release-pipeline tasks |

## Top risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Webmention/comment abuse (spam, SSRF) | High | High | verify-before-store, sanitizer corpora, moderation-by-default, bounded queue (T-17/18) |
| Provider lock-in creeps into build/hosting choices | Medium | High | artifacts must be plain files served by any static host; provider only in `variants/` |
| Feed/SEO regressions on change | Medium | Medium | official validators as build gates (T-13) |
| Silent scope growth (multi-author, multi-tenant) | Medium | High | out-of-scope list in README; reject PRs that require tenant isolation |
| Export promise rots | Medium | High (trust) | quarterly drill is a tracked CI/staging event, not docs (T-21/22) |
| CN deployment needs ICP filing + different edge choices | situational | Medium | explicit variant overlay; never entangle core (CTL-009) |

## Variant candidates (not core)

1. `static-pages-only` (no authoring service; Git + CI only — cheapest).
2. `managed-cdn` provider overlays.
3. `cn-hosting` (ICP variant; compliant analytics/comment choices).
4. `self-hosted-origin` (single VPS with reverse proxy; backup story adjusted).

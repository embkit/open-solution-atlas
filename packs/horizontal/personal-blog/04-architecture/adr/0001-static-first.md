# ADR-0001 — Static-public, thin-dynamic-edge architecture

- Status: Accepted
- Date: 2026-10-08
- Deciders: pack maintainers

## Context

Read traffic is modest but spike-prone; the operator is a non-on-call
individual; public pages change only when the author acts. Requirements
demand near-perfect public availability during operator absence (NFR-004),
strong security with minimal surface (NFR-007), sub-5 USD/month cost
(NFR-014), and a ≤ 2.5 s mobile LCP (NFR-001). Options:

1. **Traditional dynamic CMS** (PHP/Node + DB rendering per request)
2. **Static-first** — pre-built artifacts on CDN, small dynamic service only
   for authoring and ingestion
3. **Hybrid ISR** — static shell with server-rendered/edge functions per page

## Options considered

1. **Dynamic CMS** — easy editing UX; but continuous server/DB upkeep, large
   attack surface, cache-dependent performance, security rot during months of
   neglect, cost floor higher.
2. **Static-first** — best availability (cache serves even if everything
   dynamic dies), smallest attack surface, cheapest, fastest; build-time
   complexity for site-wide changes and a separate dynamic edge for
   mentions/scheduling.
3. **Hybrid ISR** — flexible; introduces per-request failure modes and
   debugging complexity that a single operator cannot service.

## Decision

Adopt static-public/thin-dynamic-edge (option 2). The only live runtime is
the authoring/ingestion service; public content is a versioned, atomically
promoted static Release.

## Consequences

- Positive: NFR-001/003/004/007/014 fall out naturally; "fail static" means
  operator absence cannot take the site down.
- Negative: site-wide rebuild cost grows with content (acceptable to
  thousands of posts; incremental builds specified); comments/mentions need a
  separate service and trigger rebuilds.
- Harder to change later: truly real-time public features (live presence,
  per-reader personalization) are structurally excluded — consistent with
  scope.

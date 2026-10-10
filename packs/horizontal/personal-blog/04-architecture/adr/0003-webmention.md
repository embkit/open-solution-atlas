# ADR-0003 — Webmention as the default interaction mechanism

- Status: Accepted
- Date: 2026-10-08
- Deciders: pack maintainers

## Context

Readers should be able to respond without accounts (stakeholders table;
BR-11), spam must never render, and readers' personal data should be minimal
(CTL-001). Options:

1. Native account-free comments, moderated
2. Third-party comment SaaS
3. Webmention-centric interaction (W3C), with optional native comment form
4. No interaction at all

## Options considered

1. **Native comments** — familiar; invites spam, requires storing
   name/email-ish data and a moderation burden forever.
2. **Third-party SaaS** — zero ops; violates privacy-by-default and ownership
   (reader data leaves the system), contradicts CTL-001/FR-017.
3. **Webmention-centric** — replies live on responders' own sites; identity
   is a URL, not an account here; data minimal; federated, open, POSSE-
   aligned; discoverability is lower for non-IndieWeb readers — mitigated by
   offering the optional native form (FR-015).
4. **None** — removes a core community signal (BP-02).

## Decision

Webmention receiving + verification + moderation is the default (FR-013/014);
native comments are an explicitly optional, off-by-default feature
(FR-015). No third-party comment service in any default path.

## Consequences

- Positive: no reader accounts, minimal PII, interaction data is owned and
  exportable (BR-13), aligns with IndieWeb/POSSE.
- Negative: must run an endpoint with SSRF/spam defenses (security.md);
  mainstream readers find mentioning unfamiliar — addressed by how-to UI
  copy and the optional form.

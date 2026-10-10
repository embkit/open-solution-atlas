# 00 · Regulatory Landscape

A personal blog carries almost no sector-specific regulation, but four
general regimes apply. Requirements derived here are traced in
`02-requirements/compliance.md` as `CTL-*`.

| Regime | When it applies | Core obligations affecting design |
|---|---|---|
| **Privacy laws** (GDPR/UK-GDPR, CCPA/CPRA, PIPL 个保法) | Collecting any personal data — including comment metadata, analytics cookies, server logs | Lawful basis; minimal collection; privacy policy; deletion on request; no intrusive third-party trackers by default |
| **Cookie/tracking consent** (ePrivacy-style rules) | Non-essential cookies or fingerprinting | Default to cookieless, privacy-preserving analytics; consent banner only if non-essential tracking is enabled |
| **Copyright & licensing** | All posts, embedded media, comments | Explicit per-post license; DMCA-style takedown contact; media provenance recorded; comment licensing terms |
| **Accessibility** (ADA/EN 301 549 — applies where public-sector reach is claimed) | Public pages | WCAG 2.1 AA semantic markup, alt text, keyboard navigation, contrast |

### Regional deployment notes

- **Mainland China**: hosting a public website requires ICP filing (备案) on
  the domain; real-name rules apply to interactive features. Tracked as a
  deployment `variant`, never baked into the vendor-neutral core.
- **EU**: IP addresses in access logs are personal data; anonymize or set
  short retention.

### What is explicitly *not* required

- No payment/PCI surface, no accounts for the public, no sector compliance
  (HIPAA/FINREG) — keeping this surface small is a design goal.

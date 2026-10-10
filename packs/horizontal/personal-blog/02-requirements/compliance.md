# 02 · Compliance Controls

Derived from `00-context/regulatory-landscape.md`. Controls are implemented
as concrete behavior and verified by acceptance criteria.

| ID | Control | Implementation commitment | Traces |
|---|---|---|---|
| CTL-001 | Data minimization & privacy-by-default | No accounts for readers; default analytics cookieless & self-hosted; no third-party embeds without explicit enablement; IPs not persisted | GDPR Art.5, PIPL 第6条, NFR-008, FR-016 |
| CTL-002 | Privacy notice | Versioned privacy page listing every data item, purpose, retention; rendered automatically from a machine-readable tracking manifest so it cannot silently drift | GDPR Art.13 |
| CTL-003 | Erasure path | Single operator action to delete a comment/mention + its metadata; documented 30-day response commitment template for reader requests | GDPR Art.17, PIPL 第47条 |
| CTL-004 | Cookie consent | No consent UI unless non-essential tracking is enabled; enabling such tracking turns on a deny-by-default banner automatically | ePrivacy |
| CTL-005 | Content licensing | Per-post license selector (default CC BY-SA 4.0 or author-chosen); license rendered on page + in feed; comments submitted under stated terms | Copyright |
| CTL-006 | Takedown contact | Fixed `/rights` page with abuse/copyright contact and response SLA | DMCA-style |
| CTL-007 | Accessibility conformance | Semantic HTML, alt enforcement (BR-10/FR-003), keyboard operable, AA contrast; CI a11y gate | WCAG 2.1 AA |
| CTL-008 | Untrusted-input safety | Webmention/comment HTML sanitized (allowlist), links `rel="nofollow noopener"`, SSRF protection on source fetch, rate limiting | Security + abuse law |
| CTL-009 | Regional deployment variance | ICP-filing variant for CN hosting exists as an explicit `variants/` overlay; core never assumes a jurisdiction | Local filing rules |
| CTL-010 | Auditability | Authoring actions (publish/unpublish/redirect/moderation) append an immutable audit log with actor + timestamp | General accountability |

# 04 · Security

> Framing: ISO 28000:2022 (supply-chain security management) at standard
> level; article-level control mapping is an open item `(A)` — see
> [`../SOURCES.md` §4](../SOURCES.md).

## Threat-surface notes specific to TMS

- **Partner channel spoofing**: forged carrier tenders/status messages can
  redirect goods or fake delivery. All carrier channels authenticate
  (mutual TLS or signed messages) and every message is logged per adapter
  (FR-022 audit).
- **Invoice fraud**: bank-detail changes and phantom invoices. Settlement
  honors only invoices matched to executed legs (BR-05) and only to the
  registered carrier identity; payee changes require out-of-band verification
  `(A)`.
- **DG data tampering**: loading an *attacker-chosen* "regulation edition"
  would bypass BR-07. Editions are integrity-protected and import-audited;
  NFR-010 guards dispatch on edition validity.
- **Location PII**: driver position streams are personal data (CTL-06,
  GDPR): minimized at ingest, retention-capped, access-logged.

## Controls summary

| Area | Control | Ref |
|---|---|---|
| Access | SSO + least-privilege RBAC; separation of duties dispatcher vs. settlement approver `(A)` | NFR-012 |
| Audit | Append-only audit of dispatch overrides, tender outcomes, match results, disputes | BR-11, CTL-05 |
| Channels | Authenticated carrier/partner channels; message-level audit logs | FR-022 |
| Data integrity | Snapshot immutability; edition integrity; compensating events only | BR-04, BR-11 |
| CN baseline | 等保2.0 zone controls at standard level | CTL-07 |

> The sibling `iam-platform` pack is the identity/RBAC reference; this pack
> does not re-specify it.

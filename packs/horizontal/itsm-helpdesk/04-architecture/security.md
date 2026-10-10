# 04 · Security

> Framing: ISO/IEC 27001:2022 Annex A where cited; clause-level
> interpretations marked in [`../SOURCES.md`](../SOURCES.md) §4.

## Threat-surface notes specific to ITSM

- **Intake forgery**: spoofed email or unsigned webhook creating/resolving
  tickets (or leaking restricted KB). Controls: channel authentication,
  header rules + allow-lists, unregistered-requester sandbox (BR-13,
  FR-018), restricted-KB never served outside entitlement (FR-002).
- **Ticket content as an exfiltration path**: tickets carry PII, IPs,
  sometimes secrets pasted by users. Controls: content scanning hooks
  `(A)`, retention limits, GDPR/PIPL erasure with audit preservation
  (NFR-006, CTL-08).
- **Privileged path via change**: a malicious/errant RFC alters production.
  Controls: risk-class workflow, CAB evidence, emergency post-review
  (BR-09, CTL-04); agents cannot approve their own RFCs `(A)` SoD note.
- **Entitlement leakage**: security-classified incidents visible in search/
  exports. Controls: scope enforced server-side on list/search/export paths,
  classification inherited by linked records (BR-11, CTL-03).

## Controls summary

| Area | Control | Ref |
|---|---|---|
| Authentication | SSO via cross-pack `iam-platform`; no local passwords | NFR-008 |
| Authorization | RBAC by agent role + catalog/org scope; restricted classification | BR-11, CTL-03 |
| Audit | Append-only ticket/automation history; rule version stamped | BR-07, BR-14, CTL-07 |
| Intake trust | Authenticated channels; quarantine with raw evidence | BR-13, FR-018 |
| Change SoD | Approver ≠ implementer ≠ requester where feasible; emergency post-review | BR-09 `(A)` |
| Data protection | Retention windows, minimization, erasure preserving audit facts | NFR-006, CTL-08 |
| CN baseline | 等保2.0 zone controls, standard level | CTL-09 |

> The `iam-platform` pack is the identity/RBAC reference; this pack does not
> re-specify it.

# 05-data / Data Dictionary

Field-level definitions for core entities. Not exhaustive DDL; defines
meaning, type band, and classification. Classification: **OP** operational,
**REF** reference, **PII** personal data, **CTL** control/audit, **SENS**
sensitive secret material (never returned in clear).

## Identity / Account

| Field | Type | Definition / rule | Class |
|---|---|---|---|
| identity_id | uuid | immutable subject key | OP |
| realm_id | string | isolation scope; every query/token must match (BR-07) | CTL |
| identity_type | enum | workforce / customer / partner / service | REF |
| authoritative_source | string | system of record for existence (HRIS/dir/self) | REF |
| source_key | string | correlation key, unique within source (FR-002) | OP/CTL |
| lifecycle_state | enum | invited/provisioned/active/suspended/mover/leaver/disabled/purged (SM-1) | OP |
| org_unit_id | string | owning org unit (ABAC attribute) | REF |
| attributes | map | extensible profile; each with source & precedence | PII/REF |
| display_name / email | string | human identifiers | **PII** |
| is_federated | bool | true ⇒ no local password (BR-15) | REF/CTL |
| account.external_id | string | target-system identifier (per target) | OP |
| account.status | enum | active/disabled/pending (deprovisioning precedence BR-13) | OP/CTL |

## Credential / Authenticator

| Field | Type | Definition / rule | Class |
|---|---|---|---|
| credential.type | enum | password / totp / webauthn / recovery | REF |
| credential.aal | enum | assurance level this factor provides (BR-11) | REF |
| secret_ref | string | reference to stored material (hash/encrypted seed/public key) | **SENS** |
| password hash | — | memory-hard salted hash + pepper in HSM/KMS (BR-10) | **SENS/CTL** |
| webauthn public key | bytes | public key only; private key never stored (WebAuthn) | OP |
| credential.state | enum | pending/active/revoked (SM-1/03.5) | OP/CTL |
| last_used_at | ts | last successful use; supports anomaly detection | CTL |

## Session / Token / Grant

| Field | Type | Definition / rule | Class |
|---|---|---|---|
| session.assurance_level | enum | AAL bound at authentication (BR-11) | CTL |
| session.auth_time | ts | when the factor was verified; drives freshness/step-up | CTL |
| session.device_ref / source_ip | string | context binding & anomaly signal | CTL/PII |
| session.expires_at / absolute_expires_at | ts | idle timeout / absolute lifetime (BR-02) | OP |
| grant.scopes / audience | string[] | delegated authority + target resource (FR-010) | OP/CTL |
| token.token_type | enum | access / id / refresh | OP |
| token.jti | string | unique token id; used for revocation/replay defense | CTL |
| token.expires_at | ts | short-lived access token TTL (BR-01) | OP |
| token.family_id | string | refresh rotation lineage; reuse ⇒ family revoke (BR-01) | CTL |
| token.state | enum | active/used/revoked/retired | OP/CTL |
| refresh.reuse_detected | bool | set when a retired token is presented; triggers revocation | CTL |

## Consent

| Field | Type | Definition / rule | Class |
|---|---|---|---|
| consent.purpose / scope | string | processing purpose and data scope | OP/**PII** |
| consent.policy_version | string | version of the privacy/consent notice | CTL |
| consent.state | enum | granted / withdrawn (withdrawal = new record, BR-12) | OP/CTL |
| consent.method | enum | how consent was captured (self, dual-opt-in...) | CTL |
| granted_at / withdrawn_at | ts | immutable timestamps | CTL |

## Role / Permission / Assignment / Policy

| Field | Type | Definition / rule | Class |
|---|---|---|---|
| role.role_type | enum | business / technical / privileged | REF |
| role_permission | link | role → permission bundle | REF |
| entitlement.resource_scope | string | resource/org scope the entitlement applies to | REF |
| assignment.source | enum | direct/request/review/elevation/mapping (provenance, CTL-01) | CTL |
| assignment.valid_from / expires_at | ts | time-boxed access; expiry auto-removes (BR-05) | OP/CTL |
| assignment.state | enum | active/expired/revoked | OP |
| policy.effect_default | enum | deny-overrides (BR-14) | CTL |
| policy.version / status | string/enum | pinned on each decision; draft/published/retired | CTL |
| policy.author_id / approver_id | string | must differ (SoD, BR-08) | CTL |
| decision.effect | enum | permit / deny | CTL |
| decision.obligations | set | e.g. step-up, mask, log-level returned to PEP | CTL |
| decision.policy_version | string | enables decision reconstruction (FR-022) | CTL |

## Provisioning

| Field | Type | Definition / rule | Class |
|---|---|---|---|
| connection.target_type | enum | scim / ldap / app | REF |
| connection.credential_ref | string | vault-held credential (never in clear) (NFR-012) | **SENS** |
| connection.mapping_ref | string | attribute mapping (source→target) | REF |
| connection.health_state | enum | configured/testing/active/degraded/failed/suspended/decommissioned (SM-5) | OP/CTL |
| prov_operation.idempotency_key | string | (source,event_id,target,op) dedupe (BR-13) | CTL |
| prov_operation.status | enum | pending/success/failed/quarantined | OP |
| prov_operation.last_error | string | sanitized error (no secrets) | OP |

## Governance

| Field | Type | Definition / rule | Class |
|---|---|---|---|
| access_request.justification | string | business reason (mandatory) | OP/CTL |
| access_request.risk_tier | enum | computed risk for routing/approval depth | CTL |
| access_request.sod_state | enum | ok / conflict / mitigated (BR-03) | CTL |
| approval.approver_id | string | must not be the requester (SoD, BR-08) | CTL |
| elevation.window_start/window_end | ts | bounded window; auto-revoke at end (BR-05) | CTL |
| elevation.break_glass | bool | emergency path ⇒ post-hoc review required | CTL |
| review_item.decision | enum | certify / revoke / undecided (overdue ⇒ deny-safe, BR-04) | CTL |

## Audit / Decision (append-only)

| Field | Type | Definition / rule | Class |
|---|---|---|---|
| audit.event_id | ordered id | immutable, monotonic per stream | CTL |
| audit.event_type | enum | authentication/decision/admin/lifecycle/consent families (domain-model §4) | CTL |
| audit.actor_id / subject_id | string | who caused / who it concerns | CTL |
| audit.object_type / object_id | string | affected entity | CTL |
| audit.outcome | enum | success/failure/permit/deny/error | CTL |
| audit.context | map | source_ip, device, method, risk — sanitized | CTL |
| audit.occurred_at / recorded_at | ts | event time vs. record time (late arrivals) | CTL |
| audit.correlation_id | string | links session→decision→acting event | CTL |
| audit.prev_hash | string | tamper-evidence chain (BR-09/NFR-009) | CTL |

## Common conventions

- All timestamps UTC; realm-local time derivable. `occurred_at` (when it
  happened) is retained separately from `recorded_at` (when it was stored).
- Every mutable operational table carries a `version`; audit/decision rows
  are immutable.
- Secret material (`SENS`) is stored by reference to an HSM/KMS/vault only;
  it is never logged, returned in API responses, or embedded in audit.
- PII is minimized to purpose (BR-12); erasure anonymizes PII while
  preserving audit and consent facts (BR-09/BR-12).

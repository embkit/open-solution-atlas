# 02-requirements / Compliance Controls

Control requirements `CTL-01..CTL-07`, traced to standards/regulations and to
requirements. Core implements audit-grade controls; jurisdiction-specific
cryptography and privacy overlays are variants.

| ID | Control | Requirement / mechanism | Trace |
|---|---|---|---|
| **CTL-01** | Identity proofing & lifecycle integrity | Every identity has an authoritative source, a lifecycle state, and traceable JML provenance; deprovisioning precedence is enforced and orphans are detected | NIST SP 800-63A-4; ISO/IEC 27002 5.16; FR-001, FR-002, FR-003, FR-004, BR-13 |
| **CTL-02** | Authenticator & credential control | AAL-driven enrollment; no forced composition/rotation; breach-list check; salted+peppered hashing; throttling/lockout; phishing-resistant factors available | NIST SP 800-63B-4; ISO/IEC 27002 5.17, 8.5; WebAuthn/FIDO2; FR-005, FR-006, FR-008, BR-06, BR-10, BR-11 |
| **CTL-03** | Access control & separation of duties | Deny-by-default RBAC+ABAC; least privilege; SoD rule engine blocks conflicting grants absent independent mitigation | ISO/IEC 27002 5.3, 5.15, 5.18, 8.2, 8.3; XACML 3.0; FR-015, FR-016, FR-018, BR-03, BR-08, BR-14 |
| **CTL-04** | Privileged access governance | No standing admin by default; JIT elevation time-boxed with auto-revoke; periodic access review/certification with deny-safe overdue action | ISO/IEC 27002 5.18, 8.2; GB/T 22239-2019 (MLPS 2.0); FR-019, FR-020, BR-04, BR-05 |
| **CTL-05** | Audit logging & tamper-evidence | Immutable, append-only audit of authN, decisions and admin changes; hash-chained; query/export per scope; retention policy enforced | ISO/IEC 27001:2022 Annex A 8.15 (+ 5.33 protection of records); GB/T 22239-2019; FR-022, NFR-009, NFR-010, BR-09 |
| **CTL-06** | Cryptographic key & token protection | Signing keys/secrets in HSM/KMS; scheduled rotation with JWKS/metadata overlap; short-lived tokens; refresh rotation with reuse detection | ISO/IEC 27001:2022 Annex A 8.24; RFC 7517/8725; FR-014, FR-021, NFR-012, BR-01 |
| **CTL-07** | Privacy, consent & tenant isolation | Consent recorded immutably and revocable; data minimization; data-subject access/erasure hooks; realm/tenant isolation of data & tokens | GDPR (EU 2016/679) Arts. 6/7/15–17/30; ISO/IEC 27701; FR-023, FR-024, NFR-013, BR-07, BR-12 |

## Variant-deferred controls (declared, not core)

- **National/regional cryptography** (e.g. 商用密码 SM2/SM3/SM4 and
  algorithm mandates): core specifies *crypto-agility* (algorithm is
  configurable and keys are HSM-backed) but does not bake in a national
  algorithm suite → `xinchuang-cn` variant.
- **Cross-border data transfer & data residency** (e.g. GDPR transfer
  mechanisms, CN localization): core is deployment-agnostic; residency
  topology and lawful-transfer mechanics are variant/deployment policy.
- **Advanced/premium electronic signatures** (eIDAS QTSP, qualified
  timestamps): core supports signing and audit; qualified trust services are
  an integration variant.
- **Sector-specific guidance** (e.g. regulated-industry identity rules):
  expressed as variant overlays, never in the core pack.

> Core packs encode the *control obligation* and defer statutory text,
> algorithm suites and residency mechanics to variants/deployment policy.

# 04-architecture / Observability

Metrics, logs, traces, business/security signals, SLOs and personas. Traces
NFR-014; supports CTL-05 (audit) and CTL-04 (privilege governance).

## 1. Three telemetry planes

1. **Technical**: service latency/errors, token-issuance and JWKS health,
   PDP throughput/latency, queue/outbox lag, cache hit ratio, DB health.
2. **Operational (identity)**: authN volume by method/outcome, MFA
   enrollment coverage, provisioning success/drift, review campaign
   progress, session counts.
3. **Security (control)**: failed-login and lockout rates, anomalous login
   patterns, step-up frequency, decision denials, SoD blocks, elevation
   grants/uses, revocation actions, cross-realm rejections.

> Audit records (BC-7) are the **authoritative** security evidence; telemetry
> is for detection and SLOs and must never be the only audit source
> (CTL-05).

## 2. Key metrics & signals

| Area | Metrics |
|---|---|
| Authentication | login success/failure rate, latency p95 (NFR-001), factor mix (password/MFA/WebAuthn), step-up rate |
| Token | issuance latency (NFR-002), refresh-rotation count, reuse-detection events, revocation latency |
| Authorization | decision p95/p99 (NFR-004), permit/deny ratio, expectation cache hit, obligations issued |
| Lifecycle | provisioning ops/sec, success/retry/quarantine rate, reconciliation drift, deprovisioning latency (NFR-005) |
| Governance | open access requests/age, campaign completion %, overdue items, JIT elevation count/duration |
| Security | failed-login spikes, lockouts, impossible-travel / new-device signals, cross-realm rejects, SoD blocks |
| Platform | availability (NFR-006), outbox→SIEM lag, audit ingest rate (NFR-010), error rate |

## 3. Logging & traces

- Structured logs with a **correlation id** spanning login → session →
  token → decision → provisioning, and a per-realm dimension.
- Distinct **audit events** (immutable, hash-chained) vs. **technical
  logs** (retention-limited, redacted): never log secrets, tokens, passwords
  or OTP values.
- Distributed traces across IdP, PDP and provisioning; a decision trace
  exposes policy version and attribute sources consulted (without leaking
  sensitive attribute values).
- Realm isolation applies to logs/dashboards: a realm-scoped viewer sees
  only that realm's telemetry (NFR-013).

## 4. SLOs & alerts (initial)

| SLO | Target | Alert threshold |
|---|---|---|
| AuthN latency | p95 ≤ 500 ms (NFR-001) | p95 > 800 ms for 5 min |
| Token issuance | p95 ≤ 200 ms (NFR-002) | p95 > 400 ms for 5 min |
| PDP decision | p95 ≤ 20 ms (NFR-004) | p95 > 50 ms for 5 min |
| Core availability | ≥ 99.95%/mo (NFR-006) | any sev-1 outage |
| Verification path | ≥ 99.99%/mo (NFR-006) | JWKS endpoint errors |
| Deprovisioning latency | ≤ 15 min (industry-brief §5) | any leaver not revoked in SLA |
| Audit ingest integrity | append-only, 0 gaps (NFR-009) | **page on integrity violation** |
| Deprovisioning drift | 0 orphans after reconciliation | any orphaned active account |
| Failed-login anomaly | baseline-bounded | spike > threshold vs. baseline |

## 5. Dashboards / personas

- **IAM administrator**: authN/token/PDP health, provisioning drift, app
  onboarding status.
- **Security analyst (SOC)**: anomalous logins, lockouts, step-up and
  denial rates, active/expired elevations, revocation timeline.
- **Approver / resource owner**: pending requests, campaign items, SoD
  conflicts requiring mitigation.
- **Auditor / compliance**: campaign completion, evidence-export status,
  audit-query access (read-only).
- **Service owner**: per-app token/decision volume and error rate.

## 6. Synthetic/control monitoring

- Continuously assert **fail-closed** behavior: simulate PDP unavailability
  and verify permit-requiring actions are denied (BR-14/NFR-008).
- Periodically replay a set of phantom attempts (cross-realm token,
  expired refresh reuse, SoD-conflicting grant) and assert each is rejected
  — control-level health checks (CTL-02/CTL-03/CTL-07).
- Verify audit **hash-chain continuity** and JWKS rotation overlap as
  standing checks (BR-01/BR-09).

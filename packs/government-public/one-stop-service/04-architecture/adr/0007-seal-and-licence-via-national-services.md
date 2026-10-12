# ADR-0007 — Seals and licences come from the national services, and business systems must support them

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that electronic licence and seal services are external platform
dependencies, integrated via published standards and never re-implemented. The
办法's 第九条 and 第十条 establish the services, and the Electronic Seal
Administrative Measures (国办发〔2025〕33号) supply the obligations that make the
integration concrete.

Three of those obligations change the design rather than merely describing it:

| Source | Obligation | Design consequence |
|---|---|---|
| art. 9 | seals from the national unified system | no local minting (BR-10) |
| Measures art. 16 | a seal's validity must **not exceed its certificate's** | a certificate tracking dependency, and an expiry that must be surfaced |
| Measures art. 17 | the production/filing body **must provide a status query service** | the platform **consumes** a status service, not only a signing service — and must handle a seal that becomes invalid *after* it signed a document |
| Measures art. 23 | verification confirms the seal **was valid at the time of signing** | a distinct check from "is the seal valid now", recorded as `validAtTs` |
| Measures art. 27 | business systems of administrative and public-service bodies **shall support** compliant seals | an obligation on the platform's own architecture (BR-14), not merely a reason to integrate |

The last one is the reason this ADR exists at all: 第九条 gives a mandate, and
第二十七条 turns it into a requirement that this platform's own business systems
support compliant seal integration.

## Options considered

1. **Implement a local seal** — the platform mints its own seal, and the document's
   legal status is a rendering. A second seal to secure, and one whose validity
   cannot be checked against a certificate.
2. **Integrate signing only** — the platform calls a signing service and records
   nothing else. A seal that later becomes invalid is indistinguishable from a
   properly sealed document, which is the flattering answer.
3. **Integrate signing **and** consume a status query service, recording validity
   at signing, and treat art. 27 as a constraint on the platform's business
   systems** — the integration is complete and the constraints are explicit.

## Decision

Option 3, enforced by BR-10, BR-14, FR-025 through FR-027, and model constraints
10 and 11, with NFR-013 and CTL-04.

`validAtTs` records validity at signing. A status check is a separate operation,
consulted where a validity question is asked, and its result is never substituted
for the recorded at-signing validity.

## Consequences

- Positive: a document's sealing status is a fact with a timestamp rather than a
  rendering, and a seal's later invalidation does not retroactively invalidate a
  properly sealed document.
- Positive: art. 27 makes the requirement auditable — an exception is recorded with
  an owner and an expiry, rather than being a gap.
- Negative: the certificate-validity bound means seal expiry must be surfaced before
> a document is signed, and an expired certificate blocks issuance rather than
> producing a weaker document.
# ADR-0001 — The BSS/OSS boundary is an integration contract, never a convenience

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires the commercial (BSS) and resource/fulfilment (OSS) boundary
to remain explicit as an integration contract, never blurred.

In most software a service boundary is an implementation detail. Here it is not,
because the two sides answer different questions, at different speeds, with
different failure semantics:

| | BSS | OSS |
|---|---|---|
| Answers | *what did we sell, and what do we owe?* | *is the service real right now?* |
| Unit | commercial product, order, invoice | logical/physical resource, service order |
| Latency | seconds to days | milliseconds to minutes |
| Failure consequence | money wrong, dispute, invoice credit | service down, SLA breach |

The pressure to blur comes from ordinary helpfulness: the commercial layer
"just needs to know" whether the network is up; the fulfilment side "just needs
to know" what to charge.

## Options considered

1. **Blur by convenience** — each side calls the other when convenient. Fast,
   and it migrates real-time control obligations into a commercial system that
   was not designed to carry them, and commercial authority into an operational
   one.
2. **Shared database across the seam** — avoids an interface, couples
   availability, and makes the boundary configurable rather than contractual.
3. **Explicit interface contract** — all integration through a declared,
   versioned interface with stated payload shapes, state vocabulary, timing,
   ownership and failure semantics; crossing the seam any other way is a defect.

## Decision

Option 3, enforced by BR-01 (commercial decisions never consult network state),
BR-02 (interface-only, no SCADA scope), FR-012, FR-013, and CTL-06.

The specification is the object through which the commercial side learns what an
offering means in resource terms (ADR-0002). The commercial layer does not read
network state to answer a commercial question, and the operational side does not
compute a charge.

## Consequences

- Positive: a control obligation cannot migrate into the commercial system by
  accident; each side's failure modes stay its own; and an OSS outage is
  attributable to OSS rather than to the BSS suite (NFR-011).
- Positive: the seam becomes testable. An integration that cannot declare its
  payload shapes, state vocabulary, timing, ownership and failure semantics is a
  coupling, and the declaration requirement catches it at design time.
- Negative: some genuinely useful questions are harder to answer — "can this
  customer be promised this speed today?" requires either a designated
  interface call or an honest "unknown". The pack chooses honest *unknown*
  (`integration.md` failure-mode contract) over a convenient direct read.
- Negative: the interface must be versioned and maintained, which is recurring
  work. A coupling is cheaper today and unbounded later.
# 03-domain / State Machines

> ⚠️ ASSUMPTION — SM-T1..SM-T4 states and transitions are pack design, not
> derived from a standard (EPCIS supplies event *vocabulary*, not lifecycle
> states — see [`../SOURCES.md` §4](../SOURCES.md)).

The dual-state stance (ADR-0005) is visible in SM-T1: the **plan side** and
the **actual side** are separate machines that never mutate each other.

## SM-T1 Leg (plan side × actual side)

```mermaid
stateDiagram-v2
  state "Plan side (versioned)" as Plan {
    [*] --> Planned
    Planned --> Tendered: tender issued (FR-009)
    Tendered --> Accepted: carrier ACCEPTED (BR-03)
    Tendered --> Planned: REJECTED/TIMEOUT → new tender round or re-plan
    Accepted --> Dispatched: departure fact observed
    Planned/Accepted --> PlanCancelled: cancel + compensation events
  }
  state "Actual side (append-only facts)" as Actual {
    [*] --> InTransit: departure milestone
    InTransit --> ExceptionOpen: typed exception (FR-012)
    ExceptionOpen --> InTransit: exception resolved, still moving
    InTransit --> Arrived: arrival milestone
    Arrived --> Delivered: POD captured (BR-06)
    Arrived --> ExceptionOpen: refusal/damage at delivery
    Delivered --> [*]
  }
  Plan --> Actual: dispatch links plan revision to fact stream
```

Key: replanning (window/carrier change) creates a **new plan revision**;
KPIs compare actuals against the *original accepted* revision (ADR-0005,
FR-012). `Delivered` is unreachable without a POD (BR-06).

## SM-T2 Tender (per leg, per round)

```mermaid
stateDiagram-v2
  [*] --> Offered: tender sent (C-12)
  Offered --> Accepted: carrier accept → rate snapshot frozen (BR-04)
  Offered --> Rejected: carrier reject (reason required)
  Offered --> Timeout: no response by deadline (A)
  Rejected --> Offered: next carrier / re-tender
  Timeout --> Offered: re-tender or manual fallback (BR-03)
  Accepted --> [*]
```

Every round is recorded (`leg, round` key); history of rounds is never
rewritten (BR-11).

## SM-T3 Carrier invoice → settlement

```mermaid
stateDiagram-v2
  [*] --> Received: invoice ingested (C-19)
  Received --> AutoApproved: three-way match within tolerance (BR-05)
  Received --> Disputed: mismatch beyond tolerance → dispute opened
  Disputed --> Adjusted: carrier accepts revised amount
  Disputed --> Rejected: claim unsupported, no pay / credit note
  AutoApproved --> Settled: included in settlement batch (FR-016)
  Adjusted --> Settled: adjusted amount enters batch
  Rejected --> [*]
  Settled --> [*]
```

No payment path exists without `AutoApproved` or an `Adjusted` outcome;
`MatchResult` and `Dispute` records are append-only (BR-11, FR-015).

## SM-T4 Exception

```mermaid
stateDiagram-v2
  [*] --> Open: typed raise (delay | damage | refusal | shortage | hand-off mismatch) (FR-012, BR-10)
  Open --> Acknowledged: owner assigned
  Acknowledged --> Resolved: action taken (re-route / re-tender / claim)
  Open --> Resolved: auto-resolve (e.g. late but delivered)
  Acknowledged --> Escalated: age > threshold (A) → escalation list
  Escalated --> Resolved
  Resolved --> [*]
```

Opening an exception **never** mutates the plan or the fact stream; it links
to a plan revision when replanning occurs (BR-02).

## SM-T5 Regulation edition

```mermaid
stateDiagram-v2
  [*] --> Imported: edition data imported + integrity check
  Imported --> Active: designated in-force for a regime/period
  Active --> Superseded: newer edition designated (NFR-010)
  Superseded --> [*]: retained for historical validation audit
  Imported --> Rejected: integrity/coverage check failed
  Rejected --> [*]
```

Dispatch validation always resolves the edition in force **for the
transport date**; a missing in-force edition blocks dispatch (ADR-0003,
NFR-010).

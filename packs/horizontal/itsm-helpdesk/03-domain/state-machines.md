# 03 · State Machines

> ⚠️ ASSUMPTION — states and transitions are pack design; the cited clauses
> (ISO/IEC 20000-1 cl. 8.6) require the *outcomes*, not these lifecycles
> (see [`../SOURCES.md`](../SOURCES.md) §4).

IDs `SM-S1..SM-S3` (S = service desk). The `S` prefix is deliberate: other
packs in this library already use the bare `SM-n` and `SM-Tn` families, so a
service-desk machine must not collide with them when referenced across packs.
Full coverage of every key object is an L3 obligation; these anchor the
design at L2.

## SM-S1 Ticket (incident / service request)

```mermaid
stateDiagram-v2
  [*] --> New: intake (portal/email/chat/alert/api, BR-01)
  New --> Triaged: type + category + impact×urgency → priority (BR-03)
  Triaged --> Assigned: routing rule picks owner (BR-06)
  Assigned --> InProgress: first owner action — resolution clock starts (BR-04)
  InProgress --> WaitingRequester: awaiting requester (clock pauses, reason)
  InProgress --> WaitingSupplier: awaiting supplier (clock pauses, reason)
  WaitingRequester --> InProgress: requester replied (clock resumes)
  WaitingSupplier --> InProgress: supplier responded (clock resumes)
  InProgress --> Resolved: resolution code + note (BR-15)
  Resolved --> Closed: requester confirmed
  Resolved --> Closed: silence window elapsed → auto-close (BR-15)
  Closed --> InProgress: reopened (original SLA instance kept, BR-15)
  InProgress --> Cancelled: canceled with reason
  Cancelled --> [*]
  Closed --> [*]
```

Invariants: priority changes are events (BR-03); clock transitions are events
(BR-04, NFR-002); history is append-only (BR-07); a reopen never rewrites the
closed record (BR-15).

## SM-S2 Problem

```mermaid
stateDiagram-v2
  [*] --> Open: recurrence threshold met | major incident (BR-08)
  Open --> Rca: root-cause analysis in progress
  Rca --> KnownError: cause + workaround documented (FR-011)
  KnownError --> FixScheduled: RFC linked (FR-012, BR-08)
  KnownError --> RiskAccepted: accepted with review date
  FixScheduled --> Closed: fix verified via change outcome
  RiskAccepted --> Closed: review date reached
  Open --> Closed: no problem after analysis (resolved as incident-only)
  Closed --> [*]
```

Invariant: closing a fix requires an RFC reference (BR-08, FR-012).

## SM-S3 Change request

```mermaid
stateDiagram-v2
  [*] --> Draft: RFC raised
  Draft --> Classified: risk class assigned (BR-09)
  Classified --> CabPending: normal → assessment + CAB
  Classified --> Scheduled: standard → pre-approved schedule
  Classified --> Implemented: emergency → fast path (no CAB approval)
  CabPending --> Scheduled: approved
  CabPending --> Rejected: denied
  Scheduled --> Implemented: change executed (implementer, verify, outcome)
  Implemented --> ReviewComplete: post-implementation review recorded
  Implemented --> ReviewComplete: emergency post-review mandated ≤ window (BR-09)
  Rejected --> [*]
  ReviewComplete --> [*]
```

Invariant: the emergency path is the only one bypassing CAB approval and it
always terminates in `ReviewComplete` (BR-09).

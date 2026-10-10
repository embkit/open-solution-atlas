# 03 · State Machines

> ⚠️ ASSUMPTION — the SM-01..SM-05 states, transitions and guards are pack
> design; they are not derivable from ISA-95/IEC 62264 or the other cited
> standards (see [`../SOURCES.md` §4](../SOURCES.md)).

## SM-01 WorkOrder lifecycle

```mermaid
stateDiagram-v2
    [*] --> CREATED : intake from ERP (FR-002)
    CREATED --> RELEASED : gate passes (FR-004)
    CREATED --> CANCELLED : ERP cancel / gate irrecoverable
    RELEASED --> IN_PROGRESS : first operation starts
    IN_PROGRESS --> ON_HOLD : quality hold / material stop
    ON_HOLD --> IN_PROGRESS : hold released
    IN_PROGRESS --> COMPLETED : all operations done & confirmed
    COMPLETED --> [*]
    CANCELLED --> [*]
```

Guards: `RELEASED` freezes routing/BOM/inspection versions (BR-13);
`COMPLETED` requires quantity reconciliation vs. ERP (BR-01); ERP changes
affect only CREATED orders (FR-002).

## SM-02 Operation (work-order operation)

```mermaid
stateDiagram-v2
    [*] --> PENDING
    PENDING --> READY : predecessor DONE + material staged (BR-02)
    READY --> IN_PROGRESS : operator start (FR-005)
    IN_PROGRESS --> PAUSED : stoppage / andon
    PAUSED --> IN_PROGRESS : resume
    IN_PROGRESS --> GATE_HOLD : blocking inspection open (BR-05)
    GATE_HOLD --> DONE : result OK / disposition closed
    IN_PROGRESS --> DONE : normal completion (no gate)
    DONE --> [*]
```

## SM-02b SerializedUnit / lot-split state

`CREATED → IN_WIP (one active work order, BR-03) → COMPLETED | SCRAPPED`;
`QUARANTINED` overlays from NCR (FR-015) and blocks transitions.

## SM-03 Andon event

`OPEN → ACKNOWLEDGED → RESOLVED`, with timed `ESCALATED` re-notifications
per role matrix (FR-007); every transition is an event (BR-07).

## SM-04 NCR lifecycle

```mermaid
stateDiagram-v2
    [*] --> OPEN : raised (FR-013/015)
    OPEN --> QUARANTINED : hold applied to units/lots
    QUARANTINED --> DISPOSITIONED : REWORK | SCRAP | USE_AS_IS + approvals
    DISPOSITIONED --> CLOSED : compensating events written, holds lifted
    CLOSED --> [*]
```

## SM-05 Equipment state (classification, not control)

`RUNNING | IDLE | SETUP | DOWN | PM` — transitions recorded as
EquipmentStateEvents; `DOWN` requires a reason code (BR-08). These states
feed OEE exactly as defined in BR-09.

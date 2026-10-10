# 04 · Architecture Overview

## Architectural style

**Event-sourced execution core with plant-edge resilience.** Shop-floor
facts are captured as immutable events at the edge, stored append-only
(ADR-0002), and projected into read models (WIP, OEE, genealogy, boards).
Services are stateless; the plant server runs the full execution plane so
production continues through WAN/cloud outages (NFR-002).

## Component view

```mermaid
flowchart TB
    subgraph ot[OT zone - IEC 62443, read-mostly]
        PLC[PLCs / line controllers] --> SCADA[SCADA / edge gateways<br/>OPC UA / MQTT]
    end

    subgraph mes[MES zone - plant server(s)]
        ING[Event Ingest<br/>validation, sequencing] --> ES[(Execution Event Store<br/>append-only)]
        ES --> PRJ[Projection services<br/>WIP · OEE · genealogy · boards]
        SVC[Application services<br/>orders · dispatch · quality · material · andon] --> ES
        SVC --> RM[(Read models)]
        TERM[Station terminals<br/>kiosk PWA] -->|commands + events| ING
        ADP[Equipment adapters<br/>per-protocol] -->|events only| ING
        SCH[Shift jobs<br/>close, completeness, OEE publish]
    end

    subgraph it[IT zone / DMZ]
        ERP[ERP] <-->|orders / confirmations<br/>B2MML vocabulary| GWD[DMZ integration gateway]
        WMS[WMS] <--> GWD
        LIMS[LIMS / QMS] <--> GWD
        CLOUD[Group DWH / cloud analytics] <--> GWD
    end

    SCADA --> ADP
    GWD <--> SVC
    PRJ --> BOARDS[Line boards / dashboards]
```

## Deployment view

```
Plant site (authoritative execution plane)
├── OT network segment: PLC/SCADA; adapters run on the OT/DMZ boundary only
├── MES network segment: 2× app nodes (active/standby) + event store
│   (replicated locally) + terminal serving; kiosk terminals on shop Wi-Fi/WAN-free VLAN
└── DMZ: integration gateway to ERP/WMS/LIMS/cloud; outbound-initiated conduits

Group level (optional)
└── Central analytics receives replicated events/aggregates — never a
    dependency for execution (NFR-002)
```

Key properties: no WAN dependency for execution; rolling upgrades around
shift calendars (NFR-007); station terminals keep serving released
instructions and buffering events during MES downtime (NFR-002).

## Failure behavior

| Failure | Behavior |
|---|---|
| ERP unreachable | dispatch/execution continue from local state; confirmations queue (idempotent replay) |
| SCADA/gateway down | manual station entry remains; equipment events gap-flagged and reconciled |
| MES node down | standby promotes; terminals buffer locally (NFR-002); no event loss (BR-07) |
| Read-model corruption | rebuild by replaying the event store (ADR-0002) |

## Variant placement

Industry differences (discrete vs. process; regulated eDHR; tooling depth)
attach as variants — core stays the event backbone, dispatch, genealogy, and
quality gates defined above.

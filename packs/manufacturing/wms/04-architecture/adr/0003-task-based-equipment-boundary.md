# ADR-0003 — Automation integrated through a task-based equipment gateway; WMS never controls machines

- Status: Accepted
- Date: 2026-10-08
- Tags: wcs, wes, ot, integration, safety, security

## Context

Automation is heterogeneous: AS-RS, conveyors/sorters, AGV/AMR, pick-to-light
each expose different protocols and motion-level APIs. Coupling WMS business
logic to vendor primitives would (a) lock the product to vendors, (b) blur
safety responsibility by letting a business system drive control loops, and
(c) violate IT/OT segmentation (IEC 62443).

## Considered options

1. WMS calls vendor motion/IO APIs directly.
2. Point-to-point adapters per vendor inside core services.
3. A single task-based equipment gateway: WMS emits business tasks and
   receives lifecycle events; WCS/WES owns all motion/control.

## Decision

Option 3. WMS publishes business tasks (move LP A→B, deliver tote to
station; source/destination/priority/HU — no motion or IO). The equipment
gateway translates to each vendor and reports accepted/arrived/picked/
placed/faulted plus scans. Stock changes only when WMS validates a
completion event and applies the **same** mutation path as a manual task
(BR-14/FR-025). The gateway is the only IT component exposed across the
IT↔OT conduit (CTL-07/NFR-012). Manual fallback reuses the same task state
machine (FR-026).

## Consequences

- Vendor-neutral core; adding automation = gateway adapter, not core change.
- Clear safety boundary: WMS cannot directly actuate equipment.
- Need robust task status reconciliation and fault/fallback semantics;
  automation outages degrade to manual, not data corruption.
- Latency/throughput of the gateway becomes operationally critical (NFR-013).

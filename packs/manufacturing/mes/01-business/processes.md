# 01 · Core Business Processes

> ⚠️ ASSUMPTION — the BP-01..BP-06 process flows are pack design (a generalized
> ISA-95 level-3 activity decomposition), not normative text from
> IEC 62264-3 (see [`../SOURCES.md` §4](../SOURCES.md)).

## BP-01 Execute a production order end-to-end

```
ERP production order ──intake──▶ work orders per routing (FR-002)
   │                                │ dispatch to work center (FR-003)
   │                                ▼
   │                     release gate (FR-004): materials staged +
   │                     routing valid + no quality hold
   │                                ▼
   │                     station execution (FR-005/006): start → run →
   │                     complete; counts & params recorded as events (BR-07)
   │                                ▼
   │                     quality gates where planned (BP-03)
   │                                ▼
   ▼                                ▼
completion & confirmation back to ERP ◀── OEE/yield updated (FR-018)
```

Quantities reconcile to the ERP order (BR-01); operations follow routing
sequence (BR-02).

## BP-02 Stage and consume materials

Staging list per work order → scan verification (FR-009) → consumption per
lot at each operation (FR-010) → genealogy edges written (FR-011) → WIP
updated (FR-012). No negative lot stock (BR-04); every unit linked to
exactly one active order (BR-03).

## BP-03 In-process quality gate

Operation completes → inspection plan triggers (FR-013) → result OK → next
operation unlocks; result NOK → NCR raised, units quarantined (FR-015) →
disposition (rework / scrap / use-as-is) → release or scrap recorded.
Blocking gates cannot be skipped (BR-05).

## BP-04 Exception & andon

Operator or equipment raises exception (FR-007) → acknowledge → escalate per
matrix (time/role) → resolution + downtime coding (FR-017) → feeds OEE and
shift reports.

## BP-05 Traceability dossier

Query by serial / lot / order / date (FR-021) → backward traversal (which
lots & components entered this unit) and forward traversal (where this lot
was used) → assemble dossier: process params, equipment, personnel,
inspections → export for audit or customer complaint.

## BP-06 Shift close & data quality

Shift end → downtime codes complete or defaulted (BR-08) → completeness
checks (missing readings flagged) → OEE published for the shift → handover
digest to next shift and management.

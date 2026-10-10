# 01 · Processes

> ⚠️ ASSUMPTION — P-01..P-06 are pack design: a generalized service-
> management decomposition. ISO/IEC 20000-1:2018 cl. 8.6 defines required
> *outcomes* for incident/service request/problem management but not these
> flows; ITIL 4 practice names are vocabulary only (licensed, not
> reproduced). See [`../SOURCES.md` §4](../SOURCES.md).

## P-01 Intake → triage → resolve (incident / request)

```
intake (portal | email | chat | alert → ticket, deduped)
  → classify (type: incident | request; category; impact×urgency → priority)
  → assign (routing rules → group → owner) with SLA clock start
  → work (investigate | fulfill catalog item) — clock per BR-04 pause rules
  → resolve → requester-confirmed close → CSAT
```

## P-02 Escalation loop

```
approaching breach (warning %) → functional escalation (L1 → resolver)
breached / overdue → hierarchical escalation (owner → manager)
escalation is an event, not a rewrite of history (BR-07)
```

## P-03 Problem management

```
recurrence signal (linked tickets ≥ threshold) | major incident
  → problem record → root-cause analysis
  → known error documented (workaround) in KEDB
  → fix via RFC (P-04) | accept risk with review date
  → linked tickets resolve faster; recurrence metric improves
```

## P-04 Change enablement

```
RFC raised (from problem | standard catalog | normal)
  → risk classification (standard | normal | emergency)
  → assessment & CAB (standard: pre-approved schedule; emergency: fast path
    with post-review) → scheduled → implemented → review/verify
  → CI states updated in CMDB
```

## P-05 CMDB truth loop

```
manual registry + discovery/monitoring feeds
  → CI & relationship maintained → drift detected (missing/changed/retired)
  → drift task → reconcile → CMDB health reported
tickets and RFCs reference CIs; dependency view answers blast-radius queries
```

## P-06 Reporting & review

```
SLA clocks & worklogs → daily ops (backlog, at-risk) → monthly service
review (SLA achievement, MTTR, CSAT, recurrence) → improvement backlog
```

## Cross-cutting principle

One backbone, explicit clocks, append-only history: every state change,
escalation, pause/resume and classification edit is an event — reports are
projections, never the source of truth (ADR-0002).

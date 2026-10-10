# 01 · Processes

> ⚠️ ASSUMPTION — P-01..P-06 are pack design: a generalized transport-execution
> decomposition. No cited standard mandates this decomposition (EPCIS supplies
> event vocabulary, not process flow). See [`../SOURCES.md` §4](../SOURCES.md).

## P-01 Order intake & consolidation

```
Demand (ERP order / WMS outbound) → Transport order lines
  → validate Incoterms & DG metadata (BR-07, BR-12)
  → consolidate by lane/window/compatibility → Shipment (possibly multi-leg)
```

## P-02 Load building & routing

```
Shipment → load plan (cube/weight vs. vehicle capacity, BR-09)
  → route & stop sequence (solver optional per ADR-0002)
  → dispatch plan (carrier, vehicle, driver, planned windows)
```

## P-03 Tender & acceptance

```
Dispatch plan → tender to carrier(s)
  → ACCEPTED | REJECTED | TIMEOUT → re-tender or manual fallback
  → accepted tender freezes the rate snapshot (BR-04)
```

## P-04 Execution & tracking

```
Departure event → milestone stream (position/status via telematics/EDI/manual)
  → ETA recompute; exceptions (delay/damage/refusal) raised & managed
  → arrival + POD capture → delivery fact (BR-06)
```

## P-05 Settlement

```
Delivery facts + frozen rate snapshot → computed freight cost
  → carrier invoice → three-way match (BR-05): order/tender ↔ execution ↔ invoice
  → auto-approve within tolerance | dispute workflow | pay
```

## P-06 Exception & claim loop

```
Exception (any phase) → classify → action (re-route/re-tender/claim)
  → outcome recorded as events; carrier scorecard input
```

## Cross-cutting principle

Planning states and actual-execution states are **never merged**. A delay
mutates nothing in the plan; it appends actual events and (optionally)
triggers a *new* plan revision (ADR-0005, BR-02).

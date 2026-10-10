# 00 · Industry Brief — Manufacturing Execution

## What business this system serves

A manufacturer must turn ERP production plans into executed, recorded, and
traceable shop-floor work. MES is the **level-3** system in the ISA-95/IEC
62264 hierarchy: it receives planned orders from ERP (level 4), orchestrates
their execution on lines and stations (level 3), and reads statuses and
parameters from the automation layer (levels 1–2) — without itself
controlling machines or re-planning the supply chain.

The value proposition is regulatory and economic at once:

- **Traceability**: prove what was built, from which material lots, by whom,
  on which equipment, with which parameters — demanded by ISO 9001 customers,
  auditors, and regulators (medical devices, pharma, automotive, food).
- **Yield and OEE**: expose exactly where time and material are lost.
- **Paperless execution**: replace shift paperwork that cannot answer an
  audit or a customer complaint.

## Value chain

```
ERP plan (L4) ──▶ MES dispatch (L3) ──▶ station execution ──▶ event capture
                                                              │
        reporting & audit ◀── OEE / quality / genealogy ◀─────┘
```

## Market realities that shape the design

1. **Heterogeneous, aging equipment estate.** Lines mix modern OPC UA PLCs,
   1990s serial devices, and purely manual stations. An MES that assumes a
   uniform protocol fails; protocol adapters and edge gateways are
   structural, not optional (ADR-0003).
2. **OT/IT separation is mandatory.** Plant networks are segmented per
   IEC 62443; office-IT patterns cannot be applied directly to the shop
   floor.
3. **Users are not office workers.** Gloved operators, ten-second
   interactions, shift handovers, noise, poor lighting. Terminal UX is a hard
   requirement, not a styling concern.
4. **24/7 operation with zero tolerance for stopping production.** The MES
   must fail degraded (station-side buffering), never block the line, and
   support rolling upgrades around shift calendars.
5. **Industries differ materially.** Discrete assembly (serialized units,
   station balancing), process/batch (lots, recipes, phases), and regulated
   variants (eDHR/eBR with e-signatures) differ enough that one core with
   explicit variants beats one monolith pretending to fit all.
6. **ERP owns planning truth.** Duplicated planning data drifts and causes
   overproduction; MES consumes plans and reports back facts.

## Typical deployment contexts

| Context | Notes |
|---|---|
| Plant-local on-prem (edge/VM server) | default; satisfies OT segmentation and latency |
| Group data center + plant edge | analytics centralized, execution plane stays plant-side |
| Cloud-hybrid | history/analytics in cloud; execution never depends on WAN |
| 信创 / domestic stack (CN) | variant overlay; core stays portable |

## Sources

- ISA-95 / IEC 62264 — enterprise-control system integration
- IEC 62443 — industrial automation and control systems security
- ISO 9001:2015 cl. 8.5.2 — identification and traceability
- FDA 21 CFR Part 11; EU GMP Annex 11 — regulated-variant e-records

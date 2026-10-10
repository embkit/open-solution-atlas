# 09-delivery · Milestones

Incremental, each independently demonstrable. Scope covers the Must/Should
capabilities (capability-map 01–07); regulated/bonded/cold-chain overlays are
`variants/` and never block core milestones. Each milestone names the ACs whose
verification exits it.

| M | Name | Outcome (demonstrable) | Exits when |
|---|---|---|---|
| M0 | Foundations: event log + Inventory skeleton | append-only StockEvent store with hash chain, `fold(log)==StockPosition` reconciliation job, sole-writer internal path (C-25), RLS skeleton | fold replay reproduces projection; tamper attempt rejected — AC-N09, AC-N11 partial |
| M1 | Master data & GS1 | warehouse/zone/location with capacity validation, SKU pack hierarchy/UOM, owner model, effective-dated strategy config (ADR-0004), GS1/AI parser | AC-001..005 |
| M2 | Inbound & putaway | ASN ingest + validation, receiving count (blind/expected, tolerances), SSCC HU build, QC handoff, directed putaway + confirm, goods-receipt event | AC-006..011 |
| M3 | In-warehouse & stock control | status transitions, moves (`in_transit_intra`), replenishment (FIFO/FEFO), holds/quarantine/disposition, kitting/VAS | AC-012..016 |
| M4 | Outbound & wave | order intake/validation, wave build + atomic allocate/release, pick methods, pick confirm w/ scan control, re-allocation/back-order | AC-017..020, AC-N02 |
| M5 | Pack, ship, returns | pack verification (controlled goods), cartonization/weight/VAS, load-to-manifest, ship confirm → goods issue + ASN, returns disposition | AC-021..023 |
| M6 | Counting & reconciliation | ABC count plans + triggers, blind count, variance tolerance/recount, SoD-approved adjustment, ERP posting | AC-024 |
| M7 | Automation boundary & trace | equipment task gateway (dispatch + events), fault fallback to manual, EPCIS-aligned trace/export, exception workbench | AC-025..028, AC-N12 |
| M8 | Hardening: performance, HA/DR, security | perf profiles (NFR-001..004), HA/failover + event-log recovery (NFR-006), RF offline reconciliation (NFR-007), RLS/SoD/IT-OT tests, observability alerts | AC-N01/N03/N04/N05/N06/N07/N08/N10/N13/N14 |

Dependencies: M0 → all (the event log and sole writer are load-bearing);
M1 → M2..M6; M2 → M3 (stock must exist before in-warehouse ops); M4 → M5;
M6 independent after M3; M7 depends on M3+M4 (tasks) and M0 (events);
M8 last (needs a functional system to profile). M1, M6, and M7-gateway
adapter can run in parallel once M0 lands.

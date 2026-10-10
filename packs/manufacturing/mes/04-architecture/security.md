# 04 · Security

## Zones & conduits (IEC 62443 alignment)

```
[OT zone]          [MES zone]                 [DMZ]            [IT zone]
PLC/SCADA  ─cond→  adapters → event ingest ─cond→  gateway  ─cond→  ERP/WMS/LIMS/cloud
   (read-mostly;        (the only writer of                    (business systems;
   MES never writes     shop-floor facts)                       least-privilege service
   control — BR-12)                                             accounts per conduit)
```

- Terminals live in a shop-floor segment; they authenticate to MES with
  device certificates + operator login; no direct OT reachability.
- Every conduit crosses a firewall with explicit allow-lists; no flat
  networks (CTL-03).

## Identity & access

- Role catalog: operator, supervisor, dispatcher, quality, maintenance,
  OT-engineer, IT-admin — least privilege per role; segregation between
  quality disposition and production roles.
- Operator attribution on shared terminals (FR-008): badge/login per shift
  session; inactivity re-lock ≤ 5 min; all administrative changes audited
  (CTL-04).
- Regulated variants: e-signature ceremony = re-authentication + meaning of
  signature bound to the exact event identity (BR-11, CTL-02).

## Terminal & platform hardening

- Kiosk mode: no OS shell, signed application, auto-recovery, local event
  buffer encrypted at rest (NFR-002).
- Plant servers: minimal base image, patching within production change
  windows, backups tested by restore drills; event store replication.
- Secrets never in terminal images; per-device certificates rotated.

## Threat notes (selected)

| Threat | Mitigation |
|---|---|
| OT intrusion via MES | read-only OT conduit; no control writes (BR-12); adapter process isolation |
| Event tampering | append-only store + sequence integrity (BR-07); administrative audit (CTL-04) |
| Stolen terminal | device certificate revocation; operator re-auth; encrypted local buffer |
| Insider misapproval (quality) | role segregation; NCR approvals recorded per identity (FR-015) |
| ERP spoofing of orders | mutual authentication on DMZ gateway; version reconciliation checks (I-01) |

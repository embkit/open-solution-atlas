# 01-business / Core Business Processes

End-to-end processes with actors, trigger, preconditions, main flow,
exception paths, outcome. IDs `P-01..P-08`.

---

## P-01 Inbound from ASN to available stock

- **Trigger**: ASN received (EDI 856 / API) or PO expected.
- **Actors**: receiver, QC inspector, putaway operator, system.
- **Precondition**: PO/ASN & supplier master valid; dock calendar open.

1. Carrier checks in at gate; supervisor assigns dock door/appointment.
2. Receiver opens ASN; performs count — blind or against expected.
3. Scan/identify each handling unit; build SSCC license-plate hierarchy
   (pallet → carton → EA); capture lot/serial/expiry where required.
4. Over/short/damage recorded against ASN lines; discrepancy workflow.
5. If QC required → units land in **QC-pending** in a quarantine zone;
   else directly available-pending-putaway.
6. System computes putaway location(s) via strategy (BR-03); creates tasks.
7. Operator confirms putaway by scanning bin + LP; stock becomes available.
8. Goods-receipt event posted to ERP (physical receipt; valuation belongs
   to ERP — ADR-0001).

- **Exception**: unknown SKU/lot → exception bin + supervisor resolution;
  ASN over-delivery beyond tolerance → hold for decision.
- **Outcome**: stock at bin, available/quarantine status, GR posted, trace
  link supplier-lot → internal LP/lot.

---

## P-02 Directed putaway

- **Trigger**: received LP awaiting putaway.
- **Rules**: BR-03 (strategy), BR-04 (location compatibility), capacity.
- Flow: candidate locations scored (zone affinity, fixed bin for SKU,
  nearest free slot respecting weight/height/hazard/temp) → task assigned →
  scan confirm (system may suggest bin, operator may propose alternate with
  reason if allowed).
- **Outcome**: LP located; reserve/pick-face occupancy updated.

---

## P-03 Replenishment to pick face

- **Trigger**: pick-face qty ≤ min, or wave demand exceeds face stock, or
  scheduled top-up.
- Flow: compute required qty from reserve lot (respecting FIFO/FEFO & lot
  status) → create move task → confirm from reserve bin, confirm to face →
  reserve decremented, face incremented (net ownership/lot preserved).
- **Outcome**: no pick task goes to an empty face during a released wave.

---

## P-04 Wave planning, allocation, picking

- **Trigger**: order pool reaches planning window / cutoff approach.
1. Planner (or scheduled job) selects orders by carrier/cutoff/zone/priority
   → creates a **wave**.
2. Allocation run: soft reserve then hard reservation at release; choose
   lots by FIFO/FEFO/lot-directing (BR-06, BR-07); check pick-face and
   trigger replenishment; atomic quantity reservation prevents oversell
   (ADR-0002).
3. Generate pick tasks by method (single/batch/zone/cluster); optionally
   interleave with putaway travel.
4. Picker scans location + SKU/LP + qty; system enforces control scans;
   short pick → reason; system re-allocates from alternate bin/lot or
   back-orders.
5. Picked LPs move to pack.
- **Outcome**: reserved stock consumed on confirm; order lines satisfied or
  marked short; pick accuracy enforced at scan.

---

## P-05 Pack verification and shipping

1. Packer scans picked LP; system shows order, required qty/lot; verify
   each (mandatory scan control point, BR-08).
2. Cartonization suggests carton; capture actual weight/volume; pack VAS
   (gift/insert/labels) where configured.
3. Carrier/parcel label printed with SSCC/return info; documentation.
4. Stage by dock/trailer; loader scans into load; build manifest; seal.
5. Ship confirm → goods issue decrements stock; outbound ASN (856) + tracking
   to customer; post issue event to ERP.
- **Exception**: carton/order mismatch blocked; missing mandatory lot/serial
  blocks ship for controlled goods.
- **Outcome**: stock decremented, shipment traceable to customer/order/lot.

---

## P-06 Cycle count → adjustment → reconciliation

1. ABC plan generates count tasks (A items most frequent); plus zero-bin /
   post-short-pick triggers.
2. Counter performs **blind count** (system hides book qty); enter counted.
3. Within tolerance → auto-adjust; outside → recount / double count.
4. Remaining variance → adjustment request with reason code; supervisor /
   inventory controller approves within limit (SoD — CTL-04).
5. Approved adjustment written as an **inventory adjustment event**
   (before/after, reason, approver); posts to ERP for ledger reconciliation.
- **Outcome**: accuracy restored with full auditability; no silent overwrite.

---

## P-07 Hold, quarantine and lot recall

- **Trigger**: QC reject, customer complaint, supplier recall, expiry.
- Flow: place lot/serial or bin stock on **hold/frozen** (blocks allocation
  & outbound) → disposition decision (release / return-to-supplier / rework
  / scrap) → execute disposition move/adjustment → for recall, report all
  inbound-source and outbound-destination parties (EPCIS trace).
- **Outcome**: controlled stock cannot ship; recall dossier exportable.

---

## P-08 Automation task loop (WMS ↔ WCS/WES)

1. WMS creates an equipment-eligible task (pallet move / tote to station).
2. Task published to WCS/WES over the **task-based interface** (ADR-0003):
   source, destination, LP, priority; no vendor motion primitives.
3. WCS/WES accepts, executes, emits status (accepted/arrived/picked/placed/
   faulted) with LP confirmations.
4. On completion WMS applies the same stock-mutation event as a manual task;
   on fault → exception workbench, optional fallback to manual.
- **Outcome**: one stock-mutation path regardless of executor identity.

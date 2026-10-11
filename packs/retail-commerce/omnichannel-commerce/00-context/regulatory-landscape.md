# 00-context / Regulatory Landscape

> **Deliberately lean, by design decision.** Legal accuracy matters here only
> where it changes what the software must do. Each instrument is a
> **designation** with the capability it forces; no clause numbers, no currency
> tracking. `verification: unverified`. Not compliance advice.

## 1. Instruments in scope, and what each forces

| Instrument | Designation | Capability it forces |
|---|---|---|
| **PCI DSS** | Manifest `pci-dss`, region global | **Demonstrated removal of card data from the core** — PSP-hosted fields, tokenisation, and evidence that scope is out. `AGENTS.md` makes this demonstrable, not asserted |
| **PIPL / 《个人信息保护法》** | Manifest `pipl`, region cn | **Consent and purpose-bound use of buyer data**: checkout identity, marketing consent, and per-purpose data flows across channels |
| **《电子商务法》** | Manifest `e-commerce-law`, region cn | **Order and price transparency obligations at the point of sale** — the customer-facing display and the retention of what was displayed. Forces the pricing snapshot to be retained, not just used |
| **Cross-border / marketplace rules** | not in the manifest | ⚠️ ASSUMPTION: cross-border selling creates a declared **destination/jurisdiction property per order**. Recorded because it changes the tax and pricing model, not as a legal claim |

## 2. The one instrument that genuinely reshapes the architecture

PCI DSS, and only for one reason: it changes **where card data is allowed to be**
and the answer must be demonstrated rather than claimed.

| | |
|---|---|
| **Assumed** | Card data enters the platform. Consequence: segmentation, in-scope logging, a recurring assessment burden, and an architecture that cannot be retrofitted |
| **This pack's position** | Card data never enters the platform's processes; fields are PSP-hosted and the platform holds only tokens. Consequence: a demonstrated scope exclusion |

The demonstration is the point. `AGENTS.md` says "**demonstrated** out of the
core", and the pack treats that as a design requirement with an evidence
obligation — the platform must be able to show that no core component ever
receives a primary account number.

> ⚠️ ASSUMPTION: the pack assumes PSP-hosted fields are available in **every**
> channel, including POS and assisted sales. A channel that cannot host payment
> fields has no demonstrated scope exclusion by this argument and must either be
> excluded or carry a separate one. The pack does not specify the fallback.

## 3. Where transparency law becomes an engineering requirement

The e-commerce transparency obligations matter to this pack for one concrete
reason: **what the customer was shown becomes a record**.

That is not a compliance nicety — it is the reason the pricing snapshot must be
**retained** and not merely evaluated. If a dispute asks "was this really the
price?", the answer must be reconstructible, and a snapshot that is discarded
after capture cannot answer it.

> The design consequence is the same one the snapshot already provides for
> capture stability: keep it. This chapter exists mainly to record that the
> retention is not optional.

## 4. Regional profiles

| Profile | Distinguishing design requirement |
|---|---|
| **CN** | PIPL consent at checkout; e-commerce transparency retention |
| **EU / adjacent** | Consent, plus consumer cancellation rights that shape the **returns and cancellation** states |
| **Other** | PCI-class payment handling; local tax and consumer rules |

The profiles change **configuration values**, not architecture. That is the only
sense in which they matter to this pack.

## 5. What this chapter deliberately does not do

- No clause citation — none of it changes a design decision here.
- No currency tracking — no design effect.
- No accounting or tax-conformity rules (revenue recognition timing, e-invoicing)
  — the `data-ai` and finance-facing packs cover those.

## 6. Question that would change this

**Does any in-scope jurisdiction require that the *displayed* price, including
promotional contributions, be retained per order line?** If yes, the promotion
snapshot's retention becomes a stated capability with a retention period rather
than an implementation detail, and `01-business/capability-map.md` must carry it
explicitly.
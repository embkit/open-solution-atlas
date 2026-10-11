# 00-context / Regulatory Landscape

> **Deliberately lean, by design decision.** Legal accuracy matters here only
> where it changes what the software must do. Each instrument is a
> **designation** with the capability it forces; no clause numbers, no currency
> tracking. `verification: unverified`. Not compliance advice.

## 1. Instruments in scope, and what each forces

| Instrument | Designation | Capability it forces |
|---|---|---|
| **GDPR** | Manifest `gdpr`, region eu | **Subscriber privacy as a first-class data class**: per-class retention and erasure, purpose-bound use, and governance of CDR and location/usage data. Already a design requirement from `AGENTS.md`; this chapter states the design consequence, not the clauses |
| **ITU-T recommendations** | Manifest `itu-t`, region global | **Physical/network-layer conformance** — signalling, transmission, numbering formats. Forces the technical catalog to model external standard artefacts rather than invented shapes |
| **TM Forum ODA / TMF Open API** | Manifest `tmforum-oda`, `tmforum-open-api` | The **interface and component vocabulary** the pack adopts. Forces a decomposition into contract-bearing components with published interfaces, and a standard interface language between BSS domains and OSS |
| **Regulatory reporting & numbering** | not in the manifest | ⚠️ ASSUMPTION: subscriber counts, CDR retention and number-portability obligations exist in essentially every jurisdiction and force **statutory reporting and portability handling as capabilities**. Recorded here because they shape the data model, not as a legal claim |

## 2. The one place where privacy genuinely shapes the architecture

`AGENTS.md` requires retention and erasure **stated per data class**. This is not
a generic privacy obligation; it is specific to telecom because the data classes
have radically different natures:

| Data class | Nature | Retention consequence |
|---|---|---|
| **CDR (call data records)** | high-volume, quasi-static records | high-volume physical retention policy |
| **Location / usage** | derived, high-sensitivity, time-decaying | short *usable* horizon, longer *archival* obligation |
| **Customer/account master** | long-lived, changes rarely | long retention, active while the relationship exists |
| **Billing / invoice records** | financial assertions | statutory minimums |
| **Care & trouble-ticket history** | semi-structured narrative | often overlooked; a retention class of its own |

> ⚠️ ASSUMPTION: this pack assumes retention is declared **per data class** and
  enforced at the class level, with erasure propagated through the classes. The
  tension between a company's need to regenerate historical invoices (long
  retention) and the subscriber's erasure right is real, and this pack does
  **not** resolve it — it records that a per-class policy with a stated
  generation/regeneration window is the mechanism the design must provide.
  Which window is a business decision, not a pack thesis.

## 3. The BSS/OSS boundary is a privacy boundary too

The commercial layer and the fulfillment layer see different data, and the
boundary has a privacy consequence worth stating explicitly: the **commercial**
side should not receive network-level detail (usage records, location) at a
granularity that is not required to run the commercial process.

That is not a legal conclusion — it is a design rule that follows from
purpose limitation, and it is what `AGENTS.md`'s "never blur the boundary"
already produces in practice for correctness purposes. Recording it here makes
it an explicit capability: the **specification** decides what network detail the
commercial side needs, and the rest stops at the boundary.

## 4. Regional profiles

| Profile | Distinguishing design requirement |
|---|---|
| **EU / GDPR** | Per-class retention and erasure; purpose limitation across the boundary |
| **Other** | Reporting and numbering-portability handling; retention by local rule |

The profiles change **configuration values**, not architecture. That is the only
sense in which they matter to this pack.

## 5. What this chapter deliberately does not do

- No clause citation — none of it changes a design decision here.
- No currency tracking — no design effect.
- No sector-specific frameworks (export controls, formal regulation filings) —
  the regulated-sector packs cover those.

## 6. Question that would change this

**Does any in-scope jurisdiction mandate a *minimum* CDR retention that conflicts
with an erasure right?** Essentially every one has some version of this. If so,
per-class retention with an explicit statutory floor becomes a capability with a
real trade-off, and `01-business/capability-map.md` must carry erasure as a
*policy* surface with a stated floor, not merely as a deletion capability.
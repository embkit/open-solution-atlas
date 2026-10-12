# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. Access control belongs to the platform, or it does not exist

The central rule is structural: classification-derived access is enforced **by the
platform**, for every consumer kind (BR-09).

The check that makes it real is not "does BI enforce it" — it is *is a notebook a
consumer?* The consumers that bypass a BI-layer control are: a data-science
workspace, an export to a file, a marketplace feed, an ad-hoc query by someone
with warehouse credentials, and a scheduled job. All of them are consumers.

> A control in the BI tool is not a control. NFR-009 counts consumer **paths**
> rather than tool configurations for exactly this reason — the failure is a path,
> not a setting.

## 2. Raw immutability is an integrity control

Raw is immutable and append-only (BR-02). The reason it belongs in a security
chapter rather than an operations chapter is that the alternative is a
**silent integrity failure**: an edited raw layer means every downstream figure is
a function of a history that no longer exists, and it is discovered years later,
when someone recomputes and gets a different number.

> This is also why the append-only property is a hard requirement on the storage
> substrate rather than a convention: a compaction or snapshot-expiry job that
> invalidates a raw record is a security event, not housekeeping.

## 3. The gate is a control boundary, not a filter

Blocking gates withhold the partition from **every** consumer — not by filtering
at read. The distinction matters:

| | |
|---|---|
| **Withheld at the pipeline** | the partition does not exist downstream until the gate clears; no consumer can reach it |
| **Filtered at read** | the bad data is present and every consumer is a separate decision about whether to apply the filter |

The second is the common implementation and is the reason "why did this dashboard
show that?" survives as a question after the fact.

## 4. Deletion is a pipeline with recorded outcomes

Deletion propagates and records an outcome **per destination** (BR-12). A
destination with no recorded outcome is not deleted — it is unknown, and unknown
is recorded as a **degraded** state rather than as success (FR-021).

The destinations that get forgotten are the ones that are not obviously "data":
caches, snapshots, exports, marketplace feeds, and **derived ML data** such as
features and training snapshots. The last is recorded as its own control (CTL-05)
because it is the one most often unreachable.

> ⚠️ ASSUMPTION — the pack does not resolve how deletion interacts with
> append-only storage and derived ML artefacts. Candidate approaches
> (crypto-shredding of keyed columns, logical tombstones honoured by every reader,
> snapshot-expiry windows, bounded feature recomputation) are mechanisms a
> deployment must choose; the pack names the requirement and no method. Choosing
> one here would be inventing certainty.

## 5. Severity change is a controlled act

Changing a quality rule's blocking/warning classification requires an explicit,
attributed act (BR-06, FR-010). The alternative — an in-place downgrade — is how
a gate becomes decorative: a pipeline is blocked, someone downgrades the rule, and
the next build passes.

## 6. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **Raw partition + load record** | raw store + load table | "what was the data, when, from which source?" |
| **Contract version on a conformed partition** | conformed store | "what did this dataset mean, and under which contract?" |
| **Gate evaluation + severity-change history** | quality store | "was this partition exposed while a blocking rule failed, and who changed the rule?" |
| **Lineage edge with rule version** | lineage store | "which source field and which rule version produced this column?" |
| **Access decision per consumer** | audit trail | "who read what, under which classification-derived policy?" |
| **Deletion outcome per destination** | lifecycle store | "was this actually deleted, everywhere — or is a part of it still there?" |

> Each is answerable from the platform's own record. The load record and the
> deletion outcome are the two most often missing in practice, and both are what
> make the platform's claims checkable rather than asserted.

## 7. Retention, and the tension left open

Retention is declared per class (BR-13): raw extracts, conformed history, marts,
exports and lineage edges have different natures and different obligations.

> ⚠️ ASSUMPTION — the tension between retaining raw for recomputation and the
> personal-data obligations attached to the data raw contains is **not** resolved
> here. The mechanism the design must provide is a per-class retention policy
> with a declared generation window; the window is a business decision, and the
> pack names no value.
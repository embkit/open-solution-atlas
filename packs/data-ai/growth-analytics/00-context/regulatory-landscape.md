# 00-context / Regulatory Landscape

> **Deliberately lean, by design decision.** Legal accuracy matters here only
> where it changes what the software must do. Each instrument is named as a
> **designation** with the capability it forces; no clause numbers, no currency
> tracking. `verification: unverified`. Not compliance advice.

## 1. Instruments in scope, and what each forces

| Instrument | Designation | Capability it forces |
|---|---|---|
| **PIPL / 《个人信息保护法》** | Manifest `pipl`, region cn | **Consent enforcement at collection *and* activation**, and deletion that survives the identity-merge join keys. Already design requirements from `AGENTS.md` — this pack states the design consequence, not the clauses |
| **GDPR** | Manifest `gdpr`, region eu | Same, plus lawful-basis and rights-request handling for behavioural data |
| **Cross-border transfer rules** | not in the manifest | ⚠️ ASSUMPTION: destinations outside the jurisdiction require a **declared transfer property** per destination. Stated because it changes the destination abstraction, not as a legal claim |

## 2. The one place where law genuinely shapes the architecture

Consent enforcement has to happen at **two** points, and the reason is not
legal pedantry — it is that enforcing at one point only always fails in one of
two specific ways:

| Enforced only at | Consequence |
|---|---|
| **Collection** | Everything is collected, and the usable purpose set grows by accretion. A purpose used today was never consented |
| **Activation** | Nothing gates collection, so a single activation check is treated as a general licence |

The design consequence is concrete: **consent is a stateful, purpose-scoped
attribute of the data**, checked at both boundaries, with revocation taking
effect immediately at both.

## 3. Deletion and the identity problem

Deletion is where growth analytics becomes genuinely hard, and the mechanism is
stated here because it **is** a design requirement rather than a policy:

- Merging identity by joining on an anonymous or device identifier creates the
  very key that re-identifies a deleted user.
- A deletion that removes the profile but not the **join keys** is not a
  deletion; the profile can be reconstituted from residue.

> ⚠️ ASSUMPTION: this pack requires deletion to cover **profile, join keys, and
  derived facts** (cohort memberships, experiment assignments attributed to the
  identity). Whether derived *aggregates* must be recomputed — and what "the
  aggregate no longer reflects them" means operationally — is an L2 decision.

> ⚠️ ASSUMPTION: this pack assumes deletion is feasible without destroying
  experiment validity — an L2/L3 question with real tension between "remove
  their data" and "the experiment result must still be correct".

## 4. Regional profiles

| Profile | Distinguishing design requirement |
|---|---|
| **CN** | PIPL-purpose-scoped consent at both boundaries |
| **EU / GDPR** | Same, plus lawful basis and rights-request flows |
| **Other** | None beyond platform-level access control |

The differences change **configuration values**, not architecture. That is the
only sense in which they matter to this pack.

## 5. What this chapter deliberately does not do

- No clause citation — none of it changes a design decision here.
- No currency tracking — no design effect.
- No sector-specific regimes (health, minors, advertising rules) — the
  regulated-domain packs cover those.

## 6. Question that would change this

**Does any in-scope jurisdiction require behavioural events to be retained for a
minimum period that precludes immediate deletion on request?** If so, deletion
becomes a *scheduled* capability with a retention floor rather than an
immediate one, and this chapter plus the capabilities in
`01-business/capability-map.md` must change to match.
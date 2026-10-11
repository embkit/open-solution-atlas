# 00-context / Regulatory Landscape

> **Deliberately lean, by design decision.** Legal accuracy matters here only
> where it changes what the software must do. Each instrument is a
> **designation** with the capability it forces; no clause numbers, no currency
> tracking. `verification: unverified`. Not compliance advice.

## 1. Instruments in scope, and what each forces

| Instrument | Designation | Capability it forces |
|---|---|---|
| **NIST AI Risk Management Framework** | Manifest `nist-ai-rmf`, region global | **Risk framing plus documentation artefacts**: intended use, limitations, evaluation, and an approval record. These are governance *capabilities* in the registry, not policy prose |
| **ISO/IEC 42001** | Manifest `iso-iec-42001`, region global | A **management-system shape**: the evidence that controls exist and are operated, which is what makes the registry's approval record the governance surface |
| **EU AI Act** | Manifest `eu-ai-act`, region eu | **Risk-tier–dependent obligations**: the tier a model falls in changes documentation, monitoring and human-oversight requirements. Forces the tier to be a **declared, recorded property** of a registered model rather than an implicit assumption |
| **Data protection instruments** (GDPR, PIPL, etc.) | already across the repo's manifests | **Governance of training data**: lawful basis, purpose limitation, and the propagation of erasure into training snapshots and derived features |

## 2. The one instrument that genuinely reshapes the architecture

The EU AI Act, and for one reason: **risk tier changes obligations**, and the tier
is not knowable at build time.

That has a concrete architecture consequence: a registered model must carry its
**declared risk tier** as a recorded field, because the documentation, monitoring
and oversight requirements a deployment must satisfy depend on it. A platform
that has no field for the tier cannot produce tier-dependent evidence even if it
collects everything else.

> ⚠️ ASSUMPTION: this pack states that the tier must be a recorded property of a
  registered model. It does **not** state which tier applies to any model, does
  not define a tier taxonomy, and claims no conformance — per this repository's
  scope decision, the Act's classifications were not verified.

## 3. Governance has a shape, and it is artefact-shaped

`AGENTS.md` requires governance to follow NIST AI RMF and ISO/IEC 42001 — risk
management and documentation — **never ad-hoc policy**.

The practical consequence the pack takes from that: governance is a set of
**owned artefacts with a home in the platform**:

| Artefact | Where it lives | Why it is a capability, not a document |
|---|---|---|
| Intended-use statement | registry / model card | gates what the model may be used for |
| Limitations & known failure modes | model card | informs the evaluator and the approver |
| Evaluation results (incl. slices) | registry | the evidence the approval record cites |
| Approval record | registry | the only defensible answer to "who authorised this" |
| Drift and monitoring results | monitoring trail | the auditable basis of a response |
| Retirement record | registry | distinguishes "still approved" from "no longer approved" |

> Ad-hoc governance is what emerges when the controlled path is slower than the
> uncontrolled one. Every artefact above is a capability precisely because the
> alternative — a wiki page, a chat message, a spreadsheet — is faster and
> therefore what actually happens.

## 4. Regional profiles

| Profile | Distinguishing design requirement |
|---|---|
| **EU** | Declared risk tier; tier-dependent documentation, monitoring and human oversight |
| **CN** | Data-protection obligations over training data; erasure propagation into snapshots and features |
| **Other** | Governance shape (RMF/42001) as the default, with tier as an open property |

The profiles change **declared configuration values**, not architecture. That is
the only sense in which they matter to this pack.

## 5. What this chapter deliberately does not do

- No clause citation — none of it changes a design decision here.
- No currency tracking — no design effect.
- No conformity assessment process, no model-card schema definitions.

## 6. Question that would change this

**Does the platform need to hold the *training data* of a model in a form that
supports erasure of a specific individual's records?** If yes, retention becomes a
deliberately **bounded** design property with a stated regeneration window, and
`01-business/capability-map.md` must carry it explicitly — because the default
("keep snapshots so you can retrain") is in direct tension with erasure, and the
tension is unresolved in this pack.
# 00-context / Industry Brief — Workflow, BPM & Office Automation (OA)

## 1. What this system is in the value chain

Almost no organization runs its work as free-form email. Once more than a
handful of people must **agree on a sequence of steps, on evidence, and on a
record of who did what**, the organization needs a **workflow / BPM platform**:
the horizontal system that turns a business procedure into a running,
observable, auditable process.

It sits between **three sources of truth** and **every operational system**:

```
   HR / org master data                 Line-of-business systems
   (who exists, reports to whom)        (ERP / finance / HR / asset / CRM)
            │                                     ▲
            ▼                                     │
   ┌─────────────────────────────────────────────┴──────────────────┐
   │  WORKFLOW / BPM PLATFORM                                       │
   │                                                                │
   │  process definitions ──▶ process engine (instances, tasks)     │
   │  form definitions    ──▶ form engine (data capture, validation)│
   │  rules & gateways    ──▶ decision points (who must approve)    │
   │  documents & records ──▶ content store, 文号, 归档, retention    │
   │  events & audit      ──▶ who/when/what/result, replay           │
   └────────────────────────────────────────────────────────────────┘
            │                                     ▲
            ▼                                     │
   Notification / messaging            Identity (IAM) for participants
   (todo, reminder, escalation)         and for signature/seal identity
```

The platform **orchestrates**; it does not own the business data it moves.
That boundary is the first thing to state in a pack like this: an OA platform
that starts to "own" the business logic it was meant to route becomes a second
ERP that nobody can maintain.

Two families share the same machinery:

| Family | Typical unit of work | Characteristic |
|---|---|---|
| **Enterprise OA / 协同办公** | 审批单 — leave, expense, procurement, contract, seal use, official-document issuance | many small, short-lived, form-driven, human-heavy flows |
| **Business process management** | end-to-end processes — order-to-cash, claim handling, incident-to-resolution | fewer, longer-lived, integration-heavy, system-task-heavy |

The pack models both on one platform because the engine requirements are the
same; only the *flavour* of tasks and the compliance regime differ.

## 2. Deployment archetypes

| Archetype | Defining characteristics |
|---|---|
| **Departmental OA** | pre-built forms for leave/expense/seal, org chart sync from an HR system, light customization |
| **Enterprise process hub** | the OA forms plus BPMN-modeled cross-system processes calling ERP/finance APIs; the process layer becomes an integration fabric |
| **Government / 政务 OA** | the above plus 公文 handling, 文号 control, 电子签章, cross-department verification, records/archive obligations |
| **Embedded workflow** | the engine ships *inside* another product (an ITSM, an ERP, a low-code platform) as an internal capability rather than a standalone portal |

> ⚠️ ASSUMPTION: this pack models one logical platform serving all four
> archetypes, with the government-specific parts (公文/文号/电子签章) treated
> as a **deployment profile**, not a core feature. A real deployment will
> almost certainly buy, not build, the seal/signature integration.

## 3. Core flows (L1 view)

1. **Author & submit** — a user fills a form built from a schema, attaches
   evidence, and submits; the engine creates a **process instance**.
2. **Route & decide** — the engine evaluates the process definition: sequence
   vs. parallel branches, gateways, multi-instance countersign, delegation.
   Each step produces a **task** in someone's inbox.
3. **Human work** — assign/claim, transfer, countersign (会签), or-sign
   (或签), add-sign (加签), return for rework (退回), withdraw, delegate.
   Timers drive reminders, deadlines and escalation.
4. **System work** — service tasks call downstream systems, write back
   results, or wait for a callback / message.
5. **Complete & record** — the instance ends in a terminal state; the
   approval record, the document, the 文号 and the full event trail are
   retained and are retrievable for audit.

## 4. Why this system is unusually hard to get right

- **The model is not the implementation.** BPMN 2.0 is a *notation and
  interchange* standard; execution semantics — token flow, compensation,
  multi-instance completion — are where engines diverge. Two "BPMN-compliant"
  engines can run the same diagram differently (see
  [`SOURCES.md` §4](../SOURCES.md)).
- **Chinese approval vocabulary has no standard definition.** 会签 / 或签 /
  加签 / 转办 / 退回 are everyday terms in every Chinese OA deployment, and
  BPMN 2.0 defines none of them. Their semantics must be written down
  explicitly or every vendor defines them differently — which is exactly the
  failure this pack exists to prevent (see `03-domain/glossary.md`).
- **The org chart is a moving target.** Approvals depend on reporting lines,
  positions and roles that HR changes weekly; a platform that hard-codes
  approvers into process definitions breaks silently.
- **Auditability is a correctness requirement, not a feature.** "Every state
  transition must be auditable and replayable" is the pack's own hard rule
  ([`AGENTS.md`](../AGENTS.md)) — and an append-only trail is what makes an
  approval decision defensible months later.
- **Documents carry legal weight.** Once a 公文 or a contract is issued and
  signed inside the platform, the platform is producing legal artefacts:
  integrity, timestamps, retention and signature validity stop being
  engineering preferences.
- **Forms decay.** A schema-driven form engine trades deployment speed for
  the permanent risk of a validation expression nobody can trace back to a
  business rule.

## 5. Defining quality metrics

L1 frames intent only; thresholds and formulas are fixed as rules at L2.

| Metric | What it answers |
|---|---|
| Instance cycle time (per process type, p50/p95) | how long an approval really takes, end to end |
| On-time completion rate | how often SLA/deadline commitments are met |
| Task inbox latency (claim → first action) | whether humans, not the engine, are the bottleneck |
| Escalation / auto-remind effectiveness | whether timers actually unblock stalled work |
| Process-instance error rate (engine faults) | engine reliability independent of human latency |
| Audit completeness | proportion of transitions with a full, attributable event record |
| Document integrity check rate | proportion of retained documents whose hash still verifies |

## 6. Public standards anchoring the model

- **BPMN 2.0.2** (OMG, https://www.omg.org/spec/BPMN/2.0.2/) — the modelling
  vocabulary: flow objects, gateways, events, swimlanes, artefacts. This pack
  anchors its process notation here.
- **DMN** (OMG, https://www.omg.org/spec/DMN/) — decision modelling; the
  candidate home for approval-condition semantics once L2 specifies them.
- **CMMN** (OMG) — case management; *not currently in scope*. Noted so the
  omission is deliberate rather than an oversight.
- **CMIS 1.1** (OASIS, https://docs.oasis-open.org/cmis/CMIS/v1.1/) —
  interoperability for the document/content repository behind the
  document-management chapter.
- **IEEE 1849 XES** (IEEE, eXtensible Event Stream) — the candidate
  interchange format if/when process-mining or replay over exported logs is
  specified; the standard number is to be confirmed before any conformance
  claim (see `SOURCES.md` §4).
- **GB/T 22239-2019**《网络安全等级保护基本要求》 — the CN graded-protection
  baseline the platform is expected to satisfy.
- **《中华人民共和国电子签名法》** (2004, amended 2015 and 2019) — legal
  effect of electronic signatures; see `regulatory-landscape.md`.

> ⚠️ ASSUMPTION: engine conformance is deliberately *not* claimed. BPMN
> conformance classes are an L2/L3 decision; this pack states the notation and
> the lifecycle semantics it needs, not a vendor's conformance profile.

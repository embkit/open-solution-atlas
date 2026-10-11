# 01-business / Capability Map

L1 = the level-1 capability map: what the platform *does*, decomposed far
enough to discuss scope and priorities, and no further. Sub-capabilities are
deliberately omitted at L1 — they arrive at L2 with the requirements that carry
their IDs.

```
01-business / capability-map.md — Workflow, BPM & OA Platform (L1)

┌─ 01 Process definition & lifecycle ──────────────────────────────────┐
│  model · version · publish · deprecate · compare · migrate instances │
└──────────────────────────────────────────────────────────────────────┘
┌─ 02 Process execution engine ────────────────────────────────────────┐
│  instances · tokens · gateways · events · timers · compensation hint │
└──────────────────────────────────────────────────────────────────────┘
┌─ 03 Task & work-item management ─────────────────────────────────────┐
│  assign · claim · transfer · delegate · countersign · return        │
└──────────────────────────────────────────────────────────────────────┘
┌─ 04 Forms & data capture ───────────────────────────────────────────┐
│  schema-driven forms · validation · conditional visibility · drafts │
└──────────────────────────────────────────────────────────────────────┘
┌─ 05 Rules & decision points ─────────────────────────────────────────┐
│  approval conditions · gateway predicates · thresholds · calendar    │
└──────────────────────────────────────────────────────────────────────┘
┌─ 06 Documents & records ─────────────────────────────────────────────┐
│  content store · templates · 公文 & 文号 · seal/signature · archive  │
└──────────────────────────────────────────────────────────────────────┘
┌─ 07 Identity, participants & authority ──────────────────────────────┐
│  participant resolution · org/role model · delegation scope · SoD    │
└──────────────────────────────────────────────────────────────────────┘
┌─ 08 Events, audit & replay ─────────────────────────────────────────┐
│  event model · audit trail · retention · integrity · export         │
└──────────────────────────────────────────────────────────────────────┘
┌─ 09 Integration & extension ─────────────────────────────────────────┐
│  service tasks · callbacks · process-data API · embedding · variants │
└──────────────────────────────────────────────────────────────────────┘
┌─ 10 Monitoring, analytics & operations ──────────────────────────────┐
│  dashboards · SLA & escalation · process analytics · engine ops      │
└──────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **01** | **Process definition & lifecycle** | how a procedure becomes a running definition | model → publish → version → deprecate; definitions are artefacts under change control |
| **02** | **Process execution engine** | how an instance actually advances | token flow, gateways, events, timers, in-flight behaviour during redeploy |
| **03** | **Task & work-item management** | how human work is handed over | assign/claim/transfer/delegate/会签/或签/加签/退回 — the core OA vocabulary |
| **04** | **Forms & data capture** | how data enters the process | schema-driven forms, validation, conditional visibility, drafts, attachments |
| **05** | **Rules & decision points** | how routing and approval are decided | approval conditions, gateway predicates, thresholds, business calendars |
| **06** | **Documents & records** | what the process produces and must keep | content store, templates, 公文/文号, seal/signature, archive & retention |
| **07** | **Identity, participants & authority** | *who* is allowed to act | participant resolution via org/role, delegation scope, SoD constraints |
| **08** | **Events, audit & replay** | how it can be proven afterwards | event model, audit trail, retention, tamper-evidence, export |
| **09** | **Integration & extension** | how it connects to everything else | service tasks, callbacks, process-data API, embedding, stack variants |
| **10** | **Monitoring, analytics & operations** | how it is run and improved | dashboards, SLA/escalation, process analytics, engine operations |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 02 Execution engine | deciding business policy — that is 05 |
| 04 Forms | storing content long-term — that is 06 |
| 06 Documents & records | authenticating the signer — that is 07 + the signature service |
| 07 Identity & authority | defining *what* an approver may approve in business terms — that is 05/06 rules |
| 08 Events & audit | storage of the documents themselves — that is 06 |
| 09 Integration | owning the business data it moves — it orchestrates, it does not own |
| 10 Analytics | changing a process definition — it reports, 01 decides |

> This table exists because the most common architectural failure in this
> class of system is a capability quietly absorbing its neighbour's
> responsibility. Each boundary is a statement a reviewer can check against.

## 3. Level-1 priorities

At L1 the pack claims the map is **complete for discussion purposes** and
**incomplete for estimation**. It is deliberately silent on which capabilities
are hardest — that judgement needs a reference deployment.

> ⚠️ ASSUMPTION: capabilities 03 (task vocabulary) and 08 (audit & replay) are
> named first because the pack's own `AGENTS.md` treats the Chinese approval
> semantics and the auditable/replayable trail as non-negotiable. This is an
> editorial ordering, not a criticality assessment backed by evidence.

## 4. Out of scope for the whole platform

- Business logic of the downstream systems (finance rules, ERP posting).
- Organization master data ownership (consumed from HR/IAM, not authored here).
- The cryptographic implementation of signature/seal primitives — the pack
  specifies what must be *verifiable*, not which algorithm or provider.
- Low-code application generation beyond forms and processes.

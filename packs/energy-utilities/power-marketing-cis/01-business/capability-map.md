# 01-business / Capability Map

```
01-business / capability-map.md — Power Marketing & CIS (L1)

┌─ 01 Customer & account master ──────────────────────────────────────────┐
│  customer · account · service point · contract · customer class        │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 02 Metering & reading ─────────────────────────────────────────────────┐
│  meter asset · collection (AMR/field) · EXCEPTIONS · RULE-BOUND 估抄    │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 03 Tariff engine (REGULATED MATH) ──────────────────────────────────────┐
│  VERSIONED · AUDITABLE · EFFECTIVE-DATED rules · cycle-straddle splits  │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 04 Billing & adjustment ───────────────────────────────────────────────┐
│  bill with rule version · adjustment workflow (approval required)       │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 05 Payment & reconciliation ───────────────────────────────────────────┐
│  channels · allocation · mismatch detection · money-energy traceability │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 06 95598 service & case management ─────────────────────────────────────┐
│  intake · account/meter context · outage linkage · dispatch · closure   │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 07 Work orders & field execution ──────────────────────────────────────┐
│  dispatch · completion feedback · meter service · 停复电 execution      │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 08 Disconnect / reconnect with guardrails ─────────────────────────────┐
│  eligibility · notice · timing restricted · auditable · enforced state  │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 09 Distribution interface (INTERFACE-ONLY) ─────────────────────────────┐
│  adapter · no SCADA scope · seam is explicit and contractual            │
└─────────────────────────────────────────────────────────────────────────┘
┌─ 10 Audit, retention & platform security ──────────────────────────────┐
│  rules/approvals/reads evidence · retention · 等保 controls             │
└─────────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **01** | **Customer & account master** | who is supplied, under what terms | the service point and meter are distinct objects from the customer |
| **02** | **Metering & reading** | what did the meter say, and when | exceptions surfaced as exceptions; 估抄 only **by rule and labelled** (`AGENTS.md`) |
| **03** | **Tariff engine** | what does this reading cost | **versioned, auditable, effective-dated** (`AGENTS.md`) — regulated math |
| **04** | **Billing & adjustment** | what is owed, and how is a correction made | bill records the rule version; adjustments require an approval workflow |
| **05** | **Payment & reconciliation** | is the money recorded, and does it match | money and energy traceable to readings |
| **06** | **95598 service & cases** | what does the customer need, and what is happening | intake with real account/meter/outage context |
| **07** | **Work orders & field execution** | who does what, where | dispatch and completion feedback, incl. meter service |
| **08** | **Disconnect / reconnect** | may this legally be done | guardrails as **enforced state** (`AGENTS.md`) |
| **09** | **Distribution interface** | how operational state reaches this system | **interface-only; no SCADA scope** (`AGENTS.md`) |
| **10** | **Audit, retention & security** | can the whole record be defended | evidence of rules, approvals, readings; retention |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 01 Customer master | metering or billing semantics — it identifies who is supplied |
| 02 Metering & reading | deciding a charge — it produces readings; 03 prices them |
| 03 Tariff engine | inventing a tariff — the tariff is a **governed input**, not a platform decision |
| 04 Billing | altering a tariff rule to fit a bill — corrections go through adjustment |
| 05 Payment | correcting a bill — money correction is 04's approved workflow |
| 06 95598 | changing network state — it requests via 07/09 |
| 07 Work orders | deciding legality of a disconnection — 08 evaluates; 07 executes |
| 08 Guardrails | executing the disconnection — 07 does, on 08's verdict |
| 09 Distribution interface | real-time control — the seam is explicit and contractual |
| 10 Audit | resolving a dispute — it evidences; process resolves |

> Three boundaries carry the pack's weight. **03 vs 04**: tariff arithmetic is
> not billing logic, because a tariff change hidden in a release is
> indistinguishable from a bug fix. **02 vs 03**: an estimate is not a reading,
> and conflating them makes the bill unfalsifiable. And **07 vs 08**: the
> operator who executes must not be the one who decides.

## 3. Level-1 priorities

Complete for discussion, incomplete for estimation; deliberately silent on
relative difficulty.

> ⚠️ ASSUMPTION: capabilities **03 (tariff engine)** and **02 (reading with the
> 估抄 boundary)** are named first because `AGENTS.md` makes regulated maths and
> zero silent estimation the pack's two structural commitments. Editorial
> ordering, not an evidence-backed criticality claim.

## 4. Out of scope for the whole platform

- **SCADA / real-time control** — reached only through the interface
  (`AGENTS.md`); the two worlds have incompatible failure semantics.
- **Network engineering and asset maintenance** — meter and grid asset
  management beyond what billing needs.
- **Generation, procurement and trading** — a different pack's subject.
- **Retail competition / aggregator models** — would change the engine's shape,
  not the properties.
- **Product/application development for the utility's other domains** — this is
  the CIS.
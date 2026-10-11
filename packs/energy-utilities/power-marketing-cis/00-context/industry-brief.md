# 00-context / Industry Brief — Power Marketing & Customer Information System

## 1. What this system is in the value chain

A power utility sells electricity to every household and business in an area,
metered, priced under a regulated tariff, and billed on a cycle. The **power
marketing / customer information system (营销 / CIS / 95598)** is the commercial
core: customers, meters, readings, tariffs, bills, payments, and the
customer-service line that handles the consequences.

```
   customers / service channels          regulated & network boundaries
   ────────────────────────────           ─────────────────────────────
   retail service halls                 tariff & price regulation
   95598 hotline                         distribution systems (metering)
   online / mini-program portals          SCADA / OMS work orders
   field survey & meter reading          payment / treasury channels
          │                                       ▲
          ▼                                       │
  ┌───────────────────────────────────────────────┴───────────────────┐
  │  MARKETING / CIS                                                    │
  │                                                                    │
  │  customer & account master                                     │
  │  metering & reading (含估抄) ──▶ tariff engine (版本化、生效日)   │
  │  billing & adjustment ──▶ approval workflow                       │
  │  payment & reconciliation                                        │
  │  95598 service & work orders                                     │
  │  disconnect/reconnect (强护栏)                                    │
  └────────────────────────────────────────────────────────────────────┘
```

The defining constraint is a sentence from `AGENTS.md`: **billing and
reconciliation numbers must trace to readings with zero silent estimation**
beyond the defined 估抄 rules.

Everything else in this pack follows from the fact that the customer-facing
number is not a commercial figure the platform may optimise — it is
**regulated arithmetic** on a measurement.

## 2. Tariff calculation is regulated math

`AGENTS.md`: tariff rules must be **versioned, auditable, and effective-dated**.

Three properties, each with a distinct reason:

| Property | Why it is load-bearing |
|---|---|
| **Versioned** | a tariff change must not silently restate bills already issued on the old rate |
| **Auditable** | the arithmetic must be re-derivable — "why is this bill this amount?" is a legitimate question with a required answer |
| **Effective-dated** | rates change on a date; a cycle that straddles the change must apply each rate over its own period |

The pack therefore treats the tariff engine as a **statutory arithmetic
surface**, not a pricing configuration:

- the rules are a governed artefact, not code that changes with a release;
- the bill stores the **rule version** applied, so a historical bill is
  reproducible;
- a change is a dated, published event with an authority behind it.

> The difference from a commercial pricing engine (`omnichannel-commerce`) is
> decisive: there, a price is a commercial decision the platform implements.
> Here, the tariff is **regulation the platform must not improve upon**.

> ⚠️ ASSUMPTION: the pack models a single regulated tariff regime per deployment.
  Multi-tariff, pooled-procurement or retail-competition regimes change the
  engine's shape but not the three properties above.

## 3. Metering: reading, exception, and the 估抄 boundary

The bill starts from a reading. `AGENTS.md` names the two controls that make
that trustworthy:

**Reading exceptions** — a reading that is missing, out of range, or inconsistent
with history is not a data problem to be smoothed over; it is an **exception**
that must be surfaced and resolved against a defined rule.

**估抄 (estimated reading)** — where an actual reading cannot be obtained, an
estimate may be substituted — but only by a **defined rule**, and it must be
**visible** on the resulting bill as an estimate, not presented as a measurement.

> The boundary is the load-bearing statement. An estimate that is silently
> substituted produces a bill that is arithmetically correct and factually
> unfounded — and the customer has no way to know, and the utility has no way to
> prove.

> ⚠️ ASSUMPTION: the pack states that 估抄 must be rule-defined and visible, but
  does not specify the estimation method. That method, its period, and the
  reconciliation against the next actual reading are deployment decisions
  governed by regulation, and this pack names no method.

## 4. Adjustments require approval workflows

`AGENTS.md`: meter-reading exceptions **and** billing adjustments require
approval workflows.

Both are money-correction paths, and both are dangerous for the same reason: a
correction that can be applied unilaterally is an unbounded financial control.

The workflow is therefore a **capability**, not a process preference:

- an adjustment is an explicit, attributed, approved act;
- the original bill remains, and the adjustment is a new event;
- the approval is by a party with the authority, recorded.

> This is the same discipline as `telecom-bss`'s "recompute, never edit" and
> `omnichannel-commerce`'s idempotency-protected money operations: a financial
> assertion once made is not rewritten.

## 5. Disconnect / reconnect follows regulation, with guardrails

`AGENTS.md`: disconnect/reconnect processes follow **public-service regulations
with strict guardrails**.

Disconnection is not a collections action with a switch — it is a regulated act
with consequences for vulnerable customers, medical equipment, seasons, and
public-interest exemptions.

The pack's design consequence: the process must carry the **guardrails as
enforced state**, not as advice:

- **eligibility** — who may not be disconnected (regulated exemption classes);
- **notice** — required notice periods before the act;
- **timing** — restricted periods (season, time of day, medical need);
- **auditability** — a complete record of the decision and its basis.

> A system that holds the eligibility rules as a configuration someone may
  overlook is not compliant with its own guardrails. The rules must be evaluated
  by the process, not remembered by the operator.

> ⚠️ ASSUMPTION: the pack requires the guardrail **classes** to exist as enforced
  state and names no specific exemption class, notice period or restricted
  period — those come from regulation, not from this pack.

## 6. Distribution integration is interface-only

`AGENTS.md`: all integration with distribution systems is **interface-only, no
SCADA scope**.

This is a scope boundary with a factual reason: SCADA is a real-time control
system with its own safety and availability regime. A commercial system that
reaches into it inherits a set of constraints it is not designed to carry.

The boundary is drawn at the interface:

| The marketing/CIS side | The distribution side |
|---|---|
| customer, account, meter, reading, bill | network topology, protection, switching |
| work orders, service requests | OMS fault management and restoration |
| 95598 case handling | outage events affecting customers |

> The interface is where the utility's commercial and operational worlds meet,
  and the pack's position is that the seam must be **explicit and contractual**
  — not because the systems should not cooperate, but because the two have
  incompatible failure semantics.

## 7. Core flows (L1 view)

1. **Onboard** — customer, account, service point, meter, tariff assignment.
2. **Read** — meter reading through automated collection or field work;
   exceptions raised, 估抄 applied only by rule and labelled.
3. **Tariff** — charges computed under the effective-dated, versioned rules;
   the bill records the rule version.
4. **Adjust** — corrections for reading errors, tariff changes or disputes,
   each with an approval workflow.
5. **Bill & collect** — invoice, payment channels, reconciliation.
6. **Serve** — 95598 case, work order, field dispatch, outage-linked
   communication.
7. **Disconnect / reconnect** — only through the guarded, audited process.
8. **Reconcile** — money and energy traceable to readings.

## 8. Why this system is unusually hard to get right

- **The number is regulated.** It is not negotiable, not optimisable, and its
  arithmetic must be reconstructable years later.
- **Readings are incomplete, late, and occasionally wrong.** Estimation exists
  because reality is imperfect, and every estimate is a place where the record
  can quietly become unfounded.
- **Money corrections are a financial control surface.** An unapproved adjustment
  path is unbounded exposure.
- **Disconnection is a regulated act with humanitarian edge cases.** The rules
  are complex, change with policy, and are not optional.
- **Cycles straddle changes.** A tariff change, a meter change or a service
  change mid-cycle must be split correctly, not approximated.
- **Reconciliation must reach the meter.** Money and energy figures traceable to
  readings is what makes disputes resolvable and audits passable.

## 9. Defining quality metrics

L1 frames intent; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Bill accuracy dispute rate | whether the arithmetic holds |
| 估抄 rate and its correction-on-actual-read variance | whether estimation is bounded and honest |
| Reading exception resolution time | whether exceptions surface rather than pool |
| Adjustment approval cycle time and rejection rate | whether the control is usable as well as enforceable |
| Bill cycle on-time rate | whether the regulated schedule is met |
| Tariff rule version currency | whether rule updates are effective-dated correctly |
| Disconnect guardrail compliance | whether exemptions are enforced, not remembered |
| Connect/distribution interface availability | whether the seam holds |
| Reconciliation to readings completeness | whether the traceability rule holds |

## 10. Public materials referenced

| Topic | Source | Note |
|---|---|---|
| Industry administration & policy | National Energy Administration — https://www.nea.gov.cn/ | Manifest source; the sector regulator's site |
| Tariff & settlement reference | 电力统计与交易 — http://www.dltjyy.cn/ | Manifest source; a tariff/settlement reference site |
| 《电力法》 | Manifest `electric-power-law` | Designation; see `regulatory-landscape.md` |
| 等保 / MLPS 2.0 | Manifest `mlps-2-0` | Designation; the graded-protection baseline |

> ⚠️ ASSUMPTION: neither manifest source was verified for reachability, and
  `dltjyy.cn` in particular is a **non-authoritative commercial reference site**
  recorded as a source by the original manifest. The pack does not rely on it
  for any load-bearing claim; tariff specifics come from regulation, recorded as
  a designation only.

> Per this repository's scope decision, **no legal or regulatory clause was
> verified.** See `regulatory-landscape.md`.

## 11. The gap this pack will not fill at L1

`AGENTS.md` requires tariff calculation to be "regulated math — versioned,
auditable, effective-dated". That is a **framework**, and the actual rules are
regulatory. The pack deliberately does not encode any specific tariff; doing so
at `unverified` status would be exactly the invented-certainty the standard
forbids. A deployment's actual tariff rules are a governed input, and the pack's
job is to make their versioning, effective-dating and auditability structural.
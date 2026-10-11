# 00-context / Industry Brief — Telecom BSS/OSS Suite

## 1. What this system is in the value chain

A telecom operator sells a service that must actually reach the network. The
**BSS** (business support systems) is the commercial layer — sell it, price it,
bill it, collect for it, support it. The **OSS** (operations support systems)
is the fulfillment layer — make it real on the network.

The defining problem, as `README.md` states it, is **order-to-cash plus
order-to-activation consistency**: what the catalog sells, what the order
orchestrator fulfills, what rating charges, and what the network actually
activates must stay in agreement across long-lived, multi-domain processes.

```
   commercial layer (BSS)                    fulfillment layer (OSS)
   ──────────────────────                    ───────────────────────
   customer & party                         network inventory
   product catalog (commercial)             resource inventory
   pricing / plans                          provisioning automation
   order capture & decomposition ──────────▶ activation / reservation
   rating & billing                         network orchestration
   invoicing & receivables (dunning)         assurance / fault management
   customer care                            number/code pools
            │                                        ▲
            └──────── guaranteed by the SPECIFICATION ◀┘
                       that joins both catalogues
```

The pack is the **suite**, not one system: a set of domains that must agree about
the same commercial object as it moves from offer to invoice to activation.

## 2. The boundary that must never blur

`AGENTS.md` makes the **BSS/OSS separation an integration contract**, explicitly
"never blurred".

That is unusual. In most software a service boundary is an implementation
detail. Here it is not, because the two sides answer different questions, at
different speeds, with different failure semantics:

| | BSS | OSS |
|---|---|---|
| Answers | *what did we sell, and what do we owe?* | *is the service real right now?* |
| Unit | commercial product, order, invoice | logical/physical resource, service order |
| Latency | seconds to days (bill cycles) | milliseconds to minutes |
| Failure consequence | money wrong, dispute, invoice credit | service down, SLA breach |
| Correctness driven by | the catalog and the agreement | the network's actual state |

The contract between them is therefore the **specification** — the object that
says what a commercial product means in resource terms. Blur the boundary — let
BSS talk network, or let OSS talk price — and every subsequent reconciliation
becomes bespoke.

## 3. Two catalogs, one specification

`AGENTS.md`: the commercial product catalog and the technical/resource catalog
are **distinct models joined by a specification, not duplicated**.

This is the second structural commitment, and it has a specific failure mode if
violated. If the two catalogs are the same model:

- every commercial pricing change is a network-facing change, and vice versa;
- a resource-only product (wholesale, interconnection, M2M SIM) has no
  commercial representation, or acquires a fake one;
- commercial release cycles become gated on network engineering cycles.

```
   commercial catalog                specification                technical/resource catalog
   ─────────────────                 ─────────────                ────────────────────────
   product offering  ─────────────▶  what this offering          logical resource
   price plans                       means in resource terms  ──▶  physical resource
   eligibility rules                and how it is verified       topology / activation path
   bundling, promotions                                                   │
                                                                          ▼
                                                    one offering → N resource realisations
```

> The specification is the join, and it is where product-vs-network translation
> lives. It is also where the "what does this customer actually have" answer is
> derived, which is why the glossary treats it as a first-class object rather
> than a mapping table.

## 4. Order decomposition is a traceable chain

`AGENTS.md`: order decomposition from **customer order → service order →
resource order** must be **traceable end-to-end**.

```
   Customer order (CO)   "I want this"
        │  decompose
        ▼
   Service order (SO)    "these service instances are involved"
        │  orchestrate, per service
        ▼
   Resource order (RO)   "these network resources must be reserved/activated"
        │
        ▼
   activation status  ──▶ back-propagated to the SO and the CO
```

The traceability requirement is not bookkeeping. It is the only way to answer
the three questions that decide whether the system works:

1. *Why did this fail?* — trace the CO to the RO that did not complete.
2. *Why is the customer paying this?* — trace the invoice line back to the CO
   and the product offering.
3. *What did I actually enable?* — trace the resource order to the inventory
   item that changed.

An order that cannot be walked in both directions makes all three questions
organisational archaeology.

## 5. Rating events are immutable and reconcilable two ways

`AGENTS.md`: rating/billing events are **immutable** and **reconcilable against
both the order and the inventory**.

Two properties, each with a distinct reason:

- **Immutable** — a charge is a financial assertion. Recomputing a bill is a new
  event, not an edit, because the old assertion was communicated to the
  customer.
- **Reconcilable against the order** — because the charge must be attributable to
  what was bought.
- **Reconcilable against the inventory** — because usage of a resource belongs to
  a customer, and a resource billed to nobody or billed twice is a defect that
  only the inventory side reveals.

> The two-way reconciliation is the load-bearing property. One-way (order →
> invoice) produces systems that bill correctly and cannot detect leakage; the
> other direction catches usage with no customer, and activation with no charge.

## 6. Interfaces: ODA and TMF Open API as the normative language

`AGENTS.md` adopts **TM Forum ODA component vocabulary** and the **TMF Open API
family** as the normative interface language.

Two separate standards, used for separate purposes:

| | What it standardises | How this pack uses it |
|---|---|---|
| **ODA (Open Digital Architecture)** | The **component vocabulary** — how domains are decomposed into components with published contracts | the vocabulary for the architecture's decomposition |
| **TMF Open APIs** | The **interface family** — customer, catalog, order, billing, resource, trouble ticket | the interface language between BSS domains and to OSS |

> Using a public standard as the interface vocabulary has a specific payoff: an
> ecosystem's integration pattern is reusable, and vendor replacement means
> re-implementing a **standard** interface rather than a proprietary one. This is
> a `stack_stance: stack-agnostic` decision, in the pack's own vocabulary.

## 7. Core flows (L1 view)

1. **Sell** — a customer order is captured against a commercial product offering,
   with eligibility and pricing resolved.
2. **Decompose** — the order is decomposed into service orders and resource
   orders across the domains it touches.
3. **Fulfill** — the OSS side reserves and activates resources, reporting status
   back through the orchestration chain.
4. **Rate** — usage and recurring events are rated into charge events.
5. **Bill** — charges aggregate into invoices on a cycle; adjustments and credits
   are new events.
6. **Collect** — receivables age into dunning, payment allocation, and
   collections.
7. **Support** — trouble tickets and assurance, tying resource state back to the
   commercial relationship.
8. **Reconcile** — order ↔ charge ↔ inventory, in both directions.

## 8. Why this system is unusually hard to get right

- **The commercial object is long-lived and mutable.** A customer's product
  instance exists for years, changes price, changes resources, and is re-billed
  continuously — while the definition that produced it may have been retired.
- **Multi-domain orchestration with partial failure.** An order that touches
  five domains will partially fail, and "cancel the rest" is a stateful problem
  that cannot be a simple rollback.
- **Money must be reproducible.** An invoice must be regenerable from the events
  that produced it, years later, with the pricing that applied.
- **Numbers are a scarce, regulated inventory.** Ranges, codes and ports are
  finite public resources; allocation, release and porting rules are external and
  change.
- **The commercial/technical split cannot be collapsed.** The pressure to
  collapse it is constant, because keeping the specification current is real
  work — and its cost appears when nothing goes wrong.

## 9. Defining quality metrics

L1 frames intent; thresholds become NFR targets at L2.

| Metric | What it answers |
|---|---|
| Order-to-activation lead time (p50/p95) | whether the chain completes |
| Order fallout rate by domain and cause | whether orchestration or a specific domain is the problem |
| Bill cycle on-time rate | whether money is produced on schedule |
| Charge-event reconciliation rate (vs. order and inventory) | whether leakage is detectable |
| Invoice dispute rate | whether the customer-facing number is credible |
| Dunning recovery rate and cost | whether receivables are actually recovered |
| Catalog-publish cycle time (commercial vs. technical) | whether the two catalogs stay coupled to release speed |
| Number-inventory fragmentation (allocated vs. usable) | whether the resource is being wasted |

## 10. Public materials referenced

| Topic | Source | Note |
|---|---|---|
| Component decomposition vocabulary | TM Forum ODA — https://www.tmforum.org/ | Manifest `tmforum-oda`; the normative **component vocabulary** |
| Interface family | TMF Open API family — https://www.tmforum.org/ | Manifest `tmforum-open-api`; the normative **interface language** |
| Network/physical layer recommendations | ITU-T — https://www.itu.int/ | Manifest `itu-t`; recommendations at the physical/network layer |
| Regulatory context | GDPR (`gdpr`, EU) | Manifest designation; see `regulatory-landscape.md` |

> Per this repository's scope decision, **no standard or legal clause was
> verified** in drafting. The pack states the design consequence of adopting the
> ODA/Open API vocabulary (vendor and domain composition) and does not assert
> conformance to any clause. `SOURCES.md` records the standard as a design
> designation only.

> ⚠️ ASSUMPTION: this pack treats ODA and TMF Open APIs as **vocabulary
> adoptions**, not conformity claims. Conformance to a specific ODA maturity
> level or a specific Open API version is a deployment decision the pack does
> not make.
# 01-business / Processes

> Process definitions for the power marketing / CIS suite. Each names its
> trigger, its steps, and the rules that constrain its steps. Rules live in
> `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. No external standard is
> cited for it.

## P-01 — Onboard

| | |
|---|---|
| **Trigger** | a customer takes supply, or a service point changes |
| **Outcome** | a customer record, an account, a service point, a meter, and a tariff assignment |

1. Create the **customer** record — the party.
2. Create the **account** — the billing relationship, with its own lifecycle.
3. Create the **service point** — the physical point of supply.
4. Attach the **meter**.
5. Assign the tariff from the customer class.

> BR-01: customer, account and service point are **distinct objects** with
> distinct lifecycles. Collapsing them makes a service-point change look like a
> customer change, which corrupts both the billing relationship and the
> statistical record.

## P-02 — Read

| | |
|---|---|
| **Trigger** | a metering cycle |
| **Outcome** | readings, exceptions raised, and 估抄 **only by rule and labelled** |

1. Collect via automated collection (AMR/AMI) or field reading.
2. Validate against history: missing, out of range, and inconsistent readings
   become **exceptions** (BR-04).
3. Where a reading cannot be obtained, apply 估抄 **by a defined rule**, and
   label the result as an estimate (BR-05).
4. Record the reading with its **collection method**.

> BR-05 is the load-bearing rule of this process: an estimate substituted
> silently produces a bill that is **arithmetically correct and factually
> unfounded** — unfalsifiable by the customer and unprovable by the utility.

## P-03 — Tariff

| | |
|---|---|
| **Trigger** | readings exist |
| **Outcome** | charges computed under the **effective-dated, versioned** rules |

1. Resolve the **tariff rule version** effective for the period (BR-08).
2. Split any period that straddles an effective date, computing each part under
   the version then effective (BR-08).
3. Emit the charge, stamped with its rule version.

> BR-08 makes the engine governed arithmetic, and the stamp is what makes a
> historical charge interpretable rather than merely retained.

## P-04 — Bill

| | |
|---|---|
| **Trigger** | a cycle closes |
| **Outcome** | an invoice, regenerable from its events |

1. Aggregate charges for the cycle.
2. Apply corrections **as approved adjustments** — the original bill remains
   (BR-09, BR-10).
3. Produce the invoice **with the rule versions** each charge was computed under
   (BR-11).

## P-05 — Collect

| | |
|---|---|
| **Trigger** | an invoice issues |
| **Outcome** | payment applied, or the receivables path followed |

1. Accept payment from any channel and allocate per rule.
2. Age unpaid invoices into dunning.
3. Escalate to collections.

## P-06 — Serve & assure

| | |
|---|---|
| **Trigger** | a customer contacts 95598, or an outage affects customers |
| **Outcome** | a case with real context, dispatched, and closed |

1. Resolve the customer's real situation: account, meter, reading history,
   outstanding payments, and any affecting outage (BR-06).
2. Create a trouble ticket tied to the service instance.
3. Dispatch field work **through the interface** (BR-02).
4. Close with a recorded resolution.

> BR-06: step 1 must not require a transfer. A care surface that cannot see
> reading history is a phone directory.

## P-07 — Disconnect / reconnect

| | |
|---|---|
| **Trigger** | an arrears or policy condition |
| **Outcome** | a guarded, audited act — or a refusal |

1. Propose the act.
2. The process **evaluates** eligibility class, notice period and restricted
   period as enforced state (BR-15).
3. Block where any guardrail fails.
4. Record the evaluation, its inputs and its outcome as the complete decision
   record.

## P-08 — Reconcile

| | |
|---|---|
| **Trigger** | scheduled |
| **Outcome** | charge events reconciled against **both** sides |

1. Reconcile against the **order** — attributable to what was supplied (BR-12).
2. Reconcile against **inventory** — usage belongs to someone (BR-12).
3. Close the gaps: usage with no customer, and activation with no charge.

> BR-12: reconciliation is only load-bearing if it runs **both** directions.
> One-way produces a suite that bills correctly and is blind to leakage.

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 distinct customer/account/service point | P-01 |
| BR-02 interface only | P-06 |
| BR-03 commercial decisions never consult network state | P-01, P-06 |
| BR-04 reading exceptions | P-02 |
| BR-05 估抄 by rule and labelled | P-02 |
| BR-06 care sees the real situation | P-06 |
| BR-07 care cannot change network state | P-06 |
| BR-08 tariff rules versioned + effective-dated | P-03, P-04 |
| BR-09 charge events immutable | P-03, P-04 |
| BR-10 correction by approval, original kept | P-04 |
| BR-11 invoice carries rule versions | P-04 |
| BR-12 reconciliation two-way | P-04, P-08 |
| BR-13 retention per class | P-08 |
| BR-14 vocabulary adoption not conformance | (architecture) |
| BR-15 guardrails enforced by process | P-07 |

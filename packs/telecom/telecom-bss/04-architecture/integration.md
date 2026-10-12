# 04 · Integration

> Integration contracts with external systems and the BSS/OSS seam. IDs are
> stable; every flow traces to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design. TM Forum ODA
> and TMF Open API are adopted as **vocabulary** (BR-14); no API version is
> claimed.

## I. External integration points

| ID | Partner | Direction | Purpose |
|---|---|---|---|
| **I-01** | **Distribution / OMS** | both | resource order fulfilment and status feedback — **the seam** |
| **I-02** | **AMI / metering network** | inbound | automated reading ingestion |
| **I-03** | **Field work management** | both | dispatch and completion for meter service |
| **I-04** | **Payment channels** | inbound | collection actuals |
| **I-05** | **Treasury / accounting** | outbound | revenue and settlement |
| **I-06** | **Outage communication** | both | outage events and customer notification |
| **I-07** | **Regulatory reporting** | outbound | statutory reporting |
| **I-08** | **Fraud / risk** | inbound | CDR and order-level signal |
| **I-09** | **Notification gateway** | outbound | notices including pre-disconnection |

## F. Internal flows

### F-01 — Sell
1. Party resolves the customer, account and service point.
2. Commercial catalog resolves the offering and its price plan.
3. The **specification** resolves what the offering means in resource terms.
4. The customer order is created. **No network state is consulted** (BR-01).

### F-02 — Decompose
1. The specification yields the service instances.
2. Service orders are created per service.
3. Resource orders are created per resource, with links recorded **both ways**
   (BR-04).

### F-03 — Fulfil
1. Each RO is routed to the OSS side through the interface (BR-02).
2. Reserve, activate, report status; a domain may fail while others succeed.
3. Status propagates up to the SO and the CO (BR-04).
4. A partial completion is handled explicitly, never by reversing completed
   steps (BR-07).

### F-04 — Rate and bill
1. A usage or recurring event, or an activation, triggers rating.
2. The **effective-dated rule version** is resolved and stamped on the charge
   event (BR-08).
3. The charge event is emitted and becomes immutable (BR-09).
4. At cycle close, charges aggregate into an invoice carrying the rule versions
   used, regenerable from its events (BR-11).

### F-05 — Serve
1. A 95598 case is created with the customer's real situation resolved from
   account, meter, reading history, payment and outage context (BR-06).
2. A trouble ticket is tied to the service instance.
3. Field work is dispatched through the interface (BR-02).
4. Closure is recorded with its resolution.

### F-06 — Reconcile
1. Charge events are read from the append-only store.
2. Reconciliation runs **both** ways: against the order (BR-12), and against
   inventory usage (BR-12).
3. Leak findings — usage with no customer, activation with no charge — are
   raised and aged (NFR-004).

### F-07 — Disconnect / reconnect
1. The act is proposed.
2. The process **evaluates** eligibility class, notice period and restricted
   period as enforced state (BR-15).
3. Any failed guardrail blocks the act.
4. The evaluation, its inputs and its outcome are recorded as the complete
   decision record (FR-022).

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 Distribution/OMS** | OSS-side unavailability must not fail the commercial order path; fulfilment status is *unknown*, and the chain records that. Never assume activation |
| **I-02 metering** | a missed collection window produces an **exception** (P-04), never a silently estimated reading — and an estimate is only by rule and labelled (BR-15's neighbour in the glossary, `00-context` §3) |
| **I-04 payment** | a channel timeout is *unknown*, resolved by treasury lookup — never by retrying into a second credit |
| **I-06 outage** | outage events enrich the care context (BR-06); an unavailable feed degrades the context, never the case |
| **I-08 fraud** | an unavailable risk signal is fail-closed on the affected action, not a bypass |
| **I-07 reporting** | a reporting failure blocks the report, never silently narrows its scope |

> The pattern: external unavailability degrades the external path and is recorded
> as *unknown* — it never assumes the outcome. Fraud is the one fail-closed case,
> because a bypass converts the control into decoration.

## The interface contract (what must be declared)

| Aspect | Declared by the interface |
|---|---|
| **Payload shapes** | resource order request and status feedback, in the adopted TMF vocabulary |
| **State vocabulary** | the activation states and their permitted transitions |
| **Timing** | synchronous acknowledgement vs. asynchronous status, per operation |
| **Ownership** | which side owns resourcing, reservation and release |
| **Failure semantics** | what *unknown* looks like, and how it is resolved |

> An integration that cannot declare all five is not an interface; it is a
> coupling, and it will eventually move SCADA obligations into the BSS suite.
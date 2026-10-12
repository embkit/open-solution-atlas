# 04 · Integration

> Integration contracts with external systems and the interface seam. IDs are
> stable; every flow traces to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design. Adopted
> vocabulary only; no API version is claimed.

## I. Integration points

| ID | Partner | Direction | Purpose |
|---|---|---|---|
| **I-01** | **Distribution / OMS** | both | resource order fulfilment and status feedback — **the seam** |
| **I-02** | **AMI / metering network** | inbound | automated reading ingestion |
| **I-03** | **Field work management** | both | dispatch and completion for meter service and disconnect/reconnect |
| **I-04** | **Payment channels** | inbound | collection actuals |
| **I-05** | **Treasury / accounting** | outbound | revenue and settlement |
| **I-06** | **Outage communication** | both | outage events and customer notification |
| **I-07** | **Regulatory reporting** | outbound | statutory reporting |

## F. Internal flows

### F-01 — Onboard and assign
1. Party resolves the customer, account, service point and meter as distinct
   objects (BR-01).
2. A tariff is assigned from the customer class.

### F-02 — Read
1. Metering collects via AMR or field reading.
2. Validation raises exceptions with reasons (BR-04).
3. Where a reading is unobtainable, 估抄 is applied **by rule** and labelled
   (BR-05).
4. The collection method is recorded with each reading.

### F-03 — Rate and bill
1. The effective-dated rule version is resolved (BR-08).
2. A cycle straddling an effective date is split by evaluation, not by operator
   decision.
3. A charge event is emitted and becomes immutable (BR-09).
4. At cycle close, charges aggregate into an invoice carrying the **rule
   versions** used (BR-11).

### F-04 — Serve
1. A case is created with the customer's real situation resolved from account,
   meter, reading history, payment and outage context (BR-06).
2. A trouble ticket is tied to the service instance.
3. Field work is dispatched **through the interface**; no care act changes
   network state directly (BR-07).

### F-05 — Disconnect / reconnect
1. The act is proposed.
2. The process **evaluates** eligibility class, notice period and restricted
   period as enforced state (BR-15).
3. Any failed guardrail blocks the act.
4. The evaluation, its inputs and its outcome are recorded as the complete
   decision record.

### F-06 — Reconcile
1. Charge events are read from the append-only store.
2. Reconciliation runs **both** ways: against the order (BR-12), and against
   inventory usage (BR-12).
3. Leak findings — usage with no customer, activation with no charge — are
   raised and aged.

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 distribution/OMS** | OSS unavailability must not fail the commercial order path; the status is *unknown* and is recorded as such. Never assume activation |
| **I-02 metering** | a missed collection window produces an **exception**, never a silent substitution. An estimate is only by rule and labelled (BR-05) |
| **I-04 payment** | a channel timeout is *unknown*, resolved by treasury lookup — never by retrying into a second credit |
| **I-06 outage** | outage events enrich the care context; an unavailable feed degrades the context, never the case |
| **I-03 field work** | a failed dispatch is *unknown*, not a completed disconnect. Guardrail evaluation is unaffected |

> The pattern: external unavailability degrades the external path and is recorded
> as *unknown* — never assumed, never defaulted. There is no fail-closed
> exception here, because the acts that matter (disconnection, correction) are
> gated by the platform's own guardrail and approval processes rather than by a
> single external signal.

## The interface contract (what must be declared)

| Aspect | Declared by the interface |
|---|---|
| **Payload shapes** | resource order request and status feedback, in the adopted vocabulary |
| **State vocabulary** | the activation states and their permitted transitions |
| **Timing** | synchronous acknowledgement vs. asynchronous status, per operation |
| **Ownership** | which side owns resourcing, reservation and release |
| **Failure semantics** | what *unknown* looks like, and how it is resolved |

> An interface that cannot declare all five is not an interface; it is a coupling,
> and it will eventually move control obligations into the commercial system.
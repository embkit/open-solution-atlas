# 04 · Integration

> Integration contracts with the platform's neighbours. IDs are stable; every
> flow traces to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design.

## I. Integration points

| ID | Neighbour | Direction | Purpose |
|---|---|---|---|
| **I-01** | **Org source (HR / IAM)** | inbound | roles, positions, reporting lines — the participant source of truth |
| **I-02** | **Callers (applications, portals, APIs)** | inbound | instance creation and queries |
| **I-03** | **Downstream systems** | outbound | service tasks, callbacks, write-backs |
| **I-04** | **Notification gateway** | outbound | todo, reminder, escalation |
| **I-05** | **Document / content store** | outbound | attachments, produced documents |
| **I-06** | **Electronic signature / seal service** | outbound | the CN variant's seal application and verification |
| **I-07** | **Records / archive system** | outbound | 归档 and disposal |
| **I-08** | **SIEM / log platform** | outbound | audit and operational telemetry |

## F. Internal flows

### F-01 — Define and publish
1. The procedure is modelled in BPMN 2.0 vocabulary, with forms, gateways and
   timers.
2. The vocabulary patterns used by each activity are declared **with their
   completion policies**.
3. The version is published with an effective date and a recorded in-flight
   treatment.

### F-02 — Instantiate and route
1. A caller creates an instance; the engine pins it to the version in force.
2. Participants are resolved by role and business scope from I-01.
3. Gateways are evaluated and the next work item(s) created.

### F-03 — Human work
1. A participant claims or receives the item.
2. They act within their pattern's semantics — including transfer (permanent) and
   delegate (bounded, revocable).
3. **Every** act appends an event with actor, timestamp, reason and definition
   version.

### F-04 — Escalate
1. A timer fires.
2. The action authorised for that timer — remind, reassign, route to superior — is
   applied.
3. The escalation is an event, attributed.

### F-05 — Complete and artefact
1. The instance reaches a terminal state.
2. The artefact is produced with its authority attached.
3. In the CN variant, 文号 allocation and seal application occur, and the seal's
   validity is recorded.
4. Retention per class applies, and archive proceeds per the records duty.

### F-06 — Compensate
1. A definition defect or operator action requires correction.
2. The declared compensation path is executed as new events.
3. The correction is recorded with a named authoriser.

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 org source** | an unavailable org source means tasks are **not routed** rather than routed to a fallback. A routing to "the previous holder" is a hard-coded name in disguise (BR-04) |
| **I-03 downstream** | a service-task failure is an exception with a declared retry and compensation path — never a silently skipped step. A skipped gateway is an unexplainable instance |
| **I-04 notification** | a failed reminder degrades the notification, never the instance. The work item still exists and still ages |
| **I-06 seal service** | a failed seal application blocks the artefact rather than producing an unsealed "signed" document. CTL-04 |
| **I-07 archive** | a failed archive leaves the instance retained per class and is recorded, not silently dropped |
| **I-08 SIEM** | telemetry unavailability degrades observability, never the audit trail — the trail lives in the event log (FR-020), not in the telemetry pipeline |

> The pattern: integration unavailability degrades the external path and is
> recorded as *unknown* — never assumed, never defaulted. Participant resolution is
> the one fail-closed case, because a task routed to a guessed approver is an
> approval nobody authorised.

## The caller contract (what a caller must accept)

| Aspect | Declared by the caller integration |
|---|---|
| **Definition version** | a caller receives the version in force; it may not select an arbitrary version unless authorised |
| **Participant model** | callers do not supply approver user names — they supply the business scope, and the engine resolves (BR-04) |
| **Instance semantics** | an instance is pinned to a version; a caller may not assume a live definition after instantiation |
| **Events** | state changes arrive as events, and a caller that caches state must re-read rather than assume a transition it did not observe |

> A caller that supplies its own approver list is the integration version of
> hard-coding participants, and it fails in exactly the same way — silently, when
> someone changes jobs.
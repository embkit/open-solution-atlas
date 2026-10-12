# 01-business / Processes

> Process definitions for the workflow/BPM/OA platform. Each names its trigger,
> its steps, and the rules that constrain its steps. Rules live in
> `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. BPMN 2.0 supplies the
> modelling vocabulary; it does not supply these processes.

## P-01 — Define

| | |
|---|---|
| **Trigger** | a procedure is to be automated |
| **Outcome** | a versioned, publishable **process definition** |

1. Model the procedure in BPMN 2.0 vocabulary (BR-01).
2. Attach the business rules, gateways and SLA that govern it.
3. Version it; publication makes it a governed artefact (BR-02).

## P-02 — Publish

| | |
|---|---|
| **Trigger** | a definition version is approved |
| **Outcome** | the version becomes the one new instances use, and old instances keep theirs |

1. Publish the version with an effective date.
2. Decide the treatment of **in-flight instances** (BR-03).
3. Record the publication with its authority.

> BR-03: a new version must not silently change instances already running. The
> three treatments — let them finish, migrate, or terminate — are explicit
> choices with different consequences.

## P-03 — Instantiate

| | |
|---|---|
| **Trigger** | a caller creates an instance |
| **Outcome** | a running instance pinned to the definition version |

1. Resolve participants **by role and business scope**, never by hard-coded user
   name (BR-04).
2. Create the instance pinned to the definition version (BR-03).
3. Open the first work item.

## P-04 — Route

| | |
|---|---|
| **Trigger** | an instance advances |
| **Outcome** | the next work item(s), with vocabulary-defined semantics |

1. Evaluate gateways — exclusive, inclusive, parallel (BR-01).
2. Apply the human-task vocabulary with its **defined** semantics: assign,
   claim, transfer, delegate, 会签, 或签, 加签, 退回, 撤回, add-comment
   (BR-05).
3. Apply timers: reminders, deadlines, escalation (BR-06).

> BR-05 is the pack's core rule and the reason it exists. These terms have no
> standard definition, so an implementation that uses them without stating their
> semantics has invented them.

## P-05 — Human work

| | |
|---|---|
| **Trigger** | a work item reaches a participant |
| **Outcome** | an action, attributed and time-stamped |

1. Claim or receive the item.
2. Act: approve, reject, return for rework, transfer, delegate, countersign.
3. **Every** state change appends an event with actor, timestamp and reason
   (BR-07).
4. The event trail is **replayable** (BR-07).

> BR-07: an approval trail that cannot be replayed is not evidence. Replay is
> what makes a decision defensible months later.

## P-06 — Complete

| | |
|---|---|
| **Trigger** | an instance reaches a terminal state |
| **Outcome** | a completed record with its document, timestamp and full trail |

1. Settle the terminal state.
2. Produce the artefact — decision, document, 文号 (BR-08).
3. Retain the trail per class (BR-09).
4. Archive per the records duty.

## P-07 — Compensate

| | |
|---|---|
| **Trigger** | a definition defect or an operator action requires correction |
| **Outcome** | a compensating path, never an edit of history |

1. Identify the affected instances.
2. Apply the defined compensation path — a new event, not an edit (BR-10).
3. Record who authorised it.

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 BPMN 2.0 vocabulary | P-01, P-04 |
| BR-02 definitions are versioned artefacts | P-01, P-02 |
| BR-03 in-flight instances unaffected by a publish | P-02, P-03 |
| BR-04 participants by role and scope | P-03 |
| BR-05 approval vocabulary has defined semantics | P-04, P-05 |
| BR-06 timers are explicit | P-04 |
| BR-07 every transition auditable and replayable | P-05, P-06 |
| BR-08 artefacts carry their authority | P-06 |
| BR-09 retention per data class | P-06 |
| BR-10 compensation is an event, not an edit | P-07 |
| BR-11 公文/文号/签章 is a CN variant | P-06 |
| BR-12 conformance is not claimed | P-01 |

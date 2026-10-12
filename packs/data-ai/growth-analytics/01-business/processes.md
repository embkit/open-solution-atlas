# 01-business / Processes

> Process definitions for the growth analytics & experimentation platform. Each
> names its trigger, its steps, and the rules that constrain its steps. Rules
> live in `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. No external standard is
> cited for it.

## P-01 — Declare

| | |
|---|---|
| **Trigger** | a product or analytics need for a new event or property |
| **Outcome** | a schema declared and versioned in the registry **before any client emits it** |

1. Declare the event: name, properties, types, meanings, owning team.
2. Version the schema.
3. Publish it to the registry.

> BR-01: the declare-before-emit rule is the only defence against an
> unrepeatable number. An event arrives once; nobody can re-ingest last quarter
> with a different property name.

## P-02 — Collect

| | |
|---|---|
| **Trigger** | a client emits an event |
| **Outcome** | a validated event, or a quarantined event **with a reason** |

1. Validate the incoming event against the declared schema.
2. On success, ingest with the schema version recorded.
3. On failure, quarantine **with the reason** (missing field, wrong type,
   unknown property, version mismatch).

> BR-02: quarantine with reasons is instrumentation health signal. A quarantine
> with no reason is a bin, and the pack treats that as a defect.

## P-03 — Resolve identity

| | |
|---|---|
| **Trigger** | an event arrives |
| **Outcome** | a profile link that is recorded, reversible, and deletable |

1. Resolve anonymous identifier, device, session and known user.
2. Create the merge **with the merge recorded** (BR-03).
3. Record the join key the merge used (BR-04).
4. Derive facts — cohorts, funnel steps, attribution credit (BR-04).

> BR-03/BR-04: a merge that cannot be unmade is a decision made about a person
> that nobody can correct; and a deletion that leaves the join keys lets the
> identity be reconstituted from residue.

## P-04 — Analyze

| | |
|---|---|
| **Trigger** | an analyst asks a question |
| **Outcome** | a funnel, cohort, retention or attribution result |

1. Compute over the resolved identity graph.
2. Funnels, cohorts, retention, attribution, path analysis.
3. Every result is **descriptive** — never a causal claim (BR-06).

## P-05 — Experiment

| | |
|---|---|
| **Trigger** | a decision to run an experiment |
| **Outcome** | a randomised, verifiable experiment with a pre-declared decision rule |

1. **Declare the decision rule before reading** — ship, hold or kill (BR-08).
2. Compute the required **sample size** for the declared effect size (BR-07).
3. Randomise, and record the assignment **in the experiment engine** (BR-05).
4. Verify the assignment ratio (**SRM**) (BR-07).
5. Measure the primary **and** guardrail metrics (BR-07).
6. Compare against a **holdout** where the program warrants it (BR-07).
7. Read only at the pre-declared point — peeking is guarded by the decision rule
   (BR-08).

> BR-05: assignment must live in the experiment engine, not the flag/delivery
> system, because otherwise the ratio is unverifiable and SRM is not computable.

## P-06 — Activate

| | |
|---|---|
| **Trigger** | a segment is applied to a purpose |
| **Outcome** | the segment sent to a destination **under the consent state for that purpose** |

1. Resolve the segment into a **point-in-time member snapshot** (BR-12).
2. Check consent state for the purpose at **activation** (BR-11).
3. Map the platform's event model to the destination's schema through the
   **abstraction** (BR-13).
4. Send, and record the send with its purpose and consent basis.

## P-07 — Revoke

| | |
|---|---|
| **Trigger** | consent withdrawn, or an erasure request |
| **Outcome** | collection and activation both stop, and the identity is removed |

1. Stop **collection** for that purpose immediately (BR-11).
2. Stop **activation** immediately (BR-11).
3. Delete the profile, the **join keys**, and the **derived facts** (BR-04).

## P-08 — Export

| | |
|---|---|
| **Trigger** | scheduled or on demand |
| **Outcome** | schema-versioned curated events and experiment results to the warehouse |

1. Curve events with their **schema version** (BR-02).
2. Export, so downstream meaning is traceable rather than assumed.

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 declare before emit | P-01 |
| BR-02 schema version recorded; quarantine with reasons | P-02, P-08 |
| BR-03 merge recorded and reversible | P-03 |
| BR-04 join keys covered by deletion | P-03, P-07 |
| BR-05 assignment in the experiment engine | P-05 |
| BR-06 descriptive vs. causal | P-04, P-05 |
| BR-07 real statistics | P-05 |
| BR-08 decision rule pre-declared | P-05 |
| BR-09 destinations behind an abstraction, never owner | P-06 |
| BR-10 platform owns the model | P-06 |
| BR-11 consent enforced at collection and activation | P-06, P-07 |
| BR-12 segment is a snapshot | P-06 |
| BR-13 vocabulary adoption | P-06, P-08 |
# ADR-0004 — Disconnection guardrails are enforced state, not configuration

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires disconnect/reconnect processes to follow public-service
regulations **with strict guardrails**.

Disconnection is not a collections action with a switch. It is a regulated act
with humanitarian consequences, and its rules are complex, policy-dependent and
change over time. The classes include things like medical dependency, seasons,
times of day and notice periods — and the reasons a particular customer may not
be disconnected are rarely the ones the operator can list from memory.

The tempting implementation is configuration: a list of guardrail conditions the
operator is expected to observe.

## Options considered

1. **Guardrails as documented rules for operators** — the operator remembers and
   applies them. Correct on a good day, and a good day is not a control.
2. **Guardrails as configuration the operator consults** — better, and it makes
   the rules visible. But the operator still chooses whether to consult, and a
   list that is skipped produces a disconnection nobody can later justify.
3. **Guardrails as enforced process state** — the process evaluates eligibility,
   notice and timing, blocks the act on any failure, and persists the evaluation
   with its inputs and outcomes before the act is recorded.

## Decision

Option 3, enforced by BR-15, FR-021, FR-022, and NFR-009 as an invariant.

The evaluation is a recorded act, not a side effect. A disconnection that cannot
produce a persisted evaluation record cannot be recorded at all (constraint 9).

## Consequences

- Positive: "why was this customer disconnected, and was it permitted?" is
  answerable after the fact, from the record rather than from recollection.
- Positive: the evaluation is what makes an exception auditable — a blocked
  disconnection with its failed guardrail is a finding, not an incident.
- Positive: an operator is not the control. The consequence is that the operator
  is protected as much as the customer.
- Negative: the guardrail policy is a governed artefact that must be maintained
  as regulation changes, and the evaluation cost is on the critical path of every
  disconnection.
- Negative: an overly strict evaluation blocks legitimate acts. The pack does
  not resolve the tension between the two directions of error; it requires that
  the chosen policy be *evaluated and recorded*, which is what makes the trade
> reviewable rather than silent.
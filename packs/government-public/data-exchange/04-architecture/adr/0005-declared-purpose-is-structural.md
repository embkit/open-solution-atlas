# ADR-0005 — The declared purpose is a structural grant attribute, not documentation

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md`'s rule is that no data transfer exists without a recorded, revocable
grant — and the 国发〔2016〕51号 办法's 第十四条 adds the part that makes the
grant more than a form: a consumer department may use shared data **only for the
declared purpose**, must not pass it to third parties directly or in altered
form, and must not use it for other purposes.

The two combine into a specific consequence. If purpose is recorded as free text,
then "did the consumer stay within it?" is not a question the platform can answer —
it is a question a person answers by reading the sentence and exercising judgement.
And a judgement, made monthly, across hundreds of grants, is not a control.

## Options considered

1. **Purpose as free text** — the requirement's form is met, and conformance cannot
   be reported. Every grant looks equally compliant because none can be checked.
2. **Purpose as a selected category** — better, and categories are chosen from a
   fixed set that does not always fit. The ones that do not fit become "other" with
   free text, and "other" is where the conformance question goes to die.
3. **Purpose as a structured attribute, checkable against usage, with conformance
   reported** — the purpose can be evaluated, and a divergence is a finding.

## Decision

Option 3, enforced by BR-05, FR-012, FR-013, FR-024, and model constraint 6. NFR-008
measures the structured share before NFR-013 measures conformance, because the
second is impossible without the first.

Revocation is part of the same rule and is measured separately (BR-07, FR-016,
NFR-003): a grant's value is the lead time until access is actually removed, not the
act of recording the revocation.

## Consequences

- Positive: "did the consumer stay within the declared purpose?" becomes an
  answerable question, and the answer is a report rather than an opinion.
- Positive: a grant records purpose, scope and duration together, so expiry and
  revocation are enforceable rather than advisory (NFR-009).
- Negative: a fixed structured set constrains what a consumer can ask for, and a
> legitimate purpose outside the set must either extend the set or be refused. The
> pack's answer is that extending the set is a governed act, because a free-text
> escape hatch is where conformance reporting stops.
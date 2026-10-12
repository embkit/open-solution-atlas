# ADR-0005 — The anti-double-submission rule is per field, and the failure mode is being helpful

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

The 办法's 第七条 gives this platform its purpose:

> 行政相对人在线办理政务服务事项，应当提交真实、有效的办事材料；**政务服务机构通过
> 数据共享能够获得的信息，不得要求行政相对人另行提供。**

Information the agency can obtain through data sharing must not be demanded of the
applicant. This is the anti-double-submission rule, and it is the reason the
`sibling data-exchange pack` is a dependency rather than a nice-to-have.

The ADR is needed because the rule is violated by the **natural direction of the
system**, not by a defect:

- requiring a document is easy;
- proving it is already available is hard;
- a platform that defaults to asking looks friendlier and is non-compliant.

So the control has to be structural at the level where it can decay, which is the
**field**.

## Options considered

1. **Per-form classification** — "this form can be pre-filled". Faster, and the form
   is not the unit of the rule. A single field that could have been pre-filled is
   missed, and the form is classified as compliant.
2. **Pre-fill where convenient** — the platform pre-fills what is easy and asks for
   the rest. Every field is an independent chance to violate 第七条, and nothing
   records which ones did.
3. **Per-field classification, with a defined permitted alternative on lookup
   failure** — the unit is the field, and the fallback is part of the control rather
   than an operational detail.

## Decision

Option 3, enforced by BR-05, FR-010 through FR-014, and model constraints 6, 7 and
8, with NFR-001 through NFR-003.

Three properties carry the weight, and they are separate:

| Property | What failure it prevents |
|---|---|
| Every field classified, obtainable or not | a field that was never examined, and therefore was demanded |
| Obtainable fields never **required** | a pre-filled field that still blocks submission — the commonest form of the violation |
| A **defined permitted alternative** on lookup failure | the failure being answered by asking again, which is the natural response and the violation |

The third is where implementations fail, and the omission is invisible: a lookup
fails, the form re-asks, the applicant complies, and every metric says the platform
works.

## Consequences

- Positive: the rule is checkable **per field**, which is the only level at which it
  can be enforced, and a decay is a field-level finding rather than an aggregate
  drift.
- Positive: the failure of an integration is not converted into a compliance
  violation, because the alternative is defined.
- Negative: every field needs classification and a defined alternative, which is
> real authoring work per form. The pack's position is that the alternative is a
> hand-maintained fallback, and a fallback nobody defined is where the rule quietly
> becomes "ask".
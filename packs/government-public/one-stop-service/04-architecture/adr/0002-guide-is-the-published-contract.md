# ADR-0002 — The guide is the published contract, so a change is dated and attributed

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that the 事项 is the root and drives forms, materials and SLA.
The 办法's 第六条 makes the guide mandatory and **published**:

> 编制**办事指南**，明确政务服务事项的**受理条件、办事材料、办理流程**等信息。
> 办事指南应当在政务服务平台**公布**。

The consequence of "published" is the one that needs an ADR. A published guide is
not a document the department maintains; it is a document an **applicant is
entitled to rely on**. So a silent change is not a consistency problem — it is a
change to a public commitment that somebody relied on.

The requirement also forces a structural decision. 第六条 makes the three elements
mandatory, which means they are not optional documentation — they are the
declaration that drives form generation, material requirements and routing.

## Options considered

1. **A live document, edited in place** — fastest, and every historical submission
   was made against a guide that no longer exists. "What was I entitled to rely
   on?" becomes unanswerable.
2. **A versioned guide, with changes unnotified** — the version exists, and a
   consumer still sees the current one with no way to know it moved.
3. **A versioned, published guide, with changes dated and attributed, and the
   version relied on recorded at submission** — reliance is inspectable.

## Decision

Option 3, enforced by BR-02, FR-003, FR-004, FR-005, and model constraint 2 — the
three elements are required at publication, and a change is an attributed act.

The load-bearing part is FR-005: an application records which guide version the
applicant relied on **at submission**. Without it, "what was I entitled to rely
on?" is a question a person answers by asking another person.

## Consequences

- Positive: a dispute about whether a material was required is answerable from the
  record, at the version the applicant actually saw.
- Positive: the three mandatory elements make the material list **derivable** from
  the acceptance conditions rather than hand-maintained — which is what makes the
  anti-double-submission rule (ADR-0005) implementable at all.
- Negative: guide changes become governed acts, which is friction on the
  department that owns the item. The pack's position is that the alternative is a
> public commitment that can change without anyone recording it.
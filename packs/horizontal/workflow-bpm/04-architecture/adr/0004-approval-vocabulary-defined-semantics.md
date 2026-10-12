# ADR-0004 — The approval vocabulary is defined by this pack, because BPMN 2.0 does not define it

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` names the reason this pack exists: Chinese approval patterns must be
defined as explicit semantics, not vague labels.

会签 / 或签 / 加签 / 转办 / 退回 are everyday terms in every Chinese OA
deployment, and every vendor defines them. BPMN 2.0 defines none of them. That is
not a gap in BPMN — it is outside its scope as a notation standard — but it means
a requirement written as "when the 会签 group completes" is a sentence with no
referent until somebody writes the referent down.

Each definition in `03-domain/glossary.md` §2 is therefore this pack's
contribution, labelled `[PACK]`, and the pack does not present them as citations.

## Options considered

1. **Leave the terms to the implementation** — the fastest, and a requirement
   referencing 会签 is unbuildable. A team meeting decides what it means, and the
   decision is recorded nowhere.
2. **Choose a vendor's definitions** — the referent exists, and it is one vendor's.
   Vendor replacement changes the meaning of every requirement, and the change is
   invisible in the requirements themselves.
3. **Define them in the pack, at state-machine level, with the completion policies
   named as open decisions** — the referent is public, and the ambiguous cases are
   recorded as ambiguous rather than quietly resolved.

## Decision

Option 3, enforced by BR-05, FR-009 through FR-017, and NFR-007 as an invariant:
an action outside the defined set is illegal.

The definitions are at **state-machine level** — what happens to ownership, what
happens to the other tasks, what is reversible — because that is the level at
which the terms differ, and it is the level at which an implementation can be
checked.

Two completion policies are deliberately left open and recorded as such: whether
会签 ends on any rejection, and whether 或签 cancels the other tasks or merely
never surfaces them. Those are L2 decisions to make, not facts to look up.

## Consequences

- Positive: a requirement referencing 会签 is buildable and testable, and a
  deployment is measurable against a public definition rather than a vendor's.
- Positive: the two undecided policies are visible as decisions, which is what
  stops them being resolved by whichever implementation is installed first.
- Negative: the definitions are the pack's contribution, so a conflict with a
  vendor's semantics is a conflict with the pack. FR-013 and FR-014 require the
  policy to be *declared*, which means a deployment that must match a vendor
  declares the vendor's variant rather than being wrong.
- Negative: defining ten terms at state-machine level is real work, and the
> definitions need the same governance as any other normative content. They are
> not free.
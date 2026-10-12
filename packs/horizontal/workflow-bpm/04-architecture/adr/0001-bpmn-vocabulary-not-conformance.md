# ADR-0001 — BPMN 2.0 is the modelling vocabulary, and no conformance is claimed

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires the modelling vocabulary to be anchored on the BPMN 2.0 public
specification, and separately requires that 公文 and e-seal features live in a
labelled variant. Those are different kinds of statement, and the first one needs
splitting.

BPMN 2.0 is a **notation and interchange** standard. It specifies what diagrams
mean and how to exchange them. It does not specify execution semantics — token
flow, compensation, multi-instance completion — and that is exactly where engines
diverge. Two engines can both be "BPMN-compliant" and run the same diagram
differently.

The question this ADR answers is what the pack claims.

## Options considered

1. **No standard** — the pack invents its notation. Portable on paper, and it
   forfeits the only public vocabulary the ecosystem already shares.
2. **Claim engine conformance** — the pack states a conformance profile, and a
   deployment is measured against a claim the pack never established. This is the
   common approach, and it propagates into procurement documents where it is hard
   to retract.
3. **Adopt the vocabulary; state the semantics the pack needs; claim no
   conformance** — the notation comes from BPMN 2.0, the lifecycle semantics this
   pack requires are written down, and the pack says plainly that no maturity
   level, engine profile or DMN target is claimed.

## Decision

Option 3, enforced by BR-01, BR-12, FR-001, FR-002, FR-029, and NFR-007's
neighbour requirement that a notation extension is declared rather than silent.

The adoption splits into two parts, deliberately: the **notation** is BPMN 2.0's,
and the **semantics** this pack needs are stated in this pack — which is what
makes it possible to say what "correct" means without a vendor's profile.

## Consequences

- Positive: a vendor replacement means re-implementing a **public** vocabulary
  rather than a proprietary one, which is what `stack_stance: stack-agnostic`
  commits to.
- Positive: conformance claims become a separate act with separate evidence,
  rather than a sentence inherited from a pack.
- Negative: without a claimed profile, two deployments of this pack on different
  engines may differ on exactly the semantics the pack cares about, and the pack
  cannot tell you which is "right". That is a real cost and it is the honest one.
- Negative: a notation extension must be **declared** (FR-002), which is friction.
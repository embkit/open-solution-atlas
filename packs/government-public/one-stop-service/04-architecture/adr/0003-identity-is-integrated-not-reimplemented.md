# ADR-0003 — Identity is integrated from the national service, and re-implementation is a liability

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` requires every cross-department data call to carry consent and audit,
and states that electronic licence and seal services are external platform
dependencies. The 办法's 第五条 adds the identity part:

> 建设**全国统一身份认证系统**，为各地区、各部门政务服务平台提供统一身份认证服务，
> 实现**一次认证、全网通办**.

Integrating sounds like a convenience that could be traded away. The pack treats
re-implementation as unacceptable, and the reason is that it creates **two things
to secure and reconcile**.

## Options considered

1. **Re-implement citizen identity locally** — fastest to build, and the platform
   now holds credentials it should not hold, for a population it does not control.
   Two consequences follow: the identity must be reconciled with the national one
   (silently, forever), and it becomes a second breach surface that nobody assessed.
2. **Use the national service for the web channel, and local authentication for
   others** — the common shortcut, usually for POS or an assisted-sales path. Each
   exception is a channel with a citizen identity, and the exception is exactly
   where the reconciliation and the breach surface live.
3. **Integrate only, with no local credential of any kind** — the platform holds a
   reference, not an identity.

## Decision

Option 3, enforced by BR-03, FR-006, FR-007, and the channel contract's identity
aspect, with NFR-006 measuring channel coverage.

An unavailable identity context means **no session**, not a guest session
(`integration.md`). A guest path is how a platform acquires a citizen identity it
should not hold — by making the failure case look like a feature.

## Consequences

- Positive: one identity, one credential store, one breach surface — the national
  one, which is assessed for it.
- Positive: 一次认证、全网通办 is a real property, because no channel has an
  alternative to fall back to.
- Negative: the platform's availability is coupled to the national service's, and a
  national outage stops the platform. The pack accepts this because the alternative
> is a local credential that survives the outage and outlives the need for it.
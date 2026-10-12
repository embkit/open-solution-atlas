# ADR-0004 — A channel is a variant over the shared core, and onboarding is gated

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that mini-program and POS are channel variants. Channels also
arrive at different times, built by different teams with their own conventions — so
the pressure to fork is per-channel, immediate and constant.

The failure of a fork is not a technical regression. It is the omnichannel promise
quietly becoming false: a customer applies online and the service hall cannot see
it; a citizen completes an item on a mini-program and the POS channel starts from
scratch; a refund or a correction has no home because the two channels do not agree
on what an order is.

## Options considered

1. **Allow channel forks** — fastest per channel, and each fork starts as a shortcut
   and ends as a second order system with its own state vocabulary and its own 事项
   model.
2. **One undifferentiated core with channel flags** — avoids duplication but puts
   channel conditionals inside the core, where they compound and cannot be tested
   per channel.
3. **Shared core plus channel adapters implementing a declared contract** — the core
   owns 事项, application, identity and state machine; a channel declares its input,
   payment path, identity handling, fulfilment sources and presentation, and its
   adapter implements the contract.

## Decision

Option 3, enforced by BR-04, FR-008, FR-009, and model constraint 11 — all five
declared aspects before enabling.

The core objects — 事项, application, statutory step, identity — are shared. A
channel differs in **input**, **identity handling** and **fulfilment source**, and
any channel-specific behaviour is a variant configuration the adapter resolves, or
it does not exist.

The identity aspect is the one that fails hardest, and it is the reason the channel
contract declares it: a channel that authenticates locally has acquired a citizen
identity, which is exactly what ADR-0003 forbids.

## Consequences

- Positive: a new channel is a configuration and an adapter, not a project; the
  statutory vocabulary, the clock and the guide apply uniformly, so "why does the
  POS channel show a different state?" cannot arise.
- Positive: onboarding is objective — a channel that cannot declare all five is not
  a variant — which removes an argument otherwise settled by whoever is most
  insistent.
- Negative: every channel must fit the contract, and some will not fit naturally.
  The pack's position is that such a channel is either adapted or not onboarded; a
> fork is not a third option, and the adapter maintenance that follows is recurring
> work.
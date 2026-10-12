# ADR-0004 — A channel is a variant over the shared core, never a fork

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that mini-program and POS are channel variants. Channels also
arrive at different times, built by different teams, with their own conventions —
so the pressure to fork is per-channel, immediate and constant.

The failure of a fork is not a technical regression. It is the omnichannel
promise quietly becoming false: a customer buys online and the store cannot see
it, returns in-store for an online order and the refund has no home, and the
"one number, one price, one promise" property becomes something the business
asserts rather than the platform provides.

## Options considered

1. **Allow channel forks** — fastest per channel. Each fork starts as a shortcut
   and ends as a second order system with its own state vocabulary, its own
   inventory policy, and its own reconciliation.
2. **One undifferentiated core with channel flags** — avoids duplication but
   puts channel conditionals inside the core, where they compound and cannot be
   tested per channel.
3. **Shared core + channel adapters implementing a declared contract** — the core
   owns product, price, inventory, order and money; a channel declares its input,
   payment path, identity handling and fulfilment sources, and its adapter
   implements the contract.

## Decision

Option 3, enforced by BR-14, FR-001, FR-002, FR-016, FR-025, and the channel
contract in `04-architecture/integration.md`.

The core objects — product, price, inventory, order, money — are shared. A
channel differs in **input**, **fulfilment source** and **identity handling**, and
any channel-specific behaviour is variant configuration the adapter resolves, or
it does not exist.

Onboarding is gated (FR-025, FR-026): a channel that cannot declare all five
aspects of the contract is not a variant.

## Consequences

- Positive: a new channel is a configuration and an adapter, not a project; the
  order state machine, the pricing snapshot and the ledger apply uniformly, so
  "why does the store see a different number?" cannot arise.
- Positive: the invariant is measurable. Cross-channel visibility lag (NFR-010)
  and onboarding cycle time (NFR-012) are the early signals that a fork is
  forming in practice, before it exists in the architecture.
- Negative: every channel must fit the contract, and some will not fit
  naturally. The pack's position is that such a channel is either adapted or
  not onboarded — a fork is not a third option.
- Negative: adapters must be maintained as channels change their own APIs. This
  is real, recurring work, and it is cheaper than a fork but is not free.
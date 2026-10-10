# ADR-0001 — One ticket backbone for all intake channels

- Status: Accepted
- Date: 2026-10-09
- Deciders: pack maintainers

## Context

Portal, email, chat, monitoring alerts and API each tempt a team to keep a
"special" queue outside the ticket system. Every such queue becomes a
shadow IT desk: invisible backlog, unowned work, no SLA, no reporting. The
value of an ITSM platform collapses the moment critical work bypasses it.

## Options considered

1. **Channel-native queues** (keep alerts in monitoring, email in mailbox) —
   convenient short-term; work becomes untrackable by construction.
2. **Manual bridge** (humans re-key into tickets) — preserves visibility
   only when humans are diligent; lossy under load.
3. **Single backbone with channel adapters** — every channel creates or
   links a ticket with provenance; dedupe keys prevent spam.

## Decision

Option 3, enforced by FR-004 (dedupe + provenance), BR-01 (nothing outside
the backbone), BR-13 (channel identity rules). Merges keep provenance; the
original channel message is retained as evidence.

## Consequences

- Positive: one queue, one clock, one report; automation and escalation
  apply uniformly.
- Negative: channel adapters must be maintained; noisy sources (e.g. flappy
  monitors) need tuning or they spam the backbone — addressed by dedupe
  signatures, not by exemptions.

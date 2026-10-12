# ADR-0001 — No client emits an event whose schema is not declared

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

`AGENTS.md` states that the event schema registry is the spine, because
ungoverned events make every number unrepeatable.

The mechanism of the failure is precisely this: **an event arrives once.** Nobody
can re-ingest last quarter with a different property name. So the moment a client
ships a rename, every historical funnel built on the old name silently changes
meaning — with no deploy, no diff, and no alert.

That makes schema declaration a *write-time* control. A registry consulted after
the fact is documentation; a registry consulted on write is the spine.

## Options considered

1. **Documentation page, consulted at analysis time** — free to maintain and
   useless. The rename ships, the history changes meaning, and the page records
   what the events used to be.
2. **Schema enforced on ingestion, best-effort** — a client emitting an
   undeclared event is ingested anyway. The protection disappears exactly when it
   is needed, because a client that has drifted is a client that will keep
   drifting.
3. **Declare-before-emit, enforced on ingestion** — no event is ingested whose
   schema version is not registered; a validation failure is quarantined **with
   the reason**; exports carry the version.

## Decision

Option 3, enforced by BR-01, BR-02, FR-001, FR-002, FR-003, FR-004, and
NFR-001, NFR-002, NFR-012.

Two properties carry the weight beyond the obvious:

- **Quarantine with a reason.** A quarantine without a reason is a bin, not a
  signal. The reason is instrumentation health telemetry and is what tells a team
  that a client has drifted.
- **Version on export.** A schema-versioned export is what makes a downstream
> number interpretable later, rather than assumed to mean what it means now.

## Consequences

- Positive: a property rename becomes a visible, versioned migration with a
  mapped history, instead of a silent meaning change.
- Positive: instrumentation health is measurable. The quarantine reason is the
  earliest available signal that a client has drifted, and NFR-002 enforces that
  the signal exists.
- Positive: the export carries its meaning, so the `lakehouse-platform` and
  `enterprise-bi` siblings can rely on what they receive.
- Negative: client teams must declare before shipping, which adds a gate to
  their release path. The gate is the point, but it is real friction and will be
  resented until it has caught someone.
- Negative: a drifted client stops emitting. That is correct — an undeclared
  event is unrepeatable by construction — but it converts a data-quality problem
  into an availability problem, and the pack's position is that this trade is the
> right one.
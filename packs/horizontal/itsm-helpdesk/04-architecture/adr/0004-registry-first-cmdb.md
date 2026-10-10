# ADR-0004 — CMDB: registry-first with optional discovery feeds

- Status: Accepted
- Date: 2026-10-09
- Deciders: pack maintainers

## Context

Open question #1: full discovery/dependency mapping vs. manual registry.
History is littered with CMDBs that promised automatic truth, drifted into
garbage, and were abandoned — taking the tickets and changes that depended
on them down in spirit. Discovery tooling also drags in agent deployments
and network scanning scope that belong to ITAM/monitoring packs.

## Options considered

1. **Full discovery-led CMDB** — richest data; heavy scope (agents, scan
   rights), high drift risk when feeds break; out of this pack's boundary.
2. **Manual registry only** — cheap but rots without a feedback loop;
   dependency views degrade.
3. **Registry-first + optional feeds + mandatory drift loop** — the CI
   registry (typed, effective-dated, relationship-typed) is the source of
   truth; discovery/monitoring feeds are *advisors* that open drift tasks;
   humans reconcile (FR-015/FR-016).

## Decision

Option 3, with BR-10 (retire, don't delete), FR-016 (drift tasks + CMDB
health as a reported metric). Feed integration (I-05/I-06 in
`../integration.md`) is an adapter, not a core dependency; the pack works
with zero feeds.

## Consequences

- Positive: CMDB value is bounded by honesty — health is reported, so rot
  is visible instead of silent; scope stays inside the pack boundary.
- Negative: without feeds, dependency data ages; the pack makes
  *reconciliation a workflow* rather than pretending it away.

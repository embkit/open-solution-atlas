# ADR-0001 — Hold the ISA-95 Level-3 boundary

- Status: Accepted
- Date: 2026-10-08
- Deciders: pack maintainers

## Context

Commercial MES products routinely creep upward into planning (competing with
ERP/APS) or downward into device control (competing with SCADA), because
customers ask for "one system". Both directions create conflicts of
authority: duplicated planning data drifts (overproduction, wrong lots), and
writing to control systems raises safety and validation burdens. ISA-95/IEC
62264 defines level 3 as the execution/operations layer between them.
Options:

1. Expand upward: embed scheduling optimization and planning
2. Expand downward: write setpoints/control directly
3. Hold level 3: consume plans, read equipment, execute & record

## Options considered

1. **Upward expansion** — short-term sales appeal; permanent duplication of
   planning truth; brittle ERP coupling; out of MES's audit mandate.
2. **Downward expansion** — control-adjacent writes demand safety validation
   (IEC 61508-adjacent), regress every equipment change onto MES releases;
   unacceptable risk & cadence mismatch.
3. **Hold level 3** — clean contracts both ways; MES becomes the trusted
   executor and recorder; optimization stays in APS, control in SCADA/PLC.

## Decision

Hold the level-3 boundary (option 3), enforced by FR-002 (consume ERP
orders, no re-planning), BR-01 (quantity reconciliation), and BR-12/ADR-0003
(no control writes). APS optimization (ADR-0004) and control remain external
by contract.

## Consequences

- Positive: clear integration vocabulary (B2MML/ISA-95); MES releases never
  require control re-validation; planning truth stays singular.
- Negative: "just tweak the schedule/setpoint" requests must be routed to
  ERP/SCADA owners — a recurring education cost; some deals expect creep.
- Harder to change later: boundary erosion is easy and costly to reverse;
  this ADR exists precisely to make erosion visible in review.

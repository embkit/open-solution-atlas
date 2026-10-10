# 00 · Stakeholders

| Actor | Role | Goals | Constraints / concerns |
|---|---|---|---|
| Plant manager | accountable for output, cost, quality | trusted real-time visibility; fewer surprises | KPIs must reflect data quality (BR-09), not guesses |
| Production planner (ERP side) | level-4 planning | facts loop back quickly for replanning | MES must not duplicate planning authority |
| Line supervisor / dispatcher | shift-level orchestration | fast dispatch, exception handling, handover | real-time boards; minimal clicks under pressure |
| Operator | executes operations | unambiguous instructions, quick confirmation | gloved/touch UI, local language, ≤ 3 taps routine |
| Quality engineer | inspection plans, NCR disposition | unskippable gates; credible dossier | gates enforced technically (BR-05), not by convention |
| Maintenance technician | equipment & downtime | accurate coding, PM triggers | line-side/mobile entry during repair |
| OT/automation engineer | PLC/SCADA/gateways | clean interfaces, zero control interference | IEC 62443 zones; change windows only |
| Plant IT | platform operations | safe upgrades, backups, security | 24/7 constraints; rolling upgrades |
| Auditor / customer | traceability evidence | complete dossier in minutes | append-only records; signatures in regulated variants |
| Regulator (regulated variants) | compliance oversight | valid e-records/e-signatures | 21 CFR Part 11; EU GMP Annex 11 |

## Trust boundaries (summary; detail in 04-architecture/security.md)

- **OT zone** (PLC/SCADA): MES is a client reading data — never an authority
  writing control (ADR-0003).
- **MES zone**: event store + services — the only writer of shop-floor facts.
- **IT zone / DMZ**: ERP and cloud sync through controlled conduits only.
- **Station terminals**: shared devices; identity via operator badge/login,
  kiosk-hardened; all actions attributable (CTL-04).

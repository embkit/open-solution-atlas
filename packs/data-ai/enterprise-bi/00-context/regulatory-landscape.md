# 00-context / Regulatory Landscape

> **This chapter is deliberately lean, by design decision.** The repository's
> purpose is a complete system design; legal and policy accuracy inside that
> design is relevant **only where it changes what the software must do**.
>
> Accordingly this chapter states each instrument as a **designation** (no
> clause numbers, no currency tracking) and records only the *design
> consequence*: which capability the instrument forces to exist. Where a
> provision is merely restrictive, it is marked as such rather than elaborated.
>
> `verification: unverified`. Not compliance advice.

## 1. Instruments in scope, and what each forces the system to do

| Instrument | Designation | What it forces the platform to provide |
|---|---|---|
| **ISO/IEC 27001** — information security management | Manifest: `iso-iec-27001`, region global | An **access control model with evidence**: who could read what, and a record they did. Satisfies the RLS/CLS + audit requirements already stated from `AGENTS.md` |
| **PIPL / 《个人信息保护法》** | Manifest: `pipl`, region cn | **Row/column-level permission on personal data, and retention**: if a mart contains personal information, its access is restricted by design rather than by dashboard convention |
| **等保2.0 / MLPS 2.0 (GB/T 22239-2019)** | Manifest id used across the repo (`mlps-2-0`) | Graded-protection controls. **Design consequence only**: grading level is an external input that determines logging and access-control depth — the platform must not hard-code an assumed level |

> These three are already listed in `manifest.yaml` and are recorded here only to
> connect them to capabilities. No clause was looked up and no currency was
> checked, by design.

## 2. Regions and their design footprint

| Profile | Distinguishing design requirement |
|---|---|
| **CN** | Personal-information-driven RLS; grading level as a declared platform property |
| **EU / GDPR-adjacent** | The same, with retention limits and deletion propagation |
| **US / other** | No additional design requirement beyond ISO/IEC 27001-class controls |

> The differences do not change the architecture; they change **values in the
> access-control and retention configuration**. That is the only sense in which
> regulatory variation matters to this pack.

## 3. What this chapter deliberately does not do

- No clause-level citation, deliberately — none of it changes a design decision
  in this pack.
- No currency tracking — an instrument's renumbering or amendment has no design
  effect here.
- No HIPAA/GxP/CFR-style printable-record requirements — those apply to the
  regulated-domain packs, not enterprise BI.

> If a future requirement makes one of these provisions load-bearing — for
> example a jurisdiction requiring **per-artifact access certification** or
> **export watermarking** — the capability it implies must be stated in the
> capability map *at that point*, not pre-emptively here.

## 4. Question that would change this

**Does any in-scope jurisdiction require an analytics platform to record, per
artifact, which data it exposed to whom?** If yes, per-artifact access
certification becomes a capability rather than an audit report, and this
chapter should be rewritten around it.
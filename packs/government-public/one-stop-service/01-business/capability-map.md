# 01-business / Capability Map

```
01-business / capability-map.md — One-Stop Government Service Platform (L1)

┌─ 01 Service catalogue (事项) ──────────────────────────────────────────┐
│  事项 catalogue · 行政权力/公共服务 · 办事指南 · materials · SLA      │
└───────────────────────────────────────────────────────────────────────┘
┌─ 02 Published guide & eligibility ────────────────────────────────────┐
│  受理条件 · publication · versioning · item-code standard             │
└───────────────────────────────────────────────────────────────────────┘
┌─ 03 Forms, materials & anti-double-submission ────────────────────────┐
│  schema forms · pre-fill · sharing-vs-asking classification · 补正    │
└───────────────────────────────────────────────────────────────────────┘
┌─ 04 Unified identity integration ─────────────────────────────────────┐
│  一次认证 · national auth client · personal/enterprise identity       │
└───────────────────────────────────────────────────────────────────────┘
┌─ 05 Shared-data verification ────────────────────────────────────────┐
│  consented + audited calls to data-sharing · field-level verification  │
└───────────────────────────────────────────────────────────────────────┘
┌─ 06 Approval lifecycle ───────────────────────────────────────────────┐
│  受理 → 一次性告知 → 审查 → 补正 → 决定 → 出件 · 限时办结 timers      │
└───────────────────────────────────────────────────────────────────────┘
┌─ 07 Electronic seal & licence ────────────────────────────────────────┐
│  unified seal client · GB/T 369xx licence integration · 加注件        │
└───────────────────────────────────────────────────────────────────────┘
┌─ 08 Fee & payment ────────────────────────────────────────────────────┐
│  收费项目 · settlement · receipt · refund                             │
└───────────────────────────────────────────────────────────────────────┘
┌─ 09 Notification & progress ─────────────────────────────────────────┐
│  办件进度 · 补正 notice · result · 证照到期/政策提醒                  │
└───────────────────────────────────────────────────────────────────────┘
┌─ 10 Archive, supervision & feedback ─────────────────────────────────┐
│  electronic archiving (第十二条) · 监管 feed · 好差评 · analytics     │
└───────────────────────────────────────────────────────────────────────┘
```

## 1. Level-1 capabilities

| # | Capability | What it must answer | Notes / L1 position |
|---|---|---|---|
| **CAP-01** | **Service catalogue (事项)** | what can be applied for, and under what conditions | the **root object**, driving forms, materials, routing and deadlines (`AGENTS.md`); two statutory kinds (行政权力/公共服务, 第四条) |
| **CAP-02** | **Published guide & eligibility** | what the applicant is told, and what is actually enforced | 办事指南 with 受理条件/办事材料/办理流程 is **published** and therefore binding (第六条) |
| **CAP-03** | **Forms, materials & anti-double-submission** | what the applicant must supply — and what they must not be asked for | 第七条 is this capability's hard constraint; the material list must be *derived*, not hand-maintained |
| **CAP-04** | **Unified identity integration** | who is applying | integrates the national service; **no** local citizen identity (第五条, `AGENTS.md`) |
| **CAP-05** | **Shared-data verification** | how applicant facts are confirmed without being demanded | every call **consented and audited** (`AGENTS.md`); consumes the `data-exchange` pack |
| **CAP-06** | **Approval lifecycle** | how a 办件 moves from submission to a decision | statutory vocabulary 受理/审查/决定/出件, 一次性告知, 补正, 限时办结 |
| **CAP-07** | **Electronic seal & licence** | how the result is authenticated and how a 证照 is issued | **integrated, never re-implemented**; GB/T 369xx interfaces |
| **CAP-08** | **Fee & payment** | how administrative fees are settled | only where a 事项 has 收费项目 |
| **CAP-09** | **Notification & progress** | where the applicant stands, and what needs doing | progress, 补正 notice, result, expiry/policy reminders |
| **CAP-10** | **Archive, supervision & feedback** | what is provable afterwards, and whether service improves | electronic archiving is a **statutory obligation** (第十二条); supervision feed; 好差评 |

## 2. Boundaries (what each capability does *not* own)

| Capability | Explicitly **not** its responsibility |
|---|---|
| 01 Catalogue | making the decision — that is 06, in the department |
| 02 Guide | holding the authoritative policy — the guide *restates* it; the department owns it |
| 03 Forms | performing the verification — that is 05 |
| 04 Identity | deciding what the applicant is entitled to — that is 01/06 |
| 05 Shared data | **holding** the source data — that is the `data-exchange` pack |
| 06 Approval | drafting the guide — a guide that does not match the process is a defect, fixed jointly |
| 07 Seal & licence | **minting seals or defining licence formats** — that is a national service (第九条/第十条, `AGENTS.md`) |
| 08 Payment | deciding whether a fee is lawful — that is the department's legal basis |
| 09 Notification | making the decision — it announces, it does not decide |
| 10 Archive | deciding retention — that is the archives authority (第十二条); the platform executes |
| 10 Supervision | adjudicating a complaint — it surfaces and routes |

> The boundary that most often breaks in practice is **05 vs. 03**: when a
> shared-data lookup fails, teams reach for "just ask the applicant". That
> converts a transient integration failure into a 第七条 violation. The boundary
> must be enforced by a defined degradation path, not by team discipline.

## 3. Level-1 priorities

Complete for discussion, incomplete for estimation; deliberately silent on
relative difficulty, which needs a reference deployment.

> ⚠️ ASSUMPTION: capabilities **01 (事项 catalogue)** and **03 (materials /
> anti-double-submission)** are named first because `AGENTS.md` treats the
> 事项 as the root object and 第七条 as the platform's defining obligation.
> Editorial ordering, not an evidence-backed criticality claim.

## 4. Out of scope for the whole platform

- **The data itself** — population records, licence records and so on belong to
  the `data-exchange` pack and the owning departments.
- **The national unified services** — identity (第五条), electronic seal
  (第九条) and e-licence sharing (第十条) are integrated dependencies.
- **Departmental case systems** — integration targets, not replacements
  (国发〔2022〕5号).
- **Payments as a business** — the platform settles administrative fees; it is
  not a financial institution.
- **The legal merits of any 事项** — the platform routes and records; it does not
  adjudicate what the law requires.
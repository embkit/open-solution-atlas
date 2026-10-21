# 01 · 流程

> ⚠️ ASSUMPTION — P-01..P-06 是方案包设计：一次通用的服务管理分解。
> ISO/IEC 20000-1:2018 第 8.6 条规定了事件/服务请求/问题管理所要求的*结果*，
> 但并未规定这些流程；ITIL 4 的实践名称仅作术语使用（受许可约束，不复制原文）。
> 见 [`../SOURCES.md` §4](../SOURCES.md)。

## P-01 接入 → 分诊 → 解决（事件 / 请求）

```
intake (portal | email | chat | alert → ticket, deduped)
  → classify (type: incident | request; category; impact×urgency → priority)
  → assign (routing rules → group → owner) with SLA clock start
  → work (investigate | fulfill catalog item) — clock per BR-04 pause rules
  → resolve → requester-confirmed close → CSAT
```

## P-02 升级闭环

```
approaching breach (warning %) → functional escalation (L1 → resolver)
breached / overdue → hierarchical escalation (owner → manager)
escalation is an event, not a rewrite of history (BR-07)
```

## P-03 问题管理

```
recurrence signal (linked tickets ≥ threshold) | major incident
  → problem record → root-cause analysis
  → known error documented (workaround) in KEDB
  → fix via RFC (P-04) | accept risk with review date
  → linked tickets resolve faster; recurrence metric improves
```

## P-04 变更准入

```
RFC raised (from problem | standard catalog | normal)
  → risk classification (standard | normal | emergency)
  → assessment & CAB (standard: pre-approved schedule; emergency: fast path
    with post-review) → scheduled → implemented → review/verify
  → CI states updated in CMDB
```

## P-05 CMDB 真相闭环

```
manual registry + discovery/monitoring feeds
  → CI & relationship maintained → drift detected (missing/changed/retired)
  → drift task → reconcile → CMDB health reported
tickets and RFCs reference CIs; dependency view answers blast-radius queries
```

## P-06 报表与复盘

```
SLA clocks & worklogs → daily ops (backlog, at-risk) → monthly service
review (SLA achievement, MTTR, CSAT, recurrence) → improvement backlog
```

## 贯穿性原则

单一主干、显式时钟、仅追加的历史：每一次状态变更、升级、暂停/恢复与分级修改
都是一个事件——报表是投影，绝不是真相来源（ADR-0002）。

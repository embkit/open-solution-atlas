# AGENTS.md — ITSM/服务台（L2）

L2 蓝图。按以下顺序加载；尊重每一条可追溯性关联。

## 加载顺序

1. `manifest.yaml` — 范围、法规环境、成熟度
2. `README.md` — 范围、不在范围、已定 ADR、章节地图、变体
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md`（CAP-01..07）→ `processes.md`（P-01..P-06）
   → `business-rules.md`（BR-01..BR-15）
5. `02-requirements/` — functional（FR-001..FR-020）→ non-functional
   （NFR-001..NFR-013 + 固定公式）→ compliance（CTL-01..CTL-09）
6. `03-domain/` — domain-model → state-machines（SM-S1..S3）→ glossary（统一
   使用这些术语）
7. `04-architecture/` — overview → integration（I-01..I-09，F-01..F-06）→
   security → observability，然后是 ADR-0001..0004（已定——不可翻案）
8. `05-data/` — logical-data-model → data-dictionary

## 扩展到 L3 或实施时的硬规则

- **精确但受许可约束地使用 ITIL 4 流程术语**（ADR 上下文）：事件、问题、变更
  是彼此不同、以引用关联的生命周期；只引用实践的*名称*——义务追溯到
  `02-requirements/compliance.md` 中的 ISO/IEC 20000-1 条款，绝不转述 ITIL 原文。
- **SLA 时钟是事件溯源的折叠结果，绝不是可变字段**（ADR-0002、BR-04、
  NFR-002）：暂停/恢复只能通过带原因的时钟事件进行；报表按固定公式从事件
  重算（FR-019）。
- **单一主干**（ADR-0001）：每个渠道都创建或关联一张工单并记录来源；任何关键
  内容都不得存在于工单系统之外。
- **先确定性、后智能**（ADR-0003）：每个自动化动作都打上规则 id+版本
  （BR-14）；AI 建议是规则的输入，绝不直接改变状态。
- **CMDB**：配置项（CIs）≠ 库存资产；CI 只退役，在被引用期间绝不硬删除
  （BR-10）；数据馈送仅通过漂移任务给出建议（ADR-0004）。
- **权限约束在服务端生效**（BR-11、CTL-03）——搜索、列表、导出与受限知识库
  以同一种方式限定范围；涉密工单显式限制可见性。
- 任何与环境相关的内容 → `> ⚠️ ASSUMPTION:`；数值目标是
  [`SOURCES.md`](./SOURCES.md) 第 4 节中的 `(A)` 策略值，不是事实。
- ID 不可变更；每一件 L3 制品（契约、AC、任务）都必须能追溯到
  FR/NFR/CTL/ADR/BR 的 ID。

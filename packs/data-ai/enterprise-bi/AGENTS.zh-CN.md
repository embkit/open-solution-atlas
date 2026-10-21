# AGENTS.md — 企业 BI（L2）

L2 蓝图。按以下顺序加载；尊重每一条可追溯性关联。

## 加载顺序

1. `manifest.yaml` — 范围、法规环境、成熟度
2. `README.md` — 范围、不在范围、**已定 ADR**、章节地图、阻塞 L3 的事项
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md`（CAP-01..10）→ `processes.md`（P-01..P-08）→
   `business-rules.md`（BR-01..BR-10）
5. `02-requirements/` — functional（FR-001..FR-020）→ non-functional
   （NFR-001..NFR-012 + 固定公式）→ compliance（CTL-01..CTL-04）
6. `03-domain/` — domain-model（上下文、聚合、不变量）→ glossary
   （统一使用这些术语）
7. `04-architecture/` — overview → integration（I-01..07、F-01..F-06）→
   security → observability，然后是 ADR-0001..0005（已定——不可翻案）
8. `05-data/` — logical-data-model（10 条完整性约束）→ data-dictionary

## 扩展到 L3 或实施时的硬规则

- **指标定义是核心对象**（ADR-0001、BR-01、FR-001–FR-003）：一个具名的人作为
  负责人、一个不可变的版本，以及一个已声明的**连接键**。两个指标可比 ⇔ 它们
  按一个已声明的键相连——绝不是靠名字匹配。同名而语义不同的一对是一个
  **可检测的缺陷**（NFR-002）。
- **可比性需要已声明的关系**（BR-02、FR-004）：在查询时才发现的连接，是一个
  由用户在已发布的仪表盘里发现的缺陷。
- **权限在语义层中被求值，且该层是唯一的读取路径**（ADR-0002、BR-03、BR-10、
  FR-005–FR-009、NFR-003、NFR-004）：一个在层外读取的嵌入、导出、沙箱、预览
  或管理界面，会把访问控制设计变成装饰。
- **身份上下文失败关闭**（BR-04、`integration.md`）：没有身份上下文 ⇒ 无数据，
  绝不是全部数据。呈现时过滤不是查询内求值的替代品。
- **制品固定一个模型版本**（ADR-0003、BR-06、FR-010、FR-011）：模型版本变更
  **先报告影响**，迁移是逐制品的带版本动作。`artifact_version_unpinned` 是
  sev-1。
- **新鲜度相对于契约，认证被计算得出**（ADR-0004、BR-07、FR-012、FR-013）：
  相对于数据库最后一次写入的新鲜度是缺陷，而且刻意**没有可写的 `certified_by`
  字段**（约束 7）。成为已认证还额外要求一个负责人、一个固定版本与一条新鲜度
  契约（FR-016）。
- **自助分析把已认证与用户内容分开，并有晋升路径**（ADR-0005、BR-05、
  FR-014–FR-016）：恰好两种状态；拒绝必须记录理由。没有评审产能的晋升会退化
  成层级——NFR-007 与 NFR-008 是按其*方向*被复核的，而不是按其取值。
- **陈旧制品是无人拥有的，而不是错误**（BR-09、FR-018）：陈旧以一个归属决定
  收尾——指派或退役——绝不以静默删除收尾。
- **数仓内部留在兄弟方案包**（`AGENTS.md`、FR-020）：接入、存储、表格式与转换
  机制委托给 `lakehouse-platform`。
- 任何与环境相关的内容 → `> ⚠️ ASSUMPTION:`；`non-functional.md` 中标注
  `(A)` 的数值目标是策略，不是事实。
- ID 不可变更；每一件 L3 制品（契约、AC、任务）都必须能追溯到
  FR/NFR/CTL/ADR/BR/CAP 的 ID。

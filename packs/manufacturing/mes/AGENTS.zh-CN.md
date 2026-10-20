# AGENTS.md — 制造执行系统（L3）

L3 智能体就绪的方案包。按以下顺序加载；尊重每一条可追溯性关联。按
`09-delivery/milestones.md` 的里程碑顺序 M0→M7 构建，每次从
`09-delivery/task-map.md` 取一个任务（`T-xx`），并且**不要跳过任何验证
钩子**；一个任务只有在其 AC 全部通过后才算完成。

## 加载顺序

1. `manifest.yaml` — 范围、法规环境、成熟度
2. `README.md` — 范围、不在范围、已定 ADR、章节地图、变体
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md` → `processes.md` → `business-rules.md`
5. `02-requirements/` — functional（FR-001..021）→ non-functional（NFR-*）→
   compliance（CTL-*）
6. `03-domain/` — domain-model → state-machines（SM-01..05）→ glossary
7. `04-architecture/` — overview → integration（F-01..F-06）→ security →
   observability，然后是 ADR-0001..0004（已定决策——不可翻案）
8. `05-data/` — logical-data-model → data-dictionary
9. `06-contracts/` — api-overview（C-01..C-24）→ api/openapi.yaml
10. `08-quality/acceptance-criteria.md`（完成的定义）→
    `test-strategy.md`
11. `09-delivery/` — milestones → task-map

## 实施时的硬规则

- **ISA-95 边界（ADR-0001）**：绝不给本方案包添加规划优化或机器控制；ERP 与
  SCADA 保持各自的角色。
- **仅追加（ADR-0002）**：执行事实是不可变事件；更正以补偿事件表达。车间事实
  绝不做 UPDATE。
- **不写控制（ADR-0003）**：MES 绝不写 PLC 控制回路；只有非控制类外设
  （打印机、andon 显示屏）可以接收命令。
- **OEE 数学（BR-09）**：使用业务规则中的精确公式；不要自造 OEE 定义。
- **质量闸门（BR-05）**：阻断性检验由工作流引擎强制，而不是靠界面约定。
- 受监管能力（eDHR/eBR、电子签名）住在 `variants/`——不要把它们写进内核。
- 每一件制品（契约、AC、任务）都追溯到 FR/NFR/CTL/ADR 的 ID；验证状态是
  `source-checked`，不是现场验证过——信任 [`SOURCES.md`](./SOURCES.md) 而非记忆；
  数值目标是假设（`(A)`），要被实测值替换，绝不当作事实呈现。
- 任何与环境相关的内容 → `> ⚠️ ASSUMPTION:`；供应商选择只在 `variants/`。

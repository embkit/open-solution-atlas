# AGENTS.md — 增长分析（L2）

L2 蓝图。按以下顺序加载；尊重每一条可追溯性关联。

## 加载顺序

1. `manifest.yaml` — 范围、法规环境、成熟度
2. `README.md` — 范围、不在范围、**已定 ADR**、章节地图、阻塞 L3 的事项
3. `00-context/` — industry-brief → stakeholders → regulatory-landscape
4. `01-business/capability-map.md`（CAP-01..10）→ `processes.md`（P-01..P-08）→
   `business-rules.md`（BR-01..BR-13）
5. `02-requirements/` — functional（FR-001..FR-020）→ non-functional
   （NFR-001..NFR-012 + 固定公式）→ compliance（CTL-01..CTL-05）
6. `03-domain/` — domain-model（上下文、聚合、不变量）→ glossary
   （统一使用这些术语）
7. `04-architecture/` — overview → integration（I-01..08、F-01..F-06）→
   security → observability，然后是 ADR-0001..0004（已定——不可翻案）
8. `05-data/` — logical-data-model（12 条完整性约束）→ data-dictionary

## 扩展到 L3 或实施时的硬规则

- **schema 未被声明的事件一律不被接入**（ADR-0001、BR-01、FR-001、FR-002）：
  先声明后发出是一个写入时控制。一次校验失败被**带着理由**隔离（BR-02），导出
  携带 schema 版本（BR-02），而 `undeclared_event_ingested` 是 sev-1。
- **合并可逆且会传播**（ADR-0002、BR-03、FR-006）：一次撤销抵达派生事实——
  人群成员资格、漏斗步骤、实验分配。一个无法撤销的合并，就是关于某个人的
  一个无法更正的决定。
- **删除覆盖档案、连接键与派生事实**（ADR-0002、BR-04、FR-007、NFR-004）：
  三者齐全，且分别度量。只删档案的记录不是一次删除。
- **分配住在实验引擎里，绝不在交付/开关系统里**（ADR-0003、BR-05、FR-008）：
  如果分配住在交付里，比例就不可核查，**SRM 就无法计算**，于是每一次比较都
  不可核查。
- **决策规则预先声明**（ADR-0003、BR-08、FR-014）：在结果可见之后才选定的规则
  是一种合理化，而提前偷看是对已声明规则的违反，而不是一次判断。
- **漏斗、人群与归因是描述性的；只有实验是因果性的**（BR-06、FR-010）：这是一
  条能力边界，不是一句免责声明。
- **同意在采集**与**激活两处都被强制**（BR-11、FR-017–FR-019），而 NFR-009
  把这两项检查**分别**上报——一个合并的数字会掩盖是哪个边界缺失。撤回在两处
  都立即生效。激活处的强制是本方案包唯一的**失败关闭**规则。
- **目的地在抽象层之后，绝不是数据所有者**（ADR-0004、BR-09、BR-10、BR-13、
  FR-015、FR-016）：目的地自己回报的数字是对账输入，绝不是真相来源，而目的地
  字段名绝不出现在被存储的事件中。
- **分群是某一时点的快照**（BR-12、FR-020），绝不是实时视图。
- 任何与环境相关的内容 → `> ⚠️ ASSUMPTION:`；`non-functional.md` 中标注
  `(A)` 的数值目标是策略，不是事实。
- ID 不可变更；每一件 L3 制品（契约、AC、任务）都必须能追溯到
  FR/NFR/CTL/ADR/BR/CAP 的 ID。

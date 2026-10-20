# 制造执行系统（MES） / Manufacturing Execution System

| | |
|---|---|
| 成熟度 | 🟢 **L3 — 智能体就绪**（目标 L4） |
| 领域 | manufacturing / mes-mom |
| 技术栈立场 | 厂商中立 |
| 法规环境 | ISA-95/IEC 62264（模型）；ISO 9001:2015 8.5.2；IEC 62443；受监管变体：FDA 21 CFR Part 11、EU GMP 附件 11；等保2.0（中国） |

> **AI 智能体**：从 [`AGENTS.md`](./AGENTS.md) 开始。
> **人类读者**：按章节编号顺序阅读，从
> [`00-context/industry-brief.md`](./00-context/industry-brief.md) 开始。

> ⚠️ **已核对来源 — 未经现场验证。** 来源性质：`llm-drafted` ·
> 验证状态：`source-checked`（2026-10-08）。每一条承重的论断都在
> [`SOURCES.md`](./SOURCES.md) 中追溯到公开标准；无出处的数值目标与设计取舍
> 在使用处标注 `⚠️ ASSUMPTION (A)`。**未**在真实部署中验证——从业者评审尚未
> 完成（见规范第 8 节）。

## 本方案包覆盖什么

位于 ERP（规划）与车间控制（PLC/SCADA）之间的信息系统：把计划订单变成可执行
的工单，把工序派到产线/工位，记录实时执行与物料谱系，强制质量闸门，计算
OEE，并提供完整的批次/单件可追溯性——同时不控制机器，也不重新实现规划
（ADR-0001）。

## 范围内

- 制造模型：工厂、产线、工作中心、设备、物料、带生效日的 BOM/工艺路线、
  人员与班次日历
- 计划承接：ERP 订单接入、工单派生、带下达闸门的派工
- 执行：工位终端、事件采集（计数/参数/工时）、andon
- 物料与谱系：备料核验、消耗、批次/序列号正向/反向可追溯、在制品
- 质量执行：带不可跳过闸门的过程内检验、不合格品隔离/处置、SPC（基线）
- 设备与 OEE：状态/停机编码、公式精确的 OEE（BR-09）
- 可视化：产线看板、产出/良率报表、可追溯性档案导出

## 明确不在范围内

- PLC/SCADA/DCS 实时控制（0–2 层；仅以读为主的集成，ADR-0003）
- ERP 规划与成本核算（消费计划、回报事实——ADR-0001）
- LIMS 实验室工作流（集成边界）、APS 有限产能优化（ADR-0004）
- WMS 仓库内部（兄弟方案包）、TMS、电子商务

## L2 已定决策（ADR）

| ADR | 决策 |
|---|---|
| [ADR-0001](./04-architecture/adr/0001-isa95-level3-boundary.md) | 守住 ISA-95 第三级边界：不做规划，不做控制 |
| [ADR-0002](./04-architecture/adr/0002-append-only-event-store.md) | 仅追加的执行事件存储是车间事实的 SSOT |
| [ADR-0003](./04-architecture/adr/0003-equipment-adapter-boundary.md) | 协议适配器集成；MES 绝不写控制回路 |
| [ADR-0004](./04-architecture/adr/0004-dispatch-no-aps.md) | 基于规则的派工 + 人工干预；APS 留在外部 |

## 变体路线图（已声明，尚未编写）

1. `discrete-assembly` —— 序列化单元、工位平衡、每单元 eDHR
2. `process-batch` —— 配方/阶段、以批次为中心、批次记录审核
3. `regulated-edhr` —— 21 CFR Part 11 / 附件 11 控制作为一等能力
4. `xinchuang-cn` —— 面向中国部署的信创技术栈覆盖层

## 章节地图

| 章节 | 内容 |
|---|---|
| [`00-context/`](./00-context/) | 行业简报、法规环境（ISA-95/IEC 62264、ISO 22400-2、ISO 9001 8.5.2……）、干系人 |
| [`01-business/`](./01-business/) | 能力地图、流程、BR-01..BR-13 |
| [`02-requirements/`](./02-requirements/) | FR-001..FR-021（EARS）、NFR-001..NFR-013 `(A)`、CTL-01..CTL-06 |
| [`03-domain/`](./03-domain/) | 限界上下文与聚合、术语表、SM-01..SM-05 状态机 |
| [`04-architecture/`](./04-architecture/) | 概览、L3 集成数据流（F-01..F-06）、安全、可观测性、[4 个 ADR](./04-architecture/adr/) |
| [`05-data/`](./05-data/) | 逻辑数据模型、数据字典 |
| [`06-contracts/`](./06-contracts/) | C-01..C-24 契约清单 + [OpenAPI 3.1 子集](./06-contracts/api/openapi.yaml) |
| [`08-quality/`](./08-quality/) | AC-001..AC-022 + AC-N01..N06、测试策略 |
| [`09-delivery/`](./09-delivery/) | 里程碑 M0–M7、智能体任务地图 T-01..T-30 |

## 待决问题（延续到 L3+）

1. 嵌套工作中心之间的 OEE 聚合语义（按什么加权？）
2. 谱系图存储：投影表 vs. 规模化的图查询引擎。
3. 与 WMS 方案包的联锁：备料区库存真相归哪个方案包所有？
4. B2MML 版本与按设备的 OPC UA 配套规范清单未锁定（第 4 节）。
5. FR-014 的 SPC 规则集（Western Electric / Nelson）未指名（第 4 节）。

## 成熟度路线图

- [x] L1 — 简报
- [x] L2 — 蓝图（21 条 FR、13 条 NFR、6 项控制、4 个 ADR、模型 + 字典）
- [x] L3 — 智能体就绪（24 个契约 + OpenAPI 子集、SM-01..05、28 条 AC、
      F-01..F-06 数据流、测试策略、M0–M7 / T-01..T-30 交付地图）
- [ ] L4 — 已验证

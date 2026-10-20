# 仓储管理系统 / 仓储管理系统（WMS）

| | |
|---|---|
| 成熟度 | 🟢 **L3 — 智能体就绪（Agent-ready）** |
| 领域 | 制造业 / 物流仓储管理系统（同样适用于零售/第三方物流） |
| 技术栈定位 | 厂商中立 |
| 监管背景 | GS1 GTIN/SSCC 与 EPCIS；ISO 9001 可追溯性；ISO/IEC 27001；IEC 62443（IT/OT）；受监管变体：GDP/EU GMP Annex 11、FDA 21 CFR Part 11、冷链；等保2.0 (CN) |

> **AI 智能体**：从 [`AGENTS.md`](./AGENTS.md) 开始。
> **人员**：按编号顺序阅读章节，首先阅读
> [`00-context/industry-brief.md`](./00-context/industry-brief.md)。

> 📑 **Source-checked, not field-verified.** 来源性质：`llm-drafted` · 验证状态：`source-checked`。
> 每项关键论断均追溯至公开来源，或明确标注为
> 假设（见 [`SOURCES.md`](./SOURCES.md)）；该设计**尚未**在真实部署中
> 得到验证。从业人员审查和部署证据仍待完成。

## 本方案包涵盖的内容

库内执行：收货、质检交接、上架、库位管理、补货、波次/订单拣货、打包、发运和循环盘点/库存准确性——采用 RF 扫描枪、条码/RFID，并通过基于任务的设备边界接入自动化立体库（AS-RS）、输送机和自动导引车（AGV），实时运行。核心承诺是在库位/批次/货主粒度上实现 **系统库存 == 实物库存**，并发情况下也不会超卖。

## 涵盖范围

- 主数据：仓库/区域/库位、最小存货单位（SKU）与包装层级/UOM、货主（第三方物流）、批次/序列号/有效期、带生效日期的策略
- 入库：预先发货通知（ASN）、月台调度、收货、系列货运包装箱代码（SSCC）/装卸/物流单元（HU）构建、待质检、定向上架、向 ERP 提交收货过账
- 库内：移库、补货、冻结/待检/隔离、组套/增值服务（VAS）、货主转移
- 出库：波次、分配与软/硬预留、先进先出（FIFO）/先到期先出（FEFO）/批次流向、单件/批次/分区/集群拣货、复核、承运商标签、装载、发运确认、退货
- 库存保障：ABC 循环盘点、差异 → 经职责分离（SoD）批准的调整、ERP 对账、批次/序列号正向/反向召回追溯
- 自动化：仓储控制系统（WCS）/仓储执行系统（WES）任务网关、设备数据采集、人工回退
- 可视化：实时库存、月台/吞吐量 KPI、异常工作台、符合 EPCIS 的事件追溯

## 明确不涵盖的范围

- 运输/路线优化（TMS 配套方案包候选项）
- 库存估值/成本核算/计划——财务事实归 ERP 所有（ADR-0001）
- 采购/订单发起（消费其订单）
- 机器动作/PLC 控制——控制归 WCS/WES 所有（ADR-0003）

## 已确定的 L2 决策（ADR）

| ADR | 决策 |
|---|---|
| [ADR-0001](./04-architecture/adr/0001-physical-vs-financial-inventory.md) | 仓储管理系统负责实物库存；ERP 负责估值——通过事件进行对账 |
| [ADR-0002](./04-architecture/adr/0002-append-only-event-sourced-stock.md) | 仅追加的库存事件是单一事实来源（SSOT）；原子预留可防止超卖 |
| [ADR-0003](./04-architecture/adr/0003-task-based-equipment-boundary.md) | 基于任务的设备网关；仓储管理系统绝不发出机器控制指令 |
| [ADR-0004](./04-architecture/adr/0004-data-driven-strategy-engine.md) | 将上架/分配实现为带生效日期的数据驱动规则引擎 |

## L3 交付物（智能体就绪）

| 交付物 | 内容 |
|---|---|
| [`06-contracts/api-overview.md`](./06-contracts/api-overview.md) | 覆盖所有限界上下文的服务/API 清单 `C-01..C-31`；出站事件流；契约规则（幂等性、单变更路径、原子预留） |
| [`06-contracts/api/openapi.yaml`](./06-contracts/api/openapi.yaml) | OpenAPI 3.1 子集：ASN 接入、上架确认、波次释放、拣货确认、任务确认、设备调度/事件、盘点录入、库存查询、预留 |
| [`07-experience/key-flows.md`](./07-experience/key-flows.md) | 交互契约 `E-01..E-08`（收货、RF 拣货、打包/发运、主管波次看板、循环盘点、异常工作台、第三方物流货主门户） |
| [`08-quality/acceptance-criteria.md`](./08-quality/acceptance-criteria.md) | `AC-001..AC-028` + NFR 闸门 `AC-N01..AC-N14`，每项均映射到 FR/NFR/CTL/BR |
| [`08-quality/test-strategy.md`](./08-quality/test-strategy.md) | 测试层级、覆盖率目标、GS1/FEFO/并发语料集、性能与故障计划 |
| [`08-quality/failure-and-dr.md`](./08-quality/failure-and-dr.md) | 故障模式 `F-01..F-13`、RTO/RPO、备份、演练（RF 离线、网关故障、事件日志恢复） |
| [`09-delivery/milestones.md`](./09-delivery/milestones.md) | 带依赖关系的分阶段映射 `M0..M8` |
| [`09-delivery/task-map.md`](./09-delivery/task-map.md) | 智能体任务 `T-01..T-38`，包含验证挂钩点，并映射到里程碑和 FR/NFR/AC |
| [`09-delivery/sizing-notes.md`](./09-delivery/sizing-notes.md) | 团队形态、相对工作量区间、风险登记册 |
| [`05-data/data-flow.md`](./05-data/data-flow.md) | `DF-1..DF-6` 血缘：入库→事件→投影→ERP；出库→波次→任务→发运；重建；EPCIS 导出 |

完成定义 = 验收标准章节；交付按里程碑顺序执行任务映射，并设置验证挂钩点。

## 变体路线图（已声明，尚未编写）

1. `manufacturing-linked` — MES 暂存区交接、线边作业、成品/血缘
2. `retail-ecom-3pl` — 高吞吐波次、分拣机、退货、多货主计费事件
3. `cold-chain` — 温度分区、IoT 温度偏差、GDP/FEFO、监管链
4. `xinchuang-cn` — 信创技术栈 + 等保2.0 叠加层；保税状态模型

## 开放问题（延续至 L4/后续）

1. 制造/零售/第三方物流共用一个方案包（货主/策略变体），还是拆分出零售专用方案包——当前选择：一个方案包加若干变体（见 ADR-0004）。
2. 核心中 WCS/WES 接口的深度：核心确定基于任务的契约（06-contracts C-28）；确切的厂商字段映射仍留在变体层。
3. 暂存区库存所有权与 `mes` 方案包之间的归属——与 `mes` 开放问题 #3 一并解决（当前选择：明确的发货/转移事件）。
4. 冷链 IoT 数据流：置于事件日志内，还是使用独立的遥测管道——推迟到 `cold-chain` 变体处理。
5. NFR-006 之外针对各故障的 RTO/RPO（例如，Inventory-service 为 15 分钟、区域灾难为 4 小时——见 08-quality/failure-and-dr.md）属于 ⚠️ 方案包建议，需由采用方确认。
6. **采用时需解决的假设**：所有 NFR 目标、BR 数值参数（分桶、上架排序、预留 TTL、容差、ABC 盘点节奏、指标公式）、SM-1..SM-6 转换、API 字段约定以及 DF-1..DF-6 血缘，均为**方案包设计，而非有来源依据的事实**。这些内容在 [`SOURCES.md` §4](./SOURCES.md) 中逐项列出，并在各使用点标记为 `⚠️ ASSUMPTION`。
7. **验证状态**：截至 2026-10-08，`source-checked`——GS1/ISO/IEC 引文已核验并细化到具体部分/版本；该轮检查未发现事实性错误。要达到 `practitioner-reviewed`，必须由具名的领域专家审查范围；要达到 `field-proven`，则需要参考实现/部署。

## 成熟度路线图

- [x] L1 — 概述
- [x] L2 — 蓝图（28 项 FR、14 项 NFR、7 项控制、4 项 ADR、模型 + 数据字典）
- [x] L3 — 智能体就绪（API 契约、EARS→AC、任务映射、测试策略、DR）
- [ ] L4 — 已验证（参考实现、验证报告、部署证据）
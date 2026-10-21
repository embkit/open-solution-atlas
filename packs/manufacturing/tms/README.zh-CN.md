# 运输管理系统（TMS） / Transportation Management System

| | |
|---|---|
| 成熟度 | 🟢 **L3 — 智能体就绪**（目标 L4） |
| 领域 | 制造工业 / logistics-wms |
| 技术栈立场 | 厂商中立 |
| 法规环境 | GS1 EPCIS 2.0/CBV 2.0；ISO 28000:2022；Incoterms® 2020；危险品：ADR 2025、IMDG 2024 (A42-24)、IATA DGR 第 67 版、JT/T 617-2018 + GB 6944-2025；GDPR；等保2.0（中国） |

> **AI 智能体**：从 [`AGENTS.md`](./AGENTS.md) 开始。
> **人类读者**：按章节编号顺序阅读，从
> [`00-context/industry-brief.md`](./00-context/industry-brief.md) 开始。

> ⚠️ **已核对来源 — 未经现场验证。** 来源性质：`llm-drafted` ·
> 验证状态：`source-checked`（2026-10-09）。每一条承重的论断都在
> [`SOURCES.md`](./SOURCES.md) 中追溯到公开来源；无出处的数值目标与设计取舍
> 在使用处标注 `⚠️ ASSUMPTION (A)`。**未**在真实部署中验证——从业者评审
> 尚未完成（见规范第 8 节）。

## 本方案包覆盖什么

货物移动的运输执行层：规划、订立、派车、跟踪并结算——运输订单、承运商与费率
管理、装载构建、路径与招标、在途可视化、送达证明、运费结算。核心问题是货运中
的**计划 vs. 实际 vs. 发票**——规划好的路径/装载/承运商必须与实际执行
（里程碑、POD）以及最终被支付的发票完成对账，且约定价格在接单时被冻结。

## 范围内

- 运输订单：来自 ERP/WMS 的需求接入、集拼、多段运输
- 承运商与费率管理：承运商主数据与资质、带生效日期的费率合同、即时报价
- 装载规划：装载构建（方/重）、车辆选择、运力守卫
- 路径与派车：带可插拔求解器的路径规划（ADR-0002）、招标/接单、分配
- 在途可视化：里程碑事件、ETA 与异常、POD（回单）
- 运费结算：依据冻结费率快照的成本、发票三方审计、争议、结算批次
- 危险品合规元数据：针对带版本法规数据的校验（ADR-0003）
- 集成：ERP/WMS 交接、承运商 EDI（EDIFACT/X12）/API、EPCIS 2.0 事件发布

## 明确不在范围内

- 仓库执行——上架、拣货、打包、库存（兄弟方案包 WMS）
- ERP 采购/订单管理与财务账务（集成目标）
- 车队车载终端硬件/车载设备（集成来源）
- 全球贸易合规/报关引擎（候选兄弟方案包）

## 章节地图

| 章节 | 内容 |
|---|---|
| [`00-context/`](./00-context/) | 行业简报、法规环境（锁定版本）、干系人 |
| [`01-business/`](./01-business/) | 能力地图，P-01..P-06 流程，BR-01..BR-12 |
| [`02-requirements/`](./02-requirements/) | FR-001..FR-022（EARS），NFR-001..NFR-013 `(A)`，CTL-01..CTL-08 |
| [`03-domain/`](./03-domain/) | 限界上下文与聚合、术语表、SM-T1..SM-T5 状态机 |
| [`04-architecture/`](./04-architecture/) | 概览、L3 集成数据流（F-01..F-07）、安全、可观测性、[5 个 ADR](./04-architecture/adr/) |
| [`05-data/`](./05-data/) | 逻辑数据模型、数据字典 |
| [`06-contracts/`](./06-contracts/) | C-01..C-26 契约清单 + [OpenAPI 3.1 子集](./06-contracts/api/openapi.yaml) |
| [`08-quality/`](./08-quality/) | AC-001..AC-022 + AC-N01..N06、测试策略 |
| [`09-delivery/`](./09-delivery/) | 里程碑 M0–M7、智能体任务地图 T-01..T-32 |

## L2 已定决策（ADR）

| ADR | 决策 |
|---|---|
| [ADR-0001](./04-architecture/adr/0001-wms-tms-erp-boundary.md) | 守住 WMS/TMS/ERP 边界；TMS 绝不发明需求 |
| [ADR-0002](./04-architecture/adr/0002-pluggable-solver-boundary.md) | 优化是可插拔的求解器边界，带基于规则的兜底 |
| [ADR-0003](./04-architecture/adr/0003-dangerous-goods-data-not-logic.md) | 危险品：针对法规*数据*版本校验，绝不重新实现法律 |
| [ADR-0004](./04-architecture/adr/0004-rate-snapshot-at-acceptance.md) | 费率快照在接单时冻结；发票绝不按实时费率定价 |
| [ADR-0005](./04-architecture/adr/0005-plan-vs-actual-dual-state.md) | 计划与实际是分离的、仅追加的状态 |

## 变体路线图（已声明，尚未编写）

1. `air-dgr` — IATA DGR 接收流程、e-DGD
2. `sea-imdg` — IMDG 积载/隔离与海运单证
3. `regulated-edhr` — 受监管的电子单证/电子签名控制
4. `xinchuang-cn` — 面向中国部署的信创技术栈覆盖层

## 待决问题（延续到 L3）

1. 费率模型的深度：参考费率卡（当前决策，ADR-0004）vs. 复杂合同的完整费率
   引擎。
2. ISO 28000 / GDPR / 等保2.0 的条款级控制映射（今天只有标准级别，第 4 节）。
3. 按交易伙伴画像锁定 X12/EDIFACT 版本（名称固定；版本是部署输入，第 4 节）。
4. 燃油附加费的重算公式：合同数据 vs. 方案包提供的参考实现。
5. 多段运输的结算分摊（跨运输段/承运商拆分发票）——L2 尚未规定。

## 成熟度路线图

- [x] L1 — 简报
- [x] L2 — 蓝图（22 条 FR、13 条 NFR、8 项控制、5 个 ADR、模型 + 字典）
- [x] L3 — 智能体就绪（26 个契约 + OpenAPI 子集、SM-T1..T5、28 条 AC、
      F-01..F-07 数据流、测试策略、M0–M7 / T-01..T-32 交付地图）
- [ ] L4 — 已验证

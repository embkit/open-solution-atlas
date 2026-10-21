# 全渠道电商交易与订单履约平台 / Omnichannel Commerce & Order Platform

| | |
|---|---|
| 成熟度 | 🔵 L2 — 蓝图（目标 L3） |
| 领域 | 零售电商 / commerce-platform |
| 技术栈立场 | 厂商中立 |
| 监管背景 | 电子商务法与 PIPL (CN)；凡接触卡数据之处均适用 PCI-DSS（默认设计：绝不接触卡数据——采用托管支付字段） |

> ⚠️ **草稿——未经现场验证。** 来源性质：`llm-drafted` · 验证状态：`unverified`。
> 在 LLM 辅助下依据公开标准起草；**未**在实际部署中验证。在 [`SOURCES.md`](./SOURCES.md) 和独立审查将验证状态提升之前，应将具体声明视为假设（见标准 §8）。

## 本方案包涵盖

零售商的交易核心：商品信息与商品目录、店面搜索、购物车/结算、订单管理（含多渠道库存扣减与拆分履约）、促销/定价引擎、会员与忠诚度、售后（退款/换货），以及支撑日常商业运营的仪表板。渠道：Web、应用、小程序、线下 POS——均作为同一订单核心的变体处理。

## 范围内

- 商品/PIM：SKU/SPU 建模、属性与变体、分类体系、丰富内容、上下架生命周期、渠道专属刊登
- 商品目录与搜索：索引、分面导航、库存感知展示
- 交易：购物车（访客 + 会员）、价格快照、结算、订单状态机、幂等性、分布式事务模式（订单 ↔ 库存 ↔ 支付）
- OMS：渠道库存分配、仓库/门店路由、拆单、发货跟踪、交付承诺
- 促销：优惠券、营销活动、叠加与优先级规则、价格模拟、预算/配额控制
- 会员：注册、等级/积分、权益；同意与隐私
- 售后：退款/退货/换货工作流、库存冲正、支付提供商退款集成
- 运营：GMV/订单仪表板、库存告警、结算/对账

## 范围外（明确排除）

- 支付收单/清算内部机制（以抽象方式集成 PSP；核心中不流转卡数据）
- WMS 内部机制（同级方案包：复用 manufacturing/wms 模式）
- 直播电商托管工具（候选变体）
- 第三方平台多商家结算（独立方案包候选项）

## 待决问题

1. ~~库存一致性模式：预留 saga 与以 redis 扣减为规范做法~~ — **已由 ADR-0001 确定**：按商品设置库存占用策略，将预留与消耗作为不同操作，并强制设置预留过期。门店层面的选择留待部署时决定。
2. ~~POS/线下深度：变体还是核心渠道适配器？~~ — **已由 ADR-0004 确定**：采用变体，绝不构成渠道分叉；POS 与其他任何渠道一样声明渠道契约。
3. 促销引擎：规则 DSL 的范围与模拟保真度。

## 已确定的 ADR（不得重新讨论）

| ADR | 决策 |
|---|---|
| **0001** | 库存扣减**按商品**执行；预留与消耗是不同的操作；必须设置预留过期 |
| **0002** | 定价在请款时冻结为**不可变快照**，绝不重算；快照记录其规则集版本 |
| **0003** | 资金操作的**幂等键由平台签发**，而非 PSP 签发，因为 PSP 的幂等键无法覆盖 POS 或第三方平台路径 |
| **0004** | 渠道是**共享核心之上的变体**，绝不构成渠道分叉；渠道接入以渠道契约为闸门 |
| **0005** | 通过**托管支付字段**排除支付合规范围，且这种排除须**按渠道予以证明**，而不是仅对整体架构作一次性声明 |

## 章节地图

```
00-context   industry-brief · regulatory-landscape · stakeholders
01-business  capability-map (CAP-01..10) · processes (P-01..08) · business-rules (BR-01..15)
02-requirements  functional (FR-001..028) · non-functional (NFR-001..012 + 固定公式)
             · compliance (CTL-01..08)
03-domain   domain-model (上下文、聚合、不变量) · glossary
04-architecture  overview · integration (I-01..09, F-01..06) · security · observability
             · adr/0001..0005
05-data     logical-data-model (10 项完整性约束) · data-dictionary
```

## 成熟度路线图

- [x] L1 — 简报
  - [x] 附有来源的行业简报 (`00-context/industry-brief.md`)
  - [x] 监管环境 (`00-context/regulatory-landscape.md`)
  - [x] 利益相关方列表 (`00-context/stakeholders.md`)
  - [x] L1 能力地图 (`01-business/capability-map.md`)
  - [x] 术语表初始内容 (`03-domain/glossary.md`)
- [x] L2 — 蓝图
  - [x] 业务流程/规则 (`01-business/processes.md` P-01..08,
        `business-rules.md` BR-01..15)
  - [x] 带稳定 ID 的功能需求 (`02-requirements/functional.md`,
        FR-001..028)
  - [x] 包含可度量目标和固定公式的 NFR 目录
        (`02-requirements/non-functional.md`, NFR-001..012)
  - [x] 追溯至适用法规指定的合规控制项
        (`02-requirements/compliance.md`, CTL-01..08)
  - [x] 包含限界上下文的领域模型 (`03-domain/domain-model.md`)
  - [x] 架构视图 (`04-architecture/overview.md`, `integration.md`,
        `security.md`, `observability.md`)
  - [x] ≥3 个涵盖关键支撑决策的 ADR (`04-architecture/adr/`,
        0001..0005)
  - [x] 逻辑数据模型 + 数据字典 (`05-data/`, 10 项
        完整性约束)
- [ ] L3 — 智能体就绪
  - [ ] 核心服务的 API 契约 (`06-contracts/`)
  - [ ] 关键生命周期对象的状态机 (`03-domain/state-machines.md`)
  - [ ] 具备完整需求可追溯性的 EARS 验收标准
        (`08-quality/`)
  - [ ] 集成与数据流规格（协议、载荷、频率）
  - [ ] 测试策略，包括性能和故障场景
  - [ ] 交付里程碑 + 智能体可执行任务图 (`09-delivery/`)
  - [ ] `AGENTS.md` 加载顺序通过端到端验证
  - [ ] 一致性审查：ID 均可解析、术语表用词统一、需求、设计与契约之间不存在
        矛盾
- [ ] L4 — 已验证

### 阻断 L3 的事项

1. **订单状态机本身**——规则和需求中均已给出状态及转换的名称；L3 要求在
   `03-domain/state-machines.md` 中逐一列举。
2. **渠道适配器接口契约**——已声明的五个方面目前仅以说明形式存在于
   (`04-architecture/integration.md`)；L3 需要将其制定为契约。
3. **三个零容忍不变量的验收标准**——NFR-001、NFR-004 和 NFR-005 需要能够
   判定构建失败的判据，而不是仅供报告的阈值。
4. **按差异类型划分的对账闭环程序**——BR-13 要求闭环处理；各类型程序尚未规定。
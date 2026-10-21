# SOURCES — 制造执行系统

> 来源台账。把本方案包中承重的论断映射到公开、可核查的来源；无法追溯的内容
> 列在第 4 节，并在各章中标注 `> ⚠️ ASSUMPTION:`。
>
> **状态：`source-checked`**（2026-10-08）。来源性质：`llm-drafted`。
> 验证状态：`source-checked` — **未**经现场验证。见
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md)。
>
> 来源核对于 2026-10-08。结果：(a) ISA-95/IEC 62264 的部分标题已锁定；
> (b) **BR-09（OEE）现在有了真正的标准来源——ISO 22400-2:2014**——而起步
> 台账曾记为「无来源」；(c) 确认 **IEC 62264-3 明确规定不规定谱系**，因此
> 本方案包的谱系模型是超出标准的扩展，而不是推导结果。

## 1. 标准与规范

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| 第三级边界、设备/运营层级、对象模型（人员/设备/物料/过程）——ADR-0001、CTL-03 | ISA / IEC | ANSI/ISA-95 = **IEC 62264** —— 第 1 部分*模型与术语*；第 2 部分*对象与属性*；第 3 部分*制造运营管理的活动模型*；第 4 部分*MOM 集成的对象与属性* — https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard | 部分标题已确认；IEC 62264-2 有第 3 版（2026）。ISA 系列还记录了 1–4 之外的部分 |
| 支撑本方案包限界上下文与 BP-01..BP-06 的 MOM 活动分解 —— capability-map、processes | ISO/IEC | **IEC 62264-3:2016** —— 生产/维护/质量/库存的运营管理，每项含定义管理、资源管理、详细排程、派工、执行管理、数据采集、跟踪、绩效分析 — https://www.iso.org/obp/ui/#!iso:std:62264:-3:en | 本方案包的活动集映射到这个结构 |
| **谱系**作为一等能力 —— BR-06、CTL-01、FR-02/FR-15 | — | **IEC 62264-3 未作规定**（附录 C，「Why is genealogy not discussed?」） | 诚实的空白：谱系是**方案包的扩展**，不是标准推导。ISO 9001 8.5.2 提供的是*义务*，不是模型 |
| **OEE 公式** —— BR-09（`OEE = 可用率 × 表现 × 质量`） | ISO | **ISO 22400-2:2014**，*制造运营管理 KPI —— 第 2 部分：定义与说明*：「OEE 指数 = 可用率 × 效率 × 质量之比」，单位 %，取值 0–100% — https://www.iso.org/standard/53936.html | 关闭了起步台账的待办项。第 1 部分 = 概览/概念/术语。22400-2 正在修订中（DIS 第 2 版） |
| 对齐 IEC 62264 **工作单元**的 KPI 要素 —— BR-09、FR-018 | ISO | ISO 22400-2:2014（工作单元范围） | |
| 六大损失 / OEE 的 TPM 起源 | 文献 | Nakajima, S.,《Introduction to TPM: Total Productive Maintenance》（Productivity Press，1988） | 历史起源；**不是**规范定义（规范定义是 ISO 22400-2） |
| 产品标识与可追溯性（义务）—— BR-06、CTL-01 | ISO | ISO 9001:2015 第 **8.5.2** 条 — https://www.iso.org/standard/70089.html | 条款号已确认（`wms` 方案包也使用） |
| ERP↔MES/控制的集成词汇（「兼容 B2MML」）—— NFR-008、ADR-0001 | MESA International | **B2MML**（Business To Manufacturing Markup Language），ISA-95 的 XML 实现 — https://www.mesa.org/ | B2MML-Common **Version 0600** 是 OPC UA 为 ISA-95 配套规范引用的修订；当前 MESA 发布版待确认 |
| 设备信息模型与配套规范 —— NFR-008、ADR-0003 | OPC 基金会 / IEC | **IEC 62541**（OPC UA）系列 —— 第 3 部分地址空间模型、第 4 部分服务、第 5 部分信息模型…… — https://opcfoundation.org/ ；**OPC UA for ISA-95** 配套规范 — https://reference.opcfoundation.org/ISA-95/ | 配套规范按领域划分；本方案包说「在存在的地方」 |
| OT/IT 分区、区域与管道、最小权限 —— CTL-03、NFR-012 | IEC | **IEC 62443-3-2:2020**（区域与管道）、**62443-3-3:2013**（系统安全要求）、**62443-4-2:2019**（组件要求） | 与 `wms` 方案包同样的锁定 |
| 电子记录 / 电子签名（受监管变体）—— CTL-02/04/05、BR-11 | 美国 FDA | **21 CFR Part 11** — https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11 | 仅变体；条款级控制映射见第 4 节 |
| 计算机化系统验证、数据完整性（受监管变体）—— CTL-02、BR-11 | 欧盟委员会 | EU GMP **附件 11**（EudraLex 第 4 卷）— https://health.ec.europa.eu/medicinal-products/eudralex_en | 仅变体 |
| ALCOA+ 数据完整性框架 —— CTL-02 | MHRA | MHRA《'GXP' Data Integrity Guidance and Definitions》（2018） | 公开的监管指南；**确切 URL 待确认** |
| 中国部署基线 —— CTL-06 | SAC（中国） | **GB/T 22239-2019** 信息安全技术 网络安全等级保护基本要求（等保2.0） | 仅按**标准级别**引用；无条款级映射 |
| 器械历史记录变体触发（医疗器械） | ISO | ISO 13485（QMS） | 仅引用；条款映射待确认 |
| PPAP / 防错变体触发（汽车） | IATF | IATF 16949 | 仅引用；版本与条款待确认 |
| 车间时钟同步 —— BR-10、NFR-006 | IETF | RFC 5905（NTPv4）— https://www.rfc-editor.org/rfc/rfc5905 | RFC 定义了协议；本方案包的 `偏差 ≤ 1 秒` 界限是设计选择（第 4 节） |

## 2. 规范性文件（RFC / 官方规范）

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| NTP 时钟纪律 —— BR-10、NFR-006 | IETF | RFC 5905 — https://www.rfc-editor.org/rfc/rfc5905 | 数值偏差预算是方案包参数 |
| ISA-95 / IEC 62264（见第 1 节） | ISO/IEC | IEC 62264 系列 | 中国的 GB/T 18975 采标待确认 |
| OPC UA（见第 1 节） | IEC | IEC 62541 系列（第 4 部分*服务*有 2025 年第 4 版） | 按设备的配套规范清单待确认 |
| OT 遥测的工业 MQTT 命名空间 | Eclipse 基金会 | Eclipse **Sparkplug B** 规范 — https://sparkplug.eclipse.org/ | 作为遥测路径的选项引用，不是强制要求 |

## 3. 可引用的开源实现

| 系统 / 主题 | 项目 | 链接 | 说明 |
|---|---|---|---|
| MES / 工业 4.0 集成模型、OPC UA + AAS | Eclipse BaSyx | https://www.eclipse.org/basyx/ | 适配器/网关边界的参考（ADR-0003） |
| 工业协议集成（S7、Modbus、OPC UA……） | Apache PLC4X | https://plc4x.apache.org/ | 以读为主的适配器参考 |
| OPC UA 栈（C） | open62541 | https://open62541.org/ | 设备适配器的构建块 |
| 设备/事件集成流 | Node-RED | https://nodered.org/ | 说明性；不是控制系统 |
| OT 遥测的 MQTT / Sparkplug B | Eclipse Sparkplug | https://sparkplug.eclipse.org/ | 工业 MQTT 命名空间 |
| MQTT broker | Eclipse Mosquitto | https://mosquitto.org/ | OT 遥测的传输 |
| 仅追加事件存储 / 流处理（ADR-0002） | Apache Kafka | https://kafka.apache.org/ | 一种可行的 SSOT 底座；非强制 |
| 设备/OEE 信号的时间序列存储 | InfluxDB | https://www.influxdata.com/ | FR-017/018 信号的替代存储 |
| 指标与告警（NFR-013） | Prometheus | https://prometheus.io/ | 可观测性基元 |
| 仪表盘 / 产线看板视觉 | Grafana | https://grafana.com/ | 参考工具 |
| 身份、RBAC、SSO（FR-008、CTL-04） | Keycloak | https://www.keycloak.org/ | OIDC/SAML 参考 |
| 策略即代码的授权（RBAC/ABAC） | Open Policy Agent | https://www.openpolicyagent.org/ | 与 XACML 式 PDP 对比 |
| 集成 / EDI 与适配器路由 | Apache Camel | https://camel.apache.org/ | ERP/WMS/LIMS 集成模式 |

## 4. 已声明的假设（无法追溯到来源）

方案包策略或工程预算——**不是事实**。每一条都在使用处标注
`> ⚠️ ASSUMPTION:`，并列在 README 的「待决问题」中。

- **规模档位与全部 NFR 数值** —— 看板 `≤ 2 秒 p95`、工位确认 `≤ 500 毫秒
  p95`、终端缓冲 `≥ 4 小时`、`≤ 50 条产线` / `≤ 2,000` 台终端 /
  `≥ 5,000 事件/秒`、谱系档案 `10,000` 个事件 `≤ 5 秒 p95`、留存
  `≥ 5 年` / `产品寿命 + 2 年`、可用性 `≥ 99.9 %`、易用性 `≤ 3 次点击` /
  `≥ 10 英寸`。都是工程预算；无基准。
  （→ `02-requirements/non-functional.md` 中的 `(A)` 标记）
- **BR-08 未编码停机的自动编码** —— 班次关闭前自动编码为 `UNCODED` 并升级。
  方案包策略；时机没有外部依据。
- **BR-10 双时间戳与 `偏差 ≤ 1 秒`** —— RFC 定义了 NTP；数值界限与
  来源/接入双时间戳规则是方案包的选择。
- **可观测性阈值** —— 「> 5 % 的工位缓冲 > 0」、复制延迟 > 30 秒、班次关闭
  完整性 ≥ 99 %、缺口/拒绝激增告警。
- **SM-01/SM-02/SM-04 的迁移与守卫** —— 例如「ERP 变更只影响 CREATED
  状态的订单」、「QUARANTINED 阻断迁移」、「COMPLETED 要求数量对账」。方案包
  设计。
- **领域模型与限界上下文** —— 方案包设计；IEC 62264-3 提供 MOM 活动词汇，
  但不提供这一分解，也不提供谱系。
- **BP-01..BP-06 的流程流** —— 方案包设计（一次通用的第三级活动分解），不是
  规范文本。
- **逻辑数据模型** —— 实体、键与基数是方案包设计；只有借用的 ISA-95 对象
  词汇具有规范效力。
- **CTL-02/04/05 ↔ 21 CFR Part 11 与附件 11** —— 控制描述是宽泛的；条款级
  映射是断言的，不是引用的。
- **CTL-06 ↔ 等保2.0** —— 「MES 区域的控制映射」与数据安全法的分类范围被
  指名，但未做条款级映射。
- **FR-014（SPC 基线）** —— 「按配置规则的控制图统计」未指名任何规则集
  （例如 Western Electric / Nelson 规则）；待确认。
- **B2MML 版本与 OPC UA 配套规范清单** —— 「兼容 B2MML」与「在存在的地方
  遵循 OPC UA 配套规范」都未锁定 B2MML 发布版或按设备的配套规范清单。
- **ADR-0001..0004** —— 四份都是方案包的架构立场。ADR-0001（第三级边界）
  *符合* IEC 62264-1/3，ADR-0004（APS 在外）符合 IEC 62264-3 附录 D 把
  APS 描述为相邻领域——但两者都不是标准所强制的。

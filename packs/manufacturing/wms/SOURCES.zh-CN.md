# 来源 — 仓储管理系统

> 来源性质台账。将方案包中起关键支撑作用的主张映射到公开、可核查的来源；无法追溯的内容均列于 §4，并在各章中标记
> `> ⚠️ ASSUMPTION:`。
>
> **状态：`source-checked`**（2026-10-08）。来源性质：`llm-drafted`。
> 验证状态：`source-checked` — **未经**现场验证。请参阅
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md)。
>
> 已于 2026-10-08 对照来源完成核查。本次核查未发现所引标准中的**事实错误**；但将三处引用从“系列/通用”细化为具体部分和版本（GS1 EPCIS/TDS 版本、IEC 62443 各部分、ISO 9001 子条款）。其余未引用来源的具体内容均为**方案包设计或工程预算**，在 §4 中声明。

## 1. 标准与规范

| 主题/主张 | 来源 | 参考资料 | 备注 |
|---|---|---|---|
| 条码/AI 数据模型（批次 `10`、序列号 `21`、有效期 `17`、数量、重量）— C-05, CTL-02 | GS1 | GS1 通用规范（AI 定义）— https://ref.gs1.org/standards/ | AI 列表具有规范性；本方案包使用其中一个子集。版次需对照当前发布版本确认 |
| 托盘/容器标签、托盘及纸箱 ID — C-08, FR-008, CTL-02 | GS1 | SSCC、AI **(00)** — 物流单元的唯一 GS1 键 — https://ref.gs1.org/standards/ | 已确认：“SSCC 是唯一必须用作物流单元标识符的 GS1 键” |
| 位置/参与方标识 | GS1 | GLN — https://www.gs1.org/standards/id-keys/gln | |
| 规范事件词汇（Object/Aggregation/Transaction/Association；业务步骤/处置）— C-30, CTL-01 | GS1 | **EPCIS 2.0.0**（2022 年 6 月获批准）+ **CBV 2.0.0** — https://ref.gs1.org/standards/epcis/ | 本方案包将 EPCIS 用作*概念*词汇；外部 JSON/JSON-LD + REST 交换是一种选项（见 §4） |
| RFID 采集通道 — NFR-014 | GS1 | **EPC 标签数据标准 (TDS) 2.3.0**；**EPC UHF Gen2 空中接口 3.0.1** — https://ref.gs1.org/standards/ | |
| 标识与可追溯性、防护、不合格输出控制、记录控制 — CTL-01/03/04/05 | ISO | ISO 9001:2015 — **8.5.2** 标识与可追溯性、**8.5.4** 防护、**8.7** 不合格输出控制、**7.5** 文件化信息 — https://www.iso.org/standard/70089.html | 条款号已对照已发布标准确认 |
| 针对库存/商务数据的 ISMS 控制 — CTL-06, NFR-009 | ISO/IEC | ISO/IEC 27001:2022 附录 A — A.5.15–A.5.18, A.8.2, A.8.13, A.8.15, A.8.24, A.5.33 — https://www.iso.org/standard/27001 | 与 ISO/IEC 27002:2022 的条款编号完全相同 |
| IT/OT 分区与通道、设备边界 — CTL-07, NFR-012 | IEC | **IEC 62443-3-2:2020**（将 IACS 划分为分区与通道）、**IEC 62443-3-3:2013**（系统安全要求）、**IEC 62443-4-2:2019**（组件要求） | https://webstore.iec.ch/en/publication/30727 · /7033 · /34421 |
| 良好分销规范（药品；先到期先出 (FEFO)/温度/监管链）— 冷链变体 | 欧盟委员会 | 欧盟 GDP — **2013/C 343/01** | 仅用于变体；核心部分编码的是*义务* |
| 计算机化系统/电子记录（受监管变体）— CTL-05 | 欧盟委员会 | EU GMP **附录 11**（EudraLex 第 4 卷）— https://health.ec.europa.eu/medicinal-products/eudralex_en | 仅用于变体 |
| 电子记录/电子签名（受监管变体） | 美国 FDA | **21 CFR Part 11** — https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11 | 仅用于变体 |
| 食品链可追溯性 | ISO | ISO 22005 | 已引用（变体）；版次待确认 |
| HACCP 原则 | Codex Alimentarius | Codex **CXC 1-1969**（食品卫生通用原则，含 HACCP） | 已引用；版次待确认 |
| CN 部署基线 | SAC（中国） | **GB/T 22239-2019** 网络安全等级保护基本要求 (MLPS 2.0) | 仅在标准层级引用；本方案包未进行条款级映射 |
| B2B 单据：DESADV/预先发货通知（ASN）、ORDERS、IFTMIN — C-06/C-16 | UNECE | UN/EDIFACT — https://unece.org/trade/uncefact | 消息版本待确认 |
| B2B 单据（UN/EDIFACT 的 GS1 子集） | GS1 | **EANCOM** — https://ref.gs1.org/standards/eancom/ | 当前版本为 2022（依据 GS1 资源库） |
| B2B 单据：X12 856/850 | ANSI ASC X12 | ANSI X12 **856**（发货通知/装车/发运清单）、**850**（采购订单） | 规范集/版本待确认 |
| 危险品存储隔离 — BR-04 | UNECE / IATA / IMO | ADR / IATA DGR / IMDG Code | 方案包仅编码*属性*（危险类别）；未嵌入法规正文 |

> 此行以下凡属于**数值或设计规则**而非引用者，均列于 §4。

## 2. 规范性文档（RFC / 官方规范）

| 主题/主张 | 来源 | 参考资料 | 备注 |
|---|---|---|---|
| 错误载荷 `application/problem+json` — 06-contracts 约定 | IETF | RFC 9457（HTTP API 问题详情）— https://www.rfc-editor.org/rfc/rfc9457 | |
| HTTP 状态语义（预留冲突时为 `409`，以及 `429` 等）— C-23, F-05 | IETF | RFC 9110（HTTP 语义）— https://www.rfc-editor.org/rfc/rfc9110 | 这些状态码是标准定义；此处如何使用属于设计选择 |
| 时间戳 `occurred_at` 与 `recorded_at`、ISO-8601 UTC | IETF | RFC 3339 — https://www.rfc-editor.org/rfc/rfc3339 | |
| 运营 API 的 OAuth 2.0 持有者令牌认证 | IETF | RFC 6750 — https://www.rfc-editor.org/rfc/rfc6750 | |
| 用于人员/设备身份认证的 OIDC SSO | OpenID Foundation | OpenID Connect Core 1.0 — https://openid.net/connect/ | |

## 3. 可引用的开源实现

| 系统/主题 | 项目 | 链接 | 备注 |
|---|---|---|---|
| 仓储执行与库存管理（基于任务的 WMS） | openWMS.org | https://openwms.org/ | 任务/库存模型参考 |
| 仓库与订单/库存管理 | Apache OFBiz | https://ofbiz.apache.org/ | 仓库/订单/库存组件 |
| 库存/仓库管理 | Odoo Inventory | https://www.odoo.com/ | 以库存模块为参考 |
| 库存/供应链管理 | OpenBoxes | https://openboxes.com/ | 以批次/有效期为中心的参考 |
| 仅追加/事件驱动的库存与任务流 (ADR-0002) | Apache Kafka | https://kafka.apache.org/ | 可作为 SSOT/outbox 基础组件；并非强制要求 |
| 授权/SSO (CTL-06, NFR-011) | Keycloak | https://www.keycloak.org/ | OIDC/SAML 参考 |
| 按货主隔离的行级安全 (BR-13, CTL-06) | PostgreSQL | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | 使用 RLS 作为隔离机制 |
| EDI/B2B 单据集成（预先发货通知 ASN/订单） | Apache Camel | https://camel.apache.org/ | EDIFACT/X12 路由模式 |
| 指标与告警 (NFR-013) | Prometheus | https://prometheus.io/ | 可观测性基础组件 |
| 仪表板（月台/吞吐量 KPI） | Grafana | https://grafana.com/ | 参考工具 |

## 4. 已声明的假设（无法追溯到来源）

方案包政策或工程预算——**并非事实**。每一项都在使用位置以
`> ⚠️ ASSUMPTION:` 标记，并列入 README 的“开放问题”中。

- **规模区间及所有 NFR 数值** — 扫描 `p95 ≤ 800 ms`，分配 `p95 ≤ 30 s` 中 `≤ 10k lines`，
  `≥ 50k SKU` / `≥ 2M` 库存行 / `≥ 500M` 事件，`≥ 60`/`≥ 120` tx/s，
  `≥ 99.9%` 可用性，`RPO ≤ 5 min` / `RTO ≤ 30 min`，`13 mo` 热窗口。均为工程预算；
  无基准测试或参考硬件。
  (→ `02-requirements/non-functional.md` 中的 `(A)` 标记)
- **BR-01 分桶构成** — `on_hand = available + reserved + hold + qc_pending + in_transit_intra`。这是方案包的建模选择；没有标准定义这些桶。
  (→ `01-business/business-rules.md`)
- **BR-03 上架排序** — 固定库位 → 最近浮动库位 → 空库位 → 溢出位，并以搬运距离打破平局。启发式规则；无算法来源。
- **BR-05 预留生命周期** — 计划时为软预留，释放时为硬预留；到期/取消时释放。TTL 和“每个装卸/物流单元仅一个硬预留”是方案包规则。
- **BR-06 批次流向** — 默认采用先进先出（FIFO），食品/药品采用先到期先出（FEFO），并设置到期阻断窗口。默认值和窗口均为方案包参数；先到期先出（FEFO）本身仅由良好分销规范 (GDP)/食品规则要求（变体）。
- **BR-07 / BR-10 / BR-11 容差** — 最大拆分次数、`tol%` 差异和交付容差、绝对上限。没有来源为这些参数提供默认值。
- **BR-09 / BR-15 / BR-16** — ABC 分类的循环盘点频率 `nA/nB/nC`，以及 `accuracy`、`pick_accuracy` 公式。在方案包内定义；并非依据所引标准推导。
- **BR-12 发运完整性闸门** — 要素清单（批次/序列号、增值服务、重量、标签/装车/发运清单）。方案包政策。
- **SM-1..SM-6 状态转换** — 例如 `DiscrepancyHold → Received`、
  `ExpiredBlocked → Quarantined`、设备拒绝时的 `WaitingEquipment → Released`。
  方案包设计；GS1/ISO 未作要求。
  (→ `03-domain/state-machines.md`)
- **06-contracts 字段细节** — API 路径、`Idempotency-Key` 的组成
  `task+step+HU+ts-window`、货主认领规则、`409` 行为。方案包专用。
  (→ `06-contracts/api-overview.md`)
- **按故障划分的 RTO/RPO 与灾难恢复 (DR) 目标** — F-01 `15 min`、F-13 区域 `4 h`、
  F-03 投影重建 `≤ 30 min`、F-08 DLQ 策略。方案包提案。
  (→ `08-quality/failure-and-dr.md`)
- **05-data/data-flow `DF-1..DF-6`** — 血缘步骤和投影重建流程。方案包设计。
  (→ `05-data/data-flow.md`)
- **EPCIS 交换深度** — 对外生成 EPCIS XML/JSON-LD 是一种 L3 选项，尚未具体规定；方案包将 EPCIS 用作概念词汇。
- **GS1 标签/打印机符合性 (NFR-014)** — “GS1 尺寸/打印分辨率”未指向任何具体的标签规范条款；需确认，或改述为方案包规则。
- **海关/保税仓储 (CN)** — 仅作概念性引用；核心内容中无引用（变体关注事项）。
- **ADR-0001..0004** — 四项均为方案包的架构立场；没有标准对这些立场作出规定。
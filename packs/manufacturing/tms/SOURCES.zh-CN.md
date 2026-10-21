# SOURCES — 运输管理系统

> 来源台账。把本方案包中承重的论断映射到公开、可核查的来源；无法追溯的内容
> 列在第 4 节，并在各章中标注 `> ⚠️ ASSUMPTION:`。
>
> **状态：`source-checked`**（2026-10-09）。来源性质：`llm-drafted`。
> 验证状态：`source-checked` — **未**经现场验证。见
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md)。
>
> 来源核对于 2026-10-09。结果：(a) 危险品版本锁定到实际在生效的版本
> （ADR 2025、IMDG 2024/A42-24 自 2026-01-01 强制适用、IATA DGR 第 67 版
> 2026、JT/T 617-2018 + GB 6944-2025）；(b) EPCIS 锁定到 2.0/CBV 2.0
> （2022-06 批准；注意 ISO/IEC 19987/19988 对 EPCIS/CBV 1.2 的 PAS 已被
> **撤回**）；(c) ISO 28000 锁定到 2022 年第 2 版；(d) Incoterms 锁定到 2020
> 版（11 条规则）。所有数值目标仍是已声明的假设（第 4 节）。

## 1. 标准与规范

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| 运输事件词汇（里程碑、处置）— FR-011、FR-021、CTL-04 | GS1 | **EPCIS 2.0 / CBV 2.0**，2022-06 批准 — https://ref.gs1.org/standards/epcis/ 与 https://ref.gs1.org/standards/cbv/ ；实施指南 2.0（2023-03） | 2.0 新增 JSON/JSON-LD、REST 捕获/查询、GS1 Digital Link。ISO/IEC 19987/19988:2017（EPCIS/CBV 1.2 PAS）已被**撤回**——请引用 GS1 2.0 规范，而非 ISO PAS |
| 供应链安全框架 — CTL-03 | ISO | **ISO 28000:2022**（第 2 版，2022-03），《安全与韧性 — 安全管理体系 — 要求》— https://www.iso.org/standard/79612.html | 替代 ISO 28000:2007；存在 Amd 1:2024（气候）。条款级映射见第 4 节 |
| 订单上消费的贸易术语 — BR-12、CTL-08、FR-001 | ICC | **Incoterms® 2020**，11 条规则，2020-01-01 生效 — https://iccwbo.org/business-solutions/incoterms-rules/incoterms-2020/ | DPU 在 2020 年由 DAT 更名；FCA A6/B6 舱面提单条款；成本在 A9/B9 归集。本方案包消费该术语，不解释它 |
| 危险品公路（国际）— BR-07、CTL-01/02 | UNECE | **ADR 2025**（修正案自 2025-01-01 起适用），UN 文号 ECE/TRANS/352 — https://unece.org/transport/dangerous-goods ；两年一循环 | 仅作校验数据（ADR-0003）。下一版 ADR 2027 |
| 危险品公路（中国）— CTL-01 | 中国交通运输部 | **JT/T 617-2018**《危险货物道路运输规则》第 1–7 部分（2018-08-29 发布，2018-12-01 实施）；**GB 6944-2025** 危险货物分类和品名编号（2025-03-28 发布，2025-10-01 实施，替代 GB 6944-2012）— https://openstd.samr.gov.cn/ | 第 3 部分存在 JT/T 617.3 XG1—2024 修改单 |
| 危险品海运 — CTL-01 | IMO | **IMDG Code 2024 版**（含修正案 42-24，2024-05 通过 MSC.556(108)），**自 2026-01-01 起强制适用**，自 2025-01-01 起自愿适用 — https://www.imo.org/en/publications/pages/imdg%20code.aspx | 已发布 2025–2034 修正案周期 |
| 危险品空运 — CTL-01 | IATA | **IATA DGR 第 67 版（2026）**，2026-01-01 生效 — https://www.iata.org/en/programs/cargo/dgr/ | 每年一版；第 68 版（2027）已发布。纳入 ICAO TI 2025–2026 |
| 危险品分类词汇（类别/项别、包装类别、UN 编号、PSN）— FR-017、术语表 | UN | UN《关于危险货物运输建议书 — 示范规章》（按 ADR 2025 的定义为 ST/SG/AC.10/3/Rev.23）；同一套定义下的 GHS Rev. 10 | 作为 ADR/JT/T 617/IMDG/IATA 共享的分类骨架被引用 |
| 货运 B2B 报文 — FR-022、集成 | UNECE | **UN/EDIFACT** 贸易便利化报文：IFTMIN/IFTMBF（指令）、IFTSTA/IFCSUM（状态）— https://unece.org/trade/uncefact | 报文名称稳定；版本按交易伙伴协议（第 4 节） |
| 北美承运商状态报文 — FR-022 | ANSI ASC X12 | **X12 214**（运输状态）、**X12 990**（对 214 的响应）— https://www.x12.org/ | 交易集名称固定；版本/实施指南按伙伴（第 4 节） |
| 位置跟踪中的个人数据 — CTL-06 | 欧盟 | **GDPR**（欧盟 2016/679）— https://gdpr-info.eu/ | 引用其原则；条款级映射见第 4 节 |
| 中国部署基线 — CTL-07 | SAC（中国） | **GB/T 22239-2019** 信息安全技术 网络安全等级保护基本要求（等保2.0） | 仅到标准级别；无条款映射 |

## 2. 规范性文件（RFC / 官方规范）

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| 时钟同步 — BR-11、NFR-011 | IETF | RFC 5905（NTPv4）— https://www.rfc-editor.org/rfc/rfc5905 | `偏差 ≤ 1 秒` 的界限是方案包策略（第 4 节） |
| EPCIS 绑定 | GS1 | EPCIS 2.0 制品（XML、JSON-LD、CBV 本体）— https://ref.gs1.org/standards/epcis/artefacts | 2.0 规范命名空间：`https://ref.gs1.org/epcis/` |

## 3. 可引用的开源实现

| 系统 / 主题 | 项目 | 链接 | 说明 |
|---|---|---|---|
| VRP / 停靠排序求解器（ADR-0002） | VROOM | https://vroom-project.org/ | 契约背后一个可行的求解器；非强制 |
| 道路路径引擎 | OSRM | https://project-osrm.org/ | 路径规划的距离/时间矩阵来源 |
| 路径与优化 | GraphHopper | https://www.graphhopper.com/ | 替代引擎；支持基于 JSprit 的优化 |
| 路径 API | openrouteservice | https://openrouteservice.org/ | 托管/自托管的替代方案 |
| 里程碑主干的事件流 | Apache Kafka | https://kafka.apache.org/ | 仅追加底座的选项（ADR-0005） |
| EDI / 报文路由模式 | Apache Camel | https://camel.apache.org/ | EDIFACT/X12 组件模式 |
| 身份 / SSO | Keycloak | https://www.keycloak.org/ | OIDC/SAML 参考（跨方案包：iam-platform） |
| 策略即代码的授权 | Open Policy Agent | https://www.openpolicyagent.org/ | 隔离检查的可选 PDP |
| 地理编码 / 地图数据 | OpenStreetMap | https://www.openstreetmap.org/ | 停靠点坐标的参考地理数据 |

## 4. 已声明的假设（无法追溯到来源）

方案包策略或工程预算——**不是事实**。每一条都在使用处标注
`> ⚠️ ASSUMPTION:`，并列在 README 的「待决问题」中。

- **全部 NFR 数值** —— 可视化 `≤ 60 秒 p95`、ETA `≤ 30 秒 p95`、招标
  `≤ 60 秒 p95`、匹配 `≤ 3 秒 p95` / 批次 `≤ 1 小时`、规模档位
  （`5 万`运输单/天、`200 万`事件/天、`1 千`承运商连接）、留存 `≥ 5 年`、
  可用性 `≥ 99.9 %`、时钟偏差 `≤ 1 秒`、可观测性阈值。都是工程预算；没有
  基准。
- **BR-03 自有车队自动接单** 是配置默认值，不是任何来源的规则。
- **BR-05 容差**（`≤ 3 % 或 ≤ ¥50`）—— 方案包策略；真实容差由合同推导。
- **BR-09 运力余量**（`≥ 5 %`）—— 方案包策略；法定载重因司法辖区与车辆类别
  而异。
- **费率模型的深度** —— 「参考费率卡 + 冻结快照」（ADR-0004）是一个范围决策；
  燃油基准的重算公式属于合同数据，不是方案包逻辑。
- **求解器契约**（ADR-0002）—— 问题/解接口的形态属于方案包设计；不存在可供
  追溯的求解器标准。
- **状态分解**（SM-T1..SM-T5：运输段的计划/实际两侧、招标、发票生命周期、
  异常、版本）—— 方案包设计；没有标准规定 TMS 的生命周期状态。
- **限界上下文与逻辑数据模型** —— 方案包设计；EPCIS 提供的是事件词汇，不是
  架构。
- **流程 P-01..P-06** —— 方案包设计，从简报所述范围泛化而来；不是任何来源的
  规范文本。
- **ISO 28000 / GDPR / 等保2.0 的条款级映射** —— 只到标准级别；具体的控制
  条文是第 4 节的待办项。
- **X12/EDIFACT 版本锁定** —— 报文名称（214/990/IFTMIN/IFTSTA）固定；按
  伙伴的版本/实施指南配对是部署输入。
- **全部五个 ADR** —— 都是方案包的架构立场。ADR-0001 *符合* 通行的
  WMS/TMS/ERP 实践，ADR-0003 刻意不主张法律合规（法规管辖，方案包校验数据）
  ——没有任何一个是被引用的标准所强制的。

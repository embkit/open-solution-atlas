# SOURCES — 增长分析与实验平台

> 来源台账。把承重的论断映射到公开、可核查的来源。
> **状态：起步台账——尚未达到 `source-checked`。**
> 来源性质：`llm-drafted` · 验证状态：`unverified`。见
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md)。

## 1. 标准与规范

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| 隐私制度 — 欧盟 | 欧盟 | GDPR（欧盟 2016/679）— https://gdpr-info.eu/ | 同意、数据主体权利、驻留 |
| 隐私制度 — 中国 | 全国人民代表大会 | 中华人民共和国个人信息保护法（PIPL，2021） | 条款号待确认；未引用 URL |
| 广告/消息内容规则 — 中国 | 全国人民代表大会 | 中华人民共和国广告法 | 为消息内容而引用；条款号待确认 |
| 同意信号（可选） | IAB Europe | Transparency & Consent Framework (TCF) | 仅当声称 TCF 互操作时适用；版本/URL 待确认 |
| 数据质量词汇（事件 schema） | — | 事件 schema 注册中心未引用任何标准 | 注册中心约定待在 L2 找来源 |

## 2. 规范性文件（RFC / 官方规范）

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| 事件流传输 | Apache（开源，非 RFC） | 见第 3 节 | 本方案包不强制任何 RFC 级别的传输方式 |

## 3. 可引用的开源实现

| 系统 / 主题 | 项目 | 链接 | 说明 |
|---|---|---|---|
| 产品分析与实验 | PostHog | https://posthog.com/ | 事件采集、漏斗、开关、A/B |
| 功能开关 / 实验 | GrowthBook | https://www.growthbook.io/ | 实验平台参考 |
| 功能管理 / 开关 | Unleash | https://www.getunleash.io/ | |
| 功能开关 | Flagsmith | https://flagsmith.com/ | |
| 开关/实验标准 API | OpenFeature (CNCF) | https://openfeature.dev/ | 厂商中立的开关 API |
| 事件采集 / 行为数据平台 | Snowplow | https://snowplow.io/ | 事件跟踪流水线参考 |
| 事件流 | Apache Kafka | https://kafka.apache.org/ | ODS 接入 |
| 分析数据库 / OLAP | ClickHouse | https://clickhouse.com/ | 漏斗/留存计算 |
| 分析数据库 / OLAP | Apache Druid | https://druid.apache.org/ | |
| 数据集成 / ELT | Airbyte | https://airbyte.io/ | 激活/目的地同步 |
| BI / 自助分析 | Apache Superset | https://superset.apache.org/ | 面向产品经理的报表 |

## 4. 待厘清的未引用细节

L2 已解决（方案包设计；达到 source-checked 仍需外部来源）：

- **事件 schema 治理** —— ADR-0001 确定了先声明后发出、在接入时校验、带理由的
  隔离、导出带版本。仍然悬而未决：**schema 语言与兼容性规则**（新增/改名/移除
  的语义）。
- **身份合并 / 删除** —— ADR-0002 确定了被记录、可逆、会传播的合并，以及三段式
  删除。仍然悬而未决：一次擦除之后**派生聚合是否必须重算**——尚未决定，且与
  实验有效性存在张力。
- **实验统计** —— ADR-0003 确定了分配的位置与预先声明的决策规则。仍然悬而未决：
  样本量、SRM、护栏、保留组与偷看纪律的**规范方法论**。本方案包一个都没
  引用；这是写出可核验的实验需求的前提。
- **目的地** —— ADR-0004 确定了「抽象而非所有」与「报表作为对账输入」。仍然
  悬而未决：**传输属性的语义**（CTL-04），这是本方案包在清单名称标注之外自行
  添加的。
- **分群** —— BR-12 确定了「快照而非实时视图」。仍然悬而未决：长期活动的
  **重新解析策略**。

仍然悬而未决：

- **法规映射** —— PIPL 与 GDPR 仍然是**仅为名称标注**。按本仓库的范围决策，
  不存在条款级映射（见 docs/citation-audit-2026-10.md 第 4 节）。
- **跨境目的地要求** —— 记录为方案包自行添加的名称标注（CTL-04），未针对任何
  文件核验过。

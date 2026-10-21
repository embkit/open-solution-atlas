# SOURCES — 企业 BI 与自助分析平台

> 来源台账。把承重的论断映射到公开、可核查的来源。
> **状态：起步台账——尚未达到 `source-checked`。**
> 来源性质：`llm-drafted` · 验证状态：`unverified`。见
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md)。

## 1. 标准与规范

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| 分析工程 / 建模实践（指标、语义层） | dbt Labs | "Analytics engineering" — https://www.getdbt.com/analytics-engineering | 实践指南，不是规范标准 |
| 指标与维度建模参考 | Kimball Group | 维度建模 / Kimball 技术 | 概念性引用；具体来源待确认 |
| 分析数据的 ISMS 控制 | ISO/IEC | ISO/IEC 27001 — https://www.iso.org/standard/27001 | 附录 A 映射待确认 |
| 隐私制度 — 欧盟 | 欧盟 | GDPR（欧盟 2016/679）— https://gdpr-info.eu/ | |
| 隐私制度 — 中国 | 全国人民代表大会 | 中华人民共和国个人信息保护法（PIPL，2021） | 条款号待确认；未引用 URL |
| 中国部署基线 | 中国（SAC） | GB/T 22239-2019 等保2.0 | README 中引用；映射待确认 |

## 2. 规范性文件（RFC / 官方规范）

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| BI 消费方的 SSO / 认证 | OpenID 基金会 | OpenID Connect Core 1.0 — https://openid.net/connect/ | |
| 对数据 API 的 OAuth 2.0 委托访问 | IETF | RFC 6749 — https://www.rfc-editor.org/rfc/rfc6749 | |
| 查询 / SQL 语义 | ISO/IEC | ISO/IEC 9075（SQL） | 仅当主张 SQL 保真时；当前包内未引用 |

## 3. 可引用的开源实现

| 系统 / 主题 | 项目 | 链接 | 说明 |
|---|---|---|---|
| BI / 仪表盘 / 自助分析 | Apache Superset | https://superset.apache.org/ | |
| BI / 仪表盘 | Metabase | https://www.metabase.com/ | |
| 无头 BI / 语义层 / 指标存储 | Cube | https://cube.dev/ | 指标即代码的参考（待决问题 1） |
| 转换 / 语义模型 | dbt | https://www.getdbt.com/ | |
| OLAP 查询引擎 | Apache Druid | https://druid.apache.org/ | 加速分析 |
| OLAP / 分析型数据库 | ClickHouse | https://clickhouse.com/ | |
| 联邦查询引擎 | Trino | https://trino.io/ | 对集市的查询联邦 |
| 可观测性 / 仪表盘 | Grafana | https://grafana.com/ | |
| 目录 / 治理元数据 | OpenMetadata | https://open-metadata.org/ | 新鲜度/归属指标 |
| 目录 / 治理元数据 | DataHub | https://datahubproject.io/ | |
| 行/列级安全机制 | PostgreSQL | https://www.postgresql.org/docs/current/ddl-rowsecurity.html | 作为 RLS 的一种实现被引用 |

## 4. 待厘清的未引用细节

L2 已解决（方案包设计；达到 source-checked 仍需外部来源）：

- **连接键及其强制执行** —— ADR-0001 确定了可比性 ⇔ 一个已声明的连接键，以及
  同名/不同语义的一对是缺陷。仍然悬而未决：**它在哪里被强制执行**（建模期、
  查询期，还是两者）。
- **语义层中的权限** —— ADR-0002 确定了只走层内读取、身份上下文求值以及
  身份失败关闭。仍然悬而未决：**当无法提供身份时哪些界面被排除**（定时导出、
  基于文件的数据馈送）——刻意不予列举。
- **制品版本固定** —— ADR-0003 确定了固定与发布前的影响报告。仍然悬而未决：
  **影响报告的流程**及其规模化后的成本。
- **新鲜度与认证** —— ADR-0004 确定了相对于契约的新鲜度与被计算得出的认证。
  仍然悬而未决：**当模型没有新鲜度契约时展示什么**——刻意不予规定。
- **晋升** —— ADR-0005 确定了带经评审路径的两状态划分。仍然悬而未决：**什么
  触发晋升、已认证标准是什么**——尚未书写的 L2 规则。
- **指标负责人离职** —— BR-01 要求一名具名的人；这个空缺刻意未解决。

仍然悬而未决：

- **RLS/CLS 的外部标准** —— 陈述为来自 AGENTS.md 的设计立场。本方案包
  **不**指名任何外部标准或条款。
- **法规映射** —— ISO/IEC 27001、PIPL 与 GDPR 类文件仍然是**仅为名称标注**。
  该章节刻意精简：这里没有任何一份文件改变 AGENTS.md 尚未做出的设计决策，也
  没有一项经过核验。见 docs/citation-audit-2026-10.md 第 4 节。
- **指标复用率下限** —— NFR-001 的 (A) 目标 70% 是策略；低于多少就判定这一
  层是复制粘贴，尚未决定。

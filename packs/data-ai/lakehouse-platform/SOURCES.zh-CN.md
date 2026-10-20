# SOURCES — 企业数据仓库与湖仓平台

> 来源台账。把承重的论断映射到公开、可核查的来源。
> **状态：起步台账——尚未达到 `source-checked`。**
> 来源性质：`llm-drafted` · 验证状态：`unverified`。见
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md)。

## 1. 标准与规范

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| 数据分类分级 — 中国 | 中国（SAC） | GB/T 43697 数据分类分级规则 | README 中引用的标准号；版本/条款待确认；未引用 URL |
| 数据安全法 — 中国 | 全国人民代表大会 | 中华人民共和国数据安全法（2021） | 条款号待确认；未引用 URL |
| 中国部署基线 | 中国（SAC） | GB/T 22239-2019 等保2.0 | 映射待确认 |
| 隐私 / 删除权 — 欧盟 | 欧盟 | GDPR（欧盟 2016/679）— https://gdpr-info.eu/ | |
| ISMS 控制 | ISO/IEC | ISO/IEC 27001 — https://www.iso.org/standard/27001 | 附录 A 映射待确认 |
| 数据质量词汇 | ISO | ISO 8000（数据质量） | 仅作为一个选项被引用；待确认 |
| SQL 语义（服务层） | ISO/IEC | ISO/IEC 9075（SQL） | 仅当主张 SQL 保真时 |
| 维度建模参考 | Kimball Group | 维度建模技术 | 方法参考，不是标准 |
| Data Vault 方法 | Data Vault（Linstedt） | Data Vault 2.0 | 方法参考；来源待确认 |
| 数据管理知识体系 | DAMA | DAMA-DMBOK | 参考，非规范；版本待确认 |

## 2. 规范性文件（RFC / 官方规范）

| 主题 / 论断 | 来源 | 引用 | 说明 |
|---|---|---|---|
| CDC / 变更数据捕获 | Debezium（开源） | 见第 3 节 | 没有 RFC 强制 CDC 格式 |
| 开放血缘事件 | OpenLineage（LF AI & Data） | https://openlineage.io/ | 血缘事件发出的规范 |

## 3. 可引用的开源实现

| 系统 / 主题 | 项目 | 链接 | 说明 |
|---|---|---|---|
| 表格式（湖仓） | Apache Iceberg | https://iceberg.apache.org/ | 开放表格式 |
| 表格式（湖仓） | Apache Hudi | https://hudi.apache.org/ | 面向 upsert/CDC |
| 表格式（湖仓） | Delta Lake | https://delta.io/ | |
| 批量/流处理 | Apache Spark | https://spark.apache.org/ | |
| 流处理 | Apache Flink | https://flink.apache.org/ | |
| 编排 / 调度（DAG、SLA、回填） | Apache Airflow | https://airflow.apache.org/ | |
| 转换 / 建模 | dbt | https://www.getdbt.com/ | |
| 数据质量规则与闸门 | Great Expectations | https://greatexpectations.io/ | |
| 元数据 / 目录 / 血缘 | OpenMetadata | https://open-metadata.org/ | |
| 元数据 / 目录 / 血缘 | DataHub | https://datahubproject.io/ | |
| 元数据 / 目录 | Apache Atlas | https://atlas.apache.org/ | |
| 血缘事件规范 | OpenLineage | https://openlineage.io/ | |
| CDC 捕获 | Debezium | https://debezium.io/ | 来源→数仓接入 |
| 联邦查询 / 服务 | Trino | https://trino.io/ | 集市/服务层 |
| 分析型数据库 | ClickHouse | https://clickhouse.com/ | |
| 分析型数据库（MPP） | StarRocks | https://www.starrocks.io/ | 信创/本地部署选项 |

## 4. 待厘清的未引用细节

L2 已解决（方案包设计；达到 source-checked 仍需外部来源）：

- **各层即契约** —— ADR-0001 确定了契约版本化、原始不可变，以及规范化作为
  唯一解析层。仍然悬而未决：**规范化的向前兼容性**，因为集市够不到原始去取
  规范化未暴露的东西——而其消费方所需要的预测确实很难预测。
- **幂等性与隔离** —— ADR-0002 确定了按加载幂等与由血缘导出的重处理范围。
  仍然悬而未决：为确定性而言**哪些分区键形态是可接受的**。
- **阻断 vs. 告警** —— ADR-0003 确定了两套机制与有归属的严重级别变更。仍然
  悬而未决：**当一个具名的告警负责人从不行动时会发生什么**——刻意未解决。
- **在平台处访问** —— ADR-0004 确定了按消费方类别的强制执行与没有例外界面。
  仍然悬而未决：当强制组件不可用时的**读取失败模式**——失败开放不是一个
  选项，但本方案包不规定读取路径做什么。
- **字段级血缘** —— ADR-0005 确定了带规则版本的字段级边。仍然悬而未决：
  **重处理范围计算作为可执行流程**（L3）。
- **删除** —— ADR-0006 确定了运行流水线及其目的地清单。仍然悬而未决：仅追加
  原始与派生 ML 制品的**机制**——密码学销毁、逻辑墓碑、快照过期窗口与有界的
  特征重算都是候选，而本方案包一个都不选。

仍然悬而未决：

- **留存** —— 要求一个已声明的按类别窗口；**不指名任何取值**。与重算之间的
  张力是真实且未解决的。
- **法规映射** —— 《数据安全法》、GB/T 43697-2024、PIPL 与 GDPR 仍然是
  **仅为名称标注**。按本仓库的范围决策，不存在条款级映射（见
  docs/citation-audit-2026-10.md 第 4 节）。
- **一个不存在的引用** —— 为连续性而记录在此：先前的 manifest.yaml 列出了
  iso.org/standard/56737.html，而**找不到带该编号的 ISO/IEC 标准**。它在 PR #13
  中被移除而不是被传播下去；行业材料提示预期的标准是 ISO/IEC 38505-1（数据
  治理）与 ISO/IEC 25012（数据质量模型）——**两者都未从本环境核验，因此两者
  都不被引用**。确立它们是达到 source-checked 的前提。
- **格式选择** —— Iceberg、Delta Lake 与 Hudi 被点名为被广泛采用的开放表格式，
  且**未被比较**。一个带选择标准的 `variants/` 覆盖层需要真实的标准，而不是
  一份排名。
- **DAMA-DMBOK** —— 被记录为数据管理的行业参考模型；其原始链接 404，因此
  它在没有 URL 的情况下被点名。
- **ISO 标准的可达性** —— iso.org 对自动化请求返回 HTTP 403，这既不证明其
  存在也不证明其不存在。存在性只能从*指名*该标准及其状态的来源中确认。

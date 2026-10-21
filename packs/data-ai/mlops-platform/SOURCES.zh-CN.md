# 来源 — MLOps 与模型生命周期平台

> 来源台账。将关键主张映射到公开、可核查的来源。
> **状态：初始台账——尚未达到 `source-checked` 状态。**
> 来源性质：`llm-drafted` · 验证状态：`unverified`。参见
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md)。

## 1. 标准与规范

| 主题/主张 | 来源 | 参考资料 | 注释 |
|---|---|---|---|
| AI 风险管理流程（治理、映射、测量、管理） | NIST | AI RMF 1.0 (NIST AI 100-1) — https://www.nist.gov/itl/ai-risk-management-framework | |
| AI 管理体系要求 | ISO/IEC | ISO/IEC 42001:2023 — https://www.iso.org/ | 需确认目录页 |
| AI 监管义务（欧盟） | EU | 欧盟第 2024/1689 号法规（AI 法案） — https://eur-lex.europa.eu/eli/reg/2024/1689/oj | 风险等级适用性待确认 |
| 模型文档（模型卡） | arXiv | 模型报告用模型卡（Model Cards for Model Reporting） — https://arxiv.org/abs/1810.03993 | |
| 数据集文档 | arXiv | 数据集说明书（Datasheets for Datasets） — https://arxiv.org/abs/1803.09010 | |

## 2. 规范性文档（RFC / 官方规范）

| 主题/主张 | 来源 | 参考资料 | 注释 |
|---|---|---|---|
| 模型交换格式 | ONNX | https://onnx.ai/ | 可选；特定框架的格式同样有效 |
| 血缘事件模型 | OpenLineage | https://openlineage.io/ | 开放规范；待确认在 L2 的采用情况 |

## 3. 可引用的开源实现

| 系统/主题 | 项目 | 链接 | 注释 |
|---|---|---|---|
| 实验跟踪 / 模型注册中心 | MLflow | https://mlflow.org/ | |
| 特征存储（离线/在线，时间点正确性） | Feast | https://feast.dev/ | |
| 训练流水线编排 | Kubeflow | https://www.kubeflow.org/ | |
| 模型服务 | KServe | https://kserve.github.io/website/ | |
| 数据质量 / 验证 | Great Expectations | https://greatexpectations.io/ | |
| 数据与流水线版本管理 | DVC | https://dvc.org/ | |
| 漂移检测 | Evidently | https://www.evidentlyai.com/ | |
| 血缘采集 | OpenLineage | https://openlineage.io/ | 与框架无关的血缘 |

## 4. 待解决的无引文具体事项

已在 L2 解决（属于方案包设计；仍需外部来源支持，才能达到 source-checked）：

- **双重版本管理 / 版本绑定** — ADR-0001 确定制品单元与可查询性，并
  将该三元组明确为**最小**三元组。仍待解决：**部署会锁定哪些额外组件**——
  这是方案包已列明但尚未作出的版本化决策。
- **注册中心准入门禁与审批** — ADR-0002 确定单一准入门禁、具名主体审批
  以及将回滚作为选择操作。仍待解决：**审批证据清单**——BR-02 要求进行
  分片评估，但尚未列举证据类型集合。
- **血缘** — ADR-0003 确定查询即可作答以及 NFR-009 的延迟。
  仍待解决：追踪数据的**采样策略**——尚未作规定，且与隐私要求存在张力
  （security.md §3）。
- **分片评估** — ADR-0004 确定在审批时呈现已声明的谓词。
  仍待解决：**声明哪些分片**——这属于方案包设计范畴；按受保护属性
  进行分片会引发方案包未回答的问题。
- **时间点特征** — ADR-0005 确定时点语义以及回放结果等于训练结果。
  仍待解决：**如何对非时间点对象建模**——方案包指出它们必须属于另一类
  对象，但未给出定义。
- **漂移** — BR-07/BR-08 确定采用线上流量和四类漂移分类。
  仍待解决：每一类漂移的**统计方法**——有意不作规定。
- **保留期** — BR-11 确定版本绑定在可提供服务期间予以保留；**窗口**与
  对训练数据的删除操作之间存在张力，且有意保留为未决事项。

仍待解决：

- **治理框架** — 根据 AGENTS.md，NIST AI RMF 和 ISO/IEC 42001 被作为治理
  **框架（采用为形状）与词汇**采用。未核验任何条款，不主张符合相关标准，
  也未复现欧盟 AI 法案的风险等级分类体系。确立这些内容是达到 source-checked
  的前提条件。
- **监管映射** — 根据本仓库的范围界定决策，欧盟 AI 法案、GDPR 和 PIPL
  仍仅作为名称列出（见 docs/citation-audit-2026-10.md §4）。
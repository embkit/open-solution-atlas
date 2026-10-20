# 方案包索引

> 英文版本：[`README.md`](./README.md)

> ⚠️ **信任状态——使用任何方案包之前请先阅读。**
> 这里的每个方案包都是 **`provenance: llm-drafted`**，而且**没有一个**在真实
> 部署中被验证过。验证等级**并不统一**：`iam-platform`、`itsm-helpdesk`、
> `personal-blog`、`wms`、`mes` 与 `tms` 为 `source-checked`（它们的承重论断在
> 各自方案的 `SOURCES.md` 中追溯到公开来源）；其余方案包目前都是 `unverified`。
> 下表的成熟度一列只衡量**完整度**——它不是背书。在信任某一条具体论断之前，请
> 务必先阅读方案包的 `manifest.yaml` 与 `SOURCES.md`。这里有两条互相正交的坐标轴
> （见 [`../docs/pack-standard.v1.md` §8](../docs/pack-standard.v1.md)）：
>
> - **成熟度**——方案包的完整程度：🟣 规划中 · 🟡 L1 简报 · 🔵 L2 蓝图 ·
>   🟢 L3 智能体就绪 · ⚫ L4 已在实践中验证
> - **验证**——外部证据的强度：⛔ `unverified` · 📑 `source-checked` ·
>   👤 `practitioner-reviewed` · ✅ `field-proven`

全部方案包都在这里，按 [`../docs/taxonomy.md`](../docs/taxonomy.md) 中的分类法组织。

| 方案包 | 领域 | 成熟度 | 验证 | 摘要 |
|---|---|---|---|---|
| [personal-blog](./horizontal/personal-blog/) | horizontal / content-publishing | 🟢 L3 | 📑 source-checked | 个人博客与内容发布——智能体就绪的参考方案包（静态站点、Webmention、所有权优先） |
| [iam-platform](./horizontal/iam-platform/) | horizontal / identity-access | 🟢 L3 | 📑 source-checked | 企业 IAM/SSO（身份基座）——JML 生命周期、OIDC/OAuth2/SAML2/SCIM2、RBAC+ABAC 决策点、MFA/WebAuthn、JIT 特权访问、可审计的决策 |
| [workflow-bpm](./horizontal/workflow-bpm/) | horizontal / collaboration | 🟡 L1 | ⛔ unverified | 工作流/BPM 与 OA 审批平台——BPMN 引擎、表单、会签/加签、公文/电子签章 |
| [itsm-helpdesk](./horizontal/itsm-helpdesk/) | horizontal / service-management | 🔵 L2 | 📑 source-checked | IT 服务台/ITSM——事件/问题/变更、SLA 时钟、CMDB、服务目录 |
| [omnichannel-commerce](./retail-commerce/omnichannel-commerce/) | retail-commerce / commerce-platform | 🟡 L1 | ⛔ unverified | 全渠道商务——PIM、结算、OMS、库存、促销、会员、售后 |
| [mes](./manufacturing/mes/) | manufacturing / mes-mom | 🟢 L3 | 📑 source-checked | 制造执行（ISA-95）——工单、事件溯源的执行、谱系、质量闸门、公式精确的 OEE |
| [wms](./manufacturing/wms/) | manufacturing / logistics-wms | 🟢 L3 | 📑 source-checked | 仓储管理——事件溯源的库存、原子预留/不超卖、定向上架、FIFO/FEFO 波次、循环盘点、基于任务的 WCS 边界 |
| [tms](./manufacturing/tms/) | manufacturing / logistics-wms | 🟢 L3 | 📑 source-checked | 运输管理——运输订单、承运商/运价、装载计划、招标/调度、在途跟踪、三方运费结算 |
| [telecom-bss](./telecom/telecom-bss/) | telecom / bss-oss | 🟡 L1 | ⛔ unverified | 电信 BSS/OSS——客户与产品目录、订单到激活的编排、计费/账单、催缴、工单、号码/资源库存 |
| [his-emr](./healthcare/his-emr/) | healthcare / his-emr | 🟡 L1 | ⛔ unverified | 医院信息系统与电子病历——EMPI、挂号/门诊/住院、CPOE 与 EMR、LIS/RIS 边界、药房、医保结算 |
| [mlops-platform](./data-ai/mlops-platform/) | data-ai / ml-platforms | 🟡 L1 | ⛔ unverified | MLOps 与模型生命周期——特征库、实验跟踪、模型注册、训练流水线、推理服务、漂移监控、血缘 |
| [one-stop-service](./government-public/one-stop-service/) | government-public / government-services | 🟡 L1 | ⛔ unverified | 政务一网通办——服务目录、在线申请、跨部门核验、审批、电子证照 |
| [data-exchange](./government-public/data-exchange/) | government-public / data-exchange | 🟡 L1 | ⛔ unverified | 政务数据共享交换——目录与挂接、授权/审批、交换通道（库表/文件/API）、血缘与质量、开放数据门户 |
| [power-marketing-cis](./energy-utilities/power-marketing-cis/) | energy-utilities / power-marketing | 🟡 L1 | ⛔ unverified | 电力营销/CIS——计量、受监管的账单、收费、业扩报装、95598 工单 |
| [enterprise-bi](./data-ai/enterprise-bi/) | data-ai / bi-analytics | 🟡 L1 | ⛔ unverified | 企业 BI——指标治理、语义层、看板、自助分析、RLS |
| [growth-analytics](./data-ai/growth-analytics/) | data-ai / growth-marketing | 🟡 L1 | ⛔ unverified | 增长分析与实验——事件治理、漏斗、A/B 测试、群组、CDP 触达 |
| [lakehouse-platform](./data-ai/lakehouse-platform/) | data-ai / data-platform | 🟡 L1 | ⛔ unverified | 数仓与湖仓——采集、分层建模、数据质量、目录/血缘、治理 |

## 收录政策说明

- **银行专属系统（核心银行、银行风控、银行监管报送）目前不收录**——为避免维护
  者的利益冲突。非银行的通用金融科技与保险方案包日后可以在界限清晰的分领域下
  加入。
- 下一批升级到 L2/L3 的方案包取决于贡献者的可用性；见
  [`../docs/roadmap.md`](../docs/roadmap.md)。

要提议新的方案包，请使用方案包提案模板开 issue，并阅读
[`../CONTRIBUTING.md`](../CONTRIBUTING.md)。

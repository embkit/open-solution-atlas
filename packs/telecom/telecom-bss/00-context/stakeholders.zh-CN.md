# 00-context / 利益相关方

## 1. 组织

| 组织 | 职责 | 系统关系 |
|---|---|---|
| **Commercial / product management**（商业/产品管理） | 定义产品提供物、定价、资格条件和促销 | 负责商业产品目录 |
| **BSS engineering**（业务支撑系统研发） | 构建并运营商业层 | 负责 BSS 领域 |
| **OSS / network engineering**（运营支撑系统/网络工程） | 构建并运营履约与保障 | 负责 OSS 领域及 BSS/OSS 边界契约 |
| **Network operations (NOC)**（网络运维） | 确保网络真实运行 | 位于资源订单下游 |
| **Revenue management**（收入管理） | 计费准确性、开票、冲抵 | 消费计费事件；负责对账 |
| **Finance / accounting**（财务/会计） | 应收款、收入确认、公司间业务 | 位于发票下游 |
| **Collections**（催收） | 欠费催缴、追偿、断开连接策略 | 消费应收款 |
| **Customer care / retail**（客服/零售） | 订单、保障、投诉 | 消费所有信息；面向客户的边缘层 |
| **Wholesale / interconnection**（批发/互联） | 漫游、互联结算 | 面向结算数据的使用方 |
| **Regulators & numbering authorities**（监管机构/码号管理机构） | 码号管理、携号转网、报告义务 | 是资源和报告的外部主管机构 |
| **Legal / privacy**（法务/隐私） | 用户数据保留与擦除 | 对保留与擦除拥有治理权 |
| **Security**（安全） | 访问控制、通话详单保密、欺诈防范 | 约束所有能力 |
| **Retail partners / resellers**（零售合作伙伴/经销商） | 通过渠道销售 | 商业产品目录的使用方 |

## 2. 角色（应用行为者）

| 角色（英文） | 中文 | 关键权限/任务 |
|---|---|---|
| Product / catalog manager | 产品目录管理员 | 定义商业产品提供物、价格和资格条件；发布 |
| Pricing & rating analyst | 定价分析师 | 计费规则、资费计划、调整 |
| Order orchestrator (system) | 订单编排器 | 分解订单并跨域编排 |
| Fallout / exception analyst | 异常处理员 | 诊断并重新驱动失败的分解步骤 |
| Provisioning / activation engineer | 激活工程师 | 履行资源订单，报告状态 |
| Number/code inventory administrator | 码号管理员 | 分配、预留和释放号码与编码 |
| Billing operator | 计费操作员 | 执行账期；检查并通过新事件进行更正 |
| Collections agent | 催缴员 | 欠费催缴操作、支付分摊、断开连接工作流 |
| Customer care agent | 客服代表 | 订单受理、保障、投诉处理 |
| Revenue assurance analyst | 收入保障分析师 | 对订单 ↔ 计费事件 ↔ 库存进行对账 |
| Trouble-ticket / assurance operator | 故障单处理员 | 处理面向网络的问题；将资源状态与商业侧关联 |
| Interconnect settlement analyst | 结算管理员 | 批发与漫游结算 |
| Subscriber / customer | 用户/客户 | 一切商业事项的对象 |
| Platform administrator | 平台管理员 | 运行各平台；对目录或定价**无权** |
| Privacy operator | 隐私运营 | 按数据类别执行保留与擦除 |

### 非人类行为者

| 行为者 | 说明 |
|---|---|
| **Commercial product catalog**（商业产品目录） | 商业产品提供物、价格、资格条件——商业层面的事实 |
| **Technical/resource catalog**（技术与资源目录） | 逻辑/物理资源、拓扑、激活路径 |
| **Specification**（规格说明，即连接对象） | 将商业产品提供物映射到其资源实现及验证状态 |
| **Order orchestrator**（订单编排器） | 分解 CO → SO → RO，管理部分失败 |
| **Rating engine**（计费引擎） | 生成计费事件——一经生成即不可变 |
| **Billing/invoicing engine**（计费/开票引擎） | 账期、汇总、调整、冲抵 |
| **Receivables & dunning engine**（应收款与欠费催缴引擎） | 账龄、支付分摊、追偿、断开连接 |
| **Number/code inventory service**（码号资源库存服务） | 对有限且受监管的资源进行分配和释放 |
| **CRM / trouble-ticket system**（CRM/故障单系统） | 客服与保障，并关联回服务实例 |
| **Fault management / assurance system**（故障管理/保障系统） | 向 OSS 和计费提供资源状态信号 |
| **Interconnect settlement system**（互联结算系统） | 批发与漫游结算 |
| **Revenue assurance / reconciliation engine**（收入保障/对账引擎） | 订单 ↔ 计费事件 ↔ 库存的双向对账 |
| **Event bus**（事件总线） | 唯一经批准的跨域耦合界面 |

## 3. 作为行为者的外部/上游—下游系统

- **网络元素/控制器**——实际的服务实现。
- **ITU-T 与码号管理机构接口**——携号转网、号段。
- **面向用户的渠道**——零售、数字、合作伙伴。
- **财务与会计系统**——负责下游开票。
- **税务机关**——发票、税务、统计报告。
- **合作伙伴/经销商系统**——渠道集成。
- **欺诈管理平台**——通话详单和订单级欺诈信号。
- **数据平台/数据仓库**——大规模通话详单分析，位于本套系统下游。
- **身份/用户身份模块**——身份验证和授权。

## 4. 行为者目标（首要）

- **产品经理**：每次价格变更，无需网络工程项目
  即可发布产品提供物
- **订单编排器操作员**：准确了解链路在何处中断，并
  在不重复计费的情况下重新驱动
- **收入保障**：检测无主使用，以及无费激活
- **催收**：完成追偿，既不误断用户，也不引发
  数量超过追偿数量的争议
- **客服**：在网络半故障时，以商业术语告知
  客户其实际拥有的内容
- **业务/财务**：依据事件重算历史发票
- **面向监管机构**：从系统记录而非旁路电子表格
  生成所需报告
- **OSS**：接受与商业侧含义一致的资源订单

> ⚠️ ASSUMPTION: 本方案包假定**事件总线是唯一经批准的
> 跨域耦合界面**。域与域之间的直接调用可以存在，但
> 每次调用都必须声明为契约——这是与采用 ODA 一致的设计立场，
> 不构成引用。
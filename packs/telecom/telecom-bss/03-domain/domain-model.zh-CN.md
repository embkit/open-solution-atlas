# 03 · 领域模型

> ⚠️ ASSUMPTION — 有界上下文、聚合和不变量属于方案包设计。
> 此分解未引用任何外部标准。

## 有界上下文

| 上下文 | 职责 | 所拥有 |
|---|---|---|
| **Party**（参与方） | 谁是商业交易对手 | Customer, Party, Agreement, CustomerClass |
| **Commercial catalog**（商业产品目录） | 商业事实：销售什么、以什么价格、向谁销售 | ProductOffering, PricePlan, EligibilityRule |
| **Specification**（规格说明） | 产品提供物在**资源层面**意味着什么 | Specification, ResourceRequirement, VerificationRule |
| **Technical catalog**（技术与资源目录） | 必须实际存在什么 | LogicalResource, PhysicalResource, ActivationPath |
| **Numbering**（编号） | 有限且受外部监管的资源 | NumberRange, NumberAllocation, PortabilityCase |
| **Ordering**（订单） | 承诺链 CO → SO → RO | CustomerOrder, ServiceOrder, ResourceOrder, OrderEvent |
| **Rating**（计费） | 按生效日期进行且受治理的计算 | TariffRuleSet, TariffRuleVersion, ChargeEvent |
| **Billing**（账单） | 发票、调整/冲抵、应收款项 | Invoice, BillCycle, Adjustment, Receivable |
| **Care**（客服） | 与服务实例关联的 95598 案例 | Case, TroubleTicket, WorkOrder |
| **Reconciliation**（对账） | 双向营收完整性 | ReconciliationRun, LeakFinding |

计费是承载受监管算术属性的上下文。它之所以与账单分离，是因为计费代码中的资费变更与发布版本中的缺陷修复无法区分 (BR-08)。

## 核心聚合与不变量

### Specification（聚合根）
```
Specification: id, productOfferingRef, resourceRequirements[], verificationRules
└── invariants
    • 产品提供物未附加规格说明时不得发布 (FR-002)
    • 它是一等对象，而不是代码中的映射表 (BR-03)
    • 对其进行解析会得到一个或多个资源实现 (FR-004)
    • 它是两个目录之间唯一允许的联接 (BR-03)
      — 其他任何组件都不得推断该关系
```

### ProductOffering（聚合根，商业产品目录）
```
ProductOffering: id, status, pricePlanRefs[], eligibilityRules[],
  specificationRef, customerClasses[]
└── invariants
    • 价格和资格条件来自此处，绝不来自技术侧 (BR-05)
    • 对它们进行更改时，无需变更技术目录 (FR-003)
```

### LogicalResource / PhysicalResource（技术目录）
```
LogicalResource: id, type, capacityModel
PhysicalResource: id, type, elementRef, state
ActivationPath: id, from, to, preconditions[], failureModes[]
└── invariants
    • 绝不复制到商业产品目录中 (BR-03)
    • 纯资源产品（批发、互联、M2M SIM）没有商业表示，也不得为其创建虚假的
      表示 (BR-03)
```

### CustomerOrder / ServiceOrder / ResourceOrder（订单）
```
CustomerOrder: id, partyRef, offeringRef, state
ServiceOrder:  id, customerOrderRef, serviceInstances[], state
ResourceOrder: id, serviceOrderRef, resources[], activationState
OrderEvent:    id, kind, ts, actor, payloadRef      # 仅追加
└── invariants
    • 链接在两个方向上均存在：RO→SO→CO 和 CO→SO→RO (BR-04, FR-005)
    • 部分完成的 RO 集合是一种有效状态；其余部分必须明确取消，绝不能通过反转
      已完成步骤来取消 (BR-07, FR-007)
    • 每次状态变更都会追加一个 OrderEvent；任何内容都不会被重写
    • 商业决策绝不查询网络状态 (BR-01)
```

### TariffRuleVersion（聚合根，计费）
```
TariffRuleSet: id, purpose, versions[], activeVersion
TariffRuleVersion: id, effectiveFrom, effectiveTo?, effectiveDate,
  publishedBy, publishedTs, status (draft|published|superseded|retired)
ChargeEvent: id, kind, amount, currency, ts,
  tarRuleVersionRef, orderRef, inventoryRef   # 不可变
└── invariants
    • 按生效日期适用：横跨 effectiveFrom 的账期应按评估结果拆分，绝不依据操作员
      决定拆分 (BR-08, FR-009)
    • 已生成的 ChargeEvent 不得更新或删除 (BR-09, FR-010)
      — 更正应创建新事件 (BR-10)
    • 规则变更绝不得重述已生成的事件，也绝不让旧事件变得无法解释
      (BR-08)
    • 该引擎与账单代码分开治理 (BR-08)
```

### Invoice（账单）
```
Invoice: id, accountRef, cycleRef, lines[], ruleVersionsUsed[], total
BillCycle: id, periodFrom, periodTo, closedTs
Adjustment: id, invoiceRef, amount, reason, approvedBy, approvedTs
Receivable: id, invoiceRef, dueTs, state
└── invariants
    • 可重算：f(计费事件、各事件所用的规则版本、调整/冲抵
      事件)——结果确定 (BR-11, FR-014)
    • 调整/冲抵是一项经批准的行为；原发票仍然保留 (BR-10)
```

### Case / TroubleTicket（客服）
```
Case: id, partyRef, accountRef, meterRef, context{snapshot}, state
TroubleTicket: id, serviceInstanceRef, issue, workOrderRef
└── invariants
    • 受理时在一个视图中呈现账户、表计、读数历史、付款情况以及影响该账户的
      故障——无需转接 (BR-06, FR-018)
    • 派发通过接口进行，绝不进入控制界面 (BR-02)
```

## 关系（逻辑）

```mermaid
erDiagram
    CUSTOMER ||--o{ ACCOUNT : 拥有
    ACCOUNT ||--o{ SERVICE_POINT : 提供
    PRODUCT_OFFERING ||--o| SPECIFICATION : 由规格说明实现
    SPECIFICATION ||--o{ RESOURCE_REQUIREMENT : 要求
    LOGICAL_RESOURCE ||--o{ PHYSICAL_RESOURCE : 由物理资源实例化
    SPECIFICATION ||--o{ ACTIVATION_PATH : 使用
    CUSTOMER_ORDER ||--o{ SERVICE_ORDER : 分解为
    SERVICE_ORDER ||--o{ RESOURCE_ORDER : 分解为
    RESOURCE_ORDER }o--|| PHYSICAL_RESOURCE : 激活
    TARIFF_RULE_SET ||--o{ TARIFF_RULE_VERSION : 包含版本
    CHARGE_EVENT }o--|| TARIFF_RULE_VERSION : 据此计算
    CHARGE_EVENT }o--|| RESOURCE_ORDER : 归属于
    CHARGE_EVENT }o--o| PHYSICAL_RESOURCE : 使用
    BILL_CYCLE ||--o{ INVOICE : 生成
    INVOICE ||--o{ CHARGE_EVENT : 汇总
    INVOICE ||--o{ ADJUSTMENT : 经调整/冲抵更正
    INVOICE ||--o| RECEIVABLE : 随账龄形成
    CASE ||--o| TROUBLE_TICKET : 解决为
    TROUBLE_TICKET ||--o| WORK_ORDER : 经工单派发
    RECONCILIATION_RUN ||--o{ LEAK_FINDING : 发现
    CHARGE_EVENT ||--o{ RECONCILIATION_RUN : 在中对账
```

## 承载本方案包核心重量的四个聚合

| 聚合 | 最重要的不变量 | 所防止的情况 |
|---|---|---|
| **Specification**（规格说明） | 两个目录之间唯一允许的联接 | 两个目录合并，从而令每次定价变更都变成网络工程变更 |
| **CustomerOrder → ServiceOrder → ResourceOrder**（客户订单 → 业务订单 → 资源订单） | **两个方向**上的链接 | 只能回答一个问题而非三个问题的链路 |
| **TariffRuleVersion**（资费规则版本） | 按生效日期适用，且计费事件存储该版本 | 规则变更悄然重述已产生金额 |
| **ChargeEvent**（计费事件） | 不可变，并进行双向对账 | 计费正确却对泄漏视而不见的系统套件 |

> 第一项和第三项最常被实现为配置，而不是不变量——而这两项正是本方案包的受监管算术属性得以成立或悄然失效之处。
# 03-domain / 状态机

关键生命周期对象的状态机。ID 为 `SM-1..SM-5`。（覆盖所有关键对象是 L3 义务；这些状态机为早期设计提供锚点。）

## SM-1 身份/账号生命周期

```mermaid
stateDiagram-v2
  [*] --> Invited: 身份已创建（HRIS/手动/自助注册）
  Invited --> Provisioned: 已在目标系统创建账号
  Provisioned --> Active: 首次认证成功
  Active --> Suspended: 因风险/合规/临时休假而暂停
  Suspended --> Active: 已解除暂停
  Active --> Mover: 组织/角色变更（P-01）
  Mover --> Active: 已应用新映射（移除失效权限项）
  Active --> Leaver: 雇佣终止/离职处理（P-02）
  Suspended --> Leaver: 暂停期间离职
  Leaver --> Disabled: 所有会话和令牌均已吊销；目标系统已禁用
  Disabled --> Purged: 保留期/擦除策略（BR-09/BR-12）
  Purged --> [*]
```

不变量：处于 `Leaver`/`Disabled` 状态的身份无法完成认证或持有有效的刷新令牌（domain-model §5.2、BR-13）。

## SM-2 认证会话

```mermaid
stateDiagram-v2
  [*] --> Unauthenticated
  Unauthenticated --> PrimaryVerified: 凭证/因子 1 验证通过（SM-2）
  PrimaryVerified --> StepUpRequired: 所需 AAL 高于当前级别（BR-11）
  StepUpRequired --> Authenticated: 更强因子验证通过
  StepUpRequired --> LockedOut: 达到失败阈值（BR-06）
  PrimaryVerified --> Authenticated: 已满足 AAL
  Authenticated --> Elevated: 高价值操作升台阶认证（新鲜度窗口）
  Elevated --> Authenticated: 操作完成/新鲜度窗口失效
  Authenticated --> Idle: 达到空闲超时阈值
  Idle --> Authenticated: 有活动/重新认证
  Authenticated --> Terminated: 注销（BR-02）
  Authenticated --> Revoked: 强制吊销/离职人员（FR-021）
  Idle --> Terminated: 达到会话绝对期限
  LockedOut --> [*]
  Terminated --> [*]
  Revoked --> [*]
```

请注意 `Authenticated`（已满足 AAL）与 `Elevated`（针对高价值操作的临时更高保障级别）之间的区别。无论是否发生活动，两者都会在会话绝对期限到达时终止（BR-02）。

## SM-3 访问请求 → 审批 → 授予

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> SodChecked: 已提交
  SodChecked --> Blocked: 职责分离冲突（BR-03）
  Blocked --> PendingApproval: 缓解措施审批人已介入
  Blocked --> Rejected: 无缓解措施
  SodChecked --> PendingApproval: 无冲突/预先批准
  PendingApproval --> Approved: 审批完成
  PendingApproval --> Rejected: 拒绝
  PendingApproval --> Expired: 审批超时
  Approved --> Granted: 已创建授予项（+供给，BR-13）
  Granted --> Revoked: 评审吊销/到期/离职人员（BR-04/BR-05）
  Granted --> Granted: （限时 → 自动到期）
  Revoked --> [*]
  Rejected --> [*]
  Expired --> [*]
```

## SM-4 特权（即时授权）提权

```mermaid
stateDiagram-v2
  [*] --> Requested
  Requested --> SodChecked: 提交时填写理由
  SodChecked --> Rejected: 职责分离冲突/拒绝
  SodChecked --> PendingApproval
  PendingApproval --> Active: 已批准；窗口开始（BR-05）
  PendingApproval --> Rejected
  Active --> Active: 窗口内的操作（已捕获会话上下文）
  Active --> Expired: 达到窗口结束时间（自动吊销）
  Active --> Revoked: 手动/SOC 吊销（FR-021）
  Requested --> BreakGlass: 应急路径（P-07）
  BreakGlass --> Active: 立即生效；需要事后评审
  Active --> UnderReview: 特权操作已记录 → 评审
  UnderReview --> Closed: 事后评审完成（≤ 24 小时）
  Expired --> [*]
  Revoked --> [*]
  Rejected --> [*]
  Closed --> [*]
```

不变量：任何路径都不会产生**长期有效**的特权授予；每个 `Active` 状态都有时间上限，且最终进入 `Expired`/`Revoked`（BR-05）。

## SM-5 联邦信任/供给连接

```mermaid
stateDiagram-v2
  [*] --> Configured
  Configured --> Testing: 已设置元数据/JWKS 或 SCIM 凭证（P-08）
  Testing --> Active: 验证同步/登录成功
  Testing --> Failed: 验证/映射错误
  Failed --> Configured: 已更正并重试
  Active --> Degraded: 证书/元数据即将到期或同步漂移
  Degraded --> Active: 已续期/完成对账
  Degraded --> Failed: 已超过有效期/持续出现错误
  Active --> Suspended: 管理暂停或安全暂停
  Suspended --> Active: 已恢复
  Active --> Decommissioned: 信任关系已吊销/应用已下线
  Failed --> Decommissioned
  Decommissioned --> [*]
```

不变量：`Active` 连接以幂等方式执行供给操作，且未经管理员明确对账，绝不会重新启用已解供给的账号（BR-13）；处于 `Failed`/`Decommissioned` 状态的信任关系无法签发或接受令牌（BR-07）。
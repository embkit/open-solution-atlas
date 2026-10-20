# 05-data / 数据字典

核心实体的字段级定义。并非完整的 DDL；用于定义
含义、类型范围和分类。分类：**OP** 运营类，
**REF** 参考类，**PII** 个人数据，**CTL** 控制/审计类，**SENS**
敏感机密材料（绝不以明文返回）。

## 身份/账号

| 字段 | 类型 | 定义/规则 | 分类 |
|---|---|---|---|
| identity_id | uuid | 不可变的主体键 | OP |
| realm_id | string | 隔离范围；每个查询/令牌都必须与之匹配（BR-07） | CTL |
| identity_type | enum | workforce / customer / partner / service | REF |
| authoritative_source | string | 主体存在性的权威记录系统（HRIS/dir/self） | REF |
| source_key | string | 关联键，在来源内唯一（FR-002） | OP/CTL |
| lifecycle_state | enum | invited/provisioned/active/suspended/mover/leaver/disabled/purged (SM-1) | OP |
| org_unit_id | string | 所属组织单元（ABAC 属性） | REF |
| attributes | map | 可扩展配置文件；每个属性均包含来源和优先级 | PII/REF |
| display_name / email | string | 供人识别的标识符 | **PII** |
| is_federated | bool | 为 true ⇒ 无本地密码（BR-15） | REF/CTL |
| account.external_id | string | 目标系统标识符（按目标系统区分） | OP |
| account.status | enum | active/disabled/pending（解供给优先级 BR-13） | OP/CTL |

## 凭证/认证器

| 字段 | 类型 | 定义/规则 | 分类 |
|---|---|---|---|
| credential.type | enum | password / totp / webauthn / recovery | REF |
| credential.aal | enum | 此因子提供的认证保障级别（BR-11） | REF |
| secret_ref | string | 对所存材料的引用（哈希值/加密种子/公钥） | **SENS** |
| password hash | — | 内存硬性加盐哈希 + 存放于 HSM/KMS 的 pepper（BR-10） | **SENS/CTL** |
| webauthn public key | bytes | 仅公钥；绝不存储私钥（WebAuthn） | OP |
| credential.state | enum | pending/active/revoked (SM-1/03.5) | OP/CTL |
| last_used_at | ts | 最近一次成功使用的时间；支持异常检测 | CTL |

## 会话/令牌/授权

| 字段 | 类型 | 定义/规则 | 分类 |
|---|---|---|---|
| session.assurance_level | enum | 认证时绑定的 AAL（BR-11） | CTL |
| session.auth_time | ts | 因子完成验证的时间；驱动新鲜度/升台阶判定 | CTL |
| session.device_ref / source_ip | string | 上下文绑定与异常信号 | CTL/PII |
| session.expires_at / absolute_expires_at | ts | 空闲超时/绝对有效期（BR-02） | OP |
| grant.scopes / audience | string[] | 委托权限 + 目标资源（FR-010） | OP/CTL |
| token.token_type | enum | access / id / refresh | OP |
| token.jti | string | 唯一令牌 ID；用于吊销/重放防护 | CTL |
| token.expires_at | ts | 短期访问令牌 TTL（BR-01） | OP |
| token.family_id | string | 刷新令牌轮换血缘；重复使用 ⇒ 吊销整个令牌族（BR-01） | CTL |
| token.state | enum | active/used/revoked/retired | OP/CTL |
| refresh.reuse_detected | bool | 提交已退役令牌时设置；触发吊销 | CTL |

## 同意

| 字段 | 类型 | 定义/规则 | 分类 |
|---|---|---|---|
| consent.purpose / scope | string | 处理目的和数据范围 | OP/**PII** |
| consent.policy_version | string | 隐私/同意声明的版本 | CTL |
| consent.state | enum | granted / withdrawn（撤回 = 新记录，BR-12） | OP/CTL |
| consent.method | enum | 同意的采集方式（self, dual-opt-in...） | CTL |
| granted_at / withdrawn_at | ts | 不可变时间戳 | CTL |

## 角色/权限/指派/策略

| 字段 | 类型 | 定义/规则 | 分类 |
|---|---|---|---|
| role.role_type | enum | business / technical / privileged | REF |
| role_permission | link | 角色 → 权限集合 | REF |
| entitlement.resource_scope | string | 权限项适用的资源/组织范围 | REF |
| assignment.source | enum | direct/request/review/elevation/mapping（来源性质，CTL-01） | CTL |
| assignment.valid_from / expires_at | ts | 限时访问；到期自动移除（BR-05） | OP/CTL |
| assignment.state | enum | active/expired/revoked | OP |
| policy.effect_default | enum | deny-overrides (BR-14) | CTL |
| policy.version / status | string/enum | 在每次决策时固定；draft/published/retired | CTL |
| policy.author_id / approver_id | string | 必须不同（职责分离，BR-08） | CTL |
| decision.effect | enum | permit / deny | CTL |
| decision.obligations | set | 例如升台阶认证、掩码、日志级别等义务，返回给 PEP | CTL |
| decision.policy_version | string | 支持决策重建（FR-022） | CTL |

## 供给

| 字段 | 类型 | 定义/规则 | 分类 |
|---|---|---|---|
| connection.target_type | enum | scim / ldap / app | REF |
| connection.credential_ref | string | 由保管库持有的凭证（绝不以明文形式提供）（NFR-012） | **SENS** |
| connection.mapping_ref | string | 属性映射（source→target） | REF |
| connection.health_state | enum | configured/testing/active/degraded/failed/suspended/decommissioned (SM-5) | OP/CTL |
| prov_operation.idempotency_key | string | 按（source,event_id,target,op）去重（BR-13） | CTL |
| prov_operation.status | enum | pending/success/failed/quarantined | OP |
| prov_operation.last_error | string | 脱敏错误（不含机密） | OP |

## 治理

| 字段 | 类型 | 定义/规则 | 分类 |
|---|---|---|---|
| access_request.justification | string | 业务理由（必填） | OP/CTL |
| access_request.risk_tier | enum | 用于确定路由和审批层级的已计算风险 | CTL |
| access_request.sod_state | enum | ok / conflict / mitigated (BR-03) | CTL |
| approval.approver_id | string | 不得为请求者本人（职责分离，BR-08） | CTL |
| elevation.window_start/window_end | ts | 有界窗口；结束时自动吊销（BR-05） | CTL |
| elevation.break_glass | bool | 应急路径 ⇒ 必须进行事后评审 | CTL |
| review_item.decision | enum | certify / revoke / undecided（逾期 ⇒ 以拒绝为安全默认值，BR-04） | CTL |

## 审计/决策（仅追加）

| 字段 | 类型 | 定义/规则 | 分类 |
|---|---|---|---|
| audit.event_id | ordered id | 不可变，每个流内单调递增 | CTL |
| audit.event_type | enum | authentication/decision/admin/lifecycle/consent 类别族（domain-model §4） | CTL |
| audit.actor_id / subject_id | string | 行为发起方/事件所涉主体 | CTL |
| audit.object_type / object_id | string | 受影响实体 | CTL |
| audit.outcome | enum | success/failure/permit/deny/error | CTL |
| audit.context | map | source_ip、device、method、risk——已净化 | CTL |
| audit.occurred_at / recorded_at | ts | 事件发生时间与记录时间（延迟到达） | CTL |
| audit.correlation_id | string | 将会话→决策→操作事件关联起来 | CTL |
| audit.prev_hash | string | 防篡改链（BR-09/NFR-009） | CTL |

## 通用约定

- 所有时间戳均为 UTC；域本地时间可推导。`occurred_at`（实际发生时间）与 `recorded_at`（存储时间）分开保留。
- 每个可变运营表都带有 `version`；审计/决策行不可变。
- 机密材料（`SENS`）仅以对 HSM/KMS/vault 的引用形式存储；绝不记录日志、在 API 响应中返回或嵌入审计记录。
- PII 按处理目的最小化（BR-12）；擦除操作对 PII 进行匿名化，同时保留审计事实和同意事实（BR-09/BR-12）。
# 06-contracts · API 概览

> ⚠️ ASSUMPTION — API 路径、字段名称、幂等键构成方式和 HTTP 状态码选择
> 均属方案包约定，并非所引标准强制规定
> （参见 [`../SOURCES.md` §4](../SOURCES.md)）。

IAM 平台的服务/API 清单。四个接口面：

1. **身份与管理 API** (`/api/v1`，需要认证，角色按域限定范围)。
2. **协议端点** (`/oauth2/*`, `/oidc/*`, `/saml/*`) — 标准定义的线协议接口（OIDC/OAuth 2.0/SAML 2.0/WebAuthn）。
3. **集成接口面** (`/partners/hris/*`, `/partners/scim/*`, `/partners/itsm/*`) — 经校验、具备幂等性、按交易对方划分身份。
4. **决策平面** (`/pdp/v1`) — 唯一进行授权决策的组件 (ADR-0001/0003)。

约定：使用 HTTPS 传输 JSON；采用 ISO-8601 UTC 时间戳；可重试的 POST 请求携带 `Idempotency-Key`；错误按 RFC 9457 `application/problem+json` 返回；每项管理变更都会追加一条不可变审计记录 (FR-022, NFR-009)；每次读/写操作均携带会话的域声明，并在服务端强制执行 (BR-07, NFR-013)。

> **承重语义 (ADR-0001)：** 身份提供方负责签发，策略决策点负责决策，策略执行点负责执行并上报——任何契约都不允许策略执行点推翻拒绝判定 (FR-017)，任何契约也不公开持续有效的特权授予 (BR-05)。

## 身份主数据与生命周期 (BC-1/2)

| 契约 | 方法/路径 | 认证方式 | 用途 | 需求 |
|---|---|---|---|---|
| C-01 | `GET/POST /api/v1/identities` · `POST /identities/{id}:transition` | 持有者令牌 · 身份管理员（域） | 生命周期状态 + 有效转换 (SM-1) | FR-001, CTL-01 |
| C-02 | `GET/POST /api/v1/identities/{id}/accounts` | 持有者令牌 · 身份管理员 | 各目标系统的账号；关联键唯一 | FR-002 |
| C-03 | `POST /partners/hris/events` | HRIS (mTLS) | 入职—调岗—离职事件，按源事件标识实现幂等 | FR-003, BR-13 |
| C-04 | `POST /api/v1/sync-jobs` · `GET /sync-jobs/{id}/report` | 持有者令牌 · 目录运维人员 | 增量 + 全量对账；报告孤儿账号/冲突，绝不静默处理 | FR-004 |

## 认证与凭证 (BC-3)

| 契约 | 方法/路径 | 认证方式 | 用途 | 需求 |
|---|---|---|---|---|
| C-05 | `POST /api/v1/credentials/password` | 会话 | 依据 BR-10 设置/更改密码（长度、泄露密码名单、不要求字符组合） | FR-005, BR-10, CTL-02 |
| C-06 | `POST /api/v1/credentials/factors` · `DELETE /credentials/factors/{id}` | 会话（升台阶认证） | 基于时间的一次性口令 (TOTP) / 通行密钥-WebAuthn / 恢复码；绑定至认证保障级别 (AAL) | FR-006, BR-11 |
| C-07 | `POST /oauth2/auth` + `POST /api/v1/authenticate` (protocol) | 公开 / 凭证 | 认证、风险评估、所需 AAL、升台阶认证质询 | FR-007, FR-008, SM-2, BR-06 |
| C-08 | `POST /oauth2/token` | 客户端认证 / PKCE | 代码→身份令牌+访问令牌；刷新令牌轮换 + 重用检测 | FR-009, FR-010, BR-01 |

## SSO 与联邦 (BC-4)

| 契约 | 方法/路径 | 认证方式 | 用途 | 需求 |
|---|---|---|---|---|
| C-09 | `GET /saml/sso` · `POST /saml/sso` (bindings) | SP 元数据信任 | SAML 2.0 身份提供方：元数据、已签名断言、属性 | FR-011 |
| C-10 | `POST /api/v1/applications` · `PUT /applications/{id}` | 持有者令牌 · 域管理员 | RP/SP 注册：标识符、端点、范围、受众 | FR-012, BR-07 |
| C-11 | `POST /api/v1/identities/{id}/links` | 会话（升台阶认证） | 按上游 ID 建立联邦链接；绝不存储上游密码 | FR-013, BR-15 |
| C-12 | `GET /oauth2/jwks` · `GET /.well-known/*` · `POST /oauth2/introspect` | 公开/客户端认证 | 带 `kid` 的密钥存在重叠；验证/令牌自省契约 | FR-014, BR-01 |
| C-13 | `POST /oauth2/logout` (front/back-channel) · `POST /saml/slo` | 会话 | 单点登出传播 + 全局吊销 | FR-021, BR-02 |

## 授权与策略 (BC-5)

| 契约 | 方法/路径 | 认证方式 | 用途 | 需求 |
|---|---|---|---|---|
| C-14 | `GET/POST /api/v1/roles` · `/permissions` | 持有者令牌 · 访问管理员 | 按应用 + 域限定范围的角色/权限目录 | FR-015 |
| C-15 | `POST /api/v1/policies` · `POST /policies/{id}/versions` | 持有者令牌 · 策略作者（≠ 审批人, BR-08） | 验证 + 对基于属性的访问控制 (ABAC) 策略进行版本管理 | FR-016, SM-3 |
| C-16 | `POST /pdp/v1/decision` | 服务 (mTLS) | 允许/拒绝 + 义务 + 决策依据；拒绝优先 | FR-016, FR-017, BR-14, NFR-004 |
| C-17 | `POST /api/v1/entitlements` | 持有者令牌 · 访问管理员 | 经职责分离检查的权限项授予；缓解措施审批路径 | FR-018, BR-03 |

## 特权访问与治理 (BC-6)

| 契约 | 方法/路径 | 认证方式 | 用途 | 需求 |
|---|---|---|---|---|
| C-18 | `POST /api/v1/access-requests` · `POST /access-requests/{id}:decide` | 持有者令牌 · 请求者/审批人 | 职责分离 → 审批 → 限时授予 | FR-019, SM-3 |
| C-19 | `POST /api/v1/elevations` · `POST /elevations/{id}:revoke` | 持有者令牌 · 特权运维（升台阶认证） | 即时授权窗口 ≤ BR-05；自动吊销；应急访问路径 | FR-020, SM-4, BR-05 |
| C-20 | `POST /api/v1/review-campaigns` · `POST /campaigns/{id}/items/{itemId}:dispose` | 持有者令牌 · 评审人员 | 评审活动生命周期；逾期 → 拒绝优先的安全吊销 (BR-04) | FR-020, BR-04 |

## 审计、多租户与同意 (BC-7/8/9)

| 契约 | 方法/路径 | 认证方式 | 用途 | 需求 |
|---|---|---|---|---|
| C-21 | `GET /api/v1/audit` · `GET /audit/export` | 持有者令牌 · 审计员（只读，域） | 查询/导出经哈希链连接的审计记录 | FR-022, NFR-009, CTL-05 |
| C-22 | `GET/POST /api/v1/realms` · `POST /realms/{id}/secrets:rotate` | 持有者令牌 · 平台管理员 | 域隔离、凭证/机密轮换 | FR-023, BR-07, NFR-013 |
| C-23 | `POST /api/v1/consents` · `POST /consents/{id}:withdraw` | 会话 / 主体 | 不可变同意元组；撤回操作随之传播 | FR-024, BR-12, CTL-07 |
| C-24 | `POST /partners/scim/v2/Users` (+`:deactivate`) · SIEM 流出口 | SCIM 持有者令牌 / 服务 | 供给目标；SOC 事件流 | 下游 FR-003/FR-021, I-5/I-7 |

## 出站事件流 (SIEM / 消费者)

通过事务性发件箱发布——至少一次投递，并按主体保持顺序 (集成 §3)。

| 事件 | 触发契约 | 载荷要点 | 需求 |
|---|---|---|---|
| `identity.lifecycle-changed` | C-01/C-03 | 主体、状态、来源性质、域 | FR-001, FR-003 |
| `authn.succeeded` / `authn.failed` | C-07 | 主体、AAL、风险、来源（不含机密信息） | FR-008, CTL-05 |
| `access.granted` / `access.revoked` | C-17/C-18/C-20 | 授予、职责分离判定结果、域 | FR-018, FR-019 |
| `elevation.activated` / `.expired` | C-19 | 授权窗口、审批人、应急访问标志 | FR-020, BR-05 |
| `consent.changed` | C-23 | 元组 + 生效路径 | FR-024 |

## 横切契约规则

1. **幂等性 (NFR-011, BR-13)：** HRIS/SCIM/ITSM 数据接入和令牌刷新操作按 `(source, event_id, target, op)` 去重；重放结果收敛，绝不重复。
2. **域范围限定 (BR-07, NFR-013)：** 每条路径均在服务端强制执行域声明；跨域令牌/查询 → 拒绝；隔离不得依赖调用方提供的筛选条件。
3. **安全拒绝 (NFR-008)：** 策略决策点不可达 → 需要许可的操作均被拒绝；通过缓存的 JWKS 验证已签发令牌，将暴露范围限制在 BR-01 的 TTL 内。
4. **传输或静态存储时不得含有机密信息 (BR-15, NFR-012)：** 任何契约都不会向上游传递密码；签名密钥/机密存放于 HSM/KMS。
5. **在 API 层执行职责分离 (BR-03, BR-08)：** 授予/提权/认证端点在服务端执行职责分离检查；UI 告警不构成控制措施。
6. **先审计后执行 (FR-022)：** 管理类变更操作会在与状态变更相同的事务中追加其审计记录。

核心子集的完整 OpenAPI 3.1 契约：
[`api/openapi.yaml`](./api/openapi.yaml)。
# 03-domain / 术语表

规范术语。以英文为主；中文为对应术语。在 ID、说明文字和契约中统一使用这些术语。

| 术语（英） | 中文 | 定义 |
|---|---|---|
| IAM | 身份与访问管理 | 负责身份、认证和授权的学科/平台 |
| SSO | 单点登录 | 一次认证可授予多个应用的访问权限 |
| IdP | 身份提供方 | 身份提供方；认证主体并签发令牌/断言 |
| SP (SAML) | 服务提供方 | SAML 服务提供方；依赖 IdP 完成认证 |
| RP (OIDC) | 依赖方 | OIDC 依赖方；消费身份令牌/访问令牌 |
| OIDC | OpenID Connect | OAuth 2.0 之上的认证层（身份令牌、UserInfo、发现） |
| OAuth 2.0 | — | 面向 API 访问的委托授权框架（RFC 6749） |
| SAML 2.0 | — | 基于 XML 的联邦/单点登录标准 |
| SCIM 2.0 | — | 用于身份供给的 REST 协议（RFC 7644） |
| PEP | 策略执行点 | 策略执行点；执行策略决策，但不制定决策 |
| PDP | 策略决策点 | 策略决策点；评估并返回允许/拒绝 |
| PIP | 策略信息点 | 策略信息点；向 PDP 提供属性 |
| PAP | 策略管理点 | 策略管理点；编写/管理策略 |
| XACML | — | 用于 ABAC 决策的策略语言/架构 |
| RBAC | 基于角色的访问控制 | 基于角色的访问控制（角色 → 权限 → 授予） |
| ABAC | 基于属性的访问控制 | 基于属性的访问控制（主体/资源/操作/上下文） |
| Claim | 声明 | 令牌/断言中关于主体的一项陈述 |
| Assertion (SAML) | 断言 | 经签名的、包含认证信息/属性的 SAML 陈述 |
| Access token | 访问令牌 | 提交给资源服务的短期凭证 |
| Refresh token | 刷新令牌 | 用于获取新访问令牌且会进行轮换的长期令牌 |
| ID token | 身份令牌 | 向 RP 声明认证事件的 OIDC 令牌 |
| JWKS | JSON Web Key Set | 发布的用于令牌验证的签名密钥（RFC 7517） |
| JWT / JWS | — | JSON Web Token / Signature——令牌格式与签名（RFC 7515/8725） |
| Session | 会话 | 在 IdP 处建立的有边界交互上下文 |
| Single logout (SLO) | 单点登出 | 将注销传播至所有参与方 RP/SP |
| Revocation | 注销/吊销 | 在到期前使令牌/会话/授权失效 |
| MFA | 多因素认证 | 使用两种或更多不同类型因子的认证 |
| TOTP | 基于时间的一次性口令 | 基于时间的一次性口令因子 |
| WebAuthn / FIDO2 | — | 用于公钥（抗钓鱼）认证器的浏览器 API/标准 |
| Passkey | 通行密钥 | 同步、可发现的 WebAuthn 凭证 |
| Authenticator | 认证器 | 主体注册的认证因子实例（密码、TOTP、密钥、通行密钥） |
| AAL | 认证保障级别 | 认证保障级别（Authenticator Assurance Level，NIST SP 800-63B-4） |
| IAL / FAL | 身份/联邦保障级别 | 身份保障级别/联邦保障级别（Identity / Federation Assurance Levels，NIST SP 800-63A-4 / 63C-4） |
| Identity proofing | 身份核验 | 在签发凭证前确定身份的 IAL |
| Step-up | 升台阶认证 | 为风险更高的操作/资源要求更强的认证因子 |
| Risk-based authentication | 风险自适应认证 | 根据评估的风险/上下文调整认证 |
| Credential | 凭证 | 主体持有的秘密/因子材料（哈希值、密钥、OTP 种子） |
| Identity (subject) | 身份/主体 | 平台管理的人员/对象 |
| Account | 账号 | 映射到身份的目标系统表示 |
| Orphan account | 孤儿账号 | 无权威所有者的账号——应予消除的风险 |
| Provisioning | 供给 | 在目标系统中创建/更新账号和权限项（SCIM） |
| Deprovisioning | 解供给 | 不再需要时禁用/移除访问权限 |
| JML | 入职-调岗-离职 | 入职—调岗—离职生命周期 |
| Entitlement | 权限项 | 可授予的资源/操作权利 |
| Role | 角色 | 命名的权限集合 |
| Permission | 权限 | 对资源执行操作的权限 |
| Assignment | 授予/指派 | 将权限项/角色与主体绑定的关系（直接/派生） |
| SoD | 职责分离 | 职责分离；防止有害的职责组合 |
| JIT | 即时授权 | 即时提权；有时限的特权访问 |
| PAM | 特权访问管理 | 特权访问管理（凭据保管、会话控制、即时授权） |
| Break-glass | 应急访问 | 绕过常规审批但会受到审计的紧急访问路径 |
| Access review / certification | 访问评审/认证 | 评审人员定期重新确认权限项 |
| Consent | 同意 | 主体针对某项处理目的所记录的许可 |
| Federation | 联邦 | 域之间为认证/属性交换建立的信任 |
| Attribute mapping | 属性映射 | 将源属性/声明转换为平台字段 |
| Realm / Tenant | 域/租户 | 身份、策略和数据的隔离边界 |
| CIAM | 客户身份管理 | 客户身份与访问管理（外部主体） |
| Workforce IAM | 员工身份管理 | 员工/承包商身份管理（内部主体） |
| Tenant isolation | 租户隔离 | 保证一个域的数据/令牌绝不跨入另一个域 |
| Client (OAuth) | 客户端 | 已注册以获取令牌并持有凭证的应用 |
| Idempotency key | 幂等键 | 使操作可安全重放的键 |
| Tamper-evident | 防篡改 | 审计属性：可检测修改（哈希链） |
| Deprovisioning SLA | 解供给时效 | 从离职事件发生到完全吊销所允许的最长时间 |
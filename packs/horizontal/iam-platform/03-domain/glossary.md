# 03-domain / Glossary

Canonical terms. English primary; 中文 equivalents. Use these uniformly in
IDs, prose and contracts.

| Term | 中文 | Definition |
|---|---|---|
| IAM | 身份与访问管理 | the discipline/platform governing identity, authentication and authorization |
| SSO | 单点登录 | one authentication grants access to many applications |
| IdP | 身份提供方 | identity provider; authenticates subjects and issues tokens/assertions |
| SP (SAML) | 服务提供方 | SAML service provider; relies on the IdP for authentication |
| RP (OIDC) | 依赖方 | OIDC relying party; consumes ID/access tokens |
| OIDC | OpenID Connect | authentication layer over OAuth 2.0 (ID token, UserInfo, discovery) |
| OAuth 2.0 | — | delegated authorization framework for API access (RFC 6749) |
| SAML 2.0 | — | XML-based federation/SSO standard |
| SCIM 2.0 | — | REST protocol for identity provisioning (RFC 7644) |
| PEP | 策略执行点 | policy enforcement point; enforces a decision, does not make it |
| PDP | 策略决策点 | policy decision point; evaluates and returns permit/deny |
| PIP | 策略信息点 | policy information point; supplies attributes to the PDP |
| PAP | 策略管理点 | policy administration point; authors/manages policies |
| XACML | — | policy language/architecture for ABAC decisions |
| RBAC | 基于角色的访问控制 | role-based access control (role → permissions → assignment) |
| ABAC | 基于属性的访问控制 | attribute-based access control (subject/resource/action/context) |
| Claim | 声明 | a statement about a subject in a token/assertion |
| Assertion (SAML) | 断言 | signed SAML statement of authentication/attributes |
| Access token | 访问令牌 | short-lived credential presented to a resource service |
| Refresh token | 刷新令牌 | longer-lived token used to obtain new access tokens; rotated |
| ID token | 身份令牌 | OIDC token asserting the authentication event to the RP |
| JWKS | JSON Web Key Set | published signing keys for token verification (RFC 7517) |
| JWT / JWS | — | JSON Web Token / Signature — token format and signing (RFC 7515/8725) |
| Session | 会话 | established, bounded interaction context at the IdP |
| Single logout (SLO) | 单点登出 | propagating logout to all participating RPs/SPs |
| Revocation | 注销/吊销 | invalidation of a token/session/grant before expiry |
| MFA | 多因素认证 | authentication using two or more distinct factor types |
| TOTP | 基于时间的一次性口令 | time-based one-time password factor |
| WebAuthn / FIDO2 | — | browser API/standard for public-key (phishing-resistant) authenticators |
| Passkey | 通行密钥 | synced, discoverable WebAuthn credential |
| Authenticator | 认证器 | a factor instance a subject enrolls (password, TOTP, key, passkey) |
| AAL | 认证保障级别 | Authenticator Assurance Level (NIST SP 800-63B-4) |
| IAL / FAL | 身份/联邦保障级别 | Identity / Federation Assurance Levels (NIST SP 800-63A-4 / 63C-4) |
| Identity proofing | 身份核验 | establishing IAL for an identity before credential issuance |
| Step-up | 升台阶认证 | requiring a stronger factor for a higher-risk action/resource |
| Risk-based authentication | 风险自适应认证 | adapting authentication to evaluated risk/context |
| Credential | 凭证 | a subject's secret/factor material (hash, key, OTP seed) |
| Identity (subject) | 身份/主体 | the person/thing the platform manages |
| Account | 账号 | a target-system representation mapped to an identity |
| Orphan account | 孤儿账号 | an account without an authoritative owner — a risk to eliminate |
| Provisioning | 供给 | creating/updating accounts & entitlements at targets (SCIM) |
| Deprovisioning | 解供给 | disabling/removing access when no longer required |
| JML | 入职-调岗-离职 | Joiner–Mover–Leaver lifecycle |
| Entitlement | 权限项 | a grantable right to a resource/action |
| Role | 角色 | a named bundle of permissions |
| Permission | 权限 | the right to perform an action on a resource |
| Assignment | 授予/指派 | binding of an entitlement/role to a subject (direct/derived) |
| SoD | 职责分离 | segregation of duties; preventing toxic combinations |
| JIT | 即时授权 | just-in-time elevation; time-boxed privileged access |
| PAM | 特权访问管理 | privileged access management (vaulting, session control, JIT) |
| Break-glass | 应急访问 | emergency access path that bypasses normal approval but is audited |
| Access review / certification | 访问评审/认证 | periodic re-attestation of entitlements by reviewers |
| Consent | 同意 | a subject's recorded permission for a processing purpose |
| Federation | 联邦 | trust between domains for authentication/attribute exchange |
| Attribute mapping | 属性映射 | translating source attributes/claims to platform fields |
| Realm / Tenant | 域/租户 | an isolation boundary for identities, policy and data |
| CIAM | 客户身份管理 | customer identity & access management (external subjects) |
| Workforce IAM | 员工身份管理 | employee/contractor identity management (internal subjects) |
| Tenant isolation | 租户隔离 | guarantee that one realm's data/tokens never cross into another |
| Client (OAuth) | 客户端 | an application registered to obtain tokens, with credentials |
| Idempotency key | 幂等键 | a key making an operation safe to replay |
| Tamper-evident | 防篡改 | audit property: modification is detectable (hash chain) |
| Deprovisioning SLA | 解供给时效 | maximum allowed time from leaver event to full revocation |

# 来源 — 企业身份与访问管理平台

> 来源台账。将本方案包的关键论断映射到公开、可核查的
> 来源；无法追溯的内容列于 §4，并在各章中标记为
> `> ⚠️ ASSUMPTION:`。
>
> **状态：`source-checked`**（2026-10-08）。来源性质：`llm-drafted`。
> 验证状态：`source-checked` — **未经**现场验证。请参阅
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md)。
>
> 已于 2026-10-08 对照来源完成核查。由此作出两项更正：NIST
> SP 800-63-3 已**撤回**（由 2025 年 7 月的 SP 800-63-4 取代），
> 并且 ISO/IEC 27002 的身份生命周期引用已更正为第 5.16 条。

## 1. 标准与规范

| 主题 / 论断 | 来源 | 参考资料 | 说明 |
|---|---|---|---|
| 主要 SSO / 身份验证层（FR-010..FR-013、BR-02） | OpenID Foundation | OpenID Connect Core 1.0 — https://openid.net/specs/openid-connect-core-1_0.html | ID 令牌、发现机制、会话模型 |
| 单点注销（BR-02、SM-2） | OpenID Foundation | OIDC Front-Channel 1.0 / Back-Channel 1.0 — https://openid.net/specs/openid-connect-backchannel-1_0.html | RP 通知语义 |
| API 委派授权（BR-01、FR-014） | IETF | RFC 6749 (OAuth 2.0) — https://www.rfc-editor.org/rfc/rfc6749 | |
| Bearer 令牌使用 | IETF | RFC 6750 — https://www.rfc-editor.org/rfc/rfc6750 | |
| 公共客户端的 PKCE | IETF | RFC 7636 — https://www.rfc-editor.org/rfc/rfc7636 | |
| 令牌撤销 | IETF | RFC 7009 — https://www.rfc-editor.org/rfc/rfc7009 | |
| 令牌自省（不透明令牌 PEP） | IETF | RFC 7662 — https://www.rfc-editor.org/rfc/rfc7662 | |
| JWT 访问令牌配置文件 | IETF | RFC 9068 — https://www.rfc-editor.org/rfc/rfc9068 | |
| JWKS / 密钥分发（BR-01） | IETF | RFC 7517 — https://www.rfc-editor.org/rfc/rfc7517 | |
| JWS 签名 | IETF | RFC 7515 — https://www.rfc-editor.org/rfc/rfc7515 | |
| JWT 最佳当前实践（令牌验证） | IETF | RFC 8725 — https://www.rfc-editor.org/rfc/rfc8725 | |
| 面向决策 / API 的错误响应 | IETF | RFC 9457 (Problem Details) — https://www.rfc-editor.org/rfc/rfc9457 | |
| 企业身份联合 / 互操作（FR-013） | OASIS | SAML 2.0 Core — https://docs.oasis-open.org/security/saml/v2.0/ | |
| 生命周期开通（FR-006/FR-007、BR-13） | IETF | SCIM 2.0 — RFC 7642 / 7643 / 7644 — https://www.rfc-editor.org/rfc/rfc7644 | 定义、核心模式、协议 |
| 抗钓鱼认证器 / 通行密钥（FR-009、BR-11） | W3C / FIDO Alliance | WebAuthn Level 2 — https://www.w3.org/TR/webauthn-2/ | CTAP2 是 FIDO Alliance 规范 |
| ABAC 策略架构 PDP/PEP/PIP/PAP（ADR-0003、BR-14） | OASIS | XACML 3.0 — https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html | 包括 deny-overrides 在内的组合算法 |
| 身份保证级别 IAL/AAL/FAL（BR-10、BR-11） | NIST | **SP 800-63-4**（2025 年 7 月）— https://csrc.nist.gov/pubs/sp/800/63/4/final | 取代 SP 800-63-3（于 2025-08-01 撤回） |
| 身份核验与登记（CTL-01） | NIST | SP 800-63A-4 — https://csrc.nist.gov/pubs/sp/800/63/a/4/final | Rev 4 的 A 卷 |
| 认证器与验证器要求（BR-06、BR-10、CTL-02） | NIST | SP 800-63B-4 — https://csrc.nist.gov/pubs/sp/800/63/b/4/final | 密码 / 认证器策略、节流、查找保密性 |
| 联合与断言（FR-013、CTL-01） | NIST | SP 800-63C-4 — https://csrc.nist.gov/pubs/sp/800/63/c/4/final | Rev 4 的 C 卷 |
| 访问控制策略与执行（CTL-03） | ISO/IEC | ISO/IEC 27001:2022 附录 A 5.15；27002:2022 5.15 中的指南 | https://www.iso.org/standard/27001 |
| 身份生命周期管理（CTL-01） | ISO/IEC | ISO/IEC 27001:2022 附录 A 5.16 / 27002:2022 5.16 | 已从此前的 8.1 引用更正 |
| 身份验证信息 / 凭据（CTL-02） | ISO/IEC | ISO/IEC 27001:2022 附录 A 5.17 / 27002:2022 5.17 | |
| 访问权限开通 / 审查 / 撤销（CTL-03、BR-04） | ISO/IEC | ISO/IEC 27001:2022 附录 A 5.18 / 27002:2022 5.18 | |
| 职责分离（BR-03、BR-08） | ISO/IEC | ISO/IEC 27001:2022 附录 A 5.3 / 27002:2022 5.3 | |
| 特权访问权限（CTL-04、BR-05） | ISO/IEC | ISO/IEC 27001:2022 附录 A 8.2 / 27002:2022 8.2 | |
| 信息访问限制（CTL-03） | ISO/IEC | ISO/IEC 27001:2022 附录 A 8.3 / 27002:2022 8.3 | |
| 安全身份验证（包括 MFA）（CTL-02） | ISO/IEC | ISO/IEC 27001:2022 附录 A 8.5 / 27002:2022 8.5 | |
| 日志记录 / 审计记录（CTL-05、NFR-009） | ISO/IEC | ISO/IEC 27001:2022 附录 A 8.15 / 27002:2022 8.15 | |
| 密码学使用 / 密钥管理（CTL-06、NFR-012） | ISO/IEC | ISO/IEC 27001:2022 附录 A 8.24 / 27002:2022 8.24 | |
| 记录保护（NFR-009） | ISO/IEC | ISO/IEC 27001:2022 附录 A 5.33 / 27002:2022 5.33 | |
| 控制项实施指南 | ISO/IEC | ISO/IEC 27002:2022 — https://www.iso.org/standard/27002 | 与 27001 附录 A 共用 93 项控制编号 |
| 隐私信息管理 | ISO/IEC | ISO/IEC 27701 — https://www.iso.org/standard/27701 | 说明性；作为 27001/27002 的隐私扩展 |
| 零信任逐请求决策（ADR-0001/0003） | NIST | SP 800-207 — https://csrc.nist.gov/pubs/sp/800/207/final | |
| 隐私 / 同意 / 数据主体权利（CTL-07、BR-12） | EU | GDPR (Regulation (EU) 2016/679) 第 6、7、15–17、30 条 — https://eur-lex.europa.eu/eli/reg/2016/679/oj | 同意记录、DSAR、删除 |
| 中国网络安全等级保护叠加层 | SAC（中国） | GB/T 22239-2019 网络安全等级保护基本要求 (MLPS 2.0) | 仅在标准层面引用；本方案包不进行条文级映射 |

## 2. 规范性 RFC / 规范索引

IAM 决策面依赖此 RFC 集；所有规范均已在 §1 中引用并说明其作用。
本节不重复任何论断，而是规范性索引。

| RFC / 规范 | 用途 |
|---|---|
| RFC 6749 / 6750 / 7636 / 7009 / 7662 / 9068 | OAuth 2.0 核心、Bearer、PKCE、撤销、自省、JWT 配置文件 |
| RFC 7515 / 7517 / 8725 | JWS、JWKS、JWT 最佳当前实践 |
| RFC 7642 / 7643 / 7644 | SCIM 2.0 定义、模式、协议 |
| RFC 9457 | HTTP API 的 Problem Details |
| OpenID Connect Core / Front-Channel / Back-Channel Logout 1.0 | SSO 和单点注销 |
| SAML 2.0 Core | 联合互操作 |
| WebAuthn Level 2 (W3C) + CTAP2 (FIDO Alliance) | 抗钓鱼认证器 |
| XACML 3.0 (OASIS) | PDP/PEP/PIP/PAP、组合算法 |
| NIST SP 800-63-4 (A/B/C-4), SP 800-207 | 保证级别、认证器、联合、零信任 |

## 3. 可引用的开源实现

| 系统 / 主题 | 项目 | 链接 | 说明 |
|---|---|---|---|
| IdP / SSO / OIDC / SAML 参考实现 | Keycloak | https://www.keycloak.org/ | 各 Realm 可自然映射到 BR-07 |
| IdP / CIAM | WSO2 Identity Server | https://wso2.com/identity-server/ | |
| IdP / SSO | Authentik | https://goauthentik.io/ | |
| OAuth2/OIDC 服务器 | Ory Hydra / Kratos | https://www.ory.sh/ | |
| 授权（ReBAC/FGA） | OpenFGA | https://openfga.dev/ | |
| 授权策略引擎（Rego） | Open Policy Agent | https://www.openpolicyagent.org/ | 可与 XACML PDP 对比 |
| 授权库（RBAC/ABAC） | Casbin | https://casbin.org/ | |
| 开通 / 同步 | Apache Syncope | https://syncope.apache.org/ | |
| 开通 / 同步 | Evolveum midPoint | https://evolveum.com/midpoint/ | |
| 企业 SSO 服务器 | Apereo CAS | https://apereo.github.io/cas/ | |
| 目录 / 身份管理 | FreeIPA | https://www.freeipa.org/ | LDAP/AD 风格集成 |
| 机密 / 密钥存储（NFR-012） | HashiCorp Vault | https://developer.hashicorp.com/vault | HSM/KMS 态势 |
| Java 中的 OAuth2/OIDC | Spring Authorization Server | https://spring.io/projects/spring-authorization-server | |
| CIAM / 联合 | Janssen (Gluo) | https://jans.io/ | CIAM 深度是延后处理的变体 |

## 4. 声明的假设（无法追溯到来源）

这些假设不包含外部证据。每项假设都会在使用处以 `> ⚠️ ASSUMPTION:`
标记，并列入 README 的“开放问题”。它们是**方案包策略或工程预算**，
而非事实，必须针对每次部署进行设定。

- **规模区间** — “≤ ~100k 个员工身份，≤ ~5M 个客户身份，≤ ~200k 个并发会话，持续峰值 ≤ ~500 RPS”。这些是容量估算假设；无基准测试依据。(→ `non-functional.md` 前言)
- **NFR-001..NFR-010 性能 / 可用性 / 容量目标** — 登录
  `p95 ≤ 500 ms`，令牌签发 `p95 ≤ 200 ms`，本地 JWKS 验证
  `p95 ≤ 5 ms`，自省 `p95 ≤ 50 ms`，`≥ 200k` 个会话，
  `≥ 500 auth/s`（突发 `≥ 1,000/s`），PDP `p95 ≤ 20 ms`/`p99 ≤ 50 ms`，
  开通 `p95 ≤ 5 s`，对账 `≤ 30 min`，可用性 `99.95%`
  （JWKS 读取路径 `99.99%`），`RPO ≤ 1 min`/`RTO ≤ 15 min`，审计数据摄取
  `≥ 2×` 且查询 `p95 ≤ 2 s`。这些是工程预算，尚未实测。(→
  `non-functional.md` 中的 `(A)` 标记)
- **BR-01 令牌生命周期** — 访问令牌 `≤ 15 min`，刷新令牌 `≤ 12 h`，ID 令牌
  `≤ access`，密钥退役时间 `≥ 2×` 轮换间隔。SP 800-63B-4
  提供真实性指导，而非这些 TTL。(→ `business-rules.md` BR-01)
- **BR-04 审查周期与升级处理** — `≥ quarterly`（特权）/ `≥ annual`（全部），逾期升级处理 `n1`/`n2` 天。ISO 27001 要求进行审查（A.5.18），但未规定审查周期。(→ BR-04)
- **BR-05 提权限时** — 窗口 `≤ 8 h`（默认 `≤ 4 h`）；紧急突破访问（break-glass）事后审查 `≤ 24 h`。(→ BR-05)
- **BR-06 账户锁定阈值** — 有意保留为带冷却期的参数 `n`；未规定为固定值。(→ BR-06)
- **BR-09 审计保留期** — 在线存储 `≥ 180 days` / 归档存储 `≥ 1 year`。取决于司法管辖区。(→ BR-09)
- **BR-10 密码最低要求** — `≥ 8`，目标为 `≥ 12`。Rev 4 保留
  “不设字符组合规则 / 不强制轮换”的立场；具体最低要求属于方案包策略。(→ BR-10)
- **BR-11 AAL→操作映射** — 将 AAL1/2/3 分别用于低风险读取 /
  业务写入 / 特权操作属于方案包设计选择；SP 800-63-4 定义了这些级别，
  但未定义此映射。(→ BR-11)
- **BR-14 deny-overrides 默认值** — XACML 3.0 允许采用多种组合算法；默认选择属于方案包决策。(→ BR-14)
- **BR-13 幂等键组成** — `source event id + target +
  operation`；RFC 7644 未作此规定。(→ BR-13)
- **NFR-012 密码学态势** — 算法套件属于部署时策略；FIPS/商用密码模块选型属于变体关注事项。(→ NFR-012)
- **ADR-0004 Realm 拆分** — “员工身份与 CIAM 作为独立信任域”
  属于方案包架构立场；没有标准对此作出规定。(→ ADR-0004)
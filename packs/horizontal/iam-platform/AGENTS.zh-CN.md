# AGENTS.md — 企业身份与访问管理平台 (L3)

L3 代理就绪方案包。按此顺序加载；遵循所有可追溯性关联。
本方案包是方案库的身份基础——不得削弱其中已定的决策。
按 `09-delivery/milestones.md` 中的 M0→M7 里程碑顺序构建，每次仅从
`09-delivery/task-map.md` 中选取一个任务 (`T-xx`)，并且**不得跳过任何验证关卡**；
任务只有在所有 ACs 通过后才算完成。

## 加载顺序

1. `manifest.yaml` — 范围、监管背景、成熟度 L3
2. `README.md` — 范围、明确的排除项（HRIS 主数据、应用特定角色设计、特权访问管理 (PAM) 产品功能、MDM/网络层执行均**不得**构建）、已定 ADR、章节映射、未决问题
3. `00-context/` — 行业简报 (industry-brief) → 利益相关方 (stakeholders) → 监管环境 (regulatory-landscape)
4. `01-business/capability-map.md` (01..10) → `processes.md` (P-01..P-08) → `business-rules.md` (BR-01..BR-15)
5. `02-requirements/` — 功能 (FR-001..FR-024) → 非功能 (NFR-001..NFR-014) → 合规 (CTL-01..CTL-07)
6. `03-domain/` — 领域模型 (domain-model, BC-1..BC-8) → 状态机 (state-machines, SM-1..SM-5) → 术语表 (glossary；统一使用这些术语；不得使用同义词)
7. `04-architecture/` — 概览 (overview) → 集成 (integration, I-1..I-12, F-01..F-06) → 安全 (security) → 可观测性 (observability)，然后是 ADR-0001..ADR-0004（**已定决策——不得重新讨论**）
8. `05-data/` — 逻辑数据模型 (logical-data-model) → 数据字典 (data-dictionary)
9. `06-contracts/` — API 概览 (api-overview, C-01..C-24) → `api/openapi.yaml`
10. `08-quality/acceptance-criteria.md` (完成定义) → `test-strategy.md`
11. `09-delivery/` — 里程碑 (milestones) → 任务映射 (task-map)

## 实施硬性规则 (L3)

- **不要推翻已定 ADR。** ADR-0001..ADR-0004 是关键支撑；静默重新讨论这些决策属于正确性缺陷，而非设计选择。
- **将认证与授权决策分离 (ADR-0001)**：身份提供方 (IdP) 负责认证并签发令牌；策略决策点 (PDP) 负责决策；资源服务 (PEPs，策略执行点) 仅验证令牌并执行决策。绝不在应用中嵌入业务授权逻辑；绝不让 PEP 推翻拒绝决定 (BR-14, FR-017)。
- **短期令牌 (BR-01/ADR-0002)**：访问令牌有效期短；刷新令牌轮换并启用重用检测；签名密钥轮换并通过 JSON Web Key Set (JWKS)/元数据发布，保留重叠有效期。仅身份平面可签发令牌。
- **每次认证和每次授权决策都必须可审计 (ADR-0003/BR-09)**：记录必须仅追加且防篡改，并包含主体/操作/资源/上下文/策略版本/结果。绝不记录机密信息、令牌、密码或 OTP 值。
- **联邦用户没有本地密码 (BR-15)**：通过上游标识符进行关联；绝不存储或代理上游密码；密码认证仅适用于本地管理的身份 (BR-10)。
- **职责分离 (SoD) 与提权时限控制在服务器端强制执行 (BR-03/BR-05)**：不允许设置常设权限；即时授权 (JIT) 提权在窗口结束时自动吊销；若不存在独立缓解措施，则拒绝任何会形成有害组合的授予。
- **域隔离是强制要求 (BR-07/ADR-0004)**：员工信任域与客户信任域彼此分离；在一个域中签发的令牌会被另一个域拒绝；管理员范围仅限于获授权的域。
- **供给必须具备幂等性，且解供给优先 (BR-13)**：操作可安全重放；离职信号绝不会被例行同步静默撤销；需要保留审计记录时，应执行禁用而非硬删除。
- **协议必须基于标准 (ADR-0002)**：OpenID Connect (OIDC)/OAuth 2.0/SAML 2.0/SCIM 2.0/WebAuthn——核心中不得使用专有令牌或供给格式。
- 司法辖区特定的密码套件、数据驻留拓扑以及客户身份管理 (CIAM)/特权访问管理 (PAM) 产品功能位于 `variants/`——不得将其固化到核心中。
- 任何环境特定事项 → `> ⚠️ ASSUMPTION:`；供应商/产品选择只能放在 `variants/` 中。

## L3 纪律（不可协商）

- ID 不可变：实现 FR/NFR/CTL/ADR/BR/SM/P/BC 各项时，必须使用相同编号。
- **每一项产出物（契约、验收标准、任务）都必须可追溯到一个或多个 FR/NFR/CTL/ADR/BR ID。** 无法追溯的产出物不算完成。
- 验证状态为 `source-checked`，而不是 field-verified——应以 [`SOURCES.md`](./SOURCES.md) 为准，而非依赖记忆；数值目标均为假设（`(A)`），应替换为实测值，绝不可作为事实呈现。

## 建议的 SDD 交接（Spec Kit / Kiro / BMAD）

- 规格定义 ← 00/01/02 章
- 规划 ← 04/05 + ADRs
- 任务 ← 09-delivery 任务映射 (T-01..T-32，按里程碑顺序)
- 验收闸门 ← 映射到 FR/NFR/CTL 的 08-quality 验收标准
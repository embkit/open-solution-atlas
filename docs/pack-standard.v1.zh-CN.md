# 解决方案包标准 v1.0

> 状态：供社区评审的草案
> **解决方案包**是 Open Solution Atlas 中的内容单元：针对某个现实软件系统的完整、
> 厂商中立蓝图，同时面向人类架构师和 AI 编码智能体编写。

## 1. 设计原则

1. **达到规范级，而非随笔级。** 方案包是工程产物，而非文章。每项论断都必须具体到足以实施或测试。不得只写“使用缓存提升性能”，而不说明缓存什么、在哪里缓存、采用什么失效规则，以及服务于哪项需求。
2. **默认厂商中立，按需面向特定技术栈。** 核心方案包不得依赖任何云厂商或产品。可选的 `variants/` 可以描述具体技术栈（例如 AWS、Spring Cloud、国产化栈）。
3. **仅收录泛化知识。** 方案包收录公开、可复用的行业知识——法规、标准、公开参考资料和泛化实践。绝不收录机密数据、客户名称或专有文档。
4. **可追溯性。** 需求映射到能力；设计决策映射到需求；验收标准反向映射到需求。编码智能体必须能够针对每个组件回答“它为何存在？”。
5. **可由智能体读取。** Markdown + YAML + 文本型图表（Mermaid、PlantUML、ArchiMate）。每个方案包都提供 `AGENTS.md` 入口，使编码智能体无需抓取 HTML 或二进制文档即可加载方案包。
6. **渐进式披露。** 从业务上下文到实施任务逐层展开，使人类先掌握全局，智能体则按需加载细节。

## 2. 成熟度等级

| 等级 | 名称 | 闸门 |
|---|---|---|
| **L1** | 简述 | 上下文、能力地图、术语表、关键法规 |
| **L2** | 蓝图 | L1 + 功能/非功能需求、领域模型、架构与 ADR、数据模型、合规控制 |
| **L3** | 智能体就绪 | L2 + API 契约、验收标准（EARS）、状态机、集成与部署规格、交付任务地图、内部一致性审查 |
| **L4** | 经证实 | L3 + 已链接的参考实现、验证报告和现实世界部署证据（可公开描述） |

等级在 `manifest.yaml` 中声明，并在评审时对照第 6 节中的清单进行核验。

> **成熟度不等于可信度。** `maturity`（成熟度）衡量方案包的*完整*程度。它不说明内容是否已经依据现实证据得到验证。这是另一个维度，由 `verification`（验证状态）和 `provenance`（来源性质）声明，并在第 8 节中定义。方案包可以是 L3 *且* unverified；它必须如实说明。

## 3. 规范方案包目录结构

```
<pack-slug>/
├── manifest.yaml              # 机器可读元数据（必需）
├── AGENTS.md                  # 智能体入口：加载什么、按何种顺序加载
├── README.md                  # 面向人员的概述、范围、范围外事项、状态
├── SOURCES.md                 # 来源台账：论断 -> 公开引用
│                              #   （当 verification >= source-checked 后为必需）
├── 00-context/
│   ├── industry-brief.md      # 行业背景、业务模式、价值链
│   ├── stakeholders.md        # 参与者、角色、组织
│   └── regulatory-landscape.md# 法律、标准、审计期望 + 来源
├── 01-business/
│   ├── capability-map.md      # 业务能力模型（分级）
│   ├── processes.md           # 核心端到端业务流程
│   ├── user-journeys.md       # 各主要参与者的用户旅程
│   └── business-rules.md      # 决策表/规则目录
├── 02-requirements/
│   ├── functional.md          # 功能需求，EARS 格式
│   ├── non-functional.md      # 含可度量目标的 NFR 目录
│   └── compliance.md          # 追溯至法规的控制要求
├── 03-domain/
│   ├── domain-model.md        # 限界上下文、聚合、实体
│   ├── state-machines.md      # 关键对象的生命周期/状态模型
│   └── glossary.md            # 标准术语
├── 04-architecture/
│   ├── overview.md            # 组件/分层/部署视图
│   ├── integration.md         # 上游/下游系统、协议、数据流
│   ├── security.md            # 信任边界、authN/authZ、关键控制
│   ├── observability.md       # 指标、日志、跟踪、告警、SLO
│   └── adr/
│       └── 0000-example.md    # 架构决策记录
├── 05-data/
│   ├── logical-data-model.md  # 实体、关系、基数
│   ├── data-dictionary.md     # 字段级定义、分类
│   └── data-flow.md           # 摄取、流转、保留期、血缘
├── 06-contracts/
│   ├── api-overview.md        # 服务/API 清单
│   └── api/                   # OpenAPI / AsyncAPI / gRPC proto 草案
├── 07-experience/
│   └── key-flows.md           # 关键界面、线框图、交互说明
├── 08-quality/
│   ├── acceptance-criteria.md # 映射到需求 ID 的验收标准
│   ├── test-strategy.md       # 测试层级、覆盖率目标、测试数据、性能计划
│   └── failure-and-dr.md      # 故障模式、RTO/RPO、备份、灾难恢复演练
├── 09-delivery/
│   ├── milestones.md          # 分阶段交付地图与依赖关系
│   ├── task-map.md            # 可由智能体执行的工作分解
│   └── sizing-notes.md        # 团队配置、工作量区间、风险登记表
├── assets/                   # 图表（mermaid/plantuml 源文件）、插图
└── variants/                 # 可选的特定技术栈覆盖层
    └── <variant-slug>/
```

按等级标记为“必需”的文件：见第 6 节。L1 方案包可以只包含 `manifest.yaml`、`README.md` 和少量其他文件；缺失的目录应列为 README 中的路线图事项，而不是默默省略。

**可选章节**（绝不作为等级闸门）：`07-experience/`、`05-data/data-flow.md`、`08-quality/failure-and-dr.md`、`09-delivery/sizing-notes.md`、`assets/`、`variants/`。鼓励在 L3 等级包含这些内容，但缺少它们不会导致任何等级被拒绝。

## 4. manifest.yaml 架构

```yaml
schema: osa-pack/v1
slug: mes                                 # kebab-case，唯一
title: Manufacturing Execution System     # 显示名称
title_zh: 制造执行系统（MES）
domain: manufacturing                     # 顶层分类体系 id
subdomain: mes-mom
tags: [isa-95, work-order, traceability, quality, oee]
maturity: L1                              # L1 | L2 | L3 | L4   （完整度）
provenance: llm-drafted                   # llm-drafted | human-authored | community | mixed
verification: unverified                  # unverified | source-checked
                                          #   | practitioner-reviewed | field-proven
stack_stance: stack-agnostic              # stack-agnostic | stack-specific
variants: []                              # 例如：[aws, spring-cloud, domestic-cn]
regulatory:                               # 方案包涉及的法规体系
  - id: isa-95
    region: global
  - id: iso-9001
    region: global
language: en                              # 方案包主要语言
translations: [zh-CN]
maintainers: []                           # GitHub 用户名
version: 0.1.0
last_reviewed: 2026-10-08
sources: []                               # 方案包级公开参考来源
verified_by: []                           # practitioner-reviewed+ 的 [{who, role, date, scope}]
evidence: []                              # [{type, ref, note}]，type:
                                          #   standard | spec | oss-implementation
                                          #   | case-study | deployment
```

## 5. 编写规则

- **各处均使用 ID**：`FR-012`、`NFR-003`、`CTL-007`、`ADR-005`、`ENT-ACCOUNT`、`API-PAYMENT-01`。交叉引用时使用 ID。
- 行为需求采用 **EARS 验收句式**：
  `WHEN <trigger> THE SYSTEM SHALL <response>`。
- **可度量的 NFR**：延迟 p99、RPO/RTO、并发用户数、数据量区间、可用性目标——绝不使用含糊形容词。
- **决策记录**：非显而易见的选型需要一份 ADR，说明背景、备选方案、决策和后果。
- **图表即代码**：Mermaid 或 PlantUML 源文件提交至 `assets/`。
- **不得杜撰确定性**：使用 `> ⚠️ ASSUMPTION:` 标记不确定点，并在 README 的开放问题中列出。智能体不得擅自填补空缺。
- **引用或加限定**：任何起关键支撑作用的论断——标准条款、监管义务、协议行为、作为事实呈现的数值目标——都必须引用公开、可核查的来源，或标记为假设。没有来源的具体表述属于缺陷，而非优点。
- **双语关键资产**：标题（manifest 中的 `title_zh`）、术语表和 README 标题应在贡献者有能力的情况下同时提供英文和中文。这些*关键资产*建议尽早提供，且**不等同于**翻译工作。
- **`translations` 意味着确有译文**：仅当方案包中存在对应产物时，才可列出区域设置（例如 `zh-CN`）——即存在 `README.<locale>.md` 或 `translations/<locale>/` 包。声明没有此类文件的区域设置属于虚假声明，`tools/validate-packs.py` 会拒绝它。完整翻译需渐进完成；在关键资产为双语时，将列表留空（`[]`）是诚实且符合预期的做法。
- **译文是同级文件，而非并行目录树**：`01-business/business-rules.md` 的中文版本是 `01-business/business-rules.zh-CN.md`，与原文件并列。因此两种语言的 URL 空间完全相同，翻译中编写的相对链接会解析到中文读者所需页面，构建流程中任何地方都无需重写链接。中文构建会在原文件 URL 处用同级译文*取代*原文件；尚未翻译的章节则呈现英文原文，并在页面上说明。
- **声明区域设置意味着整个方案包均已翻译**：`translations: [zh-CN]` 声明每个可翻译文件都有 `.zh-CN.md` 同级文件，`tools/validate-packs.py` 正是这样检查的。只翻译了一半的方案包不声明任何区域设置，因为诚实的声明是 `[]`。

## 6. 等级清单

> 这些清单仅衡量**成熟度**——方案包中已有的内容。它们不赋予可信度。通过此处 L3 检验的方案包仍可能为 `verification: unverified`；验证状态阶梯及其规则见第 8 节。不要混同这两个维度。
>
> **执行情况由机器检查。** `tools/validate-packs.py` 是这些清单以及第 8 节诚实性规则的权威实现；它会在每个 PR 的 CI 中运行。当下方清单与工具不一致时，应在同一个 PR 中同时修复二者。`schemas/pack-manifest.schema.json` 是 `manifest.yaml` 字段级的权威依据。

**L1 — 简述**（最低文件：`manifest.yaml`、`README.md`、`SOURCES.md`、`AGENTS.md`；清单项可以位于专门章节**或** `README.md` 本身——当它们仅作为章节存在时，必须通过工具检查；当完全缺失时，必须列为 README 路线图事项）
- [ ] `manifest.yaml` 通过 schema 校验
- [ ] 含来源的行业简述
- [ ] L1 能力地图
- [ ] 利益相关者列表
- [ ] 含引用的监管环境
- [ ] 已建立初始内容的术语表

**L2 — 蓝图**（包含 L1 全部内容，另加）
- [ ] 具有稳定 ID 的功能需求
- [ ] 含可度量目标的 NFR 目录
- [ ] 追溯至法规的合规控制
- [ ] 包含限界上下文的领域模型
- [ ] 架构视图（组件、部署）
- [ ] ≥3 份 ADR，涵盖关键支撑性决策
- [ ] 核心实体的逻辑数据模型 + 数据字典
- [ ] 安全与可观测性章节

**L3 — 智能体就绪**（包含 L2 全部内容，另加）
- [ ] 核心服务的 API 契约
- [ ] 关键生命周期对象的状态机
- [ ] 具有完整需求可追溯性的 EARS 验收标准
- [ ] 集成与数据流规格（协议、载荷、频率）
- [ ] 测试策略，包括性能场景和故障场景
- [ ] 交付里程碑 + 可由智能体执行的任务地图
- [ ] `AGENTS.md` 加载顺序通过端到端验证
- [ ] 一致性审查：所有 ID 均可解析、术语表术语使用一致、需求、设计和契约之间不存在矛盾

**L4 — 经证实**（包含 L3 全部内容，另加）
- [ ] 已链接公开可用的参考实现
- [ ] 验证报告：说明了哪些验收标准已验证，以及验证方式
- [ ] 无需机密信息即可描述的部署证据或有文档记录的试点

## 7. 与 SDD 工具的关系

方案包是**内容**，而不是流程。它旨在接入规格驱动开发工具：

| 工具 | 使用方案包的方式 |
|---|---|
| GitHub Spec Kit | 将 L3 章节输入 `specify` / `plan`；任务映射对应 `tasks.md` |
| BMAD-METHOD | 将上下文/领域章节用作分析师与架构师的输入 |
| Kiro | 需求和验收章节映射到 `requirements.md`/`design.md` |
| Claude Code / Codex / Cursor | 指向 `AGENTS.md`；渐进式加载章节 |

方案包标准将保持工具中立；转换指南位于 `docs/`。

## 8. 来源性质与验证状态

成熟度（第 2 节）衡量方案包的**完整程度**。它丝毫不说明方案包**有多可信**。三个相互正交的字段使可信度变得明确：

| 字段 | 所回答的问题 | 取值 |
|---|---|---|
| `maturity` | 蓝图内容已具备多少？ | L1–L4 |
| `provenance` | 内容是如何产生的？ | `llm-drafted` · `human-authored` · `community` · `mixed` |
| `verification` | 外部证据有多强？ | `unverified` · `source-checked` · `practitioner-reviewed` · `field-proven` |

### 8.1 来源性质取值

- `llm-drafted` — 主要由 LLM 在人的指导下产出，未经现场验证。可以且欢迎采用，但必须加以标注。
- `human-authored` — 由具备第一手经验的实践者撰写。
- `community` — 由多位贡献者汇编而成。
- `mixed` — 上述各项的任意组合。

### 8.2 验证状态阶梯

每一级都要求具备其下所有级别的证据。

1. **`unverified`** — 没有外部证据。应将每一项具体主张视为假设。对于由 LLM 起草的材料，这是诚实的默认值。
2. **`source-checked`** — 每一项关键性主张均可追溯到公开、可核查的来源（标准条款、RFC、正式规范，或可引用的开源实现）。不得保留任何未经引用的具体内容。需要一份 `SOURCES.md` 来源性质台账。
3. **`practitioner-reviewed`** — 一名或多名具名的领域实践者已根据方案包声明的范围对其进行审查；每名审查者均记录在 `verified_by` 中，并注明角色、日期和范围。
4. **`field-proven`** — 存在公开的参考实现和/或可描述的部署证据。这与 L4（第 6 节）的标准相同。

### 8.3 规则

1. **不得自行提升等级。** 方案包的 `verification` 绝不能声称拥有超过实际存在的证据。编写本身不是证据。
2. **`source-checked` 必须有台账。** 方案包根目录必须包含 `SOURCES.md`，将每项关键性主张映射到其引用来源。没有引用来源的主张必须降级为 `> ⚠️ ASSUMPTION:`。
3. **低于 `source-checked` 时须使用草稿横幅。** 任何 `verification` 为 `unverified` 的方案包都必须在 `README.md` 顶部显示醒目的草稿横幅，说明其来源性质和验证状态取值。
4. **作者与审查者须分离。** 撰写方案包的人不得成为 `practitioner-reviewed` 或更高级别的唯一批准者。
5. **LLM 起草的内容绝不能通过生成过程获得 `verified` 状态。** 它只能通过获取外部证据来提升等级——引用来源、实践者审查或实际实现。LLM 不得通过审查另一个 LLM 的输出使其成为已验证状态。
6. **验证具有明确的范围和日期。** `verified_by` 和 `evidence` 条目均须包含范围和日期；方案包发生实质性变更时，验证状态会衰减。
7. **衰减机制。** 如果变更会修改 `SOURCES.md` §1/§2 中列出的主张、添加/删除或重新编号 BR/FR/NFR/CTL ID、更改数值目标，或编辑 ADR 决策，则该变更属于*实质性*变更。合并实质性变更时，PR 必须选择以下一种方式：(a) 重新核查受影响的主张，更新 `last_reviewed` 并附上更新后的证据；或 (b) 将 `verification` 降一级。当 `last_reviewed` 距今超过 180 天时，工具会发出告警；过期的验证声明属于缺陷，而非形式要求。

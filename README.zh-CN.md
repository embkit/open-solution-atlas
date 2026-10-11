# Open Solution Atlas · 开放方案图谱

<p align="center">
<i>Talk is cheap. Show me the code.</i> —— Linus Torvalds, 2000<br/>
<b><i>Code is cheap. Show me the solution.</i></b><br/>
代码廉价，给我看解决方案。
</p>

<p align="center">
<b>面向真实软件系统的开放、规格级蓝图库 —— 同时为人类架构师和 AI Coding Agent 而写。</b><br/>
<a href="./README.md">English</a>
</p>

<p align="center">
<img alt="CI" src="https://github.com/embkit/open-solution-atlas/actions/workflows/ci.yml/badge.svg">
<img alt="License: CC BY-SA 4.0 + MIT" src="https://img.shields.io/badge/license-CC%20BY--SA%204.0%20%2B%20MIT-blue">
<img alt="Pack Standard" src="https://img.shields.io/badge/pack%20standard-v1.0%20draft-orange">
<img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen">
</p>

## 这个项目为什么存在

软件工程的开源知识在两端都很丰富：

- **面试与高并发教程**：设计短链、信息流、聊天系统
- **可运行的开源框架**：拿一个观点固化的完整产品去改造

但行业真正运转所依赖的中间层，在开源世界几乎是空白：**某一类业务系统的
解决方案蓝图本身**——工厂的 MES 制造执行系统、仓储管理系统、政务一网通办、
企业级 BI 与增长分析平台。这些知识如今锁在咨询交付物、厂商白皮书和架构师个人的经验
里：分散、没有统一命名、更几乎从未以"完整到可以据此把系统真正做出来"的程度
被写下来。

当 Coding Agent 接管了大量常规实现工作，交付严肃系统的关键约束上移了：从写
代码，上移到**规格与设计**。Open Solution Atlas 就是为这一转变准备的开放内容
层——一个方案库，每一个系统都被记录到足够完整，可以直接交给规格驱动开发
（Spec-Driven Development）工作流去实现。

## 一个 Solution Pack（方案包）包含什么

每个方案包描述**一个系统**，从业务上下文一直到交付任务：

```
行业背景与监管合规环境
        │
业务能力 · 业务流程 · 业务规则
        │
功能需求（EARS 句式）· 非功能需求 · 合规控制项
        │
领域模型 · 状态机 · 术语表
        │
架构与 ADR 决策记录 · 数据模型 · API 契约
        │
验收标准 · 测试策略 · 容灾设计
        │
里程碑 · 可被 AI Agent 执行的任务地图
```

所有需求、决策、契约、测试都带稳定编号、可双向追溯；每个方案包附带
`AGENTS.md` 作为 AI 代理的加载入口。完整规范见
[`docs/pack-standard.v1.md`](docs/pack-standard.v1.md)。

### 成熟度分级

| 级别 | 含义 |
|---|---|
| 🟡 **L1 简报** | 行业背景、能力地图、干系人、监管环境 |
| 🔵 **L2 蓝图** | 需求、领域模型、架构、数据模型、合规控制 |
| 🟢 **L3 Agent 就绪** | API 契约、验收标准、任务地图——可由 Coding Agent 直接实施 |
| ⚫ **L4 已验证** | 有关联的参考实现与真实验证证据 |

方案包如实声明成熟度。一份持续维护的 L1，远比一份注水的 L3 有价值。

### 信任：两个独立轴，不可混同

成熟度度量的是**完整性**，与**可信度**无关。因此每个方案包还独立声明第二个
字段 `verification`，它只能靠获取外部证据来升级（[规范 §8](docs/pack-standard.v1.md)）：

| 验证等级 | 含义 |
|---|---|
| ⛔ `unverified` | 无外部证据。所有具体断言都按假设对待；必须挂草稿横幅。 |
| 📑 `source-checked` | 每条承重断言可追溯到包内 `SOURCES.md` 记录的公开来源；无据具体值一律标 `⚠️ ASSUMPTION`。 |
| 👤 `practitioner-reviewed` | 由具名领域从业者评审——逐人记入 `verified_by`。 |
| ✅ `field-proven` | 有关联的公开参考实现或可描述的部署证据（与 L4 同一标准）。 |

所有内容在被证明之前一律 `provenance: llm-drafted`，且**目前没有任何方案包
经过真实部署验证**。这不是口头承诺，而是机器强制：每个 PR 上 CI 运行
[`tools/validate-packs.py`](tools/validate-packs.py)——横幅规则、验证阶梯
诚实性、各级别必备章节、相对链接完整性均由机器校验
（[schema](schemas/pack-manifest.schema.json)）。LLM 不得把另一个 LLM 的
方案包"评审"成已验证状态。

## 与现有项目的差异

| | 面试类仓库（system-design-primer 等） | 云厂商架构中心 | 开源核心系统（Fineract 等） | SDD 工具（Spec Kit / BMAD / Kiro） | **Open Solution Atlas** |
|---|---|---|---|---|---|
| 带合规纵深的真实行业系统 | ✗ | 部分 | 只覆盖单一领域 | ✗ | **✓** |
| 厂商中立 | ✓ | ✗ | ✓ | ✓ | **✓** |
| 完整可实施的规格（而非代码） | ✗ | ✗ | 是代码而非规格 | 只有流程没有内容 | **✓ 内容层** |
| Agent 原生封装（AGENTS.md、可追溯编号） | ✗ | ✗ | ✗ | 仅工具侧 | **✓** |
| 跨全部行业的开放社区库 | ✓ | ✗ | 单一产品 | ✗ | **✓** |

我们是 SDD 工具所缺失的**内容层**，也是咨询机构与云厂商私有方案资产的**开放
对位物**。

## 在线浏览

已生成一个带**全文搜索与筛选**的站点，可检索整个图谱（试试搜 “FEFO”、“OEE”、“联邦登录”，直接落到对应章节）：

**https://embkit.github.io/open-solution-atlas/**

本地构建：`python tools/build-site.py`（输出到 `_site/`；任何内部死链都会导致构建失败）。每次 push 到 `main` 自动发布到 GitHub Pages。

## 书架地图

完整行业分类见 [`docs/taxonomy.md`](docs/taxonomy.md)：

- **通用能力 horizontal**：统一身份 IAM、CMS/博客、工作流 BPM/OA、ITSM 服务台
- **制造 manufacturing**：MES/MOM、WMS/TMS、ERP、质量/PLM
- **零售电商 retail-commerce**：全渠道电商、平台电商、门店运营
- **政务公共 government-public**：一网通办、数据共享交换、智慧城市、税务
- **能源电力 energy-utilities**：电力营销/CIS、电网运行 IT、能源数据
- **数据与智能 data-ai**：BI、数仓/湖仓、增长分析、MLOps
- **通信 · 医疗**
- **金融 finance**：当前仅征集非银行方向（保险、通用金融科技）；银行类系统
  因维护者利益冲突回避，暂不征集

现有方案包及进度：[`packs/`](./packs/)。

## 如何使用方案包

**给人读**——像阅读一份成熟交付团队梦寐以求的方案文档：先业务上下文，再架
构与权衡。

**交给 Coding Agent**——L3 方案包可直接接入规格驱动开发工作流：

```bash
# 1. 引用或复制方案包
# 2. 让 AI 代理读取包内 AGENTS.md
# 3. 将 09-delivery 任务地图展开为 plan/tasks（Spec Kit / BMAD / Kiro 等）
# 4. 在人工评审闸门处把关；"完成"的标准由验收标准定义
```

## 参与贡献

请先读 [`CONTRIBUTING.md`](CONTRIBUTING.md)（有中文版），核心约定一句话：贡献
**通用化的公开知识**，绝不放入任何可识别雇主或客户的材料；公开法规与来源必须
引用；默认厂商中立，技术栈倾向放入明确标注的 `variants/`。

一份你深刻了解的行业系统 L1 简报，就是极好的第一个 PR。

**对某个方案包或规范本身有疑问？** 请到
[Discussions](https://github.com/embkit/open-solution-atlas/discussions)
开一个话题——提问请走那里，Issue 追踪器留给真实的缺陷与提案。如果你在某个包里
发现了错误论断、失效引用或死链，那确实是 Issue，请使用勘误模板。

## 许可证

两份许可，对应两类材料：

| 材料 | 许可 | 文件 |
|---|---|---|
| 文档与蓝图内容——Markdown、图表、目录页、方案包数据 | [CC BY-SA 4.0](./LICENSE) | `LICENSE` |
| 代码与模板——`tools/`、`tests/`、`templates/` | [MIT](./LICENSE-MIT) | `LICENSE-MIT` |

`LICENSE` 为 CC BY-SA 4.0 官方法律文本逐字全文（以便许可证扫描器正确识别仓库），
`LICENSE-MIT` 为 MIT 全文。贡献按两者共同接受，见
[`CONTRIBUTING.md`](CONTRIBUTING.md)。

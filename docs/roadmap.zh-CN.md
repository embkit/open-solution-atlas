# 路线图

## 阶段 0 — 基础建设（当前）

- [x] 项目使命、定位和许可证
- [x] 方案包标准 v1 草案
- [x] 分类体系 v1
- [x] 方案包模板 + 审查清单
- [x] 首个用于验证标准的示例方案包：
  - [x] `horizontal/personal-blog` — **L3 智能体就绪（agent-ready）**（证明 L3 端到端能力：
    18 项 FR / 15 项 NFR / 10 项控制项 / 4 项 ADR / OpenAPI 3.1 / 24 项任务）
- [x] `manufacturing/mes` — **L2 蓝图（blueprint）**（21 项 FR / 13 项 NFR / 6 项控制项 /
  4 项 ADR；在邻近 OT 的复杂领域中验证该标准）
- [x] `manufacturing/wms` — **L3 智能体就绪（agent-ready）**（28 项 FR / 14 项 NFR / 7 项控制项 /
  4 项 ADR；C-01..31 契约 + OpenAPI 3.1 / AC-001..028 与 AC-N01..14 /
  T-01..38 任务映射；事件溯源库存、预留/防超卖、WCS
  任务边界）
- [x] `horizontal/iam-platform` — **L2 蓝图（blueprint）**（24 项 FR / 14 项 NFR /
  7 项控制项 / 4 项 ADR；身份基础：OIDC/OAuth2/SAML2/SCIM2、
  RBAC+ABAC PDP、JIT 特权访问）
- [x] `manufacturing/tms` — **L1→L3**（22 项 FR / 13 项 NFR / 8 项控制项 /
  5 项 ADR / C-01..26 / AC-001..022 / T-01..32；固定使用以下危险品规则版本：
  ADR 2025、IMDG 2024 A42-24、IATA DGR 67、JT/T 617 + GB 6944-2025）
- [x] `manufacturing/mes` — 已提升至 **L2→L3**（24 项契约 / AC-001..022 /
  SM-01..05 / F-01..06 数据流 / T-01..30）
- [x] 初始跨行业 L1 方案集（12 份简报；见 packs/README.md）
  — 共 7 个领域、17 个方案包
- [x] **信任与治理层（双轴标准 §8）** — 清单模式、
  `tools/validate-packs.py` + `tools/check-links.py`、GitHub Actions CI、
  从业人员评审问题模板、验证状态衰减规则
- [x] 方案包模板已完善为完整的 L3 骨架（已通过验证器冒烟测试）
- [x] 仓库门面：根 README 信任章节（EN/zh-CN）、CHANGELOG
- [ ] 社区评审该标准；发布 v1.0

> **方案集范围说明：**目前不收集银行专用系统（避免维护者存在利益冲突）。
> 参见分类体系中的金融说明。

## 阶段 1 — 核心方案包集

目标：按分类体系形成约 12 个方案包，其中至少 3 个达到 L3。
**状态：已实现方案包集目标（17 个方案包，5× L3：personal-blog、iam-platform、
wms、mes、tms；1× L2：itsm-helpdesk）；剩余工作是深化，而非扩展数量。**

- [x] 制造业：MES、WMS、TMS（均为 L3，source-checked）
- [x] 横向领域：IAM（L3）、personal-blog（L3，source-checked）
- [x] 横向领域：ITSM 服务台 → L2 + source-checked
- [ ] 横向领域：工作流/BPM（OA）→ L2 + source-checked
- [ ] 政务：一站式政务服务平台 → L2
- [ ] 能源：电力营销/CIS → L2
- [ ] 零售：全渠道商业 → L2
- [ ] 数据与 AI：企业 BI、增长分析、数据仓库/湖仓 → L2

### 已知技术债（机器可见）

11 个 L1 方案包是仅含 4 个文件的简报，缺少 §6 L1 检查清单章节
（`00-context/*`、能力映射、术语表）——`tools/validate-packs.py`
会为它们发出 55 条告警；各方案包升级至 L2 时都会补齐这些章节。

`verification` 分布（核查于 2026-10-09）：**6 个 source-checked**
（iam-platform、itsm-helpdesk、personal-blog、wms、mes、tms），11 个 unverified，
**0 个 practitioner-reviewed，0 个 field-proven**——第 3–4 级需要明确指定的人员
和实际部署，这属于社区/现场任务，而非编辑工作。

## 阶段 2 — 工具与质量闸门

- [x] `packlint` 核心：清单模式验证、级别检查清单、
  验证阶梯一致性、横幅规则、相对链接检查、OpenAPI
  可解析性、翻译一致性（在 CI 中运行）
- [x] `packlint` 高级功能：ID 交叉引用检查（`tools/check-ids.py` —
  悬空的 FR/NFR/CTL/BR/AC/ADR/SM/CAP/BC 引用将导致 CI 失败；跨方案包引用
  作为信息报告）
- [x] 工具测试（`tests/`，pytest；在 CI 中运行）
- [x] 外部引用链接探测（`check-links.py --check-external`，CI 作业）
- [ ] 术语表一致性检查（推迟：需要先建立术语注册表）
- [ ] 智能体使用指南：Spec Kit、BMAD-METHOD、Kiro、Claude Code、Codex
- [x] 方案包注册表索引——**可搜索静态站点**（`tools/build-site.py`
  → GitHub Pages），具备全文搜索、分面筛选和链接自检功能
- [ ] 双语（EN/zh-CN）一致性跟踪——目前整个方案包集中均为
  `translations: []`（关键资产为双语；完整翻译将逐步推进）

## 阶段 3 — 成熟方案包与生态

- 附带关联开源参考实现的 L4 方案包
- 面向主流技术栈的变体叠加层（云原生、国产化/信创）
- 维护者治理：各行业的领域维护者、评审轮换
- 教学路径：如何阅读/编写方案包，用于架构课程

## 非目标（明确声明）

- 本仓库**不**提供生产代码框架（对实现的引用仅提供链接，不以内置方式收录）。
- 本仓库不偏向任何云厂商，也不销售任何云厂商的产品。
- 本仓库绝不托管机密材料或源自客户的材料。
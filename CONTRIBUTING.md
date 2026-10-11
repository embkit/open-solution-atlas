# Contributing to Open Solution Atlas

First: thank you. The value of this library is the industry knowledge that
practitioners choose to share in a generalized, reusable form.

[中文说明见下](#中文贡献指南)

## What we accept

- **Solution Packs** at any maturity level (L1–L4) following
  [docs/pack-standard.v1.md](docs/pack-standard.v1.md).
- Improvements to existing packs: precision, corrections, sources, diagrams,
  translations.
- Taxonomy changes (see the rule in [docs/taxonomy.md](docs/taxonomy.md)).
- Tooling that validates or converts packs.

## What we do not accept

- **Any confidential material**: client names, internal documents, proprietary
  architecture slides, credentials, or data. When in doubt, leave it out.
- Vendor marketing: vendor-neutral core is the default; a vendor/stack view
  belongs in `variants/` and must be labeled.
- Vague prose that cannot be implemented or tested ("it should be fast", "use
  best practices").
- AI-generated bulk content without a knowledgeable human sponsor. Every pack
  needs at least one maintainer who can defend its accuracy.
- Content that claims more verification than it has. Declare `provenance` and
  `verification` honestly in `manifest.yaml` (see
  [standard section 8](docs/pack-standard.v1.md)). An LLM may draft a pack;
  it may never *verify* one.

## The one hard rule

> Contribute generalized knowledge, never generalized *experience dumps*.
> Names, numbers, and documents that identify an employer or client must be
> removed. Capabilities, patterns, and public regulations are exactly what we
> want.

## Flow

1. **Propose**: open an issue describing the system, its domain, and the
   maturity level you can commit to.
2. **Scaffold**: copy `templates/pack-template/` to
   `packs/<domain>/<slug>/` and fill `manifest.yaml`.
3. **Build to a level**: stop at L1 if that is honest today; do not fake L3.
4. **Declare trust honestly**: set `provenance` and `verification` in
   `manifest.yaml`. New LLM-drafted packs start
   `provenance: llm-drafted` / `verification: unverified` and carry the draft
   banner in `README.md`.
5. **Self-review** against the level checklist in the pack standard.
6. **Pull request**: every PR must pass the required CI checks and carry **one
   approving review** before merge — enforced by branch protection, not by
   convention. The intent is a domain reviewer *and* an architecture reviewer;
   with a single maintainer today, one approval is what the gate can require
   (an author cannot approve their own PR, and a second approver does not
   exist yet — see [`MAINTAINERS.md`](MAINTAINERS.md)). L2+ packs require
   cited public sources.

## Verification (raising `verification`)

Verification is a separate track from maturity. Raise it only with evidence:

| To reach | You must supply |
|---|---|
| `source-checked` | a `SOURCES.md` ledger mapping every load-bearing claim to a public citation; no uncited specifics |
| `practitioner-reviewed` | named practitioners in `verified_by` (role, date, scope); author may not self-approve |
| `field-proven` | a linked public reference implementation and/or describable deployment evidence |

Rules: no self-escalation; keep the draft banner while `unverified`; a pack may
be L3 and `unverified` at the same time — say so.

## Style

- Markdown + YAML + diagrams-as-code (Mermaid/PlantUML).
- Stable IDs (`FR-*`, `NFR-*`, `CTL-*`, `ADR-*`); never renumber.
- English is the repository's primary language; Chinese (zh-CN) is a
  first-class translation. Bilingual packs are encouraged.
- Mark uncertainty explicitly with `> ⚠️ ASSUMPTION:`.

## Developer Certificate of Origin (DCO)

Every commit must be signed off, certifying the
[Developer Certificate of Origin](https://developercertificate.org/). Add a
trailer to each commit:

```
Signed-off-by: Your Name <you@example.com>
```

Git can add it automatically: `git commit -s`. A commit without a matching
`Signed-off-by` trailer cannot be merged. There is no separate CLA — the DCO
plus the dual license below is the entire agreement.

## License

By contributing you agree to the dual license in [LICENSE](LICENSE):
CC BY-SA 4.0 for content, MIT for code/templates.

---

# 中文贡献指南

## 我们接收什么

- 遵循 [方案包规范 v1](docs/pack-standard.v1.md) 的各成熟度方案包（L1–L4）
- 对现有方案的精确化、勘误、公开来源补充、图表、翻译
- 行业分类（taxonomy）的演进、校验与转换工具

## 我们不接收什么

- **任何涉密材料**：客户名称、内部文档、专有架构 PPT、账号密钥、业务数据。
  拿不准就不放。
- 厂商软文：核心方案默认厂商中立；特定云/技术栈视角放入 `variants/` 并明确标注。
- 无法被实现或验证的空话（"性能要高"、"采用最佳实践"）。
- 无专业负责人背书的 AI 批量生成内容。每个方案包至少有一名能为其准确性负责的
  维护者。
- 声明了超出实际证据的验证等级的内容。请在 `manifest.yaml` 中如实声明
  `provenance` 与 `verification`（见[规范第 8 节](docs/pack-standard.v1.md)）。
  LLM 可以起草方案包，但**永远不能"验证"方案包**。

## 唯一铁律

> 贡献的是**通用化的知识**，不是脱敏不彻底的项目回忆录。
> 任何能识别出雇主或客户的名称、数字、文档都必须移除；业务能力、通用模式、
> 公开监管要求才是我们需要的内容。

## 流程

1. **提案**：issue 描述目标系统、所属领域、你能承诺的成熟度。
2. **建包**：复制 `templates/pack-template/` 到 `packs/<domain>/<slug>/`。
3. **按级交付**：今天只有 L1 就如实停在 L1，不要伪装成 L3。
4. **如实声明可信度**：在 `manifest.yaml` 里设置 `provenance` 与
   `verification`；新建的 LLM 起草包从
   `provenance: llm-drafted` / `verification: unverified` 起步，并在
   `README.md` 顶部挂草稿横幅。
5. **自检**：对照规范中的成熟度清单。
6. **评审**：需一名领域评审 + 一名架构评审；L2 起必须引用公开来源。

## 验证（提升 `verification`）

验证与成熟度是两条独立轨道，只有拿到证据才能升级：

| 目标等级 | 必须提供的证据 |
|---|---|
| `source-checked` | 一份 `SOURCES.md` 溯源台账，把每条承重论断挂到公开出处，不留无据细节 |
| `practitioner-reviewed` | `verified_by` 中具名实践者（角色/日期/范围）；作者不得自审自批 |
| `field-proven` | 已链接的公开参考实现，和/或可公开描述的部署佐证 |

规则：不得自我拔高；`unverified` 期间保留草稿横幅；一个包可以同时是 L3 且
`unverified`——如实说明即可。

## 风格

- Markdown + YAML + 代码化图表（Mermaid/PlantUML）
- 稳定编号（`FR-*`、`NFR-*`、`CTL-*`、`ADR-*`），不复用、不重排
- 英文为主语言，中文（zh-CN）为一等翻译语言，鼓励双语方案
- 不确定处用 `> ⚠️ ASSUMPTION:` 显式标注

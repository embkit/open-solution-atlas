# 为 Open Solution Atlas 作出贡献

首先：感谢你。这个库的价值在于行业实践者选择以通用、可复用的形式分享的行业知识。

[中文说明见下](#中文贡献指南)

## 我们接收什么

- **方案包**：遵循 [方案包规范 v1](docs/pack-standard.v1.md) 的各成熟度方案包（L1–L4）。
- 对现有方案的精确化、勘误、公开来源补充、图表、翻译。
- 分类体系变更（见 [docs/taxonomy.md](docs/taxonomy.md) 中的规则）。
- 用于验证或转换方案包的工具。

## 我们不接收什么

- **任何涉密材料**：客户名称、内部文档、专有架构 PPT、账号密钥、业务数据。拿不准就不放。
- 厂商软文：核心方案默认厂商中立；特定云/技术栈视角放入 `variants/` 并明确标注。
- 无法实施或测试的含糊表述（"它应该很快"、"采用最佳实践"）。
- 无专业负责人背书的 AI 批量生成内容。每个方案包至少有一名能为其准确性负责的维护者。
- 声称验证程度超出实际证据的内容。请在 `manifest.yaml` 中如实声明 `provenance`（来源性质）与 `verification`（验证状态）（见[规范第 8 节](docs/pack-standard.v1.md)）。LLM 可以起草方案包，但**永远不能"验证"方案包**。

## 唯一铁律

> 贡献的是**通用化的知识**，不是脱敏不彻底的项目回忆录。
> 必须移除所有能够识别雇主或客户的名称、数字和文档。能力、模式和公开
> 法规正是我们想要的内容。

## 流程

1. **提案**：创建一个 issue，描述目标系统、所属领域，以及你能承诺达到的成熟度等级。
2. **建包**：将 `templates/pack-template/` 复制到 `packs/<domain>/<slug>/`，并填写 `manifest.yaml`。
3. **按级交付**：如果当前实际水平只能达到 L1，就如实停在 L1；不要伪装成 L3。
4. **如实声明可信度**：在 `manifest.yaml` 中设置 `provenance` 与 `verification`。新建的 LLM 起草方案包从 `provenance: llm-drafted` / `verification: unverified` 起步，并在 `README.md` 顶部挂草稿横幅。
5. **自检**：对照方案包规范中的等级检查清单。
6. **拉取请求**：每个 PR 都必须通过必需的 CI 检查，并在合并前获得**一次批准评审**——这由分支保护机制强制执行，而非仅靠约定。其意图是由领域评审者*和*架构评审者共同评审；目前只有一名维护者，因此闸门只能要求一次批准（作者不能批准自己的 PR，而且目前尚无第二名批准者——见 [`MAINTAINERS.md`](MAINTAINERS.md)）。L2+ 方案包必须引用公开来源。

## 验证（提升 `verification`）

验证与成熟度是两条独立轨道，只有拿到证据才能升级：

| 目标等级 | 必须提供的证据 |
|---|---|
| `source-checked` | 一份 `SOURCES.md` 溯源台账，把每条承重论断挂到公开出处，不留无据细节 |
| `practitioner-reviewed` | `verified_by` 中具名实践者（角色/日期/范围）；作者不得自审自批 |
| `field-proven` | 已链接的公开参考实现，和/或可公开描述的部署佐证 |

规则：不得自我拔高；`unverified` 期间保留草稿横幅；一个方案包可以同时是 L3 且 `unverified`——如实说明即可。

## 风格

- Markdown + YAML + 代码化图表（Mermaid/PlantUML）。
- 稳定 ID（`FR-*`、`NFR-*`、`CTL-*`、`ADR-*`）；绝不重新编号。
- 英文是仓库的主要语言；中文（zh-CN）是一等翻译语言。鼓励双语方案包。
- 翻译是原文的**同级兄弟文件**（`01-business/business-rules.zh-CN.md`），而不是另一套并行目录：两份文件共用同一套 URL 空间，因此相对链接在任一语言下都指向读者要的页面。结构保持不变——同样的标识符、同样的表格、同样的代码块——只翻译它们周围的文字。`python tools/check-translations.py` 会逐个比对译文与原文并报出偏离；`tools/validate-packs.py` 会拒绝声称 `translations: [zh-CN]` 却没有把全包翻完的方案包。
- 不确定处用 `> ⚠️ ASSUMPTION:` 显式标注。

## 开发者原创声明（DCO）

每次提交都必须签署确认，以证明遵守[开发者原创声明](https://developercertificate.org/)。为每次提交添加以下尾注：

```
Signed-off-by: Your Name <you@example.com>
```

Git 可以自动添加：`git commit -s`。没有匹配的 `Signed-off-by` 尾注的提交不得合并。这里没有单独的 CLA——DCO 与下述双重许可共同构成全部协议。

## 许可

贡献即表示你同意 [LICENSE](LICENSE) 中的双重许可：内容采用 CC BY-SA 4.0，代码和模板采用 MIT。

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
- 翻译是原文的**同级兄弟文件**（`01-business/business-rules.zh-CN.md`），而不是另一套
  并行目录：两份文件共用同一套 URL 空间，因此相对链接在任一语言下都指向读者
  要的页面。结构保持不变——同样的编号、同样的表格、同样的代码块——只翻译
  它们周围的文字。`python tools/check-translations.py` 会逐个比对译文与原文并报出偏离；
  `tools/validate-packs.py` 会拒绝声称 `translations: [zh-CN]` 却没有把全包翻完的方案包。
- 不确定处用 `> ⚠️ ASSUMPTION:` 显式标注
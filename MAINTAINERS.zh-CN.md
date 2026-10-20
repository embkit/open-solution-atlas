# 维护者

Open Solution Atlas 采用**按领域划分的维护者**模式：每个分类体系领域（见 [`docs/taxonomy.md`](docs/taxonomy.md)）均由在该领域具有第一手经验的人员负责，因此方案包评审是实质性的，而非仅做编辑工作。

## 当前状态

| 角色 | 负责人 | 说明 |
|---|---|---|
| 仓库维护者 | [@ebk-slm](https://github.com/ebk-slm) | 负责标准、工具、CI 和发布标记。目前是唯一的维护者。 |
| 领域维护者 | _尚未任命_ | 从实践者评审队列中招募（见下文）。每次新任命都会为相应领域启用 `practitioner-reviewed` 验证。 |

> 本文件记录的是实际任职者，而非意向人选。在领域维护者接受其职责之前，仓库维护者负责审查该领域的 PR——这会成为瓶颈；而目前单项价值最高的贡献就是补齐这些行。

## 角色

- **仓库维护者** — 负责 `docs/pack-standard.v1.md`、`tools/`、CI、模板和发布标记。对所有内容拥有合并权限。
- **领域维护者** — 负责审查 `packs/<domain>/**` 下的 PR；为该领域运行实践者评审流程（`.github/ISSUE_TEMPLATE/practitioner-review.yml`）；可与一名具名领域实践者共同批准向 `practitioner-reviewed` 提升（标准 §8.3 规则 4：作者不得自行批准）。
- **方案包作者** — 任何人均可担任，详见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 提升权限（谁可以提升 `verification`）

| 提升 | 执行者 | 机器闸门 |
|---|---|---|
| `unverified` → `source-checked` | 任何贡献者 + CI 通过 | `tools/validate-packs.py`（台账、证据、横幅） |
| → `practitioner-reviewed` | 由具名实践者通过问题模板发起 + 领域维护者合并 | `verified_by` 非空，条目完整 |
| → `field-proven` | 仓库维护者，并附有公开参考实现或可描述的部署证据 | `deployment`/`case-study` 证据条目 |

> **验证阶梯在第 2 级之上是空的。** 本库中没有任何方案包处于 `practitioner-reviewed` 或 `field-proven` 状态，因为这两个级别都要求有具名人员和实际部署——这类工作无论投入多少工具都无法替代。这里明确说明这一事实，而不是加以掩饰。

## 成为领域维护者

创建一个议题：说明你的领域、你的第一手经验（需概括说明——绝不能涉及雇主机密），以及你愿意持续评审的方案包。我们会以持续开展两次实质性评审作为起始门槛。
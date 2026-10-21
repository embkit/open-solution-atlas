# AGENTS.md - Open Solution Atlas

## 项目形态

Open Solution Atlas 是一个内容与工具仓库，而非生产应用。其主要交付物是厂商中立的 Solution Pack（解决方案包）：面向真实行业系统的完整规范，同时供人类读者和规范驱动型编码代理使用。该仓库还提供验证器、方案包注册表、提示词生成器以及静态 GitHub Pages 站点。

英语是仓库的主要语言；简体中文是一级翻译。不要将正确的全角中文标点改写为 ASCII 标点。

## 源文件边界

只有受 Git 跟踪的仓库内容才属于项目源文件。尤其是：

- `packs/` - 17 个 Solution Pack 及所有方案包级源材料。
- `docs/` - 规范性方案包标准、分类体系、路线图、站点 UI 契约和引用审计。
- `schemas/` - 面向编辑器的清单架构。
- `tools/` - Python 验证器和构建器，以及注册表站点资源。
- `tests/` - Python 工具链和生成站点的测试。
- `templates/` - 可复用的方案包模板和脚手架说明。
- `design-systems/` - 外置的设计系统参考：互操作协议与品牌对照库，站点 token 工作以此为映射对象。以英文**逐字提交**：属于外部参考材料，不属翻译语料，其中文树页面带未翻译横幅是设计之内的行为。
- `.github/` - CI、Pages、CodeQL 和贡献工作流配置。
- 根目录下的 `README*`、`CONTRIBUTING.md`、`CHANGELOG.md` 和许可证文件。

以下顶层目录仅作为本地被忽略的工具或构建输出存在；它们不属于 Open Solution Atlas 内容，且不得编辑，也不得作为仓库更改提交：

- `accessibility/`、`components/`、`content/`、`frameworks/`、`scripts/`、`taste/`、`tokens/`、`workflows/`、`.claude/`
- `_site/`、`_final2/`、`_v2/`、`_v3/`、`_v4/` 以及其他所有 `_*` 目录
- `package.json`、`package-lock.json`、`node_modules/`

当源文件与本地工具之间存在歧义时，应优先使用 `git ls-files` 和 `.gitignore`，而不是直接列出原始文件系统内容。

## 加载顺序

对于任何仓库范围的任务：

1. 阅读本文件。
2. 阅读相关的根入口：
   - 方案包内容或信任规则：`README.md`、`docs/pack-standard.v1.md`
   - 贡献约束：`CONTRIBUTING.md`
   - 分类体系与收录范围：`docs/taxonomy.md`
   - 计划中的晋级工作：`docs/roadmap.md`
   - 站点行为或 UI 规则：`docs/embkit-ui-contract.md`

对于 `packs/<domain>/<slug>/` 内的工作，紧接本文件之后阅读该方案包的 `AGENTS.md`，随后阅读其 `manifest.yaml`、`README.md` 和 `SOURCES.md`。遵循该方案包自身的章节加载顺序；不要以对方案包进行通用扫描来替代。

## 硬性规则

- `maturity` 和 `verification` 相互独立。成熟度衡量完整性；验证状态衡量外部证据。绝不暗示其中一项能够证明另一项。
- 新增的 LLM 起草内容以 `provenance: llm-drafted` 和 `verification: unverified` 开始，并带有规定的草案横幅。LLM 可以起草内容，但绝不能对其进行验证。
- `FR-*`、`NFR-*`、`CTL-*`、`BR-*`、`AC-*`、`ADR-*`、`SM-*`、`CAP-*` 和 `T-*` 等稳定 ID 不可变。只能新增 ID；绝不可重新编号。
- 已定案的 ADR 构成约束条件。如果所请求的更改似乎会重新开启其中一项，应指出冲突，而不是悄然推翻该决策。
- 按照仓库既定的标记样式，将未决事实明确标记为 `> ASSUMPTION:`。
- 保持核心内容厂商中立。特定于技术的立场应置于明确标注的 `variants/` 覆盖层中。
- 绝不添加机密、源自客户、凭据类或可识别雇主/客户身份的材料。
- 将 L2/L3 主张追溯到公开来源，或追溯到方案包中已经记录的证据。没有规定证据时，绝不提升 `verification`。

## 常用命令

编辑期间运行相关命令子集；在宣布仓库范围的工作完成之前，运行完整命令序列。

```powershell
python tools/validate-packs.py
python tools/check-ids.py
python tools/check-links.py
python tools/build-site.py --site-url=
python -m pytest tests/ -q
ruff check .
```

CI 一致性细节见 `.github/workflows/ci.yml`。运行时依赖项的版本固定在 `requirements.txt` 和 `requirements-dev.txt` 中；Node 仅供本地浏览器验证工具使用，发布站点不使用 Node。

## 完成标准

当一项更改的内容与其生成后的行为一致时，该更改即为完成：

- 方案包编辑内容满足适用的成熟度检查清单和信任横幅规则。
- 相对 Markdown 链接能够正确解析。
- 跨章节引用的稳定 ID 仍能正确解析。
- 静态站点构建成功。
- 工具链更改通过 pytest 和 Ruff 检查。
- 生成的 `_*` 输出绝不提交。
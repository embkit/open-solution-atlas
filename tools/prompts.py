"""prompts.py — assemble working prompts from a pack's structured content.

The catalog's value is that its content is *traceable*: an identifier resolves,
a rule has a stated proposition, an ADR records what it decided and why. An
off-the-shelf prompt does not carry any of that, so a model handed one produces
a generic implementation of a workflow engine — correct-looking and missing
every decision this repository exists to record.

So the prompts are assembled at build time **from the pack's own content**, and
never written by hand. A prompt that carries `BR-05`'s semantics, `ADR-0004`'s
decision and the store-enforced constraints has a chance of producing an
implementation with defined guarantees; a prompt that says "build a workflow
engine with approval" does not, and no amount of editing fixes that.

Three templates are short enough to inline in a page and copy in one click:

    ``implement``  the pack as a build brief — capabilities, rules, decisions,
                   constraints, and the honesty conditions that must survive
    ``adr``        one decision, with the requirements and rules it drives
    ``test``       one rule and the requirements that enforce it

A fourth is too large to inline and is emitted as a file instead:

    ``context``    the whole pack, chapter by chapter, for a model that needs
                   the source rather than a summary of it

Every prompt states the repository's conditions — `verification: unverified`,
no claimed conformance, policy numbers marked `(A)` — because a prompt that
omits them gets an implementation that quietly invents them.

The templates exist in two languages. The *content* of a prompt comes from the
pack index, which the build already reads in its own language; the framing
around it — the headings, the instructions, the honesty conditions — comes
from `STRINGS` below. A Chinese build therefore produces a Chinese prompt
whose rules are Chinese too, rather than a Chinese list of English sentences.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# How much of a pack's prose the context bundle carries. Packs run 14 chapters
# and several of them are long; the cap keeps one file to a sane size rather
# than dropping chapters wholesale.
MAX_CHAPTER_CHARS = 9000

# Chapters worth carrying in full, in the order a builder needs them.
CONTEXT_CHAPTERS = (
    "AGENTS.md",
    "01-business/capability-map.md",
    "01-business/business-rules.md",
    "02-requirements/functional.md",
    "02-requirements/non-functional.md",
    "02-requirements/compliance.md",
    "03-domain/domain-model.md",
    "03-domain/glossary.md",
    "04-architecture/overview.md",
    "04-architecture/security.md",
    "05-data/logical-data-model.md",
    "05-data/data-dictionary.md",
    "README.md",
    "SOURCES.md",
)

#: The framing prose of the prompts, in both languages.
#:
#: The content inside a prompt — rule names, propositions, decisions — is read
#: from the pack index, which the build already reads in the page's language.
#: This table is the frame around that content: the headings and the
#: instructions that tell a model what to do with it. A prompt half in one
#: language and half in the other is the mixed state the site avoids
#: everywhere else, so it is avoided here too.
STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "meta.source": "source pack",
        "meta.maturity": "maturity",
        "meta.verification": "verification",
        "meta.version": "version",
        "meta.stack": "stack stance",
        "meta.not_stated": "not stated",
        "cond.heading": "## Conditions that must survive into whatever you build",
        "cond.body": (
            "This repository is `verification: unverified`. Every pack is "
            "`llm-drafted`, no deployment evidence exists, and the draft banner "
            "in each chapter is part of the content — do not remove it, and do "
            "not upgrade a claim because your implementation happens to satisfy "
            "it."
        ),
        "cond.specifically": "Specifically:",
        "cond.no_conformance": (
            "- Claim **no** conformance to any standard named in the pack. They "
            "are adopted as vocabulary and shape only."
        ),
        "cond.policy": (
            "- Numeric targets marked `(A)` are **policy assumptions authored by "
            "this repository**, not measurements. Keep the marker and say so."
        ),
        "cond.gaps": (
            "- Where the pack records a gap (a retention period, a cryptographic "
            "primitive, an estimation method), leave it a gap. Do not fill it "
            "with a plausible value."
        ),
        "cond.ids": (
            "- Retain every identifier (`BR-`, `FR-`, `NFR-`, `CTL-`, `ADR-`) "
            "and let traces resolve, so the implementation stays checkable "
            "against this pack."
        ),
        "impl.heading": "## What you are building",
        "impl.body": (
            "A working prototype of the system described by this pack. It is a "
            "**blueprint**, so the point is fidelity to the recorded decisions "
            "rather than breadth of features: an implementation that shows the "
            "decision and the constraint beats one that grows a feature the "
            "pack did not specify."
        ),
        "impl.capabilities": "### Capabilities",
        "impl.rules": "### Business rules (normative; do not simplify them away)",
        "impl.enforced_by": "enforced by:",
        "impl.decisions": "### Decisions already taken (do not relitigate)",
        "impl.decision": "decision:",
        "impl.adr_note": (
            "Each ADR file under `04-architecture/adr/` states its options and "
            "consequences. Read the ones your design touches before choosing "
            "an approach; the alternatives were weighed and rejected for "
            "reasons recorded there."
        ),
        "impl.constraints": "### Enforced constraints",
        "impl.store_enforced": " **[store-enforced]**",
        "impl.enforces": "enforces:",
        "impl.constraints_note": (
            "Constraints marked **[store-enforced]** must be impossible to "
            "violate in your implementation, not merely discouraged — they "
            "belong in the schema or the store's own rules, not in application "
            "code that a later change can bypass."
        ),
        "impl.targets": "### Measurable targets",
        "impl.policy_note": " **(policy — not a measurement)**",
        "impl.target": "target:",
        "impl.formula": "formula:",
        "impl.produce": "### What to produce",
        "impl.produce_1": (
            "- A runnable prototype covering the capabilities above, in a single "
            "repository, with the key entities from the domain model."
        ),
        "impl.produce_2": (
            "- The store-enforced constraints implemented as schema or store "
            "rules, with a test that proves each one rejects the violation it "
            "names."
        ),
        "impl.produce_3": (
            "- A short report of where your implementation had to *choose* "
            "something the pack left open, so the choice is visible rather than "
            "silent."
        ),
        "impl.scale": "### Scale of the pack",
        "impl.scale_line": (
            "{rules} business rules · {requirements} functional requirements · "
            "{nfrs} measurable targets · {controls} controls · {adrs} ADRs · "
            "{constraints} integrity constraints ({store_constraints} store-enforced)"
        ),
        "adr.heading": "## The decision: `{id}` — {name}",
        "adr.ruled_out": "### Ruled out (do not re-derive these)",
        "adr.rejected": "Rejected, for reasons recorded in the ADR:",
        "adr.no_alternatives": "(alternatives not extracted — read the ADR file)",
        "adr.source": (
            "Source: `{src}` — read the Context, Options and Consequences "
            "sections for the reasoning behind each rejection."
        ),
        "adr.depends": "### What depends on it",
        "adr.nothing": "- (nothing traces to this ADR in the pack index)",
        "adr.task": "## Task",
        "adr.task_body": (
            "Implement the decision above. The requirements listed are what it "
            "forces, so your implementation should make each of them true "
            "rather than merely compatible with the decision's wording."
        ),
        "adr.trade": (
            "Where the decision trades something away, keep the trade rather "
            "than optimising it out: each consequence was accepted for a "
            "recorded reason, and an implementation that quietly reverses one "
            "is harder to review than one that names the problem."
        ),
        "adr.missing": "# {id}\n\nNo such ADR in this pack.\n",
        "test.heading": "## The rule: `{id}` — {name}",
        "test.no_proposition": "(see the rule file for the proposition)",
        "test.source": "Source: `{src}`",
        "test.requires": "### Requirements that enforce it",
        "test.when": "WHEN",
        "test.shall": "SHALL",
        "test.shall_not": "SHALL NOT",
        "test.no_requirements": (
            "- (no requirement traces to this rule in the pack index)"
        ),
        "test.measured": "### Targets that measure it",
        "test.nothing": "- (nothing measures this rule directly)",
        "test.task": "## Task",
        "test.task_body": (
            "Write tests that fail when this rule is violated. For each test:"
        ),
        "test.step_1": "1. Name the identifier from this pack it protects.",
        "test.step_2": "2. Arrange the state the rule's precondition describes.",
        "test.step_3": (
            "3. Assert the consequence, including the prohibition — the "
            "`SHALL NOT` half is the half that fails first in a real system."
        ),
        "test.after": (
            "A test that only exercises the happy path does not test this rule; "
            "the rule exists to reject something specific."
        ),
        "test.missing": "# {id}\n\nNo such rule in this pack.\n",
        "ctx.body": (
            "This bundle is the pack itself. Read it before implementing "
            "anything from this repository: the decisions and their "
            "consequences are in the ADR files, the normative propositions are "
            "in the business rules, and the conditions at the end apply to "
            "whatever you produce."
        ),
        "common.none": "- (none recorded)",
    },
    "zh": {
        "meta.source": "来源方案包",
        "meta.maturity": "成熟度",
        "meta.verification": "验证状态",
        "meta.version": "版本",
        "meta.stack": "技术栈立场",
        "meta.not_stated": "未声明",
        "cond.heading": "## 必须带入你所构建之物的条件",
        "cond.body": (
            "本仓库的 `verification` 为 `unverified`。每个方案包都是 "
            "`llm-drafted`，不存在任何部署证据；每一章顶部的草稿横幅属于内容"
            "的一部分——不要删除它，也不要因为你的实现恰好满足了某条论断，就"
            "抬高它的验证等级。"
        ),
        "cond.specifically": "具体来说：",
        "cond.no_conformance": (
            "- 对方案包中提到的任何标准都**不得声称符合**。它们只被采纳为"
            "词汇与形状。"
        ),
        "cond.policy": (
            "- 标注 `(A)` 的数值目标是**本仓库自行设定的策略假设**，不是测量值。"
            "保留这个标记，并如实说明。"
        ),
        "cond.gaps": (
            "- 方案包记录为缺口的地方（保留期限、密码学原语、估算方法），就让它"
            "保持缺口。不要用一个看似合理的数值把它填上。"
        ),
        "cond.ids": (
            "- 保留每一个编号（`BR-`、`FR-`、`NFR-`、`CTL-`、`ADR-`），并让追溯"
            "关系能够解析，使实现始终可以与本方案包相互校验。"
        ),
        "impl.heading": "## 你要构建什么",
        "impl.body": (
            "本方案包所描述系统的一个可运行原型。它是一份**蓝图**，因此重点是"
            "忠实于已记录的决策，而不是功能的广度：一个体现了决策与约束的实现，"
            "胜过一个长出了方案包未曾规定之功能的实现。"
        ),
        "impl.capabilities": "### 能力",
        "impl.rules": "### 业务规则（规范性；不得简化掉）",
        "impl.enforced_by": "由以下强制执行：",
        "impl.decisions": "### 已作出的决策（不要重新争论）",
        "impl.decision": "决策：",
        "impl.adr_note": (
            "`04-architecture/adr/` 下的每个 ADR 文件都写明了它的备选方案与"
            "后果。在选定做法之前，先读那些与你的设计相关的文件；那些备选方案"
            "都曾被权衡，并因文件中记录的理由被否决。"
        ),
        "impl.constraints": "### 强制约束",
        "impl.store_enforced": " **[存储层强制执行]**",
        "impl.enforces": "强制以下约束：",
        "impl.constraints_note": (
            "标注 **[存储层强制执行]** 的约束，在你的实现中必须**无法被违反**，"
            "而不只是“不被鼓励”——它们应当落在 schema 或存储自身的规则里，"
            "而不是写在日后一次改动就能绕过的应用代码中。"
        ),
        "impl.targets": "### 可度量目标",
        "impl.policy_note": " **（策略，不是测量值）**",
        "impl.target": "目标：",
        "impl.formula": "公式：",
        "impl.produce": "### 需要产出什么",
        "impl.produce_1": (
            "- 一个覆盖上述各项能力的可运行原型，放在同一个仓库里，并包含领域"
            "模型中的关键实体。"
        ),
        "impl.produce_2": (
            "- 把存储层强制执行的约束实现为 schema 或存储规则，并各写一个测试，"
            "证明它确实会拒绝它所命名的违规行为。"
        ),
        "impl.produce_3": (
            "- 一份简短报告，说明实现中哪些地方不得不**自行选择**方案包留下的"
            "空白，使这些选择可见，而不是无声无息。"
        ),
        "impl.scale": "### 方案包的规模",
        "impl.scale_line": (
            "{rules} 条业务规则 · {requirements} 条功能需求 · "
            "{nfrs} 个可度量目标 · {controls} 项控制 · {adrs} 个 ADR · "
            "{constraints} 条完整性约束（其中 {store_constraints} 条由存储层强制执行）"
        ),
        "adr.heading": "## 决策：`{id}` — {name}",
        "adr.ruled_out": "### 已被否决（不要重新推导）",
        "adr.rejected": "以下方案已被否决，原因记录在 ADR 中：",
        "adr.no_alternatives": "（未提取到备选方案——请阅读 ADR 文件）",
        "adr.source": (
            "来源：`{src}`——阅读其中的背景、备选方案与后果各节，了解每次否决"
            "背后的推理。"
        ),
        "adr.depends": "### 谁依赖它",
        "adr.nothing": "- （方案包索引中没有任何内容追溯到这个 ADR）",
        "adr.task": "## 任务",
        "adr.task_body": (
            "实现上面的决策。所列的需求正是它强制出来的东西，因此你的实现应当"
            "让每一条需求**成立**，而不只是与决策的措辞兼容。"
        ),
        "adr.trade": (
            "当这个决策以某种东西为代价时，保留这份取舍，而不是把它优化掉：每一"
            "条后果都是出于有记录的理由被接受的；一个悄悄把后果反转回去的实现，"
            "比一个把问题讲出来的实现更难评审。"
        ),
        "adr.missing": "# {id}\n\n本方案包中没有这个 ADR。\n",
        "test.heading": "## 规则：`{id}` — {name}",
        "test.no_proposition": "（命题见规则文件）",
        "test.source": "来源：`{src}`",
        "test.requires": "### 强制执行它的需求",
        "test.when": "当",
        "test.shall": "系统应当",
        "test.shall_not": "系统不应当",
        "test.no_requirements": "- （方案包索引中没有任何需求追溯到这条规则）",
        "test.measured": "### 度量它的目标",
        "test.nothing": "- （没有任何目标直接度量这条规则）",
        "test.task": "## 任务",
        "test.task_body": "编写当这条规则被违反时就会失败的测试。每个测试：",
        "test.step_1": "1. 指出它保护的是本方案包里的哪一个编号。",
        "test.step_2": "2. 布置这条规则的前置条件所描述的状态。",
        "test.step_3": (
            "3. 断言后果，包括那条禁止——`SHALL NOT` 那一半，才是真实系统中"
            "最先失效的一半。"
        ),
        "test.after": (
            "只走通顺路径的测试并没有测试这条规则；这条规则的存在，是为了拒绝"
            "某个具体的东西。"
        ),
        "test.missing": "# {id}\n\n本方案包中没有这条规则。\n",
        "ctx.body": (
            "本文件就是方案包本身。在实现本仓库中的任何内容之前先读它：决策及其"
            "后果在 ADR 文件里，规范性命题在业务规则里，末尾的条件适用于你"
            "产出的任何东西。"
        ),
        "common.none": "- （未记录）",
    },
}


def bundle_filename(kind: str, item_id: str) -> str:
    """Filename for one per-identifier prompt.

    ``ADR-0004`` already states its own kind, so its file is ``adr-0004.md``;
    ``BR-05`` does not, so its file is ``test-br-05.md``. The rule lives here
    and nowhere else, so the emitted file and the link that points at it come
    from the same function — the same reasoning as ``pack_index.doc_url``.
    """
    name = item_id.strip().lower()
    if kind == "adr":
        return f"{name}.md"
    return f"{kind}-{name}.md"


def _t(lang: str, key: str) -> str:
    """One framing string, in the prompt's language."""
    table = STRINGS.get(lang) or STRINGS["en"]
    return table.get(key) or STRINGS["en"].get(key, key)


def _bullets(items: list[str], lang: str = "en") -> str:
    return "\n".join(f"- {i}" for i in items) if items else _t(lang, "common.none")


def _entry(entry: dict) -> dict:
    return entry


def _cond(entry: dict, lang: str = "en") -> str:
    """The honesty conditions every prompt carries.

    A prompt that omits these gets an implementation that invents them: a
    conformance claim, a retention period, a seal primitive. They cost four
    lines and they are the difference between a prototype and a plausible lie.
    """
    lines = [
        _t(lang, "cond.heading"),
        "",
        _t(lang, "cond.body"),
        "",
        _t(lang, "cond.specifically"),
        "",
        _t(lang, "cond.no_conformance"),
        _t(lang, "cond.policy"),
        _t(lang, "cond.gaps"),
        _t(lang, "cond.ids"),
        "",
    ]
    return "\n".join(lines)


def _meta(entry: dict, lang: str = "en") -> str:
    zh = f" ({entry['title_zh']})" if entry.get("title_zh") else ""
    maturity = entry.get("maturity", "L1")
    return (
        f"# {entry['title']}{zh}\n\n"
        f"- {_t(lang, 'meta.source')}: `packs/{_domain_path(entry)}`\n"
        f"- {_t(lang, 'meta.maturity')}: {maturity}\n"
        f"- {_t(lang, 'meta.verification')}: "
        f"{entry.get('verification', 'unverified')}\n"
        f"- {_t(lang, 'meta.version')}: {entry.get('version', '')}\n"
        f"- {_t(lang, 'meta.stack')}: "
        f"{entry.get('stack_stance') or _t(lang, 'meta.not_stated')}\n"
    )


def _domain_path(entry: dict) -> str:
    """Rebuild the pack's source path from its index entry."""
    return f"{entry['domain']}/{entry['slug']}"


def _localized(path: Path, locale: str | None) -> Path:
    """The translation of `path`, when the pack has one.

    A translation is a sibling, so the chapter a bundle carries in a Chinese
    build is the Chinese chapter — the same file with `.zh-CN` before the
    extension. Without this the context bundle would carry English chapters
    under a Chinese frame.
    """
    if locale:
        alt = path.with_name(path.stem + "." + locale + ".md")
        if alt.is_file():
            return alt
    return path


# --------------------------------------------------------------------------- #
# Template: implement the pack
# --------------------------------------------------------------------------- #


def implement(entry: dict, lang: str = "en") -> str:
    """A build brief: what to build, what constrains it, what decided it."""
    counts = entry["counts"]
    parts = [
        _meta(entry, lang),
        _t(lang, "impl.heading"),
        "",
        _t(lang, "impl.body"),
        "",
        _t(lang, "impl.capabilities"),
        "",
        _bullets(
            [f"`{c['id']}` {c['name']} — {c['one_liner']}"
             for c in entry["capabilities"]],
            lang,
        ),
        "",
        _t(lang, "impl.rules"),
        "",
    ]
    for rule in entry["rules"]:
        parts.append(f"- `{rule['id']}` {rule['name']}")
        if rule["proposition"]:
            parts.append(f"  {rule['proposition']}")
        if rule["enforced_by"]:
            parts.append(
                f"  {_t(lang, 'impl.enforced_by')} "
                f"{', '.join(rule['enforced_by'])}"
            )
    parts += ["", _t(lang, "impl.decisions"), ""]
    for adr in entry["adrs"]:
        parts.append(f"- `{adr['id']}` {adr['name']}")
        if adr["decision"]:
            parts.append(f"  {_t(lang, 'impl.decision')} {adr['decision']}")
    if entry["adrs"]:
        parts += ["", _t(lang, "impl.adr_note")]
    parts += ["", _t(lang, "impl.constraints"), ""]
    for con in entry["constraints"]:
        where = _t(lang, "impl.store_enforced") if con["store"] else ""
        parts.append(f"- `constraint {con['n']}`{where} {con['text']}")
        if con["enforces"]:
            parts.append(
                f"  {_t(lang, 'impl.enforces')} {', '.join(con['enforces'])}"
            )
    parts += [
        "",
        _t(lang, "impl.constraints_note"),
        "",
        _t(lang, "impl.targets"),
        "",
    ]
    for nfr in entry["nfrs"]:
        policy = _t(lang, "impl.policy_note") if nfr["is_policy"] else ""
        parts.append(f"- `{nfr['id']}` {nfr['name']}{policy}")
        if nfr["target"]:
            parts.append(f"  {_t(lang, 'impl.target')} {nfr['target']}")
        if nfr["formula"]:
            parts.append(f"  {_t(lang, 'impl.formula')} {nfr['formula']}")
    parts += [
        "",
        _t(lang, "impl.produce"),
        "",
        _t(lang, "impl.produce_1"),
        _t(lang, "impl.produce_2"),
        _t(lang, "impl.produce_3"),
        "",
        _t(lang, "impl.scale"),
        "",
        _t(lang, "impl.scale_line").format(**counts),
        "",
        _cond(entry, lang),
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Template: implement one decision
# --------------------------------------------------------------------------- #


def adr(entry: dict, adr_id: str, lang: str = "en") -> str:
    """A single decision, plus the requirements and rules that carry it."""
    record = next((a for a in entry["adrs"] if a["id"] == adr_id), None)
    if record is None:
        return _t(lang, "adr.missing").format(id=adr_id)
    src = f"packs/{_domain_path(entry)}/04-architecture/adr/{record['slug']}.md"
    body = record["decision"] or _t(lang, "adr.no_alternatives")
    dependents = [
        r for r in entry["requirements"] if adr_id in r["traces"]
    ] or [r for r in entry["rules"] if adr_id in r["trace_adrs"]]
    parts = [
        _meta(entry, lang),
        _t(lang, "adr.heading").format(id=record["id"], name=record["name"]),
        "",
        body,
        "",
        _t(lang, "adr.ruled_out"),
        "",
        # The rejected options are the half an implementer most needs: an ADR
        # exists to record what was rule out and why, so a prompt that carries
        # only the winner lets a model re-derive the loser.
        (_t(lang, "adr.rejected") + "\n\n"
         + "\n".join(f"- {r}" for r in record.get("rejected", [])))
        if record.get("rejected")
        else _t(lang, "adr.no_alternatives"),
        "",
        _t(lang, "adr.source").format(src=src),
        "",
        _t(lang, "adr.depends"),
        "",
    ]
    if dependents:
        for dep in dependents:
            label = dep.get("name", "")
            parts.append(f"- `{dep['id']}` {label}")
            if dep.get("shall"):
                parts.append(f"  {dep['shall']}")
    else:
        parts.append(_t(lang, "adr.nothing"))
    parts += [
        "",
        _t(lang, "adr.task"),
        "",
        _t(lang, "adr.task_body"),
        "",
        _t(lang, "adr.trade"),
        "",
        _cond(entry, lang),
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Template: test one rule
# --------------------------------------------------------------------------- #


def test(entry: dict, rule_id: str, lang: str = "en") -> str:
    """One rule, the requirements that enforce it, and the targets that measure it."""
    rule = next((r for r in entry["rules"] if r["id"] == rule_id), None)
    if rule is None:
        return _t(lang, "test.missing").format(id=rule_id)
    src = f"packs/{_domain_path(entry)}/01-business/business-rules.md"
    parts = [
        _meta(entry, lang),
        _t(lang, "test.heading").format(id=rule["id"], name=rule["name"]),
        "",
        rule["proposition"] or _t(lang, "test.no_proposition"),
        "",
        _t(lang, "test.source").format(src=src),
        "",
        _t(lang, "test.requires"),
        "",
    ]
    related = [q for q in entry["requirements"] if rule["id"] in q["traces"]]
    if related:
        for q in related:
            parts.append(f"- `{q['id']}` {q['name']}")
            if q["when"]:
                parts.append(f"  {_t(lang, 'test.when')} {q['when']}")
            if q["shall"]:
                parts.append(f"  {_t(lang, 'test.shall')} {q['shall']}")
            if q["shall_not"]:
                parts.append(f"  {_t(lang, 'test.shall_not')} {q['shall_not']}")
    else:
        parts.append(_t(lang, "test.no_requirements"))
    parts += ["", _t(lang, "test.measured"), ""]
    measured = [
        n for n in entry["nfrs"]
        if rule["id"] in " ".join(n.get("traces", [])) or any(
            rule["id"] in c.get("enforces", []) for c in entry["constraints"]
        )
    ] or [n for n in entry["nfrs"] if rule["id"] in (n.get("name", "") + n.get("target", ""))]
    if measured:
        for n in measured:
            policy = _t(lang, "impl.policy_note") if n["is_policy"] else ""
            parts.append(f"- `{n['id']}` {n['name']}{policy}")
            if n["formula"]:
                parts.append(f"  {_t(lang, 'impl.formula')} {n['formula']}")
    else:
        parts.append(_t(lang, "test.nothing"))
    parts += [
        "",
        _t(lang, "test.task"),
        "",
        _t(lang, "test.task_body"),
        "",
        _t(lang, "test.step_1"),
        _t(lang, "test.step_2"),
        _t(lang, "test.step_3"),
        "",
        _t(lang, "test.after"),
        "",
        _cond(entry, lang),
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Template: the whole pack as context
# --------------------------------------------------------------------------- #


def context_bundle(entry: dict, pack_dir: Path, lang: str = "en",
                   locale: str | None = None) -> str:
    """The pack's own chapters, concatenated — for a model needing the source."""
    parts = [
        _meta(entry, lang),
        _t(lang, "ctx.body"),
        "",
        _cond(entry, lang),
        "---",
        "",
    ]
    for rel in CONTEXT_CHAPTERS:
        path = _localized(pack_dir / rel, locale)
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if len(text) > MAX_CHAPTER_CHARS:
            text = text[:MAX_CHAPTER_CHARS] + "\n\n…(truncated by tools/prompts.py)\n"
        parts.append(f"\n## ===== {rel} =====\n\n{text.rstrip()}\n")
    # ADRs are separate files and each matters on its own.
    for adr in entry["adrs"]:
        path = _localized(
            pack_dir / "04-architecture" / "adr" / f"{adr['slug']}.md", locale
        )
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        parts.append(
            f"\n## ===== 04-architecture/adr/{adr['slug']}.md =====\n\n"
            f"{text.rstrip()}\n"
        )
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Assembly
# --------------------------------------------------------------------------- #

TEMPLATES = {
    "implement": {
        "label": "按规格实现原型",
        "blurb": "能力、规则、已决决策、强制约束、可测目标——连同必须被继承的诚实条件",
        "inline": True,
    },
    "adr": {
        "label": "实现一条 ADR 的决策",
        "blurb": "单个决策 + 依赖它的需求 + 被否掉的备选项所在文件",
        "inline": True,
    },
    "test": {
        "label": "为一条规则生成测试",
        "blurb": "规则命题 + 强制它的需求 + 测量它的目标（含公式）",
        "inline": True,
    },
    "context": {
        "label": "导出整包上下文",
        "blurb": "整包章节原文，供需要原文而非摘要的模型使用",
        "inline": False,
    },
}


def build_bundles(entry: dict, pack_dir: Path, lang: str = "en",
                  locale: str | None = None) -> dict:
    """Everything a page needs to offer: inline prompts and emitted files.

    The per-identifier variants (one ADR, one rule) are generated for the
    handful that matter most — the pack's ADRs and its load-bearing rules —
    rather than for every combination, which would be thousands of files.
    """
    inline = {
        "implement": implement(entry, lang),
        "adr": [{"id": a["id"], "label": a["name"], "text": adr(entry, a["id"], lang)}
                for a in entry["adrs"]],
        "test": [{"id": r["id"], "label": r["name"], "text": test(entry, r["id"], lang)}
                 for r in entry["rules"][:8]],
    }
    files = {
        "context.md": context_bundle(entry, pack_dir, lang, locale),
        "implement.md": inline["implement"],
    }
    for item in inline["adr"]:
        files[bundle_filename("adr", item["id"])] = item["text"]
    for item in inline["test"]:
        files[bundle_filename("test", item["id"])] = item["text"]
    return {"inline": inline, "files": files}

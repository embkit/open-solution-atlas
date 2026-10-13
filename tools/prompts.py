#!/usr/bin/env python3
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


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {i}" for i in items) if items else "- (none recorded)"


def _entry(entry: dict) -> dict:
    return entry


def _cond(entry: dict) -> str:
    """The honesty conditions every prompt carries.

    A prompt that omits these gets an implementation that invents them: a
    conformance claim, a retention period, a seal primitive. They cost four
    lines and they are the difference between a prototype and a plausible lie.
    """
    lines = [
        "## Conditions that must survive into whatever you build",
        "",
        "This repository is `verification: unverified`. Every pack is "
        "`llm-drafted`, no deployment evidence exists, and the draft banner in "
        "each chapter is part of the content — do not remove it, and do not "
        "upgrade a claim because your implementation happens to satisfy it.",
        "",
        "Specifically:",
        "",
        "- Claim **no** conformance to any standard named in the pack. They are "
        "adopted as vocabulary and shape only.",
        "- Numeric targets marked `(A)` are **policy assumptions authored by this "
        "repository**, not measurements. Keep the marker and say so.",
        "- Where the pack records a gap (a retention period, a cryptographic "
        "primitive, an estimation method), leave it a gap. Do not fill it with a "
        "plausible value.",
        "- Retain every identifier (`BR-`, `FR-`, `NFR-`, `CTL-`, `ADR-`) and let "
        "traces resolve, so the implementation stays checkable against this pack.",
        "",
    ]
    return "\n".join(lines)


def _meta(entry: dict) -> str:
    zh = f" ({entry['title_zh']})" if entry.get("title_zh") else ""
    maturity = entry.get("maturity", "L1")
    return (
        f"# {entry['title']}{zh}\n\n"
        f"- source pack: `packs/{_domain_path(entry)}`\n"
        f"- maturity: {maturity}\n"
        f"- verification: {entry.get('verification', 'unverified')}\n"
        f"- version: {entry.get('version', '')}\n"
        f"- stack stance: {entry.get('stack_stance', 'not stated')}\n"
    )


def _domain_path(entry: dict) -> str:
    """Rebuild the pack's source path from its index entry."""
    return f"{entry['domain']}/{entry['slug']}"


# --------------------------------------------------------------------------- #
# Template: implement the pack
# --------------------------------------------------------------------------- #

def implement(entry: dict) -> str:
    """A build brief: what to build, what constrains it, what decided it."""
    counts = entry["counts"]
    parts = [
        _meta(entry),
        "## What you are building",
        "",
        "A working prototype of the system described by this pack. It is a "
        "**blueprint**, so the point is fidelity to the recorded decisions "
        "rather than breadth of features: an implementation that shows the "
        "decision and the constraint beats one that grows a feature the pack "
        "did not specify.",
        "",
        "### Capabilities",
        "",
        _bullets([f"`{c['id']}` {c['name']} — {c['one_liner']}" for c in entry["capabilities"]]),
        "",
        "### Business rules (normative; do not simplify them away)",
        "",
    ]
    for rule in entry["rules"]:
        parts.append(f"- `{rule['id']}` {rule['name']}")
        if rule["proposition"]:
            parts.append(f"  {rule['proposition']}")
        if rule["enforced_by"]:
            parts.append(f"  enforced by: {', '.join(rule['enforced_by'])}")
    parts += ["", "### Decisions already taken (do not relitigate)", ""]
    for adr in entry["adrs"]:
        parts.append(f"- `{adr['id']}` {adr['name']}")
        if adr["decision"]:
            parts.append(f"  decision: {adr['decision']}")
    if entry["adrs"]:
        parts += [
            "",
            "Each ADR file under `04-architecture/adr/` states its options and "
            "consequences. Read the ones your design touches before choosing "
            "an approach; the alternatives were weighed and rejected for "
            "reasons recorded there.",
        ]
    parts += ["", "### Enforced constraints", ""]
    for con in entry["constraints"]:
        where = " **[store-enforced]**" if con["store"] else ""
        parts.append(f"- `constraint {con['n']}`{where} {con['text']}")
        if con["enforces"]:
            parts.append(f"  enforces: {', '.join(con['enforces'])}")
    parts += [
        "",
        "Constraints marked **[store-enforced]** must be impossible to violate "
        "in your implementation, not merely discouraged — they belong in the "
        "schema or the store's own rules, not in application code that a later "
        "change can bypass.",
        "",
        "### Measurable targets",
        "",
    ]
    for nfr in entry["nfrs"]:
        policy = " **(policy — not a measurement)**" if nfr["is_policy"] else ""
        parts.append(f"- `{nfr['id']}` {nfr['name']}{policy}")
        if nfr["target"]:
            parts.append(f"  target: {nfr['target']}")
        if nfr["formula"]:
            parts.append(f"  formula: {nfr['formula']}")
    parts += [
        "",
        "### What to produce",
        "",
        "- A runnable prototype covering the capabilities above, in a single "
        "repository, with the key entities from the domain model.",
        "- The store-enforced constraints implemented as schema or store rules, "
        "with a test that proves each one rejects the violation it names.",
        "- A short report of where your implementation had to *choose* "
        "something the pack left open, so the choice is visible rather than "
        "silent.",
        "",
        "### Scale of the pack",
        "",
        f"{counts['rules']} business rules · {counts['requirements']} functional "
        f"requirements · {counts['nfrs']} measurable targets · "
        f"{counts['controls']} controls · {counts['adrs']} ADRs · "
        f"{counts['constraints']} integrity constraints "
        f"({counts['store_constraints']} store-enforced)",
        "",
        _cond(entry),
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Template: implement one decision
# --------------------------------------------------------------------------- #

def adr(entry: dict, adr_id: str) -> str:
    """A single decision, plus the requirements and rules that carry it."""
    record = next((a for a in entry["adrs"] if a["id"] == adr_id), None)
    if record is None:
        return f"# {adr_id}\n\nNo such ADR in this pack.\n"
    src = f"packs/{_domain_path(entry)}/04-architecture/adr/{record['slug']}.md"
    body = record["decision"] or "(see the ADR file for the decided option)"
    dependents = [
        r for r in entry["requirements"] if adr_id in r["traces"]
    ] or [r for r in entry["rules"] if adr_id in r["trace_adrs"]]
    parts = [
        _meta(entry),
        f"## The decision: `{record['id']}` — {record['name']}",
        "",
        body,
        "",
        "### Ruled out (do not re-derive these)",
        "",
        # The rejected options are the half an implementer most needs: an ADR
        # exists to record what was rule out and why, so a prompt that carries
        # only the winner lets a model re-derive the loser.
        ("Rejected, for reasons recorded in the ADR:\n\n"
         + "\n".join(f"- {r}" for r in record.get("rejected", [])))
        if record.get("rejected")
        else "(alternatives not extracted — read the ADR file)",
        "",
        f"Source: `{src}` — read the Context, Options and Consequences "
        "sections for the reasoning behind each rejection.",
        "",
        "### What depends on it",
        "",
    ]
    if dependents:
        for dep in dependents:
            label = dep.get("name", "")
            parts.append(f"- `{dep['id']}` {label}")
            if dep.get("shall"):
                parts.append(f"  {dep['shall']}")
    else:
        parts.append("- (nothing traces to this ADR in the pack index)")
    parts += [
        "",
        "## Task",
        "",
        "Implement the decision above. The requirements listed are what it "
        "forces, so your implementation should make each of them true rather "
        "than merely compatible with the decision's wording.",
        "",
        "Where the decision trades something away, keep the trade rather than "
        "optimising it out: each consequence was accepted for a recorded "
        "reason, and an implementation that quietly reverses one is harder to "
        "review than one that names the problem.",
        "",
        _cond(entry),
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Template: test one rule
# --------------------------------------------------------------------------- #

def test(entry: dict, rule_id: str) -> str:
    """One rule, the requirements that enforce it, and the targets that measure it."""
    rule = next((r for r in entry["rules"] if r["id"] == rule_id), None)
    if rule is None:
        return f"# {rule_id}\n\nNo such rule in this pack.\n"
    src = f"packs/{_domain_path(entry)}/01-business/business-rules.md"
    parts = [
        _meta(entry),
        f"## The rule: `{rule['id']}` — {rule['name']}",
        "",
        rule["proposition"] or "(see the rule file for the proposition)",
        "",
        f"Source: `{src}`",
        "",
        "### Requirements that enforce it",
        "",
    ]
    related = [q for q in entry["requirements"] if rule["id"] in q["traces"]]
    if related:
        for q in related:
            parts.append(f"- `{q['id']}` {q['name']}")
            if q["when"]:
                parts.append(f"  WHEN {q['when']}")
            if q["shall"]:
                parts.append(f"  SHALL {q['shall']}")
            if q["shall_not"]:
                parts.append(f"  SHALL NOT {q['shall_not']}")
    else:
        parts.append("- (no requirement traces to this rule in the pack index)")
    parts += ["", "### Targets that measure it", ""]
    measured = [
        n for n in entry["nfrs"]
        if rule["id"] in " ".join(n.get("traces", [])) or any(
            rule["id"] in c.get("enforces", []) for c in entry["constraints"]
        )
    ] or [n for n in entry["nfrs"] if rule["id"] in (n.get("name", "") + n.get("target", ""))]
    if measured:
        for n in measured:
            policy = " **(policy — not a measurement)**" if n["is_policy"] else ""
            parts.append(f"- `{n['id']}` {n['name']}{policy}")
            if n["formula"]:
                parts.append(f"  formula: {n['formula']}")
    else:
        parts.append("- (nothing measures this rule directly)")
    parts += [
        "",
        "## Task",
        "",
        "Write tests that fail when this rule is violated. For each test:",
        "",
        "1. Name the identifier from this pack it protects.",
        "2. Arrange the state the rule's precondition describes.",
        "3. Assert the consequence, including the prohibition — the "
        "`SHALL NOT` half is the half that fails first in a real system.",
        "",
        "A test that only exercises the happy path does not test this rule; the "
        "rule exists to reject something specific.",
        "",
        _cond(entry),
    ]
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# Template: the whole pack as context
# --------------------------------------------------------------------------- #

def context_bundle(entry: dict, pack_dir: Path) -> str:
    """The pack's own chapters, concatenated — for a model needing the source."""
    parts = [
        _meta(entry),
        "This bundle is the pack itself. Read it before implementing anything "
        "from this repository: the decisions and their consequences are in the "
        "ADR files, the normative propositions are in the business rules, and "
        "the conditions at the end apply to whatever you produce.",
        "",
        _cond(entry),
        "---",
        "",
    ]
    for rel in CONTEXT_CHAPTERS:
        path = pack_dir / rel
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
        path = pack_dir / "04-architecture" / "adr" / f"{adr['slug']}.md"
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        parts.append(f"\n## ===== 04-architecture/adr/{adr['slug']}.md =====\n\n{text.rstrip()}\n")
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


def build_bundles(entry: dict, pack_dir: Path) -> dict:
    """Everything a page needs to offer: inline prompts and emitted files.

    The per-identifier variants (one ADR, one rule) are generated for the
    handful that matter most — the pack's ADRs and its load-bearing rules —
    rather than for every combination, which would be thousands of files.
    """
    inline = {
        "implement": implement(entry),
        "adr": [{"id": a["id"], "label": a["name"], "text": adr(entry, a["id"])}
                for a in entry["adrs"]],
        "test": [{"id": r["id"], "label": r["name"], "text": test(entry, r["id"])}
                 for r in entry["rules"][:8]],
    }
    files = {
        "context.md": context_bundle(entry, pack_dir),
        "implement.md": inline["implement"],
    }
    for item in inline["adr"]:
        files[bundle_filename("adr", item["id"])] = item["text"]
    for item in inline["test"]:
        files[bundle_filename("test", item["id"])] = item["text"]
    return {"inline": inline, "files": files}

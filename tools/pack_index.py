#!/usr/bin/env python3
"""pack_index.py — extract the machine-readable core of every pack.

The pack documents are written to be read. This module reads them again as
*data*: it turns ``BR-01 …``, ``FR-001 …`` and the numbered integrity
constraints into a JSON structure that a page, a prompt bundle or a code
generator can consume without re-parsing prose.

What it emits for one pack::

    capabilities[].{id,name,one_liner,what}
    rules[].{id,name,enforced_by,trace_adrs,proposition}
    requirements[].{id,name,when,shall,shall_not,traces}
    nfrs[].{id,name,target,formula,rationale,is_policy}
    controls[].{id,name,instruments[],capabilities[],rules[],requirements[]}
    adrs[].{id,name,decision,url}
    constraints[].{n,text,enforces[],store}
    contexts[].{name,responsibility,owns[]}
    sections = {name: {status, count}}     <- see "Extraction quality" below
    demo = None | {title, demonstrates[], entry, url}

Extraction quality, and why it is reported rather than hidden
-------------------------------------------------------------
The 17 packs were written across several batches and do **not** share one ID
convention. Three are in active use:

    rules    `### BR-01 — Proposition`      L2 packs
             `**BR-01 Name** (parameterized)`  L3 packs, under a `## Topic`
             `| BR-01 | rule | rationale |`    ITSM-style table
    FR/NFR   `### FR-001 — name` + WHEN/SHALL/Traces bullets   L2 packs
             `- **FR-001** WHEN … THE SYSTEM SHALL …`         L3 packs, inline
    CAP      `| **CAP-01** |`  or  `| **01** |`

A parser that silently returns ``[]`` for the forms it does not know would
report *zero rules* for a pack that has fifteen — and a page built on that
would state a falsehood about the corpus. So each section also reports a
status:

    structured   the IDs and their fields were extracted
    prose-only   the file exists and mentions IDs, but not in a shape this
                 extractor can decompose; the count is the **lower bound**
    absent       the file does not exist

``prose-only`` is a content backlog made visible, not a defect to paper over.
Every pack's section status is surfaced on the site, so "this pack's rules are
not yet machine-readable" is a fact a reader can act on.

The ``store`` flag on a constraint is **derived, not asserted**: every
``05-data/logical-data-model.md`` closes with a sentence naming which numbered
constraints are enforced in the store rather than in application code. Those
numbers are parsed out of the sentence, which means the flag is only as good
as the sentence — so it is presented as *claimed*, never as verified.

Usage:  python tools/pack_index.py [--out FILE]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required (pip install -r requirements.txt)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"

# --------------------------------------------------------------------------- #
# Identifiers
# --------------------------------------------------------------------------- #

# An ID may carry a letter suffix (`BR-03a`), which some packs use for a
# sub-rule of its parent. Tolerated rather than dropped, because dropping one
# silently would report a rule count that the pack itself contradicts.
ID_RE = re.compile(r"\b((?:CAP|BR|FR|NFR|CTL|ADR)-\d+[a-z]?)\b")

RULE_HEADING_RE = re.compile(r"^###\s+(BR-\d+[a-z]?)\s*[\u2014\u2013-]\s*([^\n]*)")
RULE_BOLD_RE = re.compile(r"^\*\*(BR-\d+[a-z]?)\s+([^*]+?)\*\*(.*)$")
REQ_HEADING_RE = re.compile(r"^###\s+(FR-\d+[a-z]?)\s*[\u2014\u2013-]\s*([^\n]*)")
REQ_INLINE_RE = re.compile(r"^-\s*\*\*(FR-\d+[a-z]?)\*\*\s*(.*)$")
NFR_HEADING_RE = re.compile(r"^##\s+(NFR-\d+[a-z]?)\s*[\u2014\u2013-]\s*([^\n]*)")
NFR_INLINE_RE = re.compile(r"^-\s*\*\*(NFR-\d+[a-z]?)\b([^*]*)\*\*\s*(.*)$")
ENFORCED_BY_RE = re.compile(r"\*\(enforced by (.*?)(?:;|\)\*)")


def _clean(text: str) -> str:
    """Collapse Markdown emphasis so a value renders the same everywhere.

    Underscores are **not** stripped: `DEFINITION_VERSION` and
    `task_available_ts` are identifiers, and removing the underscores turns
    them into something no reader recognises. Markdown italic by underscore
    is rare in this corpus and the identifier case is common, so the trade
    goes the other way.
    """
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"[*`]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _row_cells(line: str) -> list[str]:
    """Unwrap a Markdown table row into its cells, never the outer pipes."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    return [c.strip() for c in stripped.split("|")[1:-1]]


def _flat(text: str) -> str:
    """Markdown with blockquote markers, emphasis and line wraps removed.

    Needed because a sentence can be **wrapped mid-phrase** by the source's
    line width — ``are **enforced in the\\n> store**`` — and a regex over the
    raw text never sees the phrase it is looking for.
    """
    return re.sub(r"\s+", " ", text.replace(">", " ").replace("*", " "))


def doc_url(rel_path: str) -> str:
    """Source Markdown path -> site-relative URL.

    The mapping is a property of the content model; ``tools/build-site.py``
    imports it from here rather than keeping a second copy that could drift.
    """
    rel = rel_path.replace("\\", "/")
    if rel.endswith("README.md"):
        return rel[: -len("README.md")] + "index.html"
    return rel[:-3] + ".html" if rel.endswith(".md") else rel


def _status(count: int, text: str) -> str:
    """Structured / prose-only / absent, from what the parse actually found."""
    if count:
        return "structured"
    return "prose-only" if ID_RE.search(text) else "absent"


# --------------------------------------------------------------------------- #
# Capabilities
# --------------------------------------------------------------------------- #

def parse_capabilities(text: str) -> list[dict]:
    """`| **CAP-01** | **Name** | one-liner | what |`, or `| **01** | … |`.

    Some packs label the capability column with the bare number, so the ID is
    normalised to `CAP-nn` in both cases.
    """
    out: list[dict] = []
    for line in text.splitlines():
        cells = _row_cells(line)
        if len(cells) < 3:
            continue
        head = cells[0]
        m = re.match(r"^\*\*(CAP-\d+)\*\*$", head) or re.match(r"^\*\*(\d{1,2})\*\*$", head)
        if not m:
            continue
        cap_id = m.group(1) if m.group(1).startswith("CAP-") else f"CAP-{int(m.group(1)):02d}"
        out.append({
            "id": cap_id,
            "name": _clean(cells[1]),
            "one_liner": _clean(cells[2]),
            "what": _clean(cells[3]) if len(cells) > 3 else "",
        })
    return out


# --------------------------------------------------------------------------- #
# Rules — three conventions
# --------------------------------------------------------------------------- #

def _enforced_by(lines: list[str], start: int) -> tuple[list[str], list[str]]:
    """The `*(enforced by FR-…, ADR-…; violated when …)*` line under a rule."""
    for raw in lines[start : start + 6]:
        m = ENFORCED_BY_RE.search(raw)
        if not m:
            continue
        ids = ID_RE.findall(m.group(1))
        return (
            [i for i in ids if not i.startswith("ADR-")],
            [i for i in ids if i.startswith("ADR-")],
        )
    return [], []


def _first_paragraph(lines: list[str]) -> str:
    """First prose block after a heading: the rule's proposition."""
    buf: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            if buf:
                break
            continue
        if line.startswith(("#", "|", ">", "```", "- ", "* ", "<!--")) or ENFORCED_BY_RE.search(line):
            break
        buf.append(line)
        if len(" ".join(buf)) > 400:
            break
    return _clean(" ".join(buf))[:400]


def parse_rules(text: str) -> list[dict]:
    """Rules in any of the three conventions, de-duplicated by ID."""
    lines = text.splitlines()
    parsed: dict[str, dict] = {}
    for i, line in enumerate(lines):
        hit = None
        # --- convention 1: `### BR-01 — Proposition` ------------------------
        m = RULE_HEADING_RE.match(line)
        if m:
            hit = (m.group(1), _clean(m.group(2)), _first_paragraph(lines[i + 1 :]))
        if hit is None:
            # --- convention 2: `**BR-01 Name** (parameterized)` -------------
            m = RULE_BOLD_RE.match(line)
            if m:
                hit = (m.group(1), _clean(m.group(2)), _first_paragraph(lines[i + 1 :]))
        if hit is None:
            # --- convention 3: a table `| BR-01 | rule | rationale |` -------
            cells = _row_cells(line)
            if len(cells) >= 2 and re.match(r"^BR-\d+[a-z]?$", cells[0]):
                hit = (cells[0], _clean(cells[1]), _clean(cells[2]) if len(cells) > 2 else "")
        if hit is None:
            continue
        rid, name, body = hit
        req, adrs = _enforced_by(lines, i + 1)
        if rid in parsed:  # a rule stated twice: keep the richer record
            if not parsed[rid]["proposition"] and body:
                parsed[rid]["proposition"] = body
            continue
        parsed[rid] = {
            "id": rid,
            "name": name,
            "enforced_by": req,
            "trace_adrs": adrs,
            "proposition": body,
        }
    def _key(rid: str) -> tuple[int, str]:
        num, _, suf = rid[3:].partition("a") if rid[3].isdigit() else ("0", "", "")
        return (int(num.split("a")[0]), suf)
    return sorted(parsed.values(), key=lambda r: _key(r["id"]))


# --------------------------------------------------------------------------- #
# Requirements — two conventions
# --------------------------------------------------------------------------- #

def _ears(block: str) -> tuple[str, str, str]:
    """Split an EARS statement into its WHEN / SHALL / SHALL NOT parts.

    The ``SHALL NOT`` clause is the half of an EARS requirement that carries
    the prohibition, so it is split out rather than left buried in the middle
    of a sentence.
    """
    when = re.search(r"\*\*WHEN\*\*\s*(.+?)(?=\n\s*-\s*(?:\*\*|\w)|\n\n|\Z)", block, re.DOTALL)
    shall = re.search(r"\*\*THE SYSTEM SHALL\*\*\s*(.+?)(?=\n\s*-\s*(?:\*\*|\w)|\n\n|\Z)", block, re.DOTALL)
    shall_text = _clean(shall.group(1)) if shall else ""
    if not shall_text:
        # Convention 2 writes the whole statement inline, without the markers:
        # `- **FR-001** WHEN a subject is created, THE SYSTEM SHALL enforce …`.
        inline = re.search(r"WHEN\b(.+?),\s*THE SYSTEM SHALL\b\s*(.+?)(?:\n|$)", block, re.DOTALL)
        if inline:
            return _clean(inline.group(1)), _clean(inline.group(2)), ""
    not_m = re.search(r"\bSHALL NOT\b\s*(.+)$", shall_text)
    return (
        _clean(when.group(1)) if when else "",
        # The prohibition is rendered on its own line, so it is cut out of
        # `shall` here rather than shown twice.
        _clean(shall_text[: not_m.start()].rstrip(" ,;")) if not_m else shall_text,
        _clean(not_m.group(1)) if not_m else "",
    )


def parse_requirements(text: str) -> list[dict]:
    parsed: dict[str, dict] = {}
    for block in re.split(r"^###\s+", text, flags=re.MULTILINE)[1:]:
        # `re.split` consumes the delimiter, so it is restored before matching.
        m = REQ_HEADING_RE.match("### " + block)
        if not m:
            continue
        rid, name = m.group(1), _clean(m.group(2))
        when, shall, shall_not = _ears(block)
        traces = re.search(r"Traces:\s*(.+)", block)
        parsed[rid] = {
            "id": rid, "name": name, "when": when,
            "shall": shall, "shall_not": shall_not,
            "traces": ID_RE.findall(traces.group(1)) if traces else [],
        }
    if parsed:
        return sorted(parsed.values(), key=lambda r: int(r["id"][3:].rstrip("a-z") or 0))
    # Convention 2: nothing heading-shaped, so look for the inline bullets.
    for line in text.splitlines():
        m = REQ_INLINE_RE.match(line)
        if not m:
            continue
        rid = m.group(1)
        when, shall, shall_not = _ears(line)
        parsed[rid] = {
            "id": rid,
            "name": _clean(re.sub(r"^WHEN\b", "", m.group(2)))[:80],
            "when": when, "shall": shall, "shall_not": shall_not,
            "traces": [i for i in ID_RE.findall(line) if i != rid],
        }
    return sorted(parsed.values(), key=lambda r: int(r["id"][3:].rstrip("a-z") or 0))


# --------------------------------------------------------------------------- #
# NFRs — two conventions
# --------------------------------------------------------------------------- #

def parse_nfrs(text: str) -> list[dict]:
    out: list[dict] = []
    for block in re.split(r"^##\s+", text, flags=re.MULTILINE)[1:]:
        # `re.split` consumes the delimiter, so it is restored before matching.
        m = NFR_HEADING_RE.match("## " + block)
        if not m:
            continue
        label = re.search(r"\*\*Target(\s*\(A\))?\*\*:?", block)
        target = re.search(r"\*\*Target(?:\s*\(A\))?\*\*:?\s*(.+?)(?=\n\s*-\s*\*\*|\n\n|\Z)", block, re.DOTALL)
        formula = re.search(r"\*\*Formula\*\*:?\s*(.+?)(?=\n\s*-\s*\*\*|\n\n|\Z)", block, re.DOTALL)
        rationale = re.search(r"\*\*Rationale\*\*:?\s*(.+?)(?=\n\s*-\s*\*\*|\n\n|\Z)", block, re.DOTALL)
        target_text = _clean(target.group(1)) if target else ""
        out.append({
            "id": m.group(1),
            "name": _clean(m.group(2)),
            "target": target_text,
            # `(A)` marks a number as a policy assumption, never a fact. The
            # marker is on the label (`- **Target (A)**:`), so it is read
            # from the label rather than from the value it qualifies.
            "is_policy": bool(label and label.group(1)) or "(A)" in target_text,
            "formula": _clean(formula.group(1)) if formula else "",
            "rationale": _clean(rationale.group(1)) if rationale else "",
        })
    if out:
        return sorted(out, key=lambda n: int(n["id"][4:].rstrip("a-z") or 0))
    # Convention 2: `- **NFR-001 (Topic)** statement`.
    for line in text.splitlines():
        m = NFR_INLINE_RE.match(line)
        if not m:
            continue
        body = _clean(m.group(3))
        out.append({
            "id": m.group(1),
            "name": _clean(m.group(2).strip("()")),
            "target": body[:300],
            "is_policy": "(A)" in body,
            "formula": "",
            "rationale": "",
        })
    if out:
        return sorted(out, key=lambda n: int(n["id"][4:].rstrip("a-z") or 0))
    # Convention 3: a table `| NFR-001 | name | target |`.
    for line in text.splitlines():
        cells = _row_cells(line)
        if len(cells) < 3 or not re.match(r"^NFR-\d+[a-z]?$", cells[0]):
            continue
        body = _clean(cells[2])
        out.append({
            "id": cells[0],
            "name": _clean(cells[1]),
            "target": body[:300],
            "is_policy": bool(re.search(r"\(A\)", body)),
            "formula": "",
            "rationale": "",
        })
    return sorted(out, key=lambda n: int(n["id"][4:].rstrip("a-z") or 0))


# --------------------------------------------------------------------------- #
# Controls
# --------------------------------------------------------------------------- #

def parse_controls(text: str) -> list[dict]:
    """A control matrix in either of the two layouts in use.

    The L2 layout is five columns — ``| **CTL-01** — name | instrument | CAP |
    BR | FR |`` — which separates the trace by kind. The L3 layout is four —
    ``| **CTL-01** | control | mechanism | trace |`` — with one mixed trace
    column. Both give an ID, a name and the IDs it traces to; the second
    simply cannot say *which kind* each trace is, so the triples stay empty
    there rather than being guessed at.
    """
    out: list[dict] = []
    for line in text.splitlines():
        cells = _row_cells(line)
        if len(cells) < 4 or "**CTL-" not in cells[0]:
            continue
        m = re.match(r"\*\*(CTL-\d+)\*\*\s*[\u2014\u2013-]\s*(.+)", cells[0])
        if m:
            name, tail = _clean(m.group(2)), cells[1:]
        else:
            m = re.match(r"\*\*(CTL-\d+)\*\*$", cells[0])
            if not m:
                continue
            name, tail = _clean(cells[1]), cells[2:]
        if len(tail) >= 4:
            instruments, caps, rules, reqs = (
                re.findall(r"`([^`]+)`", tail[0]),
                ID_RE.findall(tail[1]),
                ID_RE.findall(tail[2]),
                ID_RE.findall(tail[3]),
            )
            instrument_names = _clean(re.sub(r"\(`[^`]+`\)", "", tail[0]))
        else:
            instruments, caps, rules, reqs = [], [], [], ID_RE.findall(tail[-1])
            instrument_names = ""
        out.append({
            "id": m.group(1), "name": name,
            "instruments": instruments, "instrument_names": instrument_names,
            "capabilities": caps, "rules": rules, "requirements": reqs,
        })
    return out


# --------------------------------------------------------------------------- #
# Constraints — including which are claimed to be store-enforced
# --------------------------------------------------------------------------- #

def parse_store_claimed(text: str) -> set[int]:
    r"""Which numbered constraints the data model claims are store-enforced.

    The sentence is prose — ``Constraints 1, 4, 7 and 10 are enforced in the
    store`` — and it is routinely wrapped mid-phrase, so it is flattened
    first. This parses numbers *out of a claim*, which is why the resulting
    flag is presented as claimed rather than verified.

    The clause is matched with a negated character class rather than a
    structure like ``(?:\d+\s*(?:,|and)?\s*)+?``: the nested quantifiers of
    that form backtrack exponentially on a long digit run, and CodeQL flagged
    it on this repository. The numbers are then pulled out of the clause by a
    separate, unambiguous ``\d+`` scan.
    """
    flat = _flat(text)
    m = re.search(
        r"Constraints?\s+([^.;:]+?)\s+(?:are|is)\s+enforced\s+in\s+the\s+store", flat
    )
    if not m:
        return set()
    return {int(n) for n in re.findall(r"\d+", m.group(1))}


def parse_constraints(text: str) -> list[dict]:
    store = parse_store_claimed(text)
    out: list[dict] = []
    for line in text.splitlines():
        cells = _row_cells(line)
        if len(cells) < 3:
            continue
        m = re.match(r"^(\d+)$", cells[0])
        if not m:
            continue
        out.append({
            "n": int(m.group(1)),
            "text": _clean(cells[1]),
            "enforces": ID_RE.findall(cells[2]),
            "store": int(m.group(1)) in store,
        })
    return out


# --------------------------------------------------------------------------- #
# Bounded contexts
# --------------------------------------------------------------------------- #

def parse_contexts(text: str) -> list[dict]:
    """`| **Runtime** | responsibility | ProcessInstance, Token |` rows."""
    out: list[dict] = []
    for line in text.splitlines():
        cells = _row_cells(line)
        if len(cells) < 3 or "**" not in cells[0]:
            continue
        name = _clean(cells[0].replace("**", ""))
        if not name or len(name) > 40 or name.lower() in ("context", "name"):
            continue
        owns = [o.strip() for o in re.split(r"[,/]", _clean(cells[2])) if o.strip()]
        # A context row owns CamelCase aggregates; a capability row does not.
        if not owns or not all(re.match(r"^[A-Z][A-Za-z0-9]+$", o) for o in owns):
            continue
        out.append({"name": name, "responsibility": _clean(cells[1]), "owns": owns})
    return out


# --------------------------------------------------------------------------- #
# ADRs and the optional demo manifest
# --------------------------------------------------------------------------- #

def parse_adr(path: Path, pack_rel: str) -> dict | None:
    """An ADR file -> id, name, and the first sentence of its Decision.

    The Decision section is read rather than the status block, because the
    decision is what a reader needs and the status is visible on the page.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    head = re.search(r"^#\s+(ADR-\d+)\s*[\u2014\u2013-]\s*(.+)$", text, re.MULTILINE)
    if not head:
        return None
    dec = re.search(
        r"^##\s+Decision\s*\n+(.+?)(?:\n\n|^#)", text, re.MULTILINE | re.DOTALL
    )
    decision = _clean(dec.group(1).strip()) if dec else ""
    return {
        "id": head.group(1),
        "name": _clean(head.group(2)),
        # Kept verbatim rather than stripped of its `Option N,` prefix: the
        # prefix is what says *which* of the listed options was chosen, and
        # without it the sentence opens on a stray "enforced by …".
        "decision": decision[:320],
        # The rejected options are the half an implementer most needs, because
        # the point of an ADR is what was ruled out and why.
        "rejected": _rejected_options(text),
        # kept so a prompt bundle can cite the source file by path
        "slug": path.stem,
        "url": doc_url(f"{pack_rel}/04-architecture/adr/{path.stem}.md"),
    }


def _rejected_options(text: str) -> list[str]:
    """The option headings from an ADR's `## Options considered` section."""
    section = re.search(r"##\s+Options considered\n(.*?)(?:\n##\s|\Z)", text, re.DOTALL)
    if not section:
        return []
    return [
        _clean(m.group(1))
        for m in re.finditer(r"^\s*\d+[.)]\s*\*\*(.+?)\*\*", section.group(1), re.MULTILINE)
    ]


def parse_demo(pack_dir: Path) -> dict | None:
    """An optional ``10-demo/demo.json`` declaring what the demo demonstrates.

    The demo page itself is hand-written per pack — bespoke, because a
    generated one would demonstrate the engine rather than the pack. This
    manifest is the machine-readable half, and the half that matters:
    ``demonstrates`` is what ``check-ids.py`` validates, so a demo whose ADR
    was renumbered or whose rule was deleted fails the build instead of
    quietly demonstrating a decision that no longer exists.
    """
    path = pack_dir / "10-demo" / "demo.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    entry = str(data.get("entry", "index.html")).strip() or "index.html"
    return {
        "title": str(data.get("title", "")).strip(),
        "summary": str(data.get("summary", "")).strip(),
        "kind": str(data.get("kind", "")).strip(),
        "entry": entry,
        "demonstrates": [str(i) for i in (data.get("demonstrates") or [])],
        "url": f"{pack_dir.relative_to(ROOT).as_posix()}/demo/{entry}",
    }


# --------------------------------------------------------------------------- #
# Pack extraction
# --------------------------------------------------------------------------- #

SECTIONS = (
    ("capabilities", "01-business/capability-map.md"),
    ("rules", "01-business/business-rules.md"),
    ("requirements", "02-requirements/functional.md"),
    ("nfrs", "02-requirements/non-functional.md"),
    ("controls", "02-requirements/compliance.md"),
    ("constraints", "05-data/logical-data-model.md"),
)


def _read(pack_dir: Path, rel: str) -> str:
    path = pack_dir / rel
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def extract(pack_dir: Path) -> dict | None:
    """One pack directory -> its index entry, or None if it is not a pack."""
    manifest_path = pack_dir / "manifest.yaml"
    if not manifest_path.is_file():
        return None
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(manifest, dict):
        return None

    slug = str(manifest.get("slug", pack_dir.name))
    pack_rel = pack_dir.relative_to(ROOT).as_posix()

    parsed: dict[str, list] = {
        "capabilities": parse_capabilities(_read(pack_dir, "01-business/capability-map.md")),
        "rules": parse_rules(_read(pack_dir, "01-business/business-rules.md")),
        "requirements": parse_requirements(_read(pack_dir, "02-requirements/functional.md")),
        "nfrs": parse_nfrs(_read(pack_dir, "02-requirements/non-functional.md")),
        "controls": parse_controls(_read(pack_dir, "02-requirements/compliance.md")),
        "constraints": parse_constraints(_read(pack_dir, "05-data/logical-data-model.md")),
    }
    contexts = parse_contexts(_read(pack_dir, "03-domain/domain-model.md"))

    adr_dir = pack_dir / "04-architecture" / "adr"
    adrs = [a for a in (parse_adr(p, pack_rel) for p in sorted(adr_dir.glob("*.md"))) if a]

    # Extraction quality is recorded per section rather than assumed.
    sections: dict[str, dict] = {}
    for key, rel in SECTIONS:
        text = _read(pack_dir, rel)
        sections[key] = {
            "status": _status(len(parsed[key]), text),
            "count": len(parsed[key]),
        }
    sections["adrs"] = {"status": "structured" if adrs else "absent", "count": len(adrs)}

    demo = parse_demo(pack_dir)
    counts = {
        "capabilities": len(parsed["capabilities"]),
        "rules": len(parsed["rules"]),
        "requirements": len(parsed["requirements"]),
        "nfrs": len(parsed["nfrs"]),
        "controls": len(parsed["controls"]),
        "adrs": len(adrs),
        "constraints": len(parsed["constraints"]),
        "store_constraints": sum(1 for c in parsed["constraints"] if c["store"]),
        "policy_nfrs": sum(1 for n in parsed["nfrs"] if n["is_policy"]),
        "contexts": len(contexts),
    }
    return {
        "slug": slug,
        "domain": str(manifest.get("domain", pack_dir.parent.name)),
        "subdomain": str(manifest.get("subdomain", "")),
        "title": str(manifest.get("title", slug)),
        "title_zh": str(manifest.get("title_zh", "")),
        "maturity": str(manifest.get("maturity", "L1")),
        "verification": str(manifest.get("verification", "unverified")),
        "version": str(manifest.get("version", "")),
        "stack_stance": str(manifest.get("stack_stance", "")),
        "tags": [str(t) for t in (manifest.get("tags") or [])],
        "url": doc_url(f"{pack_rel}/README.md"),
        "doc_urls": {
            key: doc_url(f"{pack_rel}/{rel}") for key, rel in SECTIONS[:5]
        } | {"domain_model": doc_url(f"{pack_rel}/03-domain/domain-model.md"),
             "data_model": doc_url(f"{pack_rel}/05-data/logical-data-model.md")},
        "contexts": contexts,
        "adrs": adrs,
        "demo": demo,
        "sections": sections,
        "counts": counts,
        **parsed,
    }


def build_index() -> dict:
    """Extract every pack, then add the cross-pack lookups."""
    packs = [
        entry
        for p in sorted(PACKS_DIR.glob("*/*/manifest.yaml"))
        if (entry := extract(p.parent)) is not None
    ]
    packs.sort(key=lambda p: (p["domain"], p["slug"]))
    return {
        "generated_by": "tools/pack_index.py",
        "pack_count": len(packs),
        "packs": packs,
        "totals": {
            k: sum(p["counts"][k] for p in packs)
            for k in (
                "capabilities", "rules", "requirements", "nfrs", "controls",
                "adrs", "constraints", "store_constraints", "policy_nfrs",
            )
        },
        # How much of the corpus a machine can actually read. Reported, not
        # optimised for: an honest 6/17 is more useful than a flattering 12/17.
        "extraction": {
            "sections": {
                key: {
                    "structured": sum(1 for p in packs if p["sections"][key]["status"] == "structured"),
                    "prose_only": sum(1 for p in packs if p["sections"][key]["status"] == "prose-only"),
                    "absent": sum(1 for p in packs if p["sections"][key]["status"] == "absent"),
                }
                for key, _ in SECTIONS
            },
            "adrs": {
                "structured": sum(1 for p in packs if p["adrs"]),
                "absent": sum(1 for p in packs if not p["adrs"]),
            },
            "demos": sum(1 for p in packs if p["demo"]),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", help="write the JSON index here (default: stdout)")
    args = ap.parse_args()

    index = build_index()
    text = json.dumps(index, ensure_ascii=False, indent=1)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"indexed {index['pack_count']} packs: "
              + ", ".join(f"{v} {k}" for k, v in index["totals"].items()))
    else:
        # Windows consoles default to a legacy code page, so JSON written to
        # stdout raises before the reader ever sees it.
        sys.stdout.buffer.write(text.encode("utf-8") + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

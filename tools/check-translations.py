#!/usr/bin/env python3
"""check-translations.py - the Chinese corpus is complete, and it is faithful.

A translation is a *sibling* of the file it translates:
``01-business/business-rules.zh-CN.md`` beside ``business-rules.md``. The
Chinese build renders the sibling in place of the original, at the original's
URL, so a missing translation is not a missing page: it is a page that
silently stays English. This tool is what makes that visible.

Three questions, and each has a different failure mode:

1. **Is it there?** Every translatable file has a Chinese counterpart.
2. **Is it the same document?** A translation that drops a rule, loses a
   table row, renumbers an identifier or loses a code block is not a
   translation - it is a different, smaller document wearing the original's
   name. Structure is compared, not prose.
3. **Is it translated?** A line that is still English is an untranslated
   line. The check is a heuristic and says so: it looks for a *sentence* of
   ASCII words with no Chinese in it, which is what an untranslated line
   looks like, and it ignores code, URLs, identifiers and short tokens.

Usage:
    python tools/check-translations.py            # report
    python tools/check-translations.py --strict   # warnings become errors

Exit: 0 = complete; 1 = a file is missing, unfaithful or untranslated.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"
LOCALE = "zh-CN"
SUFFIX = f".{LOCALE}.md"

#: Identifiers whose numbers must survive translation unchanged.
ID_RE = re.compile(r"\b((?:CAP|BR|FR|NFR|CTL|ADR|AC|SM|T|P|I|F|C|BC|E)-\d+[a-z]?)\b")
#: A sentence-like run of ASCII words. Five words is the shortest run that
#: distinguishes "prose that was not translated" from a product name, a
#: regulation id, or a file path.
PROSE_RE = re.compile(r"(?:[A-Za-z][A-Za-z'-]*[ ,.]){4,}[A-Za-z]")
#: Lines that are structure rather than prose.
FENCE_RE = re.compile(r"^\s*```")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
HTML_COMMENT_RE = re.compile(r"^\s*<!--.*-->\s*$")
#: A link whose text is a path, a url or a bare identifier.
ONLY_LINK_RE = re.compile(r"^\s*\[[^\]]*\]\([^)]*\)\s*$")


def translatable_files(pack_dir: Path) -> list[Path]:
    """The files of a pack that a reader reads, and so that need a translation.

    `AGENTS.md` is included: it is the entry point for a Chinese-speaking
    coding agent, so it is content, not scaffolding.
    """
    out = []
    for path in sorted(pack_dir.rglob("*.md")):
        if path.name.endswith(SUFFIX):
            continue
        if "translations" in path.relative_to(pack_dir).parts:
            continue
        out.append(path)
    return out


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def structure(text: str) -> dict:
    """The shape of a document: what must survive translation."""
    fences = 0
    headings: list[int] = []
    table_rows = 0
    list_items = 0
    in_code = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_code = not in_code
            fences += 1
            continue
        if in_code:
            continue
        if line.startswith("#"):
            headings.append(len(line) - len(line.lstrip("#")))
        elif line.strip().startswith("|"):
            if not TABLE_SEP_RE.match(line):
                table_rows += 1
        elif re.match(r"^\s*([-*+]|\d+\.)\s+", line):
            list_items += 1
    return {
        "fences": fences,
        "headings": headings,
        "table_rows": table_rows,
        "list_items": list_items,
        "ids": sorted(set(ID_RE.findall(text))),
    }


def untranslated_lines(text: str) -> list[tuple[int, str]]:
    """Lines that still read as English prose."""
    hits: list[tuple[int, str]] = []
    in_code = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if TABLE_SEP_RE.match(line) or HTML_COMMENT_RE.match(line):
            continue
        if ONLY_LINK_RE.match(line):
            continue
        # Code spans, urls and identifiers are not prose and are not
        # translated; removing them keeps the check about the sentence.
        probe = re.sub(r"`[^`]*`", " ", stripped)
        probe = re.sub(r"https?://\S+", " ", probe)
        probe = ID_RE.sub(" ", probe)
        probe = re.sub(r"\b[A-Z]{2,}[A-Z0-9-]*\b", " ", probe)
        probe = re.sub(r"[*_`>#\[\]()|]", " ", probe)
        if not PROSE_RE.search(probe):
            continue
        if re.search(r"[\u4e00-\u9fff]", probe):
            continue
        hits.append((number, stripped))
    return hits


def compare(source: Path, translation: Path) -> list[str]:
    """The ways a translation can betray the document it claims to translate."""
    problems: list[str] = []
    src = read(source)
    dst = read(translation)
    a, b = structure(src), structure(dst)

    if a["fences"] != b["fences"]:
        problems.append(f"code blocks: {a['fences']} -> {b['fences']}")
    if len(a["headings"]) != len(b["headings"]):
        problems.append(f"headings: {len(a['headings'])} -> {len(b['headings'])}")
    elif a["headings"] != b["headings"]:
        problems.append("heading levels differ")
    if a["table_rows"] != b["table_rows"]:
        problems.append(f"table rows: {a['table_rows']} -> {b['table_rows']}")
    if a["list_items"] != b["list_items"]:
        problems.append(f"list items: {a['list_items']} -> {b['list_items']}")
    if a["ids"] != b["ids"]:
        missing = sorted(set(a["ids"]) - set(b["ids"]))
        added = sorted(set(b["ids"]) - set(a["ids"]))
        if missing:
            problems.append(f"identifiers lost: {', '.join(missing)}")
        if added:
            problems.append(f"identifiers invented: {', '.join(added)}")

    # A replacement character means the text was corrupted in transit, not
    # that it is untranslated. It must never ship.
    if "\ufffd" in dst:
        broken = [i for i, line in enumerate(dst.splitlines(), 1) if "\ufffd" in line]
        problems.append(f"corrupt text (U+FFFD) on line(s) {', '.join(map(str, broken[:5]))}")

    for number, line in untranslated_lines(dst):
        problems.append(f"line {number} is not translated: {line[:90]}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="treat untranslated lines as errors, not warnings")
    args = parser.parse_args()

    pack_dirs = sorted(
        d for d in PACKS_DIR.glob("*/*")
        if d.is_dir() and (d / "manifest.yaml").exists()
    )
    if not pack_dirs:
        print("ERROR: no packs found", file=sys.stderr)
        return 1

    total = done = 0
    missing: list[str] = []
    unfaithful: list[str] = []
    untranslated: list[str] = []

    for pack_dir in pack_dirs:
        pack_id = f"packs/{pack_dir.parent.name}/{pack_dir.name}"
        files = translatable_files(pack_dir)
        pack_done = 0
        for source in files:
            total += 1
            translation = source.with_name(source.stem + SUFFIX)
            if not translation.is_file():
                missing.append(f"{pack_id}/{source.relative_to(pack_dir).as_posix()}")
                continue
            done += 1
            pack_done += 1
            problems = compare(source, translation)
            hard = [p for p in problems if not p.startswith("line ")]
            soft = [p for p in problems if p.startswith("line ")]
            if hard:
                unfaithful.append(f"{pack_id}/{translation.relative_to(pack_dir).as_posix()}: "
                                  + "; ".join(hard))
            if soft:
                untranslated.append(f"{pack_id}/{translation.relative_to(pack_dir).as_posix()}: "
                                    + "; ".join(p[:120] for p in soft[:3]))
        print(f"  {pack_done:3d}/{len(files):3d}  {pack_id}")

    print()
    print(f"translated: {done}/{total} files ({done / total * 100:.1f}%)")
    if missing:
        print(f"\nmissing translations ({len(missing)}):")
        for item in missing[:40]:
            print(f"  {item}")
        if len(missing) > 40:
            print(f"  ... and {len(missing) - 40} more")
    if unfaithful:
        print(f"\nunfaithful translations ({len(unfaithful)}):")
        for item in unfaithful[:40]:
            print(f"  {item}")
    if untranslated:
        print(f"\nuntranslated lines ({len(untranslated)} files):")
        for item in untranslated[:40]:
            print(f"  {item}")
        if len(untranslated) > 40:
            print(f"  ... and {len(untranslated) - 40} more files")

    failed = bool(missing or unfaithful) or (args.strict and bool(untranslated))
    if args.strict and untranslated:
        print("\n--strict: untranslated lines are errors")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

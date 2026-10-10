#!/usr/bin/env python3
"""check-ids.py — cross-reference the traceability IDs inside each pack.

The pack standard (§8) says every artifact must resolve to FR/NFR/CTL/ADR/BR
IDs, and the roadmap's "packlint advanced" item promises machine enforcement
instead of human diligence. This script delivers the core of that: within each
pack it collects

  * **definitions** — an ID at the start of a content line, after stripping
    markdown markers (`#`, `>`, `|`, `-`, `*`, backticks). This matches every
    form the packs actually use (`### FR-001 …`, `| BR-01 | …`, `- **AC-001**`
    `# ADR-0001`, `| **CTL-01** |`).
  * **references** — every other occurrence of an ID token.

and reports:

  ERROR  referenced in a pack but defined in no pack (dangling reference)
  INFO   referenced in a pack but defined in another pack (cross-pack ref)
         — with --strict these become errors, since a self-contained
         (L2+) pack must not lean on IDs another pack defines

Leading zeros are normalized (FR-001 == FR-1, AC-N01 == AC-N1) so packs with
different padding conventions compare correctly.

Deliberately NOT checked: "duplicate definitions". Traceability matrices and
task maps legitimately re-list an ID at the start of a table row or bullet, so
any such heuristic drowns real findings in false positives — which this
project's own standard forbids. Orphan/first-definition analysis belongs in a
later rule that can consume the `--format json` output.

Usage:  python tools/check-ids.py [--strict]
Exit:   0 = no errors (info allowed unless --strict); 1 = errors.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"

# Traceability ID kinds used across the packs.
ID_RE = re.compile(
    r"\b(?P<kind>FR|NFR|CTL|BR|AC|ADR|SM|CAP|BC|C|I|T|P)-"
    r"(?P<num>[A-Za-z]?\d{1,4}[a-z]?)\b"
)

# Leading markdown markers stripped before deciding "is this a definition line".
# Backtick is deliberately NOT stripped: a line beginning with `CODE` is inline
# code (a reference), never a definition — stripping it produced false defs.
LEAD_RE = re.compile(r"^[\s#>*|\-+]+")


def normalize(kind: str, num: str) -> str:
    """FR-001 / FR-1 -> FR-1 ; AC-N01 -> AC-N1 ; BR-03a -> BR-3a ; SM-T1 -> SM-T1."""
    m = re.match(r"([A-Za-z]*)(\d+)([a-z]?)", num)
    if not m:
        return f"{kind}-{num}"
    prefix, digits, tail = m.groups()
    return f"{kind}-{prefix}{int(digits)}{tail}"


def _rel(path: Path) -> str:
    """Path relative to the repo root, or absolute if it lies outside (tests)."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def pack_markdown_files(pack_dir: Path) -> list[Path]:
    return sorted(
        p
        for p in pack_dir.rglob("*.md")
        if ".git" not in p.parts
    )


def scan_pack(pack_dir: Path) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Return (definitions, references) as maps normalized_id -> set(files)."""
    definitions: dict[str, set[str]] = {}
    references: dict[str, set[str]] = {}
    for md in pack_markdown_files(pack_dir):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        rel = _rel(md)
        for line in lines:
            lead = LEAD_RE.match(line)
            offset = lead.end() if lead else 0
            for m in ID_RE.finditer(line):
                norm = normalize(m.group("kind"), m.group("num"))
                if m.start() == offset:
                    definitions.setdefault(norm, set()).add(rel)
                else:
                    references.setdefault(norm, set()).add(rel)
            # A definition line often also carries references; the loop above
            # already classified every token by position, so nothing to add.
    return definitions, references


def main() -> int:
    strict = "--strict" in sys.argv[1:]
    pack_dirs = sorted(
        d for d in PACKS_DIR.glob("*/*") if d.is_dir() and (d / "manifest.yaml").exists()
    )
    if not pack_dirs:
        print("ERROR: no packs found", file=sys.stderr)
        return 1

    all_definitions: dict[str, set[str]] = {}
    per_pack: dict[str, tuple[str, dict[str, set[str]], dict[str, set[str]]]] = {}
    for pack_dir in pack_dirs:
        pack_id = f"packs/{pack_dir.parent.name}/{pack_dir.name}"
        defs, refs = scan_pack(pack_dir)
        per_pack[pack_id] = (pack_id, defs, refs)
        for norm, files in defs.items():
            all_definitions.setdefault(norm, set()).update({pack_id})

    errors: list[str] = []
    infos: list[str] = []
    total_ids = 0

    for pack_id, (_pid, defs, refs) in per_pack.items():
        total_ids += len(defs)
        for norm, files in sorted(refs.items()):
            if norm in defs:
                continue
            if norm in all_definitions:
                infos.append(
                    f"[INFO]  {pack_id}: {norm} is a cross-pack reference "
                    f"(defined in {', '.join(sorted(all_definitions[norm]))})"
                )
                # --strict promotes cross-pack references to failures: a pack
                # that leans on IDs it does not define is not self-contained,
                # which is exactly what an L3 "agent-ready" pack must be.
                if strict:
                    errors.append(
                        f"[ERROR] {pack_id}: {norm} is a cross-pack reference "
                        f"but --strict requires in-pack definitions"
                    )
            else:
                errors.append(
                    f"[ERROR] {pack_id}: {norm} referenced but never defined "
                    f"({', '.join(sorted(files))})"
                )

    print(f"checked {len(pack_dirs)} packs, {total_ids} distinct ID definitions")
    for line in infos:
        print(line)
    for line in errors:
        print(line)
    print(f"summary: {len(errors)} error(s), {len(infos)} info")
    if errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

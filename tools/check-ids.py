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
  ERROR  referenced in a pack, defined only in another pack, but numerically
         adjacent to the referencing pack's own IDs of the same kind
         (**in-pack gap** — see below)
  INFO   referenced in a pack but defined in another pack (cross-pack ref)
         — with --strict these become errors, since a self-contained
         (L2+) pack must not lean on IDs another pack defines

**In-pack gap detection.** A bare dangling check must look across every pack,
otherwise a reference to `T-5` is "fine" because another pack also defines a
`T-5`. That masks the real defect — the referencing pack is the one with the
gap. So when a referenced ID is missing in-pack but its *kind* is defined in-pack
by a nearby number (within +2 of that pack's maximum), it is reported as an
in-pack gap error regardless of what other packs define: a pack that defines
`ADR-1..4` and cites `ADR-5` has a broken internal reference, not a legitimate
cross-reference.

A pack's ``10-demo/demo.json`` is scanned too, and its ``demonstrates`` list
is checked the same way. The demo pages are hand-written, so they are the one
part of a pack that can drift from the pack's content: a demo still
demonstrating ``ADR-0004`` after that ADR was renumbered is worse than no
demo, because it asserts a decision that no longer exists. A missing ID is
therefore a build failure, not a discovery made by a reader.

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

import json
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


# How far past a pack's own maximum for a kind a missing number may sit and still
# count as an in-pack gap. ADR numbering is the common case: a pack defining
# ADR-1..4 and citing ADR-5 has a gap at the end of its own sequence.
ADJACENT_SLACK = 2


def _number(norm: str) -> int | None:
    """The numeric part of a normalized ID, if it is a plain number."""
    m = re.match(r"^[A-Z]+-([A-Za-z]*)(\d+)[a-z]?$", norm)
    return int(m.group(2)) if m else None


def _kind(norm: str) -> str | None:
    m = re.match(r"^([A-Z]+)-", norm)
    return m.group(1) if m else None


def in_pack_gap(norm: str, definitions: dict[str, set[str]]) -> bool:
    """True when `norm` is missing in-pack but sits next to the pack's own
    definitions of the same kind — the signature of a broken internal
    reference rather than a genuine cross-pack one."""
    num = _number(norm)
    kind = _kind(norm)
    if num is None or kind is None:
        return False
    peers = [
        _number(d)
        for d in definitions
        if _kind(d) == kind and (_number(d) is not None)
    ]
    if not peers:
        return False
    return min(peers) <= num <= max(peers) + ADJACENT_SLACK


def _rel(path: Path) -> str:
    """Path relative to the repo root, or absolute if it lies outside (tests)."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


# A demo manifest is a pack's only JSON artefact. Its shape is small and the
# pack standard fixes it, so an unknown or missing field is reported rather
# than ignored — a manifest that silently drops `demonstrates` would disarm
# the drift check exactly where it matters.
DEMO_REQUIRED = ("title", "kind", "entry", "demonstrates")


def check_demo_manifest(pack_dir: Path, definitions: dict[str, set[str]]) -> list[str]:
    """Errors for one pack's ``10-demo/demo.json``, or an empty list.

    Two things are checked. The manifest must carry the fixed fields, because
    a manifest missing ``demonstrates`` would disable the drift check it is
    there to give. And every ID it declares must be defined **in this pack**:
    a demo demonstrating another pack's decision is a demo of a decision this
    pack does not make.
    """
    rel_dir = f"packs/{pack_dir.parent.name}/{pack_dir.name}"
    path = pack_dir / "10-demo" / "demo.json"
    if not path.is_file():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"{rel_dir}/10-demo/demo.json: cannot be parsed ({exc})"]
    if not isinstance(data, dict):
        return [f"{rel_dir}/10-demo/demo.json: must be a JSON object"]

    errors: list[str] = []
    for field_name in DEMO_REQUIRED:
        if field_name not in data:
            errors.append(
                f"{rel_dir}/10-demo/demo.json: missing required field `{field_name}`"
            )
    if not isinstance(data.get("demonstrates"), list):
        errors.append(f"{rel_dir}/10-demo/demo.json: `demonstrates` must be a list")
        return errors

    entry = str(data.get("entry", "")).strip()
    if entry and not (pack_dir / "10-demo" / entry).is_file():
        errors.append(
            f"{rel_dir}/10-demo/demo.json: `entry` names `{entry}`, which does not exist"
        )

    for raw in data["demonstrates"]:
        token = str(raw).strip()
        m = ID_RE.search(token)
        if not m:
            errors.append(
                f"{rel_dir}/10-demo/demo.json: `{token}` is not a traceability ID"
            )
            continue
        norm = normalize(m.group("kind"), m.group("num"))
        if norm not in definitions:
            near = in_pack_gap(norm, definitions)
            errors.append(
                f"{rel_dir}/10-demo/demo.json: `{token}` is not defined in this pack"
                + (" (in-pack gap: it sits among the pack's own IDs)"
                   if near else "")
            )
    return errors


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
        for norm in defs:
            all_definitions.setdefault(norm, set()).update({pack_id})

    errors: list[str] = []
    infos: list[str] = []
    total_ids = 0
    demo_manifests = 0

    # The demo manifests are checked against the pack they live in, using the
    # same definitions the reference scan collected.
    for pack_dir in pack_dirs:
        pack_id = f"packs/{pack_dir.parent.name}/{pack_dir.name}"
        _pid, defs, _refs = per_pack[pack_id]
        demo_path = pack_dir / "10-demo" / "demo.json"
        if not demo_path.is_file():
            continue
        demo_manifests += 1
        errors.extend(check_demo_manifest(pack_dir, defs))

    for pack_id, (_pid, defs, refs) in per_pack.items():
        total_ids += len(defs)
        for norm, files in sorted(refs.items()):
            if norm in defs:
                continue
            if in_pack_gap(norm, defs):
                # A reference into the pack's own numbering sequence that the
                # pack itself does not define. Another pack may happen to define
                # the same ID; that collision must not hide the local defect.
                errors.append(
                    f"[ERROR] {pack_id}: {norm} is an in-pack gap "
                    f"(the pack defines the surrounding {_kind(norm)}- numbers but "
                    f"not this one) ({', '.join(sorted(files))})"
                )
            elif norm in all_definitions:
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

    print(
        f"checked {len(pack_dirs)} packs, {total_ids} distinct ID definitions, "
        f"{demo_manifests} demo manifest(s)"
    )
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

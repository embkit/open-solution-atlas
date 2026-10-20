#!/usr/bin/env python3
"""validate-packs.py — machine-check every pack against pack-standard.v1.

Enforced rules (S1/S2 in the project maturity standard):
  R1  manifest.yaml parses and matches osa-pack/v1 field rules
      (mirrors schemas/pack-manifest.schema.json; that file is the
      editor-facing authority, this script is the CI authority for the
      structural rules JSON Schema cannot express).
  R2  slug == directory name; domain == parent taxonomy directory.
  R3  Required-file matrix per maturity (standard §6):
        L1: manifest, README, SOURCES, AGENTS  (+ §6 checklist items — WARN if absent)
        L2: L1 + context/business/requirements/domain/architecture/data chapters + >=3 ADRs
        L3: L2 + state-machines, contracts (api-overview + openapi.yaml),
            acceptance-criteria, test-strategy, milestones, task-map
        L4: L3 + field-proven verification
  R4  Verification ladder honesty (standard §8):
        unverified        -> README banner (first 40 lines) names `unverified`
        source-checked+   -> SOURCES.md exists, sources/evidence non-empty,
                             README banner names the verification value
        practitioner-rev+ -> verified_by non-empty
        field-proven / L4 -> evidence contains deployment | case-study
  R5  enums, date/semver formats, evidence/verified_by entry shape.

Usage:  python tools/validate-packs.py [--strict]
Exit:   0 = no errors (warnings allowed unless --strict); 1 = errors.
"""

from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"

MATURITIES = ["L1", "L2", "L3", "L4"]
PROVENANCES = ["llm-drafted", "human-authored", "community", "mixed"]
VERIFICATIONS = ["unverified", "source-checked", "practitioner-reviewed", "field-proven"]
STACK_STANCES = ["stack-agnostic", "stack-specific"]
EVIDENCE_TYPES = ["standard", "spec", "oss-implementation", "case-study", "deployment"]
VERIFY_RANK = {v: i for i, v in enumerate(VERIFICATIONS)}

BASE_FILES = ["manifest.yaml", "README.md", "SOURCES.md", "AGENTS.md"]

L1_CHECKLIST = [  # standard §6 L1 items — WARN only (existing debt must be visible)
    "00-context/industry-brief.md",
    "00-context/regulatory-landscape.md",
    "00-context/stakeholders.md",
    "01-business/capability-map.md",
    "03-domain/glossary.md",
]

L2_FILES = [
    *L1_CHECKLIST,
    "01-business/processes.md",
    "01-business/business-rules.md",
    "02-requirements/functional.md",
    "02-requirements/non-functional.md",
    "02-requirements/compliance.md",
    "03-domain/domain-model.md",
    "04-architecture/overview.md",
    "04-architecture/integration.md",
    "04-architecture/security.md",
    "04-architecture/observability.md",
    "05-data/logical-data-model.md",
    "05-data/data-dictionary.md",
]

L3_FILES = [
    *L2_FILES,
    "03-domain/state-machines.md",
    "06-contracts/api-overview.md",
    "06-contracts/api/openapi.yaml",
    "08-quality/acceptance-criteria.md",
    "08-quality/test-strategy.md",
    "09-delivery/milestones.md",
    "09-delivery/task-map.md",
]

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, pack: str, msg: str) -> None:
        self.errors.append(f"[ERROR] {pack}: {msg}")

    def warn(self, pack: str, msg: str) -> None:
        self.warnings.append(f"[WARN]  {pack}: {msg}")


def read_readme_head(pack_dir: Path, lines: int = 40) -> str:
    readme = pack_dir / "README.md"
    if not readme.exists():
        return ""
    try:
        text = readme.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""
    return "\n".join(text.splitlines()[:lines]).lower()


def validate_manifest(pack: str, data: dict, rep: Report) -> None:
    required = [
        "schema", "slug", "title", "domain", "subdomain", "tags", "maturity",
        "provenance", "verification", "stack_stance", "language", "maintainers",
        "version", "last_reviewed", "sources", "verified_by", "evidence",
    ]
    for key in required:
        if key not in data:
            rep.err(pack, f"manifest missing required field `{key}`")
    if data.get("schema") != "osa-pack/v1":
        rep.err(pack, f"schema must be 'osa-pack/v1', got {data.get('schema')!r}")
    if data.get("maturity") not in MATURITIES:
        rep.err(pack, f"maturity must be one of {MATURITIES}, got {data.get('maturity')!r}")
    if data.get("provenance") not in PROVENANCES:
        rep.err(pack, f"provenance must be one of {PROVENANCES}, got {data.get('provenance')!r}")
    if data.get("verification") not in VERIFICATIONS:
        rep.err(pack, f"verification must be one of {VERIFICATIONS}, got {data.get('verification')!r}")
    if data.get("stack_stance") not in STACK_STANCES:
        rep.err(pack, f"stack_stance must be one of {STACK_STANCES}, got {data.get('stack_stance')!r}")
    version = data.get("version")
    if not (isinstance(version, str) and SEMVER_RE.match(version)):
        rep.err(pack, f"version must be semver X.Y.Z, got {version!r}")
    lr = data.get("last_reviewed")
    if isinstance(lr, datetime.date):  # PyYAML parses unquoted dates natively
        reviewed = lr
    elif isinstance(lr, str) and DATE_RE.match(lr):
        try:
            reviewed = datetime.date.fromisoformat(lr)
        except ValueError:
            rep.err(pack, f"last_reviewed is not a real date: {lr!r}")
            reviewed = None
    else:
        rep.err(pack, f"last_reviewed must be YYYY-MM-DD, got {lr!r}")
        reviewed = None
    if reviewed is not None:
        # UTC-normalised: a naive local `today()` would make the 180-day decay
        # warning shift by a day depending on the contributor's timezone.
        # (datetime.UTC needs Python 3.11+, which is this repo's floor.)
        age = (datetime.datetime.now(datetime.UTC).date() - reviewed).days
        if age > 180 and data.get("verification") != "unverified":
            rep.warn(pack, f"last_reviewed is {age} days old — verification claim may have decayed (standard §8.3 rule 7)")
    for key in ("tags", "sources", "verified_by", "evidence", "maintainers"):
        if key in data and not isinstance(data[key], list):
            rep.err(pack, f"`{key}` must be a list")
    for i, ev in enumerate(data.get("evidence") or []):
        if not isinstance(ev, dict) or not {"type", "ref", "note"} <= set(ev):
            rep.err(pack, f"evidence[{i}] must be an object with type/ref/note")
        elif ev["type"] not in EVIDENCE_TYPES:
            rep.err(pack, f"evidence[{i}].type must be one of {EVIDENCE_TYPES}")
    for i, vb in enumerate(data.get("verified_by") or []):
        if not isinstance(vb, dict) or not {"who", "role", "date", "scope"} <= set(vb):
            rep.err(pack, f"verified_by[{i}] must be an object with who/role/date/scope")


def validate_lifecycle(pack: str, data: dict, pack_dir: Path, rep: Report) -> None:
    maturity = data.get("maturity")
    verification = data.get("verification")
    readme_head = read_readme_head(pack_dir)

    # R3 — file matrix
    for rel in BASE_FILES:
        if not (pack_dir / rel).exists():
            rep.err(pack, f"missing base file {rel}")
    if maturity in ("L1",):
        for rel in L1_CHECKLIST:
            if not (pack_dir / rel).exists():
                rep.warn(pack, f"L1 checklist item absent: {rel} (standard §6; list it in README roadmap)")
    elif maturity in ("L2", "L3", "L4"):
        for rel in L2_FILES:
            if not (pack_dir / rel).exists():
                rep.err(pack, f"missing L2 file {rel}")
    if maturity in ("L3", "L4"):
        for rel in L3_FILES:
            if not (pack_dir / rel).exists():
                rep.err(pack, f"missing L3 file {rel}")
        openapi = pack_dir / "06-contracts" / "api" / "openapi.yaml"
        if openapi.exists():
            try:
                spec = yaml.safe_load(openapi.read_text(encoding="utf-8"))
                if not isinstance(spec, dict) or "paths" not in spec:
                    rep.err(pack, "openapi.yaml parses but has no `paths`")
            except Exception as exc:
                rep.err(pack, f"openapi.yaml does not parse: {exc}")
    if maturity in ("L2", "L3", "L4"):
        adr_dir = pack_dir / "04-architecture" / "adr"
        n_adr = len(list(adr_dir.glob("*.md"))) if adr_dir.exists() else 0
        if n_adr < 3:
            rep.err(pack, f"{maturity} requires >=3 ADRs (L2 checklist), found {n_adr}")

    # R3b - translations honesty (standard 5): a declared locale means the
    # whole pack is translated. A translation is a *sibling*
    # (`business-rules.zh-CN.md` beside `business-rules.md`), so the claim is
    # checked file by file: every translatable file needs its counterpart.
    for locale in data.get("translations") or []:
        candidates = [pack_dir / f"README.{locale}.md", pack_dir / "translations" / locale]
        if not any(c.exists() for c in candidates) and not any(
            pack_dir.rglob(f"*.{locale}.md")
        ):
            rep.err(
                pack,
                f"translations declares {locale!r} but no README.{locale}.md, "
                f"translations/{locale}/ or *.{locale}.md file exists (standard 5)",
            )
        missing = []
        for md in sorted(pack_dir.rglob("*.md")):
            rel_inside = md.relative_to(pack_dir)
            if md.name.endswith(f".{locale}.md") or "translations" in rel_inside.parts:
                continue
            if not md.with_name(md.stem + f".{locale}.md").exists():
                missing.append(rel_inside.as_posix())
        if missing:
            shown = ", ".join(missing[:5]) + ("..." if len(missing) > 5 else "")
            rep.err(
                pack,
                f"translations declares {locale!r} but {len(missing)} file(s) "
                f"have no {locale} translation: {shown} (standard 5)",
            )
    if maturity == "L4" and verification != "field-proven":
        rep.err(pack, "L4 requires verification: field-proven (standard §6/§8)")

    # R4 — verification ladder honesty
    if verification == "unverified":
        if "unverified" not in readme_head:
            rep.err(pack, "unverified pack must show a draft banner naming `unverified` in README head (§8.3)")
    else:
        if not (pack_dir / "SOURCES.md").exists():
            rep.err(pack, f"{verification} pack must contain SOURCES.md (§8.2)")
        if not data.get("sources"):
            rep.err(pack, f"{verification} pack must list pack-level sources")
        if not data.get("evidence"):
            rep.err(pack, f"{verification} pack must record evidence entries")
        if verification not in readme_head:
            rep.err(pack, f"README head must name verification value `{verification}`")
        if re.search(r"verification:\s*`?unverified`?", readme_head):
            rep.err(pack, f"README head claims `verification: unverified` but manifest is {verification}")
    if VERIFY_RANK.get(verification, 0) >= VERIFY_RANK["practitioner-reviewed"] and not data.get("verified_by"):
        rep.err(pack, f"{verification} requires non-empty verified_by (§8.2)")
    if verification == "field-proven" or maturity == "L4":
        types = {e.get("type") for e in (data.get("evidence") or []) if isinstance(e, dict)}
        if not types & {"deployment", "case-study"}:
            rep.err(pack, "field-proven requires deployment or case-study evidence (§8.2)")


def validate_slug(pack_dir: Path, data: dict, rep: Report) -> str:
    slug = pack_dir.name
    domain_dir = pack_dir.parent
    pack_id = f"packs/{domain_dir.name}/{slug}"
    if data.get("slug") != slug:
        rep.err(pack_id, f"slug {data.get('slug')!r} != directory name {slug!r}")
    if data.get("domain") != domain_dir.name:
        rep.err(pack_id, f"domain {data.get('domain')!r} != parent dir {domain_dir.name!r}")
    return pack_id


def main() -> int:
    strict = "--strict" in sys.argv[1:]
    rep = Report()
    manifests = sorted(PACKS_DIR.glob("*/*/manifest.yaml"))
    if not manifests:
        print("ERROR: no packs found", file=sys.stderr)
        return 1
    for mf in manifests:
        pack_dir = mf.parent
        try:
            data = yaml.safe_load(mf.read_text(encoding="utf-8"))
        except Exception as exc:
            rep.err(f"packs/{pack_dir.parent.name}/{pack_dir.name}", f"manifest parse error: {exc}")
            continue
        if not isinstance(data, dict):
            rep.err(f"packs/{pack_dir.parent.name}/{pack_dir.name}", "manifest is not a mapping")
            continue
        pack_id = validate_slug(pack_dir, data, rep)
        validate_manifest(pack_id, data, rep)
        validate_lifecycle(pack_id, data, pack_dir, rep)

    print(f"checked {len(manifests)} packs")
    for w in rep.warnings:
        print(w)
    for e in rep.errors:
        print(e)
    print(f"summary: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    if rep.errors or (strict and rep.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

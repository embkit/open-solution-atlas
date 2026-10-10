"""Tests for tools/validate-packs.py — manifest rules and trust-ladder honesty."""

from __future__ import annotations

from pathlib import Path


def _valid_manifest() -> dict:
    return {
        "schema": "osa-pack/v1",
        "slug": "example",
        "title": "Example",
        "domain": "horizontal",
        "subdomain": "demo",
        "tags": ["demo"],
        "maturity": "L1",
        "provenance": "llm-drafted",
        "verification": "unverified",
        "stack_stance": "stack-agnostic",
        "language": "en",
        "maintainers": [],
        "version": "0.1.0",
        "last_reviewed": "2026-10-09",
        "sources": [],
        "verified_by": [],
        "evidence": [],
    }


def _make_pack(tmp_path: Path, readme_head: str = "") -> Path:
    pack = tmp_path / "horizontal" / "example"
    pack.mkdir(parents=True, exist_ok=True)
    (pack / "manifest.yaml").write_text("slug: example\n", encoding="utf-8")
    (pack / "SOURCES.md").write_text("# SOURCES\n", encoding="utf-8")
    (pack / "AGENTS.md").write_text("# AGENTS\n", encoding="utf-8")
    (pack / "README.md").write_text(
        readme_head + "\n# Example\n", encoding="utf-8"
    )
    return pack


def test_valid_manifest_has_no_errors(validate_packs):
    rep = validate_packs.Report()
    validate_packs.validate_manifest("example", _valid_manifest(), rep)
    assert rep.errors == []


def test_missing_required_field(validate_packs):
    data = _valid_manifest()
    del data["version"]
    rep = validate_packs.Report()
    validate_packs.validate_manifest("example", data, rep)
    assert any("version" in e for e in rep.errors)


def test_bad_enums_and_version(validate_packs):
    data = _valid_manifest()
    data["maturity"] = "L9"
    data["verification"] = "totally-verified"
    data["version"] = "1.0"
    rep = validate_packs.Report()
    validate_packs.validate_manifest("example", data, rep)
    assert any("maturity" in e for e in rep.errors)
    assert any("verification" in e for e in rep.errors)
    assert any("semver" in e for e in rep.errors)


def test_evidence_entry_shape(validate_packs):
    data = _valid_manifest()
    data["evidence"] = [{"type": "bogus", "ref": "x", "note": "y"}]
    rep = validate_packs.Report()
    validate_packs.validate_manifest("example", data, rep)
    assert any("evidence[0].type" in e for e in rep.errors)


def test_unverified_requires_banner(validate_packs, tmp_path):
    pack = _make_pack(tmp_path, readme_head="plain readme")
    rep = validate_packs.Report()
    validate_packs.validate_lifecycle(
        "example", {"maturity": "L1", "verification": "unverified"}, pack, rep
    )
    assert any("unverified" in e for e in rep.errors)


def test_unverified_with_banner_passes(validate_packs, tmp_path):
    pack = _make_pack(tmp_path, readme_head="Status: unverified (draft)")
    rep = validate_packs.Report()
    validate_packs.validate_lifecycle(
        "example", {"maturity": "L1", "verification": "unverified"}, pack, rep
    )
    assert rep.errors == []


def test_source_checked_requires_evidence_and_banner(validate_packs, tmp_path):
    pack = _make_pack(tmp_path, readme_head="Status: source-checked")
    data = {
        "maturity": "L1",
        "verification": "source-checked",
        "sources": ["https://example.com"],
        "evidence": [],
    }
    rep = validate_packs.Report()
    validate_packs.validate_lifecycle("example", data, pack, rep)
    assert any("evidence" in e for e in rep.errors)


def test_practitioner_reviewed_requires_verified_by(validate_packs, tmp_path):
    pack = _make_pack(tmp_path, readme_head="Status: practitioner-reviewed")
    data = {
        "maturity": "L1",
        "verification": "practitioner-reviewed",
        "sources": ["https://example.com"],
        "evidence": [{"type": "standard", "ref": "x", "note": "y"}],
        "verified_by": [],
    }
    rep = validate_packs.Report()
    validate_packs.validate_lifecycle("example", data, pack, rep)
    assert any("verified_by" in e for e in rep.errors)


def test_field_proven_requires_deployment_evidence(validate_packs, tmp_path):
    pack = _make_pack(tmp_path, readme_head="Status: field-proven")
    data = {
        "maturity": "L1",
        "verification": "field-proven",
        "sources": ["https://example.com"],
        "evidence": [{"type": "standard", "ref": "x", "note": "y"}],
        "verified_by": [{"who": "A", "role": "r", "date": "2026-10-01", "scope": "s"}],
    }
    rep = validate_packs.Report()
    validate_packs.validate_lifecycle("example", data, pack, rep)
    assert any("deployment or case-study" in e for e in rep.errors)

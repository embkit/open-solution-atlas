"""Tests for tools/check-ids.py — ID normalization and dangling-reference detection."""

from __future__ import annotations

from pathlib import Path


def test_normalize_pads_and_prefixes(check_ids):
    assert check_ids.normalize("FR", "001") == "FR-1"
    assert check_ids.normalize("FR", "1") == "FR-1"
    assert check_ids.normalize("NFR", "014") == "NFR-14"
    assert check_ids.normalize("AC", "N01") == "AC-N1"
    assert check_ids.normalize("BR", "03a") == "BR-3a"
    assert check_ids.normalize("SM", "T1") == "SM-T1"
    assert check_ids.normalize("SM", "1") == "SM-1"


def _write(pack_dir: Path, rel: str, text: str) -> None:
    path = pack_dir / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_definition_vs_reference_detection(check_ids, tmp_path):
    pack = tmp_path / "example"
    _write(
        pack,
        "01-business/business-rules.md",
        "## Rules\n\n| ID | Rule |\n|---|---|\n| BR-01 | do a thing |\n",
    )
    _write(
        pack,
        "02-requirements/functional.md",
        "- **FR-001** SHALL do it (BR-01).\n",
    )
    defs, refs = check_ids.scan_pack(pack)
    # `| BR-01 |` at line start is a definition; FR-001 after `- **` is one too.
    assert "BR-1" in defs
    assert "FR-1" in defs
    # BR-01 on the FR line is a reference, not a re-definition.
    assert "BR-1" in refs


def test_backticked_id_at_line_start_is_not_a_definition(check_ids, tmp_path):
    """A line beginning with `CODE` is inline code — a reference, not a definition."""
    pack = tmp_path / "example"
    _write(
        pack,
        "notes.md",
        "`BR-01` is mentioned here.\n\n- **BR-02** defined only here.\n",
    )
    defs, refs = check_ids.scan_pack(pack)
    assert "BR-1" not in defs  # backticked -> reference
    assert "BR-1" in refs
    assert "BR-2" in defs


def test_dangling_reference_is_reported(check_ids, tmp_path, capsys, monkeypatch):
    pack = tmp_path / "horizontal" / "example"
    _write(pack, "manifest.yaml", "slug: example\n")
    _write(pack, "02-requirements/functional.md", "- **FR-001** SHALL x (BR-99).\n")
    monkeypatch.setattr(check_ids, "PACKS_DIR", tmp_path)
    rc = check_ids.main()
    out = capsys.readouterr().out
    assert rc == 1
    assert "BR-99" in out and "referenced but never defined" in out


def test_cross_pack_reference_is_info_not_error(check_ids, tmp_path, capsys, monkeypatch):
    pack_a = tmp_path / "horizontal" / "alpha"
    pack_b = tmp_path / "horizontal" / "beta"
    _write(pack_a, "manifest.yaml", "slug: alpha\n")
    _write(pack_a, "01-business/business-rules.md", "| BR-01 | defined here |\n")
    _write(pack_b, "manifest.yaml", "slug: beta\n")
    _write(pack_b, "02-requirements/functional.md", "- **FR-001** SHALL x (BR-01).\n")
    monkeypatch.setattr(check_ids, "PACKS_DIR", tmp_path)
    rc = check_ids.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert "cross-pack reference" in out
    assert "0 error(s)" in out

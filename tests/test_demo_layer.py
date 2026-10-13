"""Tests for the demo layer: manifests, drift protection, and the site wiring.

The demo pages are hand-written, which makes them the one part of a pack that
can drift from the pack's content. A demo still demonstrating `ADR-0004` after
that ADR was renumbered is worse than no demo — it asserts a decision that no
longer exists. So `10-demo/demo.json` declares what it demonstrates, and
check-ids validates it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


@pytest.fixture
def pack_with_demo(tmp_path, monkeypatch):
    """A minimal pack whose IDs are defined and which carries a demo manifest."""
    pack = tmp_path / "packs" / "horizontal" / "demo-test"
    (pack / "01-business").mkdir(parents=True)
    (pack / "10-demo").mkdir(parents=True)
    (pack / "manifest.yaml").write_text(
        "title: Demo Test\nslug: demo-test\ndomain: horizontal\n"
        "maturity: L2\nverification: unverified\nversion: 0.3.0\n",
        encoding="utf-8",
    )
    rules = pack / "01-business" / "business-rules.md"
    rules.write_text(
        "### BR-01 — A rule\n*(enforced by FR-001; violated when x)*\n\nThe proposition.\n",
        encoding="utf-8",
    )
    (pack / "02-requirements").mkdir(parents=True)
    (pack / "02-requirements" / "functional.md").write_text(
        "### FR-001 — A requirement\n\n- **WHEN** x\n"
        "- **THE SYSTEM SHALL** do y (BR-01)\n- Traces: CAP-01, BR-01\n",
        encoding="utf-8",
    )
    return pack


def _manifest(pack: Path, data: dict) -> Path:
    path = pack / "10-demo" / "demo.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def _demo_pages() -> list[Path]:
    root = Path(__file__).resolve().parent.parent
    return sorted(root.glob("packs/*/*/10-demo/index.html"))


# --------------------------------------------------------------------------- #
# Every element a demo reaches for is one the page actually has
# --------------------------------------------------------------------------- #
#
# This is the check the browser made and the JS harness did not. The demo's
# script asked for `#log`, the page never declared it, and `getElementById`
# returned null — so the demo threw on load and rendered three empty panels.
# The harness passed it because its stub minted a node for any id asked for, and
# `getElementById` returning a usable element is exactly the DOM behaviour a
# stub should not invent.
#
# These demos ship as the interactive part of a pack, so a demo that dies on
# load is worse than no demo. A static check catches it without a browser.

_IDS_ASKED = re.compile(r"""
    \b(?:document\[\s*["']getElementById["']\s*\]\s*\(|getElementById\s*\(|el\s*\()\s*["']([A-Za-z0-9_-]+)["']
""", re.VERBOSE)
_IDS_DECLARED = re.compile(r"""\bid\s*=\s*["']([A-Za-z0-9_-]+)["']""")


def test_every_id_a_demo_asks_for_is_declared():
    pages = _demo_pages()
    assert pages, "no demo pages found"
    for page in pages:
        text = page.read_text(encoding="utf-8")
        asked = set(_IDS_ASKED.findall(text))
        declared = set(_IDS_DECLARED.findall(text))
        built = asked - declared
        assert not built, (
            f"{page.parent.parent.name}: the script reaches for "
            f"{sorted(built)}, which the page never declares. In a browser "
            f"getElementById returns null and the demo dies on load."
        )


VALID = {
    "title": "A demo",
    "kind": "invariant-lab",
    "entry": "index.html",
    "demonstrates": ["BR-01", "FR-001"],
}


# --------------------------------------------------------------------------- #
# The manifest is the drift check
# --------------------------------------------------------------------------- #

def test_valid_manifest_passes(check_ids, pack_with_demo, monkeypatch, tmp_path):
    _manifest(pack_with_demo, VALID)
    (pack_with_demo / "10-demo" / "index.html").write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(check_ids, "PACKS_DIR", tmp_path / "packs")
    errors = check_ids.check_demo_manifest(pack_with_demo, {"BR-1": set(), "FR-1": set()})
    assert errors == []


def test_dangling_demonstrated_id_is_an_error(check_ids, pack_with_demo, monkeypatch):
    """The whole point: a demo of a decision that no longer exists must fail."""
    data = dict(VALID)
    data["demonstrates"] = ["BR-01", "FR-999"]
    _manifest(pack_with_demo, data)
    (pack_with_demo / "10-demo" / "index.html").write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(check_ids, "PACKS_DIR", pack_with_demo.parent.parent.parent)
    errors = check_ids.check_demo_manifest(pack_with_demo, {"BR-1": set(), "FR-1": set()})
    assert len(errors) == 1
    assert "FR-999" in errors[0]
    assert "not defined in this pack" in errors[0]


def test_in_pack_gap_is_labelled_as_such(check_ids, pack_with_demo, monkeypatch):
    """`FR-002` missing from a pack that defines FR-001 is a gap, not a typo."""
    data = dict(VALID)
    data["demonstrates"] = ["FR-002"]
    _manifest(pack_with_demo, data)
    (pack_with_demo / "10-demo" / "index.html").write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(check_ids, "PACKS_DIR", pack_with_demo.parent.parent.parent)
    errors = check_ids.check_demo_manifest(pack_with_demo, {"FR-1": set()})
    assert len(errors) == 1
    assert "in-pack gap" in errors[0]


def test_missing_required_field_is_reported(check_ids, pack_with_demo, monkeypatch):
    """A manifest without `demonstrates` would disarm the drift check."""
    data = {k: v for k, v in VALID.items() if k != "demonstrates"}
    _manifest(pack_with_demo, data)
    monkeypatch.setattr(check_ids, "PACKS_DIR", pack_with_demo.parent.parent.parent)
    errors = check_ids.check_demo_manifest(pack_with_demo, {"BR-1": set(), "FR-1": set()})
    assert any("demonstrates" in e for e in errors)


def test_entry_that_does_not_exist_is_reported(check_ids, pack_with_demo, monkeypatch):
    _manifest(pack_with_demo, VALID)
    monkeypatch.setattr(check_ids, "PACKS_DIR", pack_with_demo.parent.parent.parent)
    errors = check_ids.check_demo_manifest(pack_with_demo, {"BR-1": set(), "FR-1": set()})
    assert len(errors) == 1
    assert "index.html" in errors[0] and "does not exist" in errors[0]


def test_unparseable_manifest_is_reported_not_skipped(check_ids, pack_with_demo, monkeypatch):
    (pack_with_demo / "10-demo" / "demo.json").write_text("{not json", encoding="utf-8")
    monkeypatch.setattr(check_ids, "PACKS_DIR", pack_with_demo.parent.parent.parent)
    errors = check_ids.check_demo_manifest(pack_with_demo, {})
    assert errors and "cannot be parsed" in errors[0]


def test_a_pack_without_a_manifest_has_nothing_to_report(check_ids, pack_with_demo, monkeypatch):
    monkeypatch.setattr(check_ids, "PACKS_DIR", pack_with_demo.parent.parent.parent)
    assert check_ids.check_demo_manifest(pack_with_demo, {}) == []


def test_a_non_id_token_is_reported(check_ids, pack_with_demo, monkeypatch):
    data = dict(VALID)
    data["demonstrates"] = ["the whole vocabulary"]
    _manifest(pack_with_demo, data)
    monkeypatch.setattr(check_ids, "PACKS_DIR", pack_with_demo.parent.parent.parent)
    errors = check_ids.check_demo_manifest(pack_with_demo, {"BR-1": set()})
    assert any("not a traceability ID" in e for e in errors)


# --------------------------------------------------------------------------- #
# The real corpus: the one demo that exists
# --------------------------------------------------------------------------- #

def test_repository_demo_manifest_is_sound(check_ids, pack_index):
    """The shipped demo must demonstrate IDs the pack actually defines."""
    pack_dir = (
        Path(__file__).resolve().parent.parent
        / "packs" / "horizontal" / "workflow-bpm"
    )
    definitions = {
        check_ids.normalize(m.group("kind"), m.group("num"))
        for text in (pack_dir).rglob("*.md")
        for line in text.read_text(encoding="utf-8").splitlines()
        for m in check_ids.ID_RE.finditer(line)
    }
    errors = check_ids.check_demo_manifest(pack_dir, definitions)
    assert errors == [], errors


def test_demo_is_self_contained(pack_index):
    """A demo that depends on the site's assets cannot be opened on its own."""
    next(p for p in pack_index.build_index()["packs"] if p["slug"] == "workflow-bpm")
    html = (
        Path(__file__).resolve().parent.parent
        / "packs" / "horizontal" / "workflow-bpm" / "10-demo" / "index.html"
    ).read_text(encoding="utf-8")
    assert "<style>" in html, "the demo must carry its own styles"
    assert "<script>" in html, "the demo must carry its own behaviour"
    for external in ("http://", "https://", 'src="assets/', 'href="assets/'):
        assert external not in html, f"demo depends on an external asset: {external}"


# --------------------------------------------------------------------------- #
# A repo-content scanner must not scan a build output
# --------------------------------------------------------------------------- #

def test_check_links_ignores_build_output(check_links, monkeypatch, tmp_path):
    """`_site/` holds emitted prompt bundles whose links are pack-relative."""
    out = tmp_path / "_site" / "packs" / "horizontal" / "x" / "prompts"
    out.mkdir(parents=True)
    (out / "context.md").write_text(
        "[a](../SOURCES.md)\n", encoding="utf-8"
    )
    real = tmp_path / "packs" / "horizontal" / "x"
    real.mkdir(parents=True)
    (real / "SOURCES.md").write_text("# sources\n", encoding="utf-8")
    monkeypatch.setattr(check_links, "ROOT", tmp_path)
    # The exclusion lives in the discovery function, not in the per-file check:
    # check_file is deliberately low-level and stays honest about one file.
    scanned = check_links.iter_markdown()
    assert out / "context.md" not in scanned, "build output was discovered as content"
    assert real / "SOURCES.md" in scanned, "repository content must still be scanned"

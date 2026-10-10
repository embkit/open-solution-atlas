"""Tests for tools/check-links.py — relative resolution and external-URL collection."""

from __future__ import annotations

from pathlib import Path


def test_broken_relative_link_detected(check_links, tmp_path):
    md = tmp_path / "a.md"
    md.write_text("see [missing](./nope.md) and [ok](./b.md)\n", encoding="utf-8")
    (tmp_path / "b.md").write_text("# b\n", encoding="utf-8")
    problems = check_links.check_file(md)
    assert len(problems) == 1
    assert "nope.md" in problems[0]


def test_anchor_and_mailto_are_skipped(check_links, tmp_path):
    md = tmp_path / "a.md"
    md.write_text("[top](#section) [mail](mailto:x@y.z) [ext](https://e.com)\n", encoding="utf-8")
    assert check_links.check_file(md) == []


def test_fragment_is_stripped_before_resolution(check_links, tmp_path):
    md = tmp_path / "a.md"
    md.write_text("[x](./target.md#heading)\n", encoding="utf-8")
    (tmp_path / "target.md").write_text("# heading\n", encoding="utf-8")
    assert check_links.check_file(md) == []


def test_collect_external_urls_maps_to_citing_files(check_links, tmp_path, monkeypatch):
    (tmp_path / "SOURCES.md").write_text(
        "[iso](https://www.iso.org/standard/70636.html)\n", encoding="utf-8"
    )
    monkeypatch.setattr(check_links, "ROOT", tmp_path)
    urls = check_links.collect_external_urls()
    assert "https://www.iso.org/standard/70636.html" in urls
    assert "SOURCES.md" in urls["https://www.iso.org/standard/70636.html"]

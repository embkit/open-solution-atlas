"""Tests for tools/build-site.py — URL mapping, link rewriting, rendering, checks."""

from __future__ import annotations

from pathlib import Path


def test_url_for_maps_readme_to_index(build_site, monkeypatch, tmp_path):
    monkeypatch.setattr(build_site, "ROOT", tmp_path)
    pack_readme = tmp_path / "packs" / "manufacturing" / "wms" / "README.md"
    assert build_site.url_for(pack_readme) == "packs/manufacturing/wms/index.html"

    other = tmp_path / "packs" / "manufacturing" / "wms" / "SOURCES.md"
    assert build_site.url_for(other) == "packs/manufacturing/wms/SOURCES.html"

    root_readme = tmp_path / "README.md"
    assert build_site.url_for(root_readme) == "overview.html"

    doc = tmp_path / "docs" / "roadmap.md"
    assert build_site.url_for(doc) == "docs/roadmap.html"


def test_rewrite_link_cases(build_site):
    rw = build_site._rewrite_link
    assert rw("./00-context/industry-brief.md") == "./00-context/industry-brief.html"
    assert rw("../SOURCES.md") == "../SOURCES.html"
    assert rw("./README.md") == "./index.html"
    assert rw("./00-context/") == "./00-context/index.html"
    assert rw("./AGENTS.md#hard-rules") == "./AGENTS.html#hard-rules"
    assert rw("#anchor") == "#anchor"
    assert rw("https://www.iso.org/standard/70636.html") == "https://www.iso.org/standard/70636.html"
    assert rw("mailto:x@y.z") == "mailto:x@y.z"


def test_render_markdown_keeps_mermaid_intact(build_site):
    src = "# Title\n\n```mermaid\nstateDiagram-v2\n  A --> B: x\n```\n\ntext\n"
    html_out, plain, _toc = build_site.render_markdown(src)
    assert '<pre class="mermaid">' in html_out
    assert "--&gt; B" in html_out  # escaped, so the browser restores it for mermaid
    assert "A --> B" not in html_out.split('class="mermaid"')[1][:40]


def test_render_markdown_renders_tables_and_rewrites_links(build_site):
    src = "| a | b |\n|---|---|\n| 1 | 2 |\n\n[ch](./01-business/capability-map.md)\n"
    html_out, plain, _toc = build_site.render_markdown(src)
    assert "<table>" in html_out
    assert 'href="./01-business/capability-map.html"' in html_out
    assert "a b" in plain  # table cell text reaches the plain search text


def test_render_markdown_extracts_plain_text(build_site):
    _html, plain, _toc = build_site.render_markdown("# Hello\n\nSome **bold** words.\n")
    assert "Hello" in plain and "bold" in plain
    assert "<" not in plain


def test_verify_internal_links_flags_missing_target(build_site, tmp_path):
    out = tmp_path / "_site"
    out.mkdir()
    (out / "index.html").write_text(
        '<a href="ok.html">x</a><a href="missing.html">y</a>'
        '<a href="https://example.com">z</a>',
        encoding="utf-8",
    )
    (out / "ok.html").write_text("<h1>ok</h1>", encoding="utf-8")
    broken = build_site.verify_internal_links(out)
    assert len(broken) == 1
    assert "missing.html" in broken[0]


def test_verify_internal_links_accepts_fragments_and_schemes(build_site, tmp_path):
    out = tmp_path / "_site"
    out.mkdir()
    (out / "index.html").write_text(
        '<a href="page.html#sec">a</a><a href="#top">b</a>'
        '<a href="mailto:x@y.z">c</a><a href="/abs">d</a>',
        encoding="utf-8",
    )
    (out / "page.html").write_text("<h1>p</h1>", encoding="utf-8")
    assert build_site.verify_internal_links(out) == []


def test_pack_pills_and_labels(build_site):
    label, kind = build_site.MATURITY_LABEL["L3"]
    assert label == "L3 · Agent-ready" and kind == "m3"
    vlabel, vkind = build_site.VERIFICATION_LABEL["source-checked"]
    assert vlabel == "source-checked" and vkind == "v1"

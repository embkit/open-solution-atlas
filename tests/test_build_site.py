"""Tests for tools/build-site.py — URL mapping, link rewriting, rendering, checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# End-to-end build: every cached run below reads the same artifact.
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="module")
def built_site(build_site, tmp_path_factory) -> Path:
    """Build the real repository once into a temp directory."""
    out = tmp_path_factory.mktemp("site")
    code = build_site.build(out, "/", "https://example.test/atlas", "en")
    assert code == 0, "build-site.build() returned non-zero"
    return out


def _html_index(out: Path) -> str:
    return (out / "index.html").read_text(encoding="utf-8")


def test_build_emits_catalog_and_pack_pages(built_site):
    assert (built_site / "index.html").is_file()
    assert (built_site / "packs").is_dir()
    pack_pages = list((built_site / "packs").rglob("index.html"))
    assert len(pack_pages) >= 17, "one catalog entry per pack"
    # The pack READMEs must render into HTML, not stay Markdown.
    assert any(p for p in (built_site / "packs").rglob("*.html"))


def test_no_external_cdn_references(built_site):
    """The site must work offline: no CDN <script>/<link> to any origin."""
    offenders = []
    for page in built_site.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for url in re.findall(r'(?:src|href)="(https?://[^"]+)"', text):
            if any(part in url for part in (".js", ".css", "jsdelivr", "unpkg", "cdnjs")):
                offenders.append((page.name, url))
    assert offenders == [], f"external assets leaked into the site: {offenders}"


def test_vendored_libraries_are_copied_and_referenced(built_site):
    """fuse.js and mermaid are vendored locally, so search/diagrams survive CDN failure."""
    fuse = built_site / "assets" / "vendor" / "fuse.min.js"
    mermaid = built_site / "assets" / "vendor" / "mermaid.min.js"
    assert fuse.is_file() and fuse.stat().st_size > 0
    assert mermaid.is_file() and mermaid.stat().st_size > 0

    index_html = _html_index(built_site)
    assert 'src="assets/vendor/fuse.min.js"' in index_html
    assert "integrity=" in index_html, "vendored script must carry an SRI hash"

    mermaid_pages = [p for p in built_site.rglob("*.html")
                     if "assets/vendor/mermaid.min.js" in p.read_text(encoding="utf-8")]
    assert mermaid_pages, "pages containing diagrams must load the vendored mermaid"


def test_crawler_artifacts_exist(built_site):
    assert (built_site / "sitemap.xml").is_file()
    assert (built_site / "robots.txt").is_file()
    assert (built_site / "404.html").is_file()
    # GitHub Pages runs Jekyll by default; .nojekyll is what keeps our
    # vendored/vendor directory and underscore-free tree intact.
    assert (built_site / ".nojekyll").is_file()


def test_sitemap_is_absolute_and_hides_internals(built_site):
    xml = (built_site / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    assert locs, "sitemap must list pages"
    assert all(loc.startswith("https://example.test/atlas/") for loc in locs), (
        "sitemap loc entries must be absolute"
    )
    # Repository scaffolding must not be advertised to crawlers.
    assert not any("/.github/" in loc for loc in locs)
    assert not any(loc.endswith("/404.html") for loc in locs), (
        "an error page must never be listed in a sitemap"
    )


def test_robots_points_at_the_sitemap(built_site):
    robots = (built_site / "robots.txt").read_text(encoding="utf-8")
    assert "User-agent: *" in robots
    assert "Sitemap: https://example.test/atlas/sitemap.xml" in robots


def test_pages_carry_canonical_and_share_metadata(built_site):
    for page in (built_site / "index.html", built_site / "404.html"):
        text = page.read_text(encoding="utf-8")
        assert 'rel="canonical"' in text
        assert 'property="og:url"' in text
        assert 'property="og:title"' in text
        assert 'name="twitter:card"' in text
        assert 'href=""' not in text, "no empty href may be emitted"


def test_local_build_omits_origin_metadata(build_site, tmp_path):
    """A build without --site-url must not emit canonical/og:url at all."""
    out = tmp_path / "local-site"
    assert build_site.build(out, "/", "", "en") == 0
    text = (out / "index.html").read_text(encoding="utf-8")
    assert "og:url" not in text
    assert 'rel="canonical"' not in text
    # but the crawler-independent artifacts still exist
    assert (out / "robots.txt").is_file()
    assert not (out / "sitemap.xml").exists()


def test_progressive_enhancement_preserved(built_site):
    """Cards are server-rendered; JS only adds search on top."""
    index_html = _html_index(built_site)
    assert 'class="cards"' in index_html
    assert "card-link" in index_html
    # The search index is data, not markup — its absence cannot break browsing.
    assert (built_site / "search-index.json").is_file()


def test_pack_chapter_nav_is_collapsible(built_site):
    """Long chapter lists collapse on mobile via <details>, stay open on desktop."""
    nav = next(p for p in (built_site / "packs").rglob("*.html")
               if "packnav" in p.read_text(encoding="utf-8"))
    text = nav.read_text(encoding="utf-8")
    assert "<details" in text and "navgroup" in text
    assert 'aria-current="page"' in text


def test_top_nav_is_a_details_toggle_on_mobile(built_site):
    index_html = _html_index(built_site)
    assert 'class="navmenu"' in index_html
    assert "☰" in index_html


def test_search_index_includes_cjk_ngrams(built_site):
    """Chinese queries need n-grams: Fuse tokenizes on whitespace only."""
    records = json.loads((built_site / "search-index.json").read_text(encoding="utf-8"))
    assert records, "index must not be empty"
    for record in records:
        assert "n" in record, "every index record needs the n-gram field"
    # At least one record in the bilingual repo must actually have n-grams.
    assert any(record.get("n") for record in records)


def test_chinese_prose_is_language_tagged(built_site):
    """Screen readers need lang="zh-CN" on Chinese-dominant blocks."""
    tagged = [p for p in built_site.rglob("*.html")
              if 'lang="zh-CN"' in p.read_text(encoding="utf-8")]
    assert tagged, "the bilingual catalog must annotate Chinese content"


def test_internal_links_all_resolve(build_site, built_site):
    """The builder's own link checker must report nothing broken."""
    assert build_site.verify_internal_links(built_site) == []


def test_nojekyll_present_and_empty(built_site):
    nojekyll = built_site / ".nojekyll"
    assert nojekyll.read_text(encoding="utf-8") == ""


def test_pages_workflow_preserves_nojekyll(build_site, built_site):
    """The deploy must keep `.nojekyll` in the artifact.

    `pages.yml` uses actions/upload-pages-artifact, which from v4 excludes
    dotfiles unless `include-hidden-files: true` is set — verified against the
    action's own action.yml, where the default is "false" and tar receives
    `--exclude=.[^/]*`. The site emits `.nojekyll`, so a version bump without
    that input silently drops it and GitHub Pages starts running its Jekyll
    build over the catalog. This test is the tripwire for the next bump.
    """
    assert (built_site / ".nojekyll").exists(), "the build must emit .nojekyll"

    text = (build_site.ROOT / ".github" / "workflows" / "pages.yml").read_text(
        encoding="utf-8"
    )
    version = re.search(r"upload-pages-artifact@v(\d+)", text)
    assert version, "could not determine the upload-pages-artifact version"
    if int(version.group(1)) >= 4:
        assert re.search(r"include-hidden-files:\s*true", text), (
            "actions/upload-pages-artifact v4+ excludes dotfiles by default; "
            "`include-hidden-files: true` is required or `.nojekyll` is lost "
            "and GitHub Pages will Jekyll-build the catalog"
        )


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
    html_out, _plain, _toc = build_site.render_markdown(src)
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


# --------------------------------------------------------------------------- #
# Language annotation, n-grams, canonical URLs
# --------------------------------------------------------------------------- #

def test_abs_url_joins_and_tolerates_empty_base(build_site):
    assert build_site.abs_url("https://x.test/", "index.html") == "https://x.test/index.html"
    assert build_site.abs_url("https://x.test", "/a/b.html") == "https://x.test/a/b.html"
    # An unset origin must yield "" (no bogus canonical), not "None/…".
    assert build_site.abs_url("", "index.html") == ""


def test_cjk_ngrams_splits_runs_only(build_site):
    grams = build_site.cjk_ngrams("一网通办 OEE WMS")
    # 3+3 chars → bigrams+trigrams of one run; ASCII words are not n-grammed.
    assert "一网" in grams and "网通" in grams and "网通办" in grams
    assert "OEE" not in grams and "WMS" not in grams


def test_cjk_ngrams_tolerates_empty_input(build_site):
    assert build_site.cjk_ngrams("") == ""
    assert build_site.cjk_ngrams("pure ascii text") == ""


def test_annotate_lang_tags_chinese_blocks(build_site):
    html = '<p>仓储管理系统的库存账实相符原则</p>'
    out = build_site.annotate_lang(html)
    assert 'lang="zh-CN"' in out
    assert out.startswith('<p lang="zh-CN">')


def test_annotate_lang_leaves_english_alone(build_site):
    html = "<p>The WMS shall keep physical and financial inventory consistent.</p>"
    assert build_site.annotate_lang(html) == html


def test_annotate_lang_respects_existing_lang(build_site):
    html = '<p lang="en">一网通办</p>'
    out = build_site.annotate_lang(html)
    assert out.count("lang=") == 1
    assert 'lang="en"' in out


def test_annotate_lang_skips_code_blocks(build_site):
    """Source snippets are not natural language and must not be marked zh."""
    html = "<pre><code>SELECT 凭证号 FROM 表</code></pre>"
    assert build_site.annotate_lang(html) == html


def test_annotate_lang_handles_attributes_and_ids(build_site):
    html = '<h2 id="盘点">循环盘点规格</h2>'
    out = build_site.annotate_lang(html)
    assert 'id="盘点"' in out and 'lang="zh-CN"' in out


def test_annotate_lang_ignores_whitespace_only_blocks(build_site):
    html = "<p>   </p>"
    assert build_site.annotate_lang(html) == html


def test_vendored_assets_are_pinned(build_site):
    """VENDOR_EXPECTED pins every vendored file, so an upgrade must re-record provenance."""
    vendored = build_site.VENDOR_EXPECTED
    assert {"fuse.min.js", "mermaid.min.js"} <= set(vendored)
    for value in vendored.values():
        assert value.startswith("sha384-"), "supply-chain pin must be a SHA-384 SRI"


# --------------------------------------------------------------------------- #
# Structured spec view: the pack overview renders its own ID graph
# --------------------------------------------------------------------------- #

def _pack_overview(out: Path, slug: str) -> str:
    return (out / "packs" / "horizontal" / slug / "index.html").read_text(encoding="utf-8")


def test_pack_overview_renders_the_spec_panel(built_site):
    html_text = _pack_overview(built_site, "workflow-bpm")
    assert '<section class="spec"' in html_text
    # counts a reader can scan, each linking to its section
    assert html_text.count('class="stat"') >= 6
    assert 'id="sec-adr"' in html_text and 'id="sec-req"' in html_text and 'id="sec-con"' in html_text


def test_spec_panel_is_server_rendered_not_js_built(built_site):
    """Progressive enhancement: the panel must exist before any script runs."""
    html_text = _pack_overview(built_site, "workflow-bpm")
    # Identifiers are present in the HTML itself, not fetched at runtime.
    for ident in ("ADR-0004", "BR-05", "FR-013", "NFR-007"):
        assert f"spec-{ident}" in html_text, f"{ident} missing from rendered HTML"


def test_view_switch_is_usable_without_javascript(built_site):
    html_text = _pack_overview(built_site, "workflow-bpm")
    assert 'id="vs-doc"' in html_text and 'id="vs-spec"' in html_text
    # The radios are siblings of the two views so CSS alone can toggle them.
    doc = html_text.find('id="vs-spec"')
    assert html_text.find('<div class="layout">', doc) > doc
    assert html_text.find('<section class="spec"', doc) > doc


def test_structured_index_is_emitted_for_every_pack(built_site):
    data = json.loads((built_site / "data" / "pack-index.json").read_text(encoding="utf-8"))
    slugs = {p["slug"] for p in data["packs"]}
    assert len(slugs) >= 17
    assert data["totals"]["rules"] > 100
    assert data["totals"]["requirements"] > 100


def test_spec_panel_and_json_never_disagree(built_site):
    """The page and the data file are two views of one extraction.

    If these diverge, one of them is lying about the corpus — and the site's
    whole value is that it does not.
    """
    data = json.loads((built_site / "data" / "pack-index.json").read_text(encoding="utf-8"))
    entry = next(p for p in data["packs"] if p["slug"] == "workflow-bpm")
    html_text = _pack_overview(built_site, "workflow-bpm")

    # every identifier the extractor found is on the page as its own row
    missing = [
        item["id"]
        for key in ("rules", "requirements", "nfrs", "controls", "adrs")
        for item in entry[key]
        if f'id="spec-{item["id"]}"' not in html_text
    ]
    assert not missing, f"identifiers extracted but not rendered: {missing[:8]}"
    for n, _c in enumerate(entry["constraints"], start=1):
        assert f'id="spec-con-{n}"' in html_text


def test_extraction_quality_badges_are_shown(built_site):
    """A pack with an unparsable section must show it, not hide it."""
    html_text = _pack_overview(built_site, "workflow-bpm")
    assert 'class="sq structured"' in html_text


def test_store_enforced_constraints_are_flagged(built_site):
    data = json.loads((built_site / "data" / "pack-index.json").read_text(encoding="utf-8"))
    entry = next(p for p in data["packs"] if p["slug"] == "workflow-bpm")
    assert entry["counts"]["store_constraints"] > 0
    html_text = _pack_overview(built_site, "workflow-bpm")
    assert "store-enforced" in html_text


def test_non_overview_pages_do_not_get_a_spec_toggle(built_site):
    """The switch appears where there is something to switch to."""
    html_text = (built_site / "packs" / "horizontal" / "workflow-bpm" / "AGENTS.html").read_text(
        encoding="utf-8"
    )
    assert 'id="vs-spec"' not in html_text


def test_prose_view_is_still_the_default(built_site):
    html_text = _pack_overview(built_site, "workflow-bpm")
    assert 'id="vs-doc" checked' in html_text


# --------------------------------------------------------------------------- #
# Prompt bundles: assembled from the pack, never hand-written
# --------------------------------------------------------------------------- #

def _prompt_dir(out: Path, slug: str) -> Path:
    return out / "packs" / "horizontal" / slug / "prompts"


def test_prompt_files_are_emitted_per_pack(built_site):
    """A pack with nothing to say gets none; one with content gets the set."""
    prompts = sorted(built_site.rglob("prompts/*.md"))
    assert len(prompts) > 200, f"only {len(prompts)} prompt files emitted"
    names = {p.name for p in prompts}
    assert {"context.md", "implement.md"} <= names
    # no double-prefixed names survive: ADR-0004 -> adr-0004.md
    assert not [n for n in names if n.startswith("adr-adr-")]


def test_emitted_prompt_carries_the_packs_own_content(built_site):
    text = (_prompt_dir(built_site, "workflow-bpm") / "implement.md").read_text(encoding="utf-8")
    for token in ("BR-05", "ADR-0004", "store-enforced", "verification: unverified"):
        assert token in text, f"prompt omits {token}"


def test_adr_prompt_lists_what_was_ruled_out(built_site):
    """The winner alone lets a model re-derive the loser."""
    text = (_prompt_dir(built_site, "workflow-bpm") / "adr-0004.md").read_text(encoding="utf-8")
    assert "Ruled out" in text
    assert "Leave the terms to the implementation" in text
    assert "Choose a vendor's definitions" in text


def test_pack_page_offers_a_copy_button_and_real_files(built_site):
    html_text = (built_site / "packs" / "horizontal" / "workflow-bpm" / "index.html").read_text(
        encoding="utf-8"
    )
    assert 'data-copy="prm-implement"' in html_text
    assert 'id="prm-implement"' in html_text
    for href in ("prompts/implement.md", "prompts/context.md", "prompts/adr-0004.md"):
        assert href in html_text, f"{href} is emitted but not linked"
        assert (built_site / "packs" / "horizontal" / "workflow-bpm" / href).is_file()


def test_prompt_links_resolve_to_emitted_files(built_site):
    """A link to a file that was not written is the failure this guards."""
    import re

    for pack_dir in sorted((built_site / "packs").glob("*/*/prompts")):
        index = pack_dir.parent / "index.html"
        if not index.is_file():
            continue
        html_text = index.read_text(encoding="utf-8")
        for link in re.findall(r'href="([^"]*prompts/[^"]+)"', html_text):
            rel = link.split("#", 1)[0].split("?", 1)[0]
            if rel.startswith(("http", "//")):
                continue
            assert (index.parent / rel).is_file(), f"{index.relative_to(built_site)} -> {rel}"


def test_copy_script_is_an_enhancement_not_a_prerequisite(built_site):
    """Without JS the prompts are still real, openable files."""
    html_text = (built_site / "packs" / "horizontal" / "workflow-bpm" / "index.html").read_text(
        encoding="utf-8"
    )
    assert "assets/prompt-copy.js" in html_text
    assert (built_site / "assets" / "prompt-copy.js").is_file()
    other = (built_site / "packs" / "horizontal" / "workflow-bpm" / "AGENTS.html").read_text(
        encoding="utf-8"
    )
    assert "prompt-copy.js" not in other


def test_prompt_section_declares_its_provenance(built_site):
    """A prompt a reader cannot trace to a generator is a hardcoded template."""
    html_text = (built_site / "packs" / "horizontal" / "workflow-bpm" / "index.html").read_text(
        encoding="utf-8"
    )
    assert "tools/prompts.py" in html_text

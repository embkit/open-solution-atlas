# -*- coding: utf-8 -*-
"""Tests for the bilingual build: two trees, one switch.

A site that offers two languages has to answer a question the single-language
build never had to: when the reader switches, does the *prose* change? A
switch that only repaints the chrome leaves Chinese navigation over English
prose - a page in two languages at once, which reads as neither.

The bilingual build answers it by giving each language its own tree at the
same URL space, and by making the switch a link between the two trees.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ALT_RE = re.compile(
    r'<body[^>]*data-build-lang="(?P<lang>[\w-]+)"[^>]*'
    r'data-alt-en="(?P<en>[^"]*)"[^>]*data-alt-zh="(?P<zh>[^"]*)"'
)


@pytest.fixture(scope="module")
def bilingual(build_site, tmp_path_factory) -> Path:
    """The repository built in both languages, once."""
    out = tmp_path_factory.mktemp("bilingual-site")
    assert build_site.build_bilingual(out, "/", "") == 0
    return out


def _tree_pages(site: Path, prefix: str) -> list[Path]:
    """The pages of one tree.

    The English tree is the output root, so the Chinese tree lives inside it
    as a directory; walking the root has to stop at that directory or the two
    trees are counted twice.
    """
    root = site / prefix if prefix else site
    pages = []
    for page in sorted(root.rglob("*.html")):
        parts = page.relative_to(root).parts
        if "demo" in parts:
            continue
        if not prefix and parts and parts[0] == "zh":
            continue
        pages.append(page)
    return pages


def test_both_trees_are_built(bilingual):
    assert (bilingual / "index.html").is_file()
    assert (bilingual / "zh" / "index.html").is_file()


def test_the_two_trees_share_one_url_space(bilingual):
    """A translation is a sibling file, so the pages have the same names.

    If this ever fails, the switch cannot be a link: the counterpart of a
    page would not exist.
    """
    en = {p.relative_to(bilingual).as_posix() for p in _tree_pages(bilingual, "")}
    zh = {p.relative_to(bilingual / "zh").as_posix()
          for p in _tree_pages(bilingual, "zh")}
    assert en == zh


def test_every_page_points_at_its_counterpart(bilingual):
    """The switch is a link, so the link has to resolve to a real page."""
    broken = []
    for tree, other in (("", "zh"), ("zh", "")):
        for page in _tree_pages(bilingual, tree):
            match = ALT_RE.search(page.read_text(encoding="utf-8"))
            assert match, f"{page} has no counterpart link"
            href = match.group("en") if other == "" else match.group("zh")
            if not href:
                continue
            target = (page.parent / href).resolve()
            if not target.is_file():
                broken.append(f"{page} -> {href}")
    assert broken == [], f"counterpart links that resolve to nothing: {broken[:10]}"


def test_each_page_declares_the_language_it_is_written_in(bilingual):
    for tree, lang in (("", "en"), ("zh", "zh")):
        for page in _tree_pages(bilingual, tree):
            match = ALT_RE.search(page.read_text(encoding="utf-8"))
            assert match, f"{page} has no language declaration"
            assert match.group("lang") == lang, f"{page} declares the wrong tree"


def test_the_switch_leaves_the_reader_on_the_other_language(bilingual):
    """The Chinese catalog must be Chinese, and the English one English.

    Before the two trees, both catalogs were the same file in two languages'
    worth of chrome, which is how the mix got there in the first place.
    """
    zh = (bilingual / "zh" / "index.html").read_text(encoding="utf-8")
    en = (bilingual / "index.html").read_text(encoding="utf-8")
    assert "生产级蓝图" in zh, "the Chinese catalog must be in Chinese"
    assert "生产级蓝图" not in en, "the English catalog must not be"
    assert "Blueprint" in en or "blueprint" in en.lower()


def test_the_runtime_follows_the_counterpart_instead_of_repainting(i18n):
    """Repainting the chrome is the failure mode; navigating is the fix."""
    js = i18n.render_i18n_js()
    assert "altUrl" in js, "the runtime must know where the other tree is"
    assert "location.replace" in js or "location.href" in js, (
        "the runtime must navigate to the other language's page"
    )

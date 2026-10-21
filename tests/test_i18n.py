"""Tests for the site's internationalisation layer (tools/i18n.py + build).

The layer exists because the chrome used to mix languages *within one page* —
an English nav above a Chinese spec panel. These tests hold the two halves of
that apart: the build renders one language completely, and the client's
dictionary can render the other without a second build.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# The catalog itself
# --------------------------------------------------------------------------- #


def test_every_key_has_both_languages(i18n):
    """A half-translated string is worse than a build that stops."""
    gaps = [
        f"{key}: missing {lang}"
        for key, entry in i18n.STRINGS.items()
        for lang in i18n.LOCALES
        if lang not in entry or not str(entry[lang]).strip()
    ]
    assert gaps == [], f"incomplete catalog: {gaps}"


def test_no_placeholder_mismatch_between_languages(i18n):
    """`{n}` must appear on both sides or one language renders a raw token."""
    bad = []
    for key, entry in i18n.STRINGS.items():
        en = set(re.findall(r"\{(\w+)\}", entry["en"]))
        zh = set(re.findall(r"\{(\w+)\}", entry["zh"]))
        if en != zh:
            bad.append(f"{key}: en={sorted(en)} zh={sorted(zh)}")
    assert bad == [], f"placeholder sets differ: {bad}"


def test_unknown_key_and_missing_translation_raise(i18n):
    with pytest.raises(KeyError):
        i18n.t("no.such.key")
    with pytest.raises(KeyError):
        i18n.t("skip", "fr")


def test_t_fills_placeholders(i18n):
    assert i18n.t("spec.head", "en", total=72) == "Spec panel · 72 identifiers"
    assert i18n.t("spec.head", "zh", total=72) == "规格面板 · 72 条已识别标识"
    assert i18n.t("view.spec.count", "zh", n=72) == " · 72 条标识"
    assert i18n.t("prompt.ctx.blurb", "en", n="99,730").startswith("99,730 characters")


def test_strings_carry_no_markup(i18n):
    """The client re-renders these with `textContent`; markup would be shown
    as text (or, worse, half-swapped alongside the `<code>` beside it)."""
    markup = [
        f"{key}[{lang}]"
        for key, entry in i18n.STRINGS.items()
        for lang, text in entry.items()
        if re.search(r"[<>]|&[a-z]+;", text)
    ]
    assert markup == [], f"values contain markup: {markup}"


def test_strings_carry_no_single_quotes(i18n):
    """`data-i18n-vars` and friends are single-quoted attributes; an apostrophe
    inside a value would terminate the attribute."""
    quoted = [
        f"{key}[{lang}]"
        for key, entry in i18n.STRINGS.items()
        for lang, text in entry.items()
        if "'" in text
    ]
    assert quoted == [], f"values contain a single quote: {quoted}"


def test_generated_runtime_is_deterministic_and_complete(i18n):
    js = i18n.render_i18n_js()
    assert js == i18n.render_i18n_js(), "the generated runtime must be reproducible"
    assert "__DICTIONARY__" not in js
    assert "window.OSA_I18N" in js
    # every key is present in the client's dictionary, or the switch would
    # leave that element's text as its own key name
    for key in i18n.STRINGS:
        assert f'"{key}": ' in js, f"{key} missing from the generated runtime"
        assert '"en"' in js and '"zh"' in js
    # the dictionary parses as JSON on its own
    match = re.search(r"var STRINGS = (\{.*?\});\n", js, re.DOTALL)
    assert match, "the runtime must declare its dictionary"
    assert json.loads(match.group(1)) == i18n.dictionary()
    # Both cross-language navigations carry the fragment. A deep link like
    # #spec names a place on the page; a redirect that rebuilds the URL and
    # drops it lands the reader on the right page in the wrong place.
    assert "location.replace(target + window.location.hash)" in js
    assert "location.href = target + window.location.hash" in js


# --------------------------------------------------------------------------- #
# The build's half
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="module")
def i18n_site(build_site, tmp_path_factory) -> Path:
    """The real repository built once, in English, for the chrome assertions."""
    out = tmp_path_factory.mktemp("i18n-site")
    assert build_site.build(out, "/", "", "en") == 0
    return out


@pytest.fixture(scope="module")
def zh_i18n_site(build_site, tmp_path_factory) -> Path:
    """The same repository built in Chinese.

    A key that only the Chinese build renders (the translation-fallback
    notice) is referenced by the site, not dead vocabulary ? so the scan for
    dead keys has to look at both builds.
    """
    out = tmp_path_factory.mktemp("zh-i18n-site")
    assert build_site.build(out, "/", "", "zh") == 0
    return out


I18N_MARKERS = re.compile(
    r'data-i18n(?:-(?:placeholder|aria-label|title))?="([^"]+)"'
)


def _pages(site):
    """Every page the shell renders.

    The demos are excluded on purpose: each one is a bespoke, self-contained
    page written for its pack's own domain (会签, 办件, 凭证号…), so its UI is
    content rather than chrome. The link *to* it is chrome and is translated.
    """
    return [p for p in sorted(site.rglob("*.html"))
            if "demo" not in p.relative_to(site).parts]


def test_built_chrome_defaults_to_english(i18n_site):
    """`--lang en` must not render Chinese chrome — that was the mix."""
    offenders = []
    for page in _pages(i18n_site):
        text = page.read_text(encoding="utf-8")
        for m in re.finditer(r'data-i18n="([^"]+)"[^>]*>([^<]*)<', text):
            key, value = m.group(1), m.group(2)
            if key == "lang.zh":
                continue
            if re.search(r"[\u3400-\u9fff]", value):
                offenders.append(f"{page.name}: {key} -> {value.strip()[:40]}")
    assert offenders == [], f"Chinese in the default English chrome: {offenders[:10]}"


def test_every_data_i18n_key_exists_in_the_catalog(i18n_site, i18n):
    """A typo'd key would leave the element's text as the key name after a
    switch — loud, but only for the readers who switch."""
    used: set[str] = set()
    for page in _pages(i18n_site):
        text = page.read_text(encoding="utf-8")
        used |= set(I18N_MARKERS.findall(text))
    missing = sorted(k for k in used if k not in i18n.STRINGS)
    assert missing == [], f"keys used in markup but not in the catalog: {missing}"


def test_the_runtime_is_offered_on_every_page(i18n_site):
    """The switch lives in the titlebar, so the runtime that drives it has to
    be on every page — including the generated listings."""
    for page in _pages(i18n_site):
        assert "assets/i18n.js" in page.read_text(encoding="utf-8"), (
            f"{page.name} has no language runtime"
        )


def test_the_runtime_asset_is_emitted_and_parses(i18n_site):
    asset = i18n_site / "assets" / "i18n.js"
    assert asset.is_file(), "the build must emit assets/i18n.js"
    text = asset.read_text(encoding="utf-8")
    match = re.search(r"var STRINGS = (\{.*?\});\n", text, re.DOTALL)
    assert match
    data = json.loads(match.group(1))
    assert data["nav.catalog"]["zh"] == "目录"


def test_every_key_is_referenced_somewhere(i18n_site, zh_i18n_site, i18n, build_site):
    """A key nothing references is dead vocabulary.

    The catalog is the site's glossary, and an entry nobody reads is a claim
    the site does not make — it will be wrong the day someone trusts it. A key
    may be referenced by the markup (`data-i18n`, server-rendered) or by a
    runtime asset (`app.js`, `prompt-copy.js`), which writes strings the
    server never sees.
    """
    referenced: set[str] = set()
    for site in (i18n_site, zh_i18n_site):
        for page in _pages(site):
            referenced |= set(I18N_MARKERS.findall(page.read_text(encoding="utf-8")))
    assets = Path(__file__).resolve().parent.parent / "tools" / "site-assets"
    for name in ("app.js", "prompt-copy.js"):
        text = (assets / name).read_text(encoding="utf-8")
        referenced |= set(re.findall(r'"([a-z][a-z0-9._]*)"', text))
    # A key the server-rendered templates use is referenced too: the build
    # writes it into the page directly - a <title>, a <meta description> -
    # where there is no element to carry a `data-i18n` marker.
    build = (Path(__file__).resolve().parent.parent / "tools" / "build-site.py")
    source = build.read_text(encoding="utf-8")
    referenced |= set(re.findall(r'_t\(\s*"([^"]+)"', source))
    referenced |= set(re.findall(r'_ia\(\s*"([^"]+)"', source))
    referenced |= set(re.findall(r'_span\(\s*"([^"]+)"', source))
    referenced |= set(re.findall(r'_iaa\(\s*"[^"]+"\s*,\s*"([^"]+)"', source))
    # The enum tables reference their keys by construction: an L4 pack cannot
    # exist today, but the pill must not fall back to a raw "L4" when one is
    # promoted, so the vocabulary is complete even though the markup is not.
    for table in (build_site.MATURITY_LABEL, build_site.VERIFICATION_LABEL):
        referenced |= {key for key, _kind in table.values()}
    dead = sorted(k for k in i18n.STRINGS if k not in referenced)
    assert dead == [], f"catalog keys nothing references: {dead}"


def test_the_switch_marks_exactly_one_language_pressed(i18n_site, build_site):
    for page in [i18n_site / "index.html", i18n_site / "404.html"]:
        text = page.read_text(encoding="utf-8")
        pressed = re.findall(r'data-locale="(\w+)"[^>]*aria-pressed="(\w+)"', text)
        assert len(pressed) == 2, f"{page.name}: {pressed}"
        assert sorted(p for _, p in pressed) == ["false", "true"], (
            f"{page.name}: exactly one language must be pressed"
        )


def test_chinese_build_renders_chinese_chrome(zh_i18n_site, i18n_site):
    """The other half of the switch: the build's own language argument must
    actually reach every template, not only `<html lang>`."""
    out = zh_i18n_site
    index = (out / "index.html").read_text(encoding="utf-8")
    assert '<html lang="zh-CN">' in index
    assert "生产级蓝图" in index, "the catalog hero must follow --lang zh"
    assert (out / "assets" / "i18n.js").is_file()

    def spec_page(site):
        pages = [p for p in site.rglob("index.html")
                 if 'class="spec tabp tabp-spec"' in p.read_text(encoding="utf-8")]
        assert pages, "a pack overview with a structured panel must exist"
        return pages[0].read_text(encoding="utf-8")

    zh_spec = spec_page(out)
    en_spec = spec_page(i18n_site)
    assert "规格面板" in zh_spec, "the spec panel must follow --lang zh"
    assert "规格面板" not in en_spec, "the English build must not carry it"
    assert "被引用：" in zh_spec and "Referenced by:" in en_spec
    # the tab bar and the demo panel are chrome, and they follow the build too
    assert 'data-i18n="tab.overview">概览' in zh_spec
    assert 'data-i18n="tab.overview">Overview' in en_spec
    assert 'data-i18n="demo.head">交互演示' in zh_spec
    assert 'data-i18n="demo.head">Interactive demo' in en_spec
    # and the catalog's shelf headings are chrome as well
    assert "数据与智能平台" in index
    assert "Warehouses, lakes" not in index


def test_unknown_language_fails_the_build(build_site, tmp_path):
    assert build_site.build(tmp_path / "bad", "/", "", "fr") == 1


def test_browser_language_detection_is_in_the_runtime(i18n):
    js = i18n.render_i18n_js()
    assert 'navigator.language' in js and '"zh"' in js
    assert "localStorage" in js, "the choice must survive a reload"

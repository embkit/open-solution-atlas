#!/usr/bin/env python3
"""build-site.py — render this repository into a static, searchable website.

Reads the 17 pack manifests and every Markdown file, and emits a self-contained
static site into ``_site/`` (the GitHub Pages artifact):

    _site/index.html              the catalog: cards + search + facets
    _site/search-index.json       Fuse.js index (pack + document granularity)
    _site/assets/{style.css,app.js}
    _site/packs/<domain>/<slug>/  the pack, mirrored (<name>.md -> <name>.html,
                                  README.md -> index.html, directories get an
                                  index.html)
    _site/docs/…                  the standard, taxonomy, roadmap
    _site/overview.html           the root README

Design notes
- **Progressive enhancement**: every result is server-rendered, so the site is
  fully browsable with JavaScript disabled; JS only adds search + facet
  filtering.
- **No runtime dependency** beyond `markdown` (already in requirements.txt).
  Search is client-side via Fuse.js and diagrams render via mermaid.js, both
  loaded from a CDN on pages that need them.
- **Links keep working**: relative `.md` links are rewritten to `.html`,
  `README.md` to `index.html`, and directories to their generated `index.html`.

Usage:  python tools/build-site.py [--out _site] [--base-url /]
Exit:   0 = built; 1 = a pack failed to parse.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover
    print("ERROR: Markdown is required (pip install -r requirements.txt)", file=sys.stderr)
    sys.exit(2)

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required (pip install -r requirements.txt)", file=sys.stderr)
    sys.exit(2)

# tools/pack_index.py is the content model — the one place that knows how a
# pack's Markdown turns into typed records. The rendering layer imports it
# rather than keeping a second URL mapping that could drift from the first.
try:
    from pack_index import build_index as build_pack_index
    from pack_index import doc_url as _doc_url
except ImportError:  # loaded via importlib without tools/ on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from pack_index import build_index as build_pack_index
    from pack_index import doc_url as _doc_url

try:
    from prompts import build_bundles, bundle_filename
except ImportError:  # loaded via importlib without tools/ on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from prompts import build_bundles, bundle_filename

# The icon set and category palette are hand-drawn to the contract's spec
# (stroke 2, round caps, 24 viewBox) because this repository takes no runtime
# dependency; contract §3.1 permits exactly that. The category colours come
# from contract §1.4 and appear only on an icon's stroke and its tint.
try:
    from site_icons import category_for, icon, icon_for
except ImportError:  # loaded via importlib without tools/ on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from site_icons import category_for, icon, icon_for

# The chrome's vocabulary. A page renders one language at build time (--lang)
# and the reader may switch to the other at runtime; both come from here, so
# they cannot drift apart.
try:
    from i18n import (
        DEFAULT_LOCALE,
        HTML_LANG,
        LOCALES,
        has,
        render_i18n_js,
        t,
    )
except ImportError:  # loaded via importlib without tools/ on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from i18n import (
        DEFAULT_LOCALE,
        HTML_LANG,
        LOCALES,
        has,
        render_i18n_js,
        t,
    )

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"
DOCS_DIR = ROOT / "docs"
ASSETS_SRC = Path(__file__).resolve().parent / "site-assets"
VENDOR_SRC = ASSETS_SRC / "vendor"

# Third-party assets are vendored, never loaded from a CDN: the catalog must
# keep working with no network access (or with a blocked CDN — see the
# project's audience). VENDOR_EXPECTED pins the provenance of each file so an
# accidental or malicious change fails the build loudly; the values are the
# official jsdelivr hashes recorded in tools/site-assets/vendor/README.md.
VENDOR_EXPECTED = {
    # fuse.js v7.0.0 — official jsdelivr hash, verified on vendoring
    "fuse.min.js": "sha384-PCSoOZTpbkikBEtd/+uV3WNdc676i9KUf01KOA8CnJotvlx8rRrETbDuwdjqTYvt",
    # mermaid v11.4.1 — official jsdelivr hash, verified on vendoring
    "mermaid.min.js": "sha384-rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I",
}

# The four primary-nav destinations. `nav_current` is matched against these
# keys; the attribute is set only where the link *is* the page, because
# `aria-current="page"` says exactly that and a section highlight would need a
# different token.
#
# The fourth field is a key into `i18n.STRINGS`, not a literal label: the nav is
# chrome, so the reader's language decides what it says.
NAV_ITEMS = (
    ("catalog", "index.html", "grid", "nav.catalog"),
    ("standard", "docs/pack-standard.v1.html", "book", "nav.standard"),
    ("taxonomy", "docs/taxonomy.html", "network", "nav.taxonomy"),
    ("roadmap", "docs/roadmap.html", "route", "nav.roadmap"),
)

# URL -> the nav key whose link is that page.
NAV_PAGE = {url: key for key, url, _glyph, _label in NAV_ITEMS if url != "index.html"}
NAV_PAGE["index.html"] = "catalog"


def primary_nav(prefix: str, current: str = "", lang: str = DEFAULT_LOCALE) -> str:
    """The primary navigation as one `<nav>`.

    Rendered twice per page — once inline in the titlebar, once inside the
    `<details>` that replaces it below 820px — because a closed `<details>`
    hides its contents in the UA stylesheet, so a single copy inside the
    disclosure is invisible on desktop. Only one copy is ever displayed, so only
    one reaches the accessibility tree.
    """
    links = []
    for key, url, glyph, i18n_key in NAV_ITEMS:
        cur = ' aria-current="page"' if current == key else ""
        links.append(
            f'<a href="{prefix}{url}"{cur}{_ia(i18n_key)}>'
            f'{icon_glyph(glyph)}{_t(i18n_key, lang)}</a>'
        )
    return f'<nav class="topnav" aria-label="Primary">{"".join(links)}</nav>'


# The maturity and verification vocabularies. Values are keys into
# `i18n.STRINGS` because they are chrome: a pack's state shown in the reader's
# language, not the raw record.
# The build language also chooses the *content* language. The chrome has a
# vocabulary in `i18n.py`; the prose lives in the packs, and a Chinese build
# reads the translated files where they exist.
CONTENT_LOCALE = {"en": None, "zh": "zh-CN"}


#: `business-rules.zh-CN.md` -> base `business-rules`, locale `zh-CN`.
LOCALE_TAG_RE = re.compile(r"^(?P<base>.+)\.(?P<locale>[a-z]{2}(?:-[A-Z]{2})?)$")


#: Where each language's tree lives inside a bilingual build. The English tree
#: is the site root; the Chinese tree is a directory beside it. Both trees
#: share one URL space - a translation is a sibling file, not a parallel tree
#: of pages - so the counterpart of a page is the same relative path under the
#: other prefix. Switching language is therefore a path change, not a repaint:
#: the reader lands on a page whose prose is in the language they asked for.
LOCALE_TREE = {"en": "", "zh": "zh/"}


def tree_href(rel: str, tree_prefix: str, alt_prefix: str) -> str:
    """The path from a page to its counterpart in the other language's tree.

    `rel` is the page's path inside its own tree (`packs/mes/README.html`).
    The counterpart is the same path under the other tree's prefix, reached
    from the page's own directory - so the number of `..` is the depth of the
    page inside the *output* directory, which is one deeper for a tree that is
    itself a directory.
    """
    depth = rel.count("/") + tree_prefix.count("/")
    return "../" * depth + alt_prefix + rel


BODY_TAG_RE = re.compile(r'<body class="([^"]*)">')
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]*)">')


def inject_language_links(tree_dir: Path, lang: str, tree_prefix: str,
                           alt_prefix: str, site_url: str = "") -> int:
    """Teach every page in a tree where its counterpart lives.

    The switch in the titlebar is chrome, so the shell renders it; but *where*
    the other language's page is depends on the page, and only the page knows
    its own path. This pass writes that answer into the page: `data-alt-en` and
    `data-alt-zh` on the body, the canonical link and the `hreflang`
    alternates in the head.

    Without it the switch can only repaint the chrome, which is how a Chinese
    reader ends up with Chinese navigation over English prose - a page in two
    languages at once, which is worse than a page in one.
    """
    alt_lang = "zh" if lang == "en" else "en"
    touched = 0
    for page in sorted(tree_dir.rglob("*.html")):
        rel = page.relative_to(tree_dir).as_posix()
        counterpart = tree_href(rel, tree_prefix, alt_prefix)
        alts = {"en": "", "zh": ""}
        alts[alt_lang] = counterpart
        text = page.read_text(encoding="utf-8")

        def body_sub(match: re.Match, alts: dict = alts) -> str:
            attrs = " ".join(
                f'data-alt-{code}="{html.escape(value, quote=True)}"'
                for code, value in alts.items()
            )
            return (f'<body class="{match.group(1)}" data-build-lang="{lang}" '
                    f"{attrs}>")

        new = BODY_TAG_RE.sub(body_sub, text, count=1)
        if site_url:
            canonical = abs_url(site_url, tree_prefix + rel)
            new = CANONICAL_RE.sub(
                lambda m, url=canonical: f'<link rel="canonical" href="{url}">',
                new, count=1,
            )
            alternates = "".join(
                f'<link rel="alternate" hreflang="{HTML_LANG[code]}" '
                f'href="{abs_url(site_url, LOCALE_TREE[code] + rel)}">\n'
                for code in ("en", "zh")
            )
            new = new.replace(
                '<link rel="canonical"', alternates + '<link rel="canonical"', 1
            )
        if new != text:
            page.write_text(new, encoding="utf-8", newline="")
            touched += 1
    return touched


def locale_of(path: Path) -> str | None:
    """The locale a source file is written in, or None for an original."""
    if path.suffix != ".md":
        return None
    match = LOCALE_TAG_RE.match(path.stem)
    return match.group("locale") if match else None


def is_translation_source(path: Path) -> bool:
    """True when the file is a translation rather than a page of its own.

    A translation is never published as a separate page: it is rendered
    *instead of* the original, at the original's URL.

    The repository root's `README.<locale>.md` is the one exception, and it
    is a deliberate one. Those two files are two *front doors* ? the English
    README and the Chinese one, each linking to the other ? not one page
    written twice. The English README links to `./README.zh-CN.md`, so that
    file has to exist as a page in every build, or the link is a 404.
    """
    if "translations" in path.parts:
        return True
    if locale_of(path) is None:
        return False
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        return True
    return not (len(rel.parts) == 1 and rel.stem.startswith("README."))


def content_source(src: Path, locale: str | None) -> tuple[Path, bool]:
    """The file to read for `src` in `locale`, and whether it is a translation.

    A translation is a *sibling*: `business-rules.zh-CN.md` beside
    `business-rules.md`. The URL space is therefore identical in both
    languages, so a relative link inside a translation points at the page a
    Chinese reader wants without a single rewrite.
    """
    if locale and src.suffix == ".md":
        alt = src.with_name(src.stem + "." + locale + ".md")
        if alt.is_file():
            return alt, True
    return src, False


MATURITY_LABEL = {
    "L1": ("maturity.L1", "m1"),
    "L2": ("maturity.L2", "m2"),
    "L3": ("maturity.L3", "m3"),
    "L4": ("maturity.L4", "m4"),
}
VERIFICATION_LABEL = {
    "unverified": ("verify.unverified", "v0"),
    "source-checked": ("verify.source-checked", "v1"),
    "practitioner-reviewed": ("verify.practitioner-reviewed", "v2"),
    "field-proven": ("verify.field-proven", "v3"),
}

# Big search bodies are truncated so the index stays a reasonable download.
MAX_DOC_TEXT = 6000
MAX_PACK_TEXT = 12000


@dataclass
class Doc:
    """One rendered Markdown file."""

    src: Path                 # absolute source path
    rel: str                  # path relative to ROOT (posix)
    url: str                  # site-relative output path (posix)
    title: str
    html: str = ""
    text: str = ""
    toc: list = field(default_factory=list)
    # True when the rendered body came from a translation. A Chinese build
    # says so on the page, so a reader is never left guessing whether the
    # English they are reading is a gap or a quote.
    translated: bool = False


@dataclass
class Pack:
    slug: str
    domain: str
    subdomain: str
    manifest: dict
    rel_dir: str
    docs: list[Doc] = field(default_factory=list)

    @property
    def title(self) -> str:
        return str(self.manifest.get("title", self.slug))

    @property
    def title_zh(self) -> str:
        return str(self.manifest.get("title_zh", ""))

    def display_title(self, lang: str = DEFAULT_LOCALE) -> str:
        """The title in the reader's language.

        The English build shows the English title with the Chinese beneath it,
        because a bilingual key asset is the norm here. The Chinese build
        shows the Chinese title alone: the two would otherwise say the same
        thing twice, with the English first.
        """
        if lang == "zh" and self.title_zh:
            return self.title_zh
        return self.title

    @property
    def maturity(self) -> str:
        return str(self.manifest.get("maturity", "L1"))

    @property
    def verification(self) -> str:
        return str(self.manifest.get("verification", "unverified"))

    @property
    def tags(self) -> list[str]:
        return [str(t) for t in (self.manifest.get("tags") or [])]

    @property
    def index_url(self) -> str:
        return f"{self.rel_dir}/index.html"


# --------------------------------------------------------------------------- #
# Markdown rendering
# --------------------------------------------------------------------------- #

MERMAID_FENCE = re.compile(r"```mermaid[ \t]*\n(.*?)```", re.DOTALL)
HREF_RE = re.compile(r'href="([^"]+)"')
SKIP_LINK_PREFIX = ("http://", "https://", "mailto:", "#", "tel:", "ftp://", "//")


def _protect_mermaid(text: str) -> tuple[str, list[str]]:
    """Pull fenced mermaid blocks out before Markdown parsing.

    mermaid syntax contains ``-->`` and ``|`` which the Markdown/HTML pipeline
    would mangle. The blocks are swapped for opaque tokens and restored after.
    """
    blocks: list[str] = []

    def swap(match: re.Match[str]) -> str:
        blocks.append(match.group(1))
        return f"\n\nMERMAIDTOKEN{len(blocks) - 1}ENDTOKEN\n\n"

    return MERMAID_FENCE.sub(swap, text), blocks


def _restore_mermaid(html_text: str, blocks: list[str]) -> str:
    def swap(match: re.Match[str]) -> str:
        raw = blocks[int(match.group(1))]
        return f'<pre class="mermaid">{html.escape(raw.strip())}</pre>'

    return re.sub(
        r"(?:<p>)?MERMAIDTOKEN(\d+)ENDTOKEN(?:</p>)?", swap, html_text
    )


def _rewrite_link(target: str) -> str:
    """Map a relative Markdown link target to its generated HTML URL."""
    if target.startswith(SKIP_LINK_PREFIX) or "://" in target:
        return target
    path, sep, frag = target.partition("#")
    if not path:
        return target
    if path.endswith(".md"):
        path = path[: -len(".md")] + ".html"
        if path == "README.html" or path.endswith("/README.html"):
            path = path[: -len("README.html")] + "index.html"
    elif path.endswith("/"):
        path = path + "index.html"
    return path + (sep + frag if sep else "")


def _rewrite_links(html_text: str) -> str:
    return HREF_RE.sub(lambda m: f'href="{_rewrite_link(m.group(1))}"', html_text)


def render_markdown(text: str) -> tuple[str, str, list]:
    """Return (html, plain_text, toc_tokens)."""
    protected, blocks = _protect_mermaid(text)
    md = markdown.Markdown(
        extensions=["extra", "toc", "sane_lists", "admonition"],
        extension_configs={"toc": {"permalink": False}},
    )
    body = md.convert(protected)
    body = _restore_mermaid(body, blocks)
    body = _rewrite_links(body)
    plain = re.sub(r"<[^>]+>", " ", body)
    plain = html.unescape(re.sub(r"\s+", " ", plain)).strip()
    return body, plain, getattr(md, "toc_tokens", [])


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


# --------------------------------------------------------------------------- #
# Language annotation & canonical URLs
# --------------------------------------------------------------------------- #

# CJK ideographs (incl. extension A + compatibility), CJK punctuation and
# full-width forms — enough to detect a Chinese-dominant block element.
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3000-\u303f\uff00-\uffef]")
TAG_STRIP_RE = re.compile(r"<[^>]+>")
# Block elements that may hold a CJK-dominant paragraph. `pre`/`code` are
# deliberately excluded: source snippets are not natural language.
LANG_BLOCK_RE = re.compile(
    r"<(p|h1|h2|h3|h4|h5|h6|li|td|th|blockquote)((?:\s[^>]*)?)>(.*?)</\1>",
    re.DOTALL,
)
LANG_MIN_RATIO = 0.3  # >=30% CJK characters ⇒ the element is Chinese


def annotate_lang(html_text: str) -> str:
    """Tag predominantly Chinese block elements with ``lang="zh-CN"``.

    The catalog UI is English, but the pack prose — especially glossary
    entries, requirement bodies and 公文-specific notes — is frequently Chinese.
    Without an explicit ``lang``, screen readers switch to an English
    pronunciation engine and the text becomes unintelligible. The element keeps
    its existing attributes; a page-level ``lang`` is never overwritten.
    """
    def repl(match: re.Match) -> str:
        tag, attrs, inner = match.group(1), match.group(2), match.group(3)
        if "lang=" in attrs:
            return match.group(0)  # already explicit — respect it
        text = TAG_STRIP_RE.sub(" ", html.unescape(inner))
        letters = [c for c in text if c.isalpha() or CJK_RE.match(c)]
        if not letters:
            return match.group(0)
        cjk = sum(1 for c in letters if CJK_RE.match(c))
        if cjk / len(letters) < LANG_MIN_RATIO:
            return match.group(0)
        return f"<{tag}{attrs} lang=\"zh-CN\">{inner}</{tag}>"

    return LANG_BLOCK_RE.sub(repl, html_text)


def abs_url(site_url: str, rel: str) -> str:
    """Absolute canonical URL for a site-relative path (or "" if unset)."""
    base = (site_url or "").strip().rstrip("/")
    if not base:
        return ""
    return f"{base}/{rel.lstrip('/')}"


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #

INDEX_ROW_RE = re.compile(
    r"^\|\s*\[(?P<name>[^\]]+)\]\((?P<path>[^)]+)\)\s*\|(?P<rest>.+)\|\s*$"
)


def load_summaries(locale: str | None = None) -> dict[str, str]:
    """Parse packs/README.md's index table into {slug: summary}.

    The Chinese build reads `packs/README.zh-CN.md`, whose table carries the
    Chinese one-line summaries the cards show.
    """
    index = PACKS_DIR / "README.md"
    if locale:
        translated = PACKS_DIR / f"README.{locale}.md"
        if translated.is_file():
            index = translated
    summaries: dict[str, str] = {}
    if not index.exists():
        return summaries
    for line in index.read_text(encoding="utf-8").splitlines():
        match = INDEX_ROW_RE.match(line)
        if not match:
            continue
        path = match.group("path").strip().rstrip("/")
        if not path.startswith("./"):
            continue
        slug = path.split("/")[-1]
        cells = [c.strip() for c in match.group("rest").split("|")]
        if cells:
            summaries[slug] = cells[-1]
    return summaries


def discover_markdown() -> list[Path]:
    """Every Markdown file that belongs on the site.

    Excludes hidden directories (``.github``, ``.pytest_cache`` …) and
    non-content trees (``templates/`` is scaffolding, ``site-assets/`` holds
    vendored libraries, ``tests/`` is test code, ``_site/`` is output).

    Build outputs are excluded by their **leading underscore**, not by name:
    the build target is whichever directory a caller passes with ``--out``
    (``_site``, ``_compat_site`` …), and the emitted prompt bundles are
    Markdown — so a content scanner that only knew about ``_site`` treated a
    previous build's ``prompts/*.md`` as repository content, and the CI
    compatibility job, which builds before it tests, built a site containing
    its own prompts.
    """
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.md")):
        parts = path.relative_to(ROOT).parts
        if any(part.startswith((".", "_")) for part in parts):
            continue
        # node_modules is a tool install (the kit's browser verifiers resolve
        # Playwright from there), and templates/ and tests/ are scaffolding and
        # test code. None of them is content, and a scanner that missed one of
        # them fails the build with links inside somebody else's README.
        if "templates" in parts or "tests" in parts or "node_modules" in parts:
            continue
        if "site-assets" in parts:  # vendored third-party libs, not content
            continue
        if is_translation_source(path):
            # A translation is rendered instead of its original, at the
            # original's URL. Publishing it as well would give the site two
            # pages per chapter and two sets of links to keep in step.
            continue
        files.append(path)
    return files


def url_for(src: Path) -> str:
    """Map a source Markdown path to its site-relative output URL.

    Delegates to ``pack_index.doc_url`` so the mapping lives in exactly one
    place; the pack-root and repo-root special cases stay here because they
    are properties of the site's output layout, not of the content model.
    """
    rel = src.relative_to(ROOT).as_posix()
    if rel == "README.md":
        return "overview.html"
    return _doc_url(rel)


def load_packs(summaries: dict[str, str]) -> list[Pack]:
    packs: list[Pack] = []
    for manifest_path in sorted(PACKS_DIR.glob("*/*/manifest.yaml")):
        pack_dir = manifest_path.parent
        try:
            data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"[ERROR] {manifest_path}: {exc}", file=sys.stderr)
            continue
        if not isinstance(data, dict):
            continue
        slug = str(data.get("slug", pack_dir.name))
        if summary := summaries.get(slug):
            data["_summary"] = summary
        packs.append(
            Pack(
                slug=slug,
                domain=str(data.get("domain", pack_dir.parent.name)),
                subdomain=str(data.get("subdomain", "")),
                manifest=data,
                rel_dir=pack_dir.relative_to(ROOT).as_posix(),
            )
        )
    return packs


# --------------------------------------------------------------------------- #
# HTML templates
# --------------------------------------------------------------------------- #

HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="canonical" href="">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:site_name" content="Open Solution Atlas">
<meta name="twitter:card" content="summary">
<!-- The browser's own chrome on mobile: the contract's page ground, so the
     address bar matches the sheet rather than keeping a palette alive outside
     the stylesheet. One value, because the site has one theme. -->
<meta name="theme-color" content="#f6f9fc">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='24' font-size='24'>{icon}</text></svg>">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body class="{body_class}">
<a class="skip" href="#main" data-i18n="skip">Skip to content</a>
<header class="titlebar">
  <a class="brand" href="{prefix}index.html"><span class="brand-mark">{brand_icon}</span> Solution&nbsp;Atlas</a>
  {nav_inline}
  {langswitch}
  <details class="navmenu">
    <summary data-i18n-aria-label="nav.menu.label"><span class="navmenu-icon">{menu_icon}</span><span data-i18n="nav.menu">Menu</span></summary>
    {nav_menu}
  </details>
</header>
<main id="main">
"""

# The page's fixed furniture. Everything a reader can read here is chrome, so
# the literals are placeholders the shell fills from the catalog — a page built
# with `--lang zh` must not say "Skip to content".
HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="canonical" href="">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:site_name" content="Open Solution Atlas">
<meta name="twitter:card" content="summary">
<!-- The browser's own chrome on mobile: the contract's page ground, so the
     address bar matches the sheet rather than keeping a palette alive outside
     the stylesheet. One value, because the site has one theme. -->
<meta name="theme-color" content="#f6f9fc">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='24' font-size='24'>{icon}</text></svg>">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body class="{body_class}">
<a class="skip" href="#main" data-i18n="skip">{skip_text}</a>
<header class="titlebar">
  <a class="brand" href="{prefix}index.html"><span class="brand-mark">{brand_icon}</span> Solution&nbsp;Atlas</a>
  {nav_inline}
  {langswitch}
  <details class="navmenu">
    <summary data-i18n-aria-label="nav.menu.label"><span class="navmenu-icon">{menu_icon}</span><span data-i18n="nav.menu">{menu_text}</span></summary>
    {nav_menu}
  </details>
</header>
<main id="main">
"""

# Same rule as `HEAD`: the defaults are placeholders. `str.format` cannot name
# a field with a dot in it, so the shell replaces the markers directly.
FOOT_MARKERS = {
    "footer.lead": "— blueprints for real enterprise systems.",
    "footer.content": "Content ",
    "footer.comma": ", ",
    "footer.code": "code ",
    "footer.end": ".",
    "footer.draft": "Every pack is ",
    "footer.and": " and ",
    "footer.not_verified": "not field-verified",
    "footer.trust.lead": "— read its ",
    "footer.trust.tail": ".",
}
FOOT_TEMPLATE = """</main>
<footer class="sitefoot">
  <p><strong>Open Solution Atlas</strong> <span data-i18n="footer.lead">@footer.lead@</span>
     <span data-i18n="footer.content">@footer.content@</span> <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a><span data-i18n="footer.comma">@footer.comma@</span><span data-i18n="footer.code">@footer.code@</span> <a href="https://opensource.org/license/mit">MIT</a><span data-i18n="footer.end">@footer.end@</span>
     <span data-i18n="footer.draft">@footer.draft@</span> <code>llm-drafted</code><span data-i18n="footer.and">@footer.and@</span><strong data-i18n="footer.not_verified">@footer.not_verified@</strong>
     <span data-i18n="footer.trust.lead">@footer.trust.lead@</span> <code>SOURCES.md</code><span data-i18n="footer.trust.tail">@footer.trust.tail@</span></p>
</footer>
@scripts@
</body>
</html>
"""


def foot(lang: str = DEFAULT_LOCALE) -> str:
    """The page's closing furniture, in `lang`."""
    out = FOOT_TEMPLATE
    for key in FOOT_MARKERS:
        out = out.replace(f"@{key}@", _t(key, lang))
    return out.replace("@scripts@", "{scripts}")


def langswitch(lang: str = DEFAULT_LOCALE) -> str:
    """The language control: two states, exactly one pressed.

    It is chrome that has to live in the titlebar, so it lives there — once.
    On the narrow layout the nav folds into the `<details>`, but the switch is
    small enough to stay beside the brand, which is where a reader looks for it
    either way. The labels are the languages' own names, so they never change.
    """
    return (
        '<div class="langswitch" role="group"'
        + _iaa("aria-label", "lang.switch")
        + ">"
        + '<button type="button" data-locale="en" lang="en"'
        + (' aria-pressed="true"' if lang == "en" else ' aria-pressed="false"')
        + _ia("lang.en")
        + f">{_t('lang.en', lang)}</button>"
        + '<button type="button" data-locale="zh" lang="zh-CN"'
        + (' aria-pressed="true"' if lang == "zh" else ' aria-pressed="false"')
        + _ia("lang.zh")
        + f">{_t('lang.zh', lang)}</button>"
        + "</div>"
    )


def page_shell(
    *,
    title: str,
    description: str,
    prefix: str,
    body: str,
    body_class: str = "doc",
    icon: str = "◈",
    scripts: str = "",
    lang: str = DEFAULT_LOCALE,
    canonical: str = "",
    nav_current: str = "",
) -> str:
    nav = primary_nav(prefix, nav_current, lang)
    head = HEAD.format(
        title=html.escape(title), description=html.escape(description),
        prefix=prefix, body_class=body_class, icon=icon,
        # `<html lang>` takes a *language tag*, not the catalog's locale
        # key: `--lang zh` is the switch's value, `zh-CN` is what a document
        # declares.
        lang=HTML_LANG.get(lang, lang), canonical=canonical,
        brand_icon=icon_glyph("grid"),
        menu_icon=icon_glyph("menu"),
        skip_text=_t("skip", lang), menu_text=_t("nav.menu", lang),
        nav_inline=nav,
        nav_menu=nav,
        langswitch=langswitch(lang),
    )
    # og:url and a canonical link are only meaningful once the site's public
    # origin is known; without it, drop the elements entirely rather than emit
    # `href=""` (which some crawlers treat as a self-referential duplicate).
    if canonical:
        head = head.replace(
            '<link rel="canonical" href="">',
            f'<link rel="canonical" href="{canonical}">\n'
            f'<meta property="og:url" content="{canonical}">',
        )
    else:
        head = head.replace('<link rel="canonical" href="">\n', "")
    # The language runtime is the one script every page needs — it is what makes
    # the titlebar's switch work — so it is loaded here rather than by each
    # caller, and it goes first: `defer` preserves document order, and the
    # page-specific modules read `window.OSA_I18N` when they run.
    scripts = f'<script src="{prefix}assets/i18n.js" defer></script>' + scripts
    return (
        head
        + body
        + foot(lang).replace("{scripts}", scripts)
    )


def breadcrumb(prefix: str, pack: Pack | None) -> str:
    if not pack:
        return ""
    chev = icon("chevron")
    return (
        '<nav class="crumbs">'
        f'<a href="{prefix}index.html"{_ia("crumb.catalog")}>{_t("crumb.catalog")}</a>{chev}'
        f'<span>{html.escape(pack.domain)}</span>{chev}'
        f'<span class="crumb-cur">{html.escape(pack.slug)}</span>'
        "</nav>"
    )


def icon_glyph(name: str) -> str:
    """The icon helper, named once so the templates read as markup."""
    return icon(name)


def pill(label: str, kind: str, attrs: str = "") -> str:
    return f'<span class="pill {kind}"{attrs}>{html.escape(label)}</span>'


def pack_pills(pack: Pack, lang: str = DEFAULT_LOCALE) -> str:
    """Maturity and verification, as chrome: the record's state in the
    reader's language, with the raw value kept in the data attributes the
    catalog's facets filter on."""
    m_key, m_kind = MATURITY_LABEL.get(pack.maturity, (None, "m1"))
    v_key, v_kind = VERIFICATION_LABEL.get(pack.verification, (None, "v0"))
    m_label = _t(m_key, lang) if m_key else _esc(pack.maturity)
    v_label = _t(v_key, lang) if v_key else _esc(pack.verification)
    return (
        pill(m_label, m_kind, _ia(m_key) if m_key else "")
        + pill(v_label, v_kind, _ia(v_key) if v_key else "")
    )


def render_sidebar(pack: Pack, doc: Doc, prefix: str, lang: str = DEFAULT_LOCALE) -> str:
    """The pack's sidebar: contract §4.2's three parts.

    Head (logo square, product name, subtitle), navigation, and a footer that
    carries the trust state. The sidebar is `--surface` on a `--page` ground —
    the contract calls that lightness difference the key to the page's
    left/right layering, so it is not flattened.
    """
    v_key, _kind = VERIFICATION_LABEL.get(pack.verification, (None, "v0"))
    state = _t(v_key, lang) if v_key else _esc(pack.verification)
    foot = (
        '<div class="side-foot">'
        f'<p{_ia(v_key) if v_key else ""}>{icon("shield")} {state}</p>'
        f'<p>{icon("mail")} <a href="{prefix}docs/pack-standard.v1.html"{_ia("side.standard")}>'
        f'{_t("side.standard", lang)}</a></p>'
        "</div>"
    )
    return (
        '<aside class="sidebar">'
        '<div class="side-head">'
        f'<span class="side-logo">{icon(icon_for(pack.domain, pack.slug))}</span>'
        '<span><span class="side-name">Solution Atlas</span><br>'
        f'<span class="side-sub">{html.escape(pack.domain)}</span></span>'
        "</div>"
        + nav_tree(pack, doc.url, prefix, lang)
        + foot
        + "</aside>"
    )


def nav_tree(pack: Pack, current_url: str, prefix: str,
             lang: str = DEFAULT_LOCALE) -> str:
    """Sidebar: the pack's files grouped by their chapter directory.

    Groups render as ``<details>``: on desktop CSS keeps them open (they are
    short), so the nav looks unchanged; below 760px the same markup becomes
    collapsible, which keeps an L3 pack's 40+ chapters from burying the page.
    """
    groups: dict[str, list[Doc]] = {}
    for doc in pack.docs:
        rel_inside = Path(doc.rel).relative_to(pack.rel_dir).as_posix()
        if "/" in rel_inside:
            groups.setdefault(rel_inside.split("/")[0], []).append(doc)
        else:
            groups.setdefault("", []).append(doc)
    # Contract §4.2: a three-part sidebar with 36px rows, and the active item a
    # solid primary pill rather than a tint.
    out = ['<nav class="packnav" aria-label="Pack chapters">']
    for group in sorted(groups):
        # The group's own name is a file path, so it is data; only the synthesised
        # "overview" group is chrome.
        if not group:
            label, label_key = _t("side.overview", lang), "side.overview"
        else:
            label, label_key = group, None
        docs = sorted(groups[group], key=lambda d: d.rel)
        # The open group is the one holding the page you are on, so a reader on a
        # phone sees their own chapter without opening anything.
        opened = " open" if any(d.url == current_url for d in docs) else ""
        items = []
        for doc in docs:
            rel_inside = Path(doc.rel).relative_to(pack.rel_dir).as_posix()
            name = Path(rel_inside).name
            name = _t("side.overview", lang) if name == "README.md" else name[:-3]
            active = ' class="active" aria-current="page"' if doc.url == current_url else ""
            href = prefix + doc.url
            items.append(f'<li><a{active} href="{href}">{html.escape(name)}</a></li>')
        out.append(
            f'<details class="navgroup"{opened}>'
            f'<summary class="navgroup-label"{_ia(label_key) if label_key else ""}>'
            f'{html.escape(label)}</summary>'
            f'<ul>{"".join(items)}</ul></details>'
        )
    out.append("</nav>")
    return "".join(out)


def render_toc(toc_tokens: list) -> str:
    """The chapter's "on this page" rail.

    A sub-list nests *inside* its parent ``<li>``. Emitting it as the ``<li>``'s
    next sibling is the shape that is easy to write and invalid to ship: a
    ``<ul>`` may contain ``<li>``, ``<script>`` or ``<template>`` and nothing
    else, so axe-core reported a serious ``list`` violation on every chapter
    page. The rail carries no other structure, so fixing the nesting was the
    whole of it.
    """
    if not toc_tokens:
        return ""

    def walk(tokens, level=0):
        if level > 2:
            return ""
        items = []
        for tok in tokens:
            children = walk(tok.get("children", []), level + 1)
            items.append(
                "<li>"
                f'<a href="#{html.escape(tok["id"])}">{html.escape(tok["name"])}</a>'
                f"{children}"
                "</li>"
            )
        inner = "".join(items)
        return f"<ul>{inner}</ul>" if inner else ""

    return (
        '<aside class="toc" aria-label="On this page">'
        '<span class="toc-label">On this page</span>'
        f"{walk(toc_tokens)}"
        "</aside>"
    )


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

def build(out: Path, base_url: str, site_url: str = "",
          lang: str = DEFAULT_LOCALE) -> int:
    if lang not in LOCALES:
        print(f"ERROR: unknown --lang {lang!r}", file=sys.stderr)
        return 1
    locale = CONTENT_LOCALE.get(lang)
    summaries = load_summaries(locale)
    packs = load_packs(summaries)
    if not packs:
        print("ERROR: no packs found", file=sys.stderr)
        return 1

    # The structured index is extracted once and shared by the renderer and
    # the emitted JSON, so a page and the data file can never disagree.
    pack_index = build_pack_index(locale)
    spec_entries = {p["slug"]: p for p in pack_index["packs"]}

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # Render every pack document.
    for pack in packs:
        pack_dir = ROOT / pack.rel_dir
        for src in sorted(pack_dir.rglob("*.md")):
            if is_translation_source(src):
                continue
            content, translated = content_source(src, locale)
            text = content.read_text(encoding="utf-8")
            body_html, plain, toc = render_markdown(text)
            pack.docs.append(
                Doc(
                    src=src,
                    rel=src.relative_to(ROOT).as_posix(),
                    url=url_for(src),
                    title=first_heading(text, Path(src).stem),
                    html=body_html,
                    text=plain,
                    toc=toc,
                    translated=translated,
                )
            )

    # Render non-pack Markdown (docs/, root files, the packs index).
    other_docs: list[Doc] = []
    for src in discover_markdown():
        rel = src.relative_to(ROOT).as_posix()
        if rel.startswith("packs/") and rel != "packs/README.md":
            continue
        content, translated = content_source(src, locale)
        text = content.read_text(encoding="utf-8")
        body_html, plain, toc = render_markdown(text)
        other_docs.append(
            Doc(
                src=src, rel=rel, url=url_for(src),
                title=first_heading(text, Path(src).stem),
                html=body_html, text=plain, toc=toc,
                translated=translated,
            )
        )

    # ---- write pack pages -------------------------------------------------
    for pack in packs:
        for doc in pack.docs:
            depth = doc.url.count("/")
            prefix = "../" * depth
            body = render_doc_page(
                pack, doc, prefix, site_url, lang,
                spec_entry=spec_entries.get(pack.slug),
            )
            write(out / doc.url, body)

    # ---- write non-pack pages --------------------------------------------
    for doc in other_docs:
        depth = doc.url.count("/")
        prefix = "../" * depth
        body = render_plain_page(doc, prefix, site_url, lang)
        write(out / doc.url, body)

    # Non-Markdown files that prose links to (openapi.yaml, the schema, tool
    # sources…) must exist in the output or those links 404 on the site.
    copied = copy_linked_files(out)

    # LICENSE has no .md extension and may be linked; copy it too.
    license_file = ROOT / "LICENSE"
    if license_file.exists() and not (out / "LICENSE").exists():
        shutil.copy2(license_file, out / "LICENSE")
        copied += 1

    # ---- catalog page + search index --------------------------------------
    write(out / "index.html", render_catalog(packs, base_url, site_url, lang, spec_entries))
    write(out / "search-index.json", json.dumps(build_index(packs, other_docs), ensure_ascii=False))
    # The structured index is the machine-readable surface of the catalog: the
    # same records the spec panels render, for a client-side traceability
    # explorer or a code generator.
    write(out / "data/pack-index.json", json.dumps(pack_index, ensure_ascii=False))

    # Prompt bundles, assembled from each pack so they cannot go stale. Emitted
    # as files rather than inlined, because the context bundle alone is ~100 KB
    # and a page should not carry every prompt's text to copy one of them.
    prompts_written = 0
    for pack in packs:
        entry = spec_entries.get(pack.slug)
        if not entry:
            continue
        bundles = build_bundles(entry, ROOT / pack.rel_dir, lang, locale)
        for fname, text in bundles["files"].items():
            write(out / pack.rel_dir / "prompts" / fname, text)
            prompts_written += 1

    # Interactive demos. They are hand-written per pack — bespoke, because a
    # generated demo demonstrates the engine rather than the pack — so they are
    # copied verbatim, and `10-demo/demo.json` declares which pack IDs each one
    # demonstrates so a drifting demo fails check-ids instead of quietly
    # asserting a decision that no longer exists.
    demos_copied = 0
    for pack in packs:
        src_dir = ROOT / pack.rel_dir / "10-demo"
        if not src_dir.is_dir():
            continue
        for asset in sorted(src_dir.iterdir()):
            if not asset.is_file():
                continue
            # Only HTML is served; the manifest is data for the checker and the
            # index, and has nothing to render as a page of its own.
            if asset.suffix not in (".html", ".css", ".js"):
                continue
            dest = out / pack.rel_dir / "demo" / asset.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, dest)
            demos_copied += 1

    # ---- assets ------------------------------------------------------------
    assets_out = out / "assets"
    assets_out.mkdir(exist_ok=True)
    # Only .js is copied as a script asset; prompt-copy.js is the copy-button
    # enhancement and is loaded selectively by the pages that need it.
    for asset in ASSETS_SRC.iterdir():
        if not asset.is_file() or asset.suffix not in (".js", ".css"):
            continue
        shutil.copy2(asset, assets_out / asset.name)
    # The language runtime is the one *generated* script: the dictionary lives in
    # tools/i18n.py next to the Python side of the same strings, and this inlines
    # it, so a build's chrome and its runtime can never disagree. Deterministic,
    # because it is derived from the source and nothing else.
    write(assets_out / "i18n.js", render_i18n_js())
    # The vendored directory is copied recursively; a missing or altered file
    # fails the build (supply-chain tripwire) rather than shipping a broken UI.
    vendor_out = assets_out / "vendor"
    vendor_out.mkdir(exist_ok=True)
    for name, expected in VENDOR_EXPECTED.items():
        src = VENDOR_SRC / name
        if not src.is_file():
            print(f"[ERROR] missing vendored asset: {name}", file=sys.stderr)
            return 1
        actual = "sha384-" + base64.b64encode(hashlib.sha384(src.read_bytes()).digest()).decode()
        if actual != expected:
            print(f"[ERROR] vendored asset {name} fails integrity check "
                  f"({actual} != {expected})", file=sys.stderr)
            return 1
        shutil.copy2(src, vendor_out / name)

    # Any directory still lacking an index.html gets a generated listing, so
    # links to a directory (…/docs/, …/packs/) resolve.
    generated = generate_missing_indexes(out, lang)

    # ---- crawler-facing artifacts -----------------------------------------
    write_sitemap(out, site_url)
    write_robots(out, site_url)
    write_404(out, site_url, lang)

    # GitHub Pages runs Jekyll by default, which would ignore `vendor` and the
    # underscore-prefixed internal files; `.nojekyll` disables that.
    (out / ".nojekyll").write_text("", encoding="utf-8")

    pages = sum(1 for _ in out.rglob("*.html"))
    # `out` may legitimately live outside the repo (tests build into tmp_path),
    # so fall back to the absolute path instead of raising.
    try:
        where = out.relative_to(ROOT).as_posix()
    except ValueError:
        where = out.as_posix()
    print(
        f"built {pages} pages, {len(packs)} packs, "
        f"{copied} linked asset(s), {generated} generated index(es) -> {where}/"
    )
    x = pack_index["totals"]
    print(
        f"structured index: {x['rules']} rules, {x['requirements']} requirements, "
        f"{x['nfrs']} NFRs, {x['controls']} controls, {x['adrs']} ADRs, "
        f"{x['constraints']} constraints ({x['store_constraints']} store-enforced)"
    )
    print(f"emitted {prompts_written} prompt file(s), {demos_copied} demo file(s)")

    broken = verify_internal_links(out)
    if broken:
        print(f"[ERROR] {len(broken)} broken internal link(s):")
        for path in broken[:20]:
            print(f"  {path}")
        if len(broken) > 20:
            print(f"  … and {len(broken) - 20} more")
        return 1
    print("internal links: all resolve")
    return 0


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# --------------------------------------------------------------------------- #
# Structured ("spec") view
# --------------------------------------------------------------------------- #

# Sections in the order a reader wants them: the decision, then what it
# constrains, then what it is measured by, then where it is enforced.
SPEC_SECTIONS = (
    ("adrs", "Architecture decisions", "adr"),
    ("rules", "Business rules", "rule"),
    ("requirements", "Functional requirements", "req"),
    ("nfrs", "Non-functional targets", "nfr"),
    ("controls", "Compliance controls", "ctl"),
    ("constraints", "Data-model constraints", "con"),
    ("capabilities", "Capabilities", "cap"),
    ("contexts", "Bounded contexts", "ctx"),
)


def _esc(text) -> str:
    return html.escape(str(text))


def _t(key: str, lang: str = DEFAULT_LOCALE, **vars) -> str:
    """One chrome string, rendered in `lang` and escaped for HTML.

    The literal lives in `i18n.STRINGS`; the `data-i18n` attribute emitted
    alongside it (`_ia`) is what lets the client render the same string in the
    other language without a second build.
    """
    return _esc(t(key, lang, **vars))


def _ia(key: str, **vars) -> str:
    """`data-i18n` + optional `data-i18n-vars`, for a text node.

    `vars` is a `key=value` list rather than JSON because these land inside
    Python format strings, where braces are not free.
    """
    out = f' data-i18n="{key}"'
    if vars:
        out += ' data-i18n-vars="' + " ".join(f"{k}={v}" for k, v in vars.items()) + '"'
    return out


def _span(key: str, lang: str = DEFAULT_LOCALE, **vars) -> str:
    """A chrome string as its own `<span>`, so the client replaces exactly it
    and nothing around it."""
    return f'<span{_ia(key, **vars)}>{_t(key, lang, **vars)}</span>'


def _iaa(attr: str, key: str, **vars) -> str:
    """The same, for a string that lives in an attribute (placeholder,
    aria-label, title) instead of a text node."""
    out = f' data-i18n-{attr}="{key}"'
    if vars:
        out += ' data-i18n-vars="' + " ".join(f"{k}={v}" for k, v in vars.items()) + '"'
    return out


def _id_chip(id_: str, kind: str, href: str | None = None) -> str:
    """An identifier that links to its own row, or stands alone if uncited."""
    if href:
        return f'<a class="chip idchip" href="{href}" data-id="{_esc(id_)}">{_esc(id_)}</a>'
    return f'<span class="chip idchip" data-id="{_esc(id_)}">{_esc(id_)}</span>'


def _spec_status_badges(entry: dict, lang: str = DEFAULT_LOCALE) -> str:
    """Per-section extraction quality — the honest part of the panel.

    A pack whose rules live in prose gets a visible `prose-only` badge rather
    than an empty table, so the gap is a fact a reader can act on instead of
    an impression the site quietly creates.
    """
    cells = []
    for key, _title, _cls in SPEC_SECTIONS:
        if key not in entry["sections"]:
            continue
        st = entry["sections"][key]["status"]
        n = entry["sections"][key]["count"]
        cells.append(
            f'<span class="sq {st}" title="{_esc(key)}"{_ia(f"spec.status.{st}")}>'
            + _t(f"spec.status.{st}", lang)
            + (f' <b>{n}</b>' if n else "")
            + "</span>"
        )
    return '<div class="spec-quality">' + "".join(cells) + "</div>"


def _reverse_refs(entry: dict) -> dict[str, list[str]]:
    """Who cites each identifier in this pack — the traceability index.

    Built from the traces the pack *already records*, so it adds no new claim:
    it is the same graph ``check-ids.py`` validates, presented as edges rather
    than as a lint result.
    """
    refs: dict[str, list[str]] = {}

    def add(src: str, targets) -> None:
        for tgt in targets:
            refs.setdefault(tgt, [])
            if src not in refs[tgt]:
                refs[tgt].append(src)

    for rule in entry["rules"]:
        add(rule["id"], rule["enforced_by"])
    for req in entry["requirements"]:
        add(req["id"], req["traces"])
    for nfr in entry["nfrs"]:
        add(nfr["id"], nfr.get("traces", []))
    for ctl in entry["controls"]:
        add(ctl["id"], ctl["requirements"] + ctl["rules"] + ctl["capabilities"])
    return refs


def _spec_row_chips(entry: dict, ids: list[str], kind: str) -> str:
    """Trace identifiers rendered as links to their own sections."""
    if not ids:
        return '<span class="dim">—</span>'
    return "".join(_id_chip(i, kind, f"#spec-{i}") for i in ids)


def render_spec_view(entry: dict, prefix: str, lang: str = DEFAULT_LOCALE) -> str:
    """The whole structured view for one pack.

    Server-rendered so the panel is complete with JavaScript disabled — the
    same progressive-enhancement rule the rest of the site is built on. The
    JSON index in ``data/pack-index.json`` is for the interactive layer, not a
    prerequisite for reading this.
    """
    counts = entry["counts"]
    total_ids = sum(counts[k] for k in ("rules", "requirements", "nfrs", "controls", "adrs", "constraints"))
    refs = _reverse_refs(entry)

    stats = [
        ("rules", "spec.stat.rules", counts["rules"]),
        ("requirements", "spec.stat.requirements", counts["requirements"]),
        ("nfrs", "spec.stat.nfrs", counts["nfrs"]),
        ("controls", "spec.stat.controls", counts["controls"]),
        ("adrs", "spec.stat.adrs", counts["adrs"]),
        ("constraints", "spec.stat.constraints", counts["constraints"]),
        ("store_constraints", "spec.stat.store", counts["store_constraints"]),
        ("policy_nfrs", "spec.stat.policy", counts["policy_nfrs"]),
    ]
    tiles = "".join(
        f'<a class="stat" href="#sec-{k}"{_ia(i18n_key)}><b>{v}</b>'
        f'<span>{_esc(t(i18n_key, lang))}</span></a>'
        for k, i18n_key, v in stats if v
    )

    jump = "".join(
        f'<a class="jump" href="#sec-{key}"{_ia(f"spec.sec.{key}")}>'
        f'{_t(f"spec.sec.{key}", lang)} · {counts.get(key, len(entry.get(key, [])))}</a>'
        for key, title, _ in SPEC_SECTIONS if counts.get(key, len(entry.get(key, [])))
    )

    sections: list[str] = []

    # ---- ADRs ------------------------------------------------------------
    if entry["adrs"]:
        rows = "".join(
            f'<tr id="spec-{_esc(a["id"])}"><th><code>{_esc(a["id"])}</code></th>'
            f'<td><b>{_esc(a["name"])}</b>'
            + (f'<p class="dec">{_esc(a["decision"])}</p>' if a["decision"] else "")
            + f'<p class="refs"{_ia("spec.refs.cited")}>{_t("spec.refs.cited", lang)}'
            + _spec_row_chips(entry, refs.get(a["id"], []), "ref") + "</p></td></tr>"
            for a in entry["adrs"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-adr" open><summary>'
            f'<span{_ia("spec.sec.adrs")}>{_t("spec.sec.adrs", lang)}</span> · '
            f'{len(entry["adrs"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- Business rules ---------------------------------------------------
    if entry["rules"]:
        rows = "".join(
            f'<tr id="spec-{_esc(r["id"])}"><th><code>{_esc(r["id"])}</code></th>'
            f'<td><b>{_esc(r["name"])}</b>'
            + (f'<p class="prop">{_esc(r["proposition"])}</p>' if r["proposition"] else "")
            + f'<p class="refs"{_ia("spec.refs.enforced")}>{_t("spec.refs.enforced", lang)}'
            + _spec_row_chips(entry, r["enforced_by"] + r["trace_adrs"], "ref") + "</p></td></tr>"
            for r in entry["rules"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-rule" open><summary>'
            f'<span{_ia("spec.sec.rules")}>{_t("spec.sec.rules", lang)}</span> · '
            f'{len(entry["rules"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- Functional requirements -----------------------------------------
    if entry["requirements"]:
        rows = "".join(
            f'<tr id="spec-{_esc(q["id"])}"><th><code>{_esc(q["id"])}</code></th>'
            f'<td><b>{_esc(q["name"])}</b>'
            + (f'<p class="ears"><span class="ears-k">WHEN</span> {_esc(q["when"])}</p>' if q["when"] else "")
            + (f'<p class="ears"><span class="ears-k">SHALL</span> {_esc(q["shall"])}</p>' if q["shall"] else "")
            + (f'<p class="ears not"><span class="ears-k">SHALL NOT</span> {_esc(q["shall_not"])}</p>' if q["shall_not"] else "")
            + f'<p class="refs"{_ia("spec.refs.traces")}>{_t("spec.refs.traces", lang)}'
            + _spec_row_chips(entry, q["traces"], "ref") + "</p></td></tr>"
            for q in entry["requirements"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-req" open><summary>'
            f'<span{_ia("spec.sec.requirements")}>{_t("spec.sec.requirements", lang)}</span> · '
            f'{len(entry["requirements"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- NFRs -------------------------------------------------------------
    if entry["nfrs"]:
        rows = "".join(
            f'<tr id="spec-{_esc(n["id"])}"><th><code>{_esc(n["id"])}</code></th>'
            f'<td><b>{_esc(n["name"])}</b>'
            + (f'<p class="tgt">{_esc(n["target"])}</p>' if n["target"] else "")
            + (f'<p class="fml"><code>{_esc(n["formula"])}</code></p>' if n["formula"] else "")
            + ('<p><span class="sq prose-only">policy (A)</span></p>' if n["is_policy"] else "")
            + "</td></tr>"
            for n in entry["nfrs"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-nfr"><summary>'
            f'<span{_ia("spec.sec.nfrs")}>{_t("spec.sec.nfrs", lang)}</span> · '
            f'{len(entry["nfrs"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- Controls ---------------------------------------------------------
    if entry["controls"]:
        rows = "".join(
            f'<tr id="spec-{_esc(c["id"])}"><th><code>{_esc(c["id"])}</code></th>'
            f'<td><b>{_esc(c["name"])}</b>'
            + (f'<p class="inst">{_esc(c["instrument_names"])}</p>' if c["instrument_names"] else "")
            + f'<p class="refs"{_ia("spec.refs.traces")}>{_t("spec.refs.traces", lang)}'
            + _spec_row_chips(entry, c["requirements"] + c["rules"] + c["capabilities"], "ref") + "</p></td></tr>"
            for c in entry["controls"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-ctl"><summary>'
            f'<span{_ia("spec.sec.controls")}>{_t("spec.sec.controls", lang)}</span> · '
            f'{len(entry["controls"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- Data-model constraints ------------------------------------------
    if entry["constraints"]:
        rows = "".join(
            f'<tr id="spec-con-{c["n"]}"><th><code>{c["n"]}</code></th>'
            f'<td>{_esc(c["text"])}'
            + (' <span class="sq structured"' + _iaa("title", "spec.store.tooltip") + '>store</span>'
               if c["store"] else "")
            + f'<p class="refs"{_ia("spec.refs.enforced")}>{_t("spec.refs.enforced", lang)}'
            + _spec_row_chips(entry, c["enforces"], "ref") + "</p></td></tr>"
            for c in entry["constraints"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-con"><summary>'
            f'<span{_ia("spec.sec.constraints")}>{_t("spec.sec.constraints", lang)}</span> · '
            f'{len(entry["constraints"])} '
            f'(<b>{counts["store_constraints"]}</b>'
            f'<span{_ia("spec.store.tail")}>{_t("spec.store.tail", lang)}</span>)</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- Capabilities -----------------------------------------------------
    if entry["capabilities"]:
        rows = "".join(
            f'<tr id="spec-{_esc(cp["id"])}"><th><code>{_esc(cp["id"])}</code></th>'
            f'<td><b>{_esc(cp["name"])}</b>'
            + (f'<p class="dim">{_esc(cp["one_liner"])}</p>' if cp["one_liner"] else "")
            + "</td></tr>"
            for cp in entry["capabilities"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-cap"><summary>'
            f'<span{_ia("spec.sec.capabilities")}>{_t("spec.sec.capabilities", lang)}</span> · '
            f'{len(entry["capabilities"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- Bounded contexts -------------------------------------------------
    if entry["contexts"]:
        rows = "".join(
            f'<tr id="spec-ctx-{_esc(ct["name"])}"><th>{_esc(ct["name"])}</th>'
            f'<td>{_esc(ct["responsibility"])}'
            + '<p class="owns">' + ", ".join(f'<code>{_esc(o)}</code>' for o in ct["owns"]) + "</p>"
            + "</td></tr>"
            for ct in entry["contexts"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-ctx"><summary>'
            f'<span{_ia("spec.sec.contexts")}>{_t("spec.sec.contexts", lang)}</span> · '
            f'{len(entry["contexts"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    demo = ""
    if entry.get("demo"):
        demo = (
            '<a class="demobtn" href="' + _esc(prefix + entry["demo"]["url"]) + '">'
            '<b data-i18n="spec.demo">' + _t("spec.demo", lang) + "</b><span>"
            + _esc(entry["demo"].get("title") or entry["slug"]) + "</span></a>"
        )

    return f"""
<section class="spec" id="spec">
  <div class="spec-head">
    <div>
      <h2{_ia("spec.head", total=total_ids)}>{_t("spec.head", lang, total=total_ids)}</h2>
      <p class="spec-note"><span{_ia("spec.note.by")}>{_t("spec.note.by", lang)}</span>
        <code>tools/pack_index.py</code> <span{_ia("spec.note.from")}>{_t("spec.note.from", lang)}</span>
        <b{_ia("spec.note.verb")}>{_t("spec.note.verb", lang)}</b><span{_ia("spec.note.tail")}>{_t("spec.note.tail", lang)}</span></p>    </div>
    {demo}
  </div>
  <div class="spec-stats">{tiles}</div>
  <div class="spec-qlabel"><span{_ia("spec.reuse.label")}>{_t("spec.reuse.label", lang)}</span>
    <span{_ia("spec.reuse.hint")}>{_t("spec.reuse.hint", lang)}</span></div>
  {_spec_status_badges(entry, lang)}
  <nav class="spec-jump">{jump}</nav>
  <div class="spec-secs">{''.join(sections)}</div>
</section>
"""


def render_prompt_section(entry: dict, prefix: str, pack_dir: Path,
                          lang: str = DEFAULT_LOCALE) -> str:
    """Copyable prompts assembled from this pack at build time.

    The text is generated by ``tools/prompts.py`` from the pack's own records,
    so a prompt cannot go stale the way a hand-written template would: change a
    rule and the prompt changes with it. Each one states the repository's
    honesty conditions, because a prompt that omits them gets an implementation
    that quietly invents them.

    ``implement`` is inlined so it works with JavaScript disabled. The per-ADR
    and per-rule variants are emitted as real files and linked, so a page does
    not carry every prompt's full text in order to copy one of them.
    """
    # The locale follows the build's language: a Chinese tree carries the
    # Chinese chapters in the context bundle.
    bundles = build_bundles(entry, pack_dir, lang, CONTENT_LOCALE.get(lang))
    base = f"{pack_dir.relative_to(ROOT).as_posix()}/prompts/"

    inline = bundles["inline"]["implement"]
    inline_html = (
        '<div class="prm-actions">'
        '<button type="button" class="copybtn" data-copy="prm-implement"'
        + _ia("prompt.copy") + ">"
        + _t("prompt.copy", lang) + "</button>"
        '<a class="prm-dl" href="' + _esc(prefix + base + "implement.md") + '" download'
        + _ia("prompt.download") + ">"
        + _t("prompt.download", lang) + "</a>"
        "</div>"
        '<textarea class="prm-text" id="prm-implement" readonly spellcheck="false"'
        + " "
        + _iaa("aria-label", "prompt.aria.inline")
        + ' aria-describedby="prm-implement-hint">'
        + '<span id="prm-implement-hint" hidden data-i18n="prompt.hint.inline">'
        + _t("prompt.hint.inline", lang) + "</span>"
        + _esc(inline) + "</textarea>"
    )

    def _list(items, kind: str) -> str:
        if not items:
            return ""
        rows = []
        for item in items:
            fname = bundle_filename(kind, item["id"])
            rows.append(
                "<li>"
                + f"<code>{_esc(item['id'])}</code> <b>{_esc(item['label'])}</b>"
                + '<span class="prm-acts">'
                + '<button type="button" class="copybtn small" data-copy-url="'
                + _esc(prefix + base + fname) + '"' + _ia("prompt.copy_one") + ">"
                + _t("prompt.copy_one", lang) + "</button>"
                + '<a class="prm-dl" href="' + _esc(prefix + base + fname) + '" download>.md</a>'
                + "</span></li>"
            )
        return '<ul class="prm-list">' + "".join(rows) + "</ul>"

    context_size = len(bundles["files"]["context.md"])
    ctx_n = f"{context_size:,}"
    return f"""
<section class="prompts" id="prompts">
  <h3{_ia("prompts.heading")}>{_t("prompts.heading", lang)}</h3>
  <p class="prompts-note">
    <span{_ia("prompts.note.1")}>{_t("prompts.note.1", lang)}</span>
    <code>tools/prompts.py</code>
    <span{_ia("prompts.note.2")}>{_t("prompts.note.2", lang)}</span>
    <i{_ia("prompts.note.pack")}>{_t("prompts.note.pack", lang)}</i><span{_ia("prompts.note.3")}>{_t("prompts.note.3", lang)}</span>
    <code>BR-05</code><span{_ia("prompts.note.3b")}>{_t("prompts.note.3b", lang)}</span><code>ADR-0004</code><span{_ia("prompts.note.4")}>{_t("prompts.note.4", lang)}</span>
    <code>verification: unverified</code><span{_ia("prompts.note.5")}>{_t("prompts.note.5", lang)}</span>
    <code>(A)</code><span{_ia("prompts.note.6")}>{_t("prompts.note.6", lang)}</span>
  </p>
  <details class="prm" open>
    <summary><b{_ia("prompt.impl.title")}>{_t("prompt.impl.title", lang)}</b><span class="prm-blurb"{_ia("prompt.impl.blurb")}>{_t("prompt.impl.blurb", lang)}</span></summary>
    {inline_html}
  </details>
  <details class="prm">
    <summary><b{_ia("prompt.adr.title")}>{_t("prompt.adr.title", lang)}</b><span class="prm-blurb"{_ia("prompt.adr.blurb", n=len(bundles["inline"]["adr"]))}>{_t("prompt.adr.blurb", lang, n=len(bundles["inline"]["adr"]))}</span></summary>
    {_list(bundles['inline']['adr'], 'adr')}
  </details>
  <details class="prm">
    <summary><b{_ia("prompt.test.title")}>{_t("prompt.test.title", lang)}</b><span class="prm-blurb"{_ia("prompt.test.blurb", n=len(bundles["inline"]["test"]))}>{_t("prompt.test.blurb", lang, n=len(bundles["inline"]["test"]))}</span></summary>
    {_list(bundles['inline']['test'], 'test')}
  </details>
  <details class="prm">
    <summary><b{_ia("prompt.ctx.title")}>{_t("prompt.ctx.title", lang)}</b><span class="prm-blurb"{_ia("prompt.ctx.blurb", n=ctx_n)}>{_t("prompt.ctx.blurb", lang, n=ctx_n)}</span></summary>
    <div class="prm-actions">
      <button type="button" class="copybtn" data-copy-url="{_esc(prefix + base + 'context.md')}"{_ia("prompt.copy_all")}>{_t("prompt.copy_all", lang)}</button>
      <a class="prm-dl" href="{_esc(prefix + base + 'context.md')}" download{_ia("prompt.download_ctx")}>{_t("prompt.download_ctx", lang)}</a>
    </div>
  </details>
</section>
"""


def render_view_switch(entry: dict | None, lang: str = DEFAULT_LOCALE) -> str:
    """Radio-based view toggle: no JavaScript, keyboard-operable.

    The inputs must be *siblings* of the two views for the CSS `~` selector to
    reach them, so they live outside the labelled container.
    """
    if entry is None:
        return ""
    counts = entry["counts"]
    n = counts["rules"] + counts["requirements"] + counts["nfrs"] + counts["controls"] + counts["adrs"] + counts["constraints"]
    return (
        '<input class="vs-in" type="radio" name="vs" id="vs-doc" checked>'
        '<label class="vs-lab" for="vs-doc"' + _ia("view.doc") + ">"
        + _t("view.doc", lang) + "</label>"
        '<input class="vs-in" type="radio" name="vs" id="vs-spec">'
        '<label class="vs-lab" for="vs-spec"' + _ia("view.spec") + ">"
        + _t("view.spec", lang)
        + (f'<span{_ia("view.spec.count", n=n)}>'
           + _esc(t("view.spec.count", lang, n=n)) + "</span>" if n else "")
        + "</label>"
    )


def translation_note(lang: str = DEFAULT_LOCALE) -> str:
    """The notice on a page whose content has no translation yet.

    It is a notice rather than a link: the English original *is* the page,
    and saying so is more useful than offering a button to the same words.
    """
    return (
        f'<p class="transnote"{_ia("trans.banner")}>{_t("trans.banner", lang)}</p>'
    )


def render_doc_page(
    pack: Pack,
    doc: Doc,
    prefix: str,
    site_url: str = "",
    lang: str = DEFAULT_LOCALE,
    spec_entry: dict | None = None,
) -> str:
    rel_inside = Path(doc.rel).relative_to(pack.rel_dir).as_posix()
    is_overview = rel_inside == "README.md"
    # The structured view and the prompt bundles are offered only where a
    # reader lands: the pack's own overview page. A toggle on all 600 pages
    # would put the switch where there is nothing to switch to yet.
    pack_dir = ROOT / pack.rel_dir
    extra = ""
    if is_overview and spec_entry:
        extra = (
            render_spec_view(spec_entry, prefix, lang)
            + render_prompt_section(spec_entry, prefix, pack_dir, lang)
        )
    spec = extra
    header = ""
    if is_overview:
        header = (
            '<div class="packhead">'
            f'<div class="packhead-titles"><h1>{html.escape(pack.display_title(lang))}</h1>'
            + (
                f'<p class="zh" lang="zh-CN">{html.escape(pack.title_zh)}</p>'
                if pack.title_zh and lang != "zh" else ""
            )
            + "</div>"
            f'<div class="packhead-meta">{pack_pills(pack, lang)}'
            f'<span class="meta-plain">{html.escape(pack.domain)} / {html.escape(pack.subdomain)}</span>'
            f'<span class="meta-plain">v{html.escape(str(pack.manifest.get("version", "")))}</span>'
            "</div></div>"
        )
    # Both views live inside `.main`, so the sidebar is present in each. The
    # radio switch next to `.shell` reaches them with `~`; replacing the whole
    # shell instead would have hidden the navigation exactly when the reader is
    # deepest in the material.
    article_html = doc.html
    if is_overview:
        # `.packhead` above already states the title, and the README repeats it as
        # the article's own H1 with its metadata table. The table carries facts the
        # pills do not (stack stance, regulatory context) so it stays; the duplicate
        # heading goes, and with it the two empty `<th>` cells that only existed to
        # make the markdown table legal.
        article_html = re.sub(
            r"^\s*<h1[^>]*>.*?</h1>\s*", "", article_html, count=1, flags=re.DOTALL)
        article_html = re.sub(
            r"<thead>\s*<tr>\s*<th[^>]*>\s*</th>\s*<th[^>]*>\s*</th>\s*</tr>\s*</thead>\s*",
            "", article_html, count=1)
    # `.wrap` is the page's gutter and measure, so the breadcrumb, the pack header
    # and the view switch line up with the sidebar and the article below them.
    # The view switch still reaches `.shell` with `~`: they remain siblings here.
    # The rail is computed first because the reading layout depends on whether
    # there is one: `.view-doc` is a two-column grid only when it holds a rail.
    rail = render_toc(doc.toc) if not is_overview else ""
    # A Chinese build says so on the page when the body is the English
    # original, rather than letting the reader assume the gap is theirs.
    note = "" if (doc.translated or lang != "zh") else translation_note(lang)
    body = (
        '<div class="wrap">'
        + breadcrumb(prefix, pack)
        + header
        + note
        + render_view_switch(spec_entry if is_overview else None, lang)
        + '<div class="shell">'
        + render_sidebar(pack, doc, prefix, lang)
        + '<div class="main">'
        + f'<div class="view-doc{" has-toc" if rail else ""}">'
        + rail
        + f'<article class="prose">{annotate_lang(article_html)}</article>'
        + "</div>"
        + spec
        + "</div>"
        + "</div>"
        + "</div>"
    )
    scripts = ""
    # `app.js` carries the contents rail, which is the only thing it does on a
    # chapter page — so it is loaded where a rail exists and nowhere else. It was
    # never loaded here at all, which is why the rail could not mark the section
    # being read.
    if rail:
        scripts += f'<script src="{prefix}assets/app.js" defer></script>'
    if "class=\"mermaid\"" in doc.html:
        scripts += mermaid_script(prefix)
    if is_overview and spec_entry:
        # The copy buttons are an enhancement; the prompts themselves are real
        # .md files, so without JS the action is still a working link.
        scripts += '<script src="' + prefix + 'assets/prompt-copy.js" defer></script>'
    return page_shell(
        title=f"{pack.title} · {doc.title}",
        description=pack.manifest.get("_summary", doc.title),
        prefix=prefix, body=body, body_class="pack", scripts=scripts,
        lang=lang, canonical=abs_url(site_url, doc.url),
    )


def render_plain_page(doc: Doc, prefix: str, site_url: str = "",
                      lang: str = DEFAULT_LOCALE) -> str:
    note = "" if (doc.translated or lang != "zh") else translation_note(lang)
    body = (
        '<div class="wrap">'
        + note
        + f'<article class="prose prose-wide">{annotate_lang(doc.html)}</article>'
        "</div>"
    )
    scripts = mermaid_script(prefix) if 'class="mermaid"' in doc.html else ""
    return page_shell(
        title=doc.title, description=doc.title,
        prefix=prefix, body=body, body_class="doc", scripts=scripts,
        lang=lang, canonical=abs_url(site_url, doc.url),
        nav_current=NAV_PAGE.get(doc.url, ""),
    )


def mermaid_script(prefix: str = "") -> str:
    """The diagram renderer, pinned by SRI like every other vendored asset."""
    return (
        f'<script src="{prefix}assets/vendor/mermaid.min.js" '
        f'integrity="{VENDOR_EXPECTED["mermaid.min.js"]}" '
        'crossorigin="anonymous"></script>'
    )


def render_catalog(
    packs: list[Pack], base_url: str, site_url: str = "",
    lang: str = DEFAULT_LOCALE,
    spec_entries: dict | None = None,
) -> str:
    """The register of packs.

    Contract §9 governs the hero, because this page is the product's marketing
    surface: the indigo wash with its light banding, the two-part headline with
    the second half in `--primary`, and the sub-line joined with `·`.
    """
    spec_entries = spec_entries or {}
    domains = sorted({p.domain for p in packs})
    maturities = sorted({p.maturity for p in packs})
    verifications = [v for v in ("unverified", "source-checked",
                                 "practitioner-reviewed", "field-proven")]

    def facet(field: str, values) -> str:
        """One filter group. The value on the chip is chrome where the catalog
        knows a translation for it (`verify.*`, `maturity.*`) and data
        otherwise (a domain slug), because the `data-value` the filter reads is
        always the raw record and must not change with the language."""
        chips = []
        for value in values:
            n = sum(1 for p in packs if getattr(p, field) == value)
            key = f"{'maturity' if field == 'maturity' else 'verify'}.{value}"
            text = _t(key, lang) if has(key) else _esc(value)
            chips.append(
                f'<button class="chip" data-facet="{field}" data-value="{html.escape(value)}">'
                + (f'<span{_ia(key)}>{text}</span>' if has(key) else f"{text}")
                + f'<span class="chip-n">{n}</span></button>'
            )
        return ('<div class="facet"><span class="facet-label"'
                + _ia(f"facet.{field}") + ">"
                + _t(f"facet.{field}", lang) + "</span>"
                + "".join(chips) + "</div>")

    facets = (
        '<div class="facets">'
        + facet("domain", domains)
        + facet("maturity", maturities)
        + facet("verification", verifications)
        + "</div>"
    )
    cards = "".join(render_card(p, spec_entries.get(p.slug), lang) for p in packs)
    # §7.8: an empty result is a moment for direction — icon, title, what
    # happened, and a way out. Never a bare "no data".
    empty = (
        '<div class="empty" id="empty" hidden>'
        f'<span class="empty-icon">{icon("empty")}</span>'
        f'<h3{_ia("catalog.empty.title")}>{_t("catalog.empty.title", lang)}</h3>'
        f'<p{_ia("catalog.empty.body")}>{_t("catalog.empty.body", lang)}</p>'
        '<div class="empty-actions">'
        f'<button class="clear" id="empty-clear" type="button"{_ia("catalog.search.clear")}>'
        f'{_t("catalog.search.clear", lang)}</button>'
        "</div></div>"
    )

    hero = (
        '<section class="hero">'
        f'<p class="eyebrow">{icon("grid")}Open Solution Atlas</p>'
        f'<h1{_ia("catalog.hero.title1")}>{_t("catalog.hero.title1", lang)} '
        f'<span class="tail"{_ia("catalog.hero.title2")}>{_t("catalog.hero.title2", lang)}</span></h1>'
        f'<p class="hero-sub"{_ia("catalog.hero.sub")}>{_t("catalog.hero.sub", lang)}</p>'
        "</section>"
    )

    body = (
        # `.wrap` is the page's gutter and measure. The hero and the trust note
        # are rounded panels designed to sit inside it, so without it their left
        # edge landed on the viewport edge and the facet labels were clipped at
        # x=0 — the panels' own padding made them *look* inset.
        '<div class="wrap">'
        + hero
        + '<p class="trustnote">'
        + _span("catalog.trust.draft", lang) + " <code>llm-drafted</code>"
        + _span("catalog.trust.none", lang)
        + f'<strong{_ia("catalog.trust.verified")}>{_t("catalog.trust.verified", lang)}</strong>'
        + _span("catalog.trust.maturity", lang) + _span("catalog.trust.check", lang)
        + "<code>SOURCES.md</code>"
        + _span("catalog.trust.tail", lang)
        + "</p>"        + '<div class="searchwrap">'
        + '<input id="q" type="search" autocomplete="off" spellcheck="false"'
        + _iaa("placeholder", "catalog.search.placeholder", n=len(packs))
        + f' placeholder="{_t("catalog.search.placeholder", lang, n=len(packs))}">'
        + f'<button id="clear" class="clear" hidden{_ia("catalog.search.clear")}>'
        + _t("catalog.search.clear", lang) + "</button>"
        + "</div>"
        + '<p class="index-status" id="index-status" hidden></p>'
        + facets
        + '<div class="controls">'
        + f'<span class="count" id="count"><b>{len(packs)}</b>'
        + f' <span data-i18n="word.pack">{_t("word.pack", lang)}</span></span>'
        + '<span id="hits"></span></div>'
        + f'<div class="cards" id="cards">{cards}{empty}</div>'
        + f'<p class="hint"{_ia("catalog.hint")}>{_t("catalog.hint", lang)}</p>'
        + "</div>"
    )
    return page_shell(
        title=_t("catalog.page.title", lang),
        description=_t("catalog.page.desc", lang),
        prefix="", body=body, body_class="catalog", icon="\u25c8",
        nav_current="catalog",
        # SRI on the vendored library: the hash is pinned in VENDOR_EXPECTED
        # and the build already fails if the file's bytes change, so the
        # attribute is the browser-side half of the same check.
        scripts=(
            '<script src="assets/vendor/fuse.min.js" '
            f'integrity="{VENDOR_EXPECTED["fuse.min.js"]}" '
            'crossorigin="anonymous" defer></script>'
            '<script src="assets/app.js" defer></script>'
        ),
        lang=lang, canonical=abs_url(site_url, "index.html"),
    )


def render_card(pack: Pack, entry: dict | None = None,
                lang: str = DEFAULT_LOCALE) -> str:
    """One pack as a contract §7.4 category card.

    The reference's most characteristic block is a grid of cards whose first
    row is an icon on a category tint with a large number right-aligned in
    tabular figures. That maps onto a pack almost exactly — icon, identifier
    count, name, path — and the number is real rather than decorative: it is how
    much machine-readable content the pack carries.

    Category colour (contract §1.4) appears on the icon's stroke and its tinted
    background only, never on the card fill, the title or a button.
    """
    slug = pack.slug
    stroke, tint = category_for(pack.domain, slug)
    num = ""
    if entry:
        counts = entry["counts"]
        total = sum(counts[k] for k in (
            "rules", "requirements", "nfrs", "controls", "adrs", "constraints"))
        num = f'<span class="card-num">{total}</span>'
    tags = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in pack.tags[:6])
    summary = str(pack.manifest.get("_summary", ""))
    zh = (
        f'<p class="zh" lang="zh-CN">{html.escape(pack.title_zh)}</p>'
        if pack.title_zh and lang != "zh" else ""
    )
    return (
        f'<article class="card" data-slug="{html.escape(slug)}"'
        f' data-domain="{html.escape(pack.domain)}"'
        f' data-maturity="{html.escape(pack.maturity)}"'
        f' data-verification="{html.escape(pack.verification)}">'
        '<div class="card-top">'
        f'<span class="cat-icon" style="background:{tint};color:{stroke}">'
        f'{icon(icon_for(pack.domain, slug))}</span>'
        f'{num}'
        '</div>'
        f'<a class="card-link" href="{pack.index_url}">'
        f'<h3>{html.escape(pack.display_title(lang))}</h3></a>{zh}'
        f'<p class="card-sum">{html.escape(summary)}</p>'
        f'<div class="card-meta">{pack_pills(pack, lang)}'
        f'<span class="meta-plain">{html.escape(pack.domain)}</span></div>'
        f'<div class="tags">{tags}</div>'
        "</article>"
    )


def cjk_ngrams(text: str) -> str:
    """Character n-grams of the CJK runs in ``text``, space-joined.

    Fuse.js tokenizes on whitespace, so a multi-character Chinese query
    ("一网通办") cannot match an indexed run that is not written identically.
    Splitting each CJK run into overlapping bigrams/trigrams is a cheap,
    dependency-free substitute for segmentation: the query decomposes the same
    way client-side and matches on overlap.
    """
    grams: list[str] = []
    for run in re.findall(r"[\u3400-\u9fff\uf900-\ufaff]+", text or ""):
        for n in (2, 3):
            grams.extend(run[i : i + n] for i in range(len(run) - n + 1))
    return " ".join(grams)


def build_index(packs: list[Pack], other_docs: list[Doc]) -> list[dict]:
    index: list[dict] = []
    for pack in packs:
        index.append({
            "k": "pack",
            "t": pack.title,
            "z": pack.title_zh,
            "u": pack.index_url,
            "d": pack.domain,
            "s": pack.subdomain,
            "m": pack.maturity,
            "v": pack.verification,
            "g": pack.tags,
            "x": str(pack.manifest.get("_summary", ""))[:MAX_PACK_TEXT],
            "n": cjk_ngrams(" ".join([pack.title, pack.title_zh, *pack.tags])),
        })
        for doc in pack.docs:
            index.append({
                "k": "doc",
                "t": doc.title,
                "u": doc.url,
                "d": pack.domain,
                "s": pack.subdomain,
                "m": pack.maturity,
                "v": pack.verification,
                "p": pack.slug,
                "g": [],
                "x": doc.text[:MAX_DOC_TEXT],
                "n": cjk_ngrams(doc.text[:MAX_DOC_TEXT]),
            })
    for doc in other_docs:
        index.append({
            "k": "meta",
            "t": doc.title,
            "u": doc.url,
            "d": "project",
            "s": "",
            "m": "",
            "v": "",
            "g": [],
            "x": doc.text[:MAX_DOC_TEXT],
            "n": cjk_ngrams(doc.text[:MAX_DOC_TEXT]),
        })
    return index


LINK_TARGET_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_ATTR_RE = re.compile(r'(?:href|src)="([^"]+)"')
# Link targets that are not site-relative: anchors, absolute URLs/schemes, and
# root-absolute paths (which a sub-path deployment handles differently).
NON_LOCAL_PREFIX = ("#", "/", "http://", "https://", "mailto:", "data:", "tel:")


def copy_linked_files(out: Path) -> int:
    """Copy non-Markdown files that prose links to, preserving their path.

    Packs link to ``api/openapi.yaml``, the manifest schema, and tool sources.
    Those links are meaningful on GitHub; on the site they 404 unless the file
    is present, so each referenced asset is copied verbatim.
    """
    copied = 0
    seen: set[Path] = set()
    for md in discover_markdown():
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in LINK_TARGET_RE.finditer(text):
            target = match.group(1)
            if target.startswith(NON_LOCAL_PREFIX) or "://" in target:
                continue
            path = target.split("#", 1)[0]
            if not path or path.endswith(".md"):
                continue
            src = (md.parent / path).resolve()
            try:
                rel = src.relative_to(ROOT)
            except ValueError:
                continue
            if not src.is_file() or src in seen:
                continue
            seen.add(src)
            dest = out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            copied += 1
    return copied


def _entry_label(name: str) -> tuple[str, str]:
    """(human label, extension) for a file or directory name.

    `warm-editorial/` reads as "Warm Editorial" and `DESIGN.html` as "DESIGN"
    with `.html` handed back so the card can name the kind. Nothing is invented:
    the label is the name with its separators resolved, and the raw path stays on
    the page as the subtitle, so a reader who came for the exact filename still
    has it.
    """
    stem, dot, ext = name.rpartition(".")
    if not dot:
        stem, ext = name, ""
    words = [w for w in re.split(r"[-_]+", stem) if w]
    if not words:
        return name, ext
    # Title case, but only when the whole segment is lower case: a slug like
    # `data-ai` is shown as "Data Ai" and `energy-utilities` as "Energy
    # Utilities", while `DESIGN`, `AGENTS` and `README.zh-CN` are already in the
    # form their authors chose and capitalising them would give "Readme".
    if stem.islower():
        words = [w[:1].upper() + w[1:] for w in words]
    return " ".join(words), ext


def _path_crumbs(parts, prefix: str, lang: str = DEFAULT_LOCALE) -> str:
    """A breadcrumb for a generated listing page, from the catalog inward.

    `/design-systems/library/stripe/` says `Catalog › design-systems › library ›
    stripe` rather than opening on a slug with no context, which is what these
    pages did before.
    """
    if not parts:
        return ""
    chev = icon("chevron")
    out = ['<nav class="crumbs">',
           f'<a href="{prefix}index.html"{_ia("crumb.catalog")}>'
           f'{_t("crumb.catalog", lang)}</a>', chev]
    last = len(parts) - 1
    for i, part in enumerate(parts):
        if i == last:
            out.append(f'<span class="crumb-cur">{html.escape(part)}</span>')
        else:
            up = "../" * (last - i)
            out.append(f'<a href="{up}index.html">{html.escape(part)}</a>{chev}')
    out.append("</nav>")
    return "".join(out)


def generate_missing_indexes(out: Path, lang: str = DEFAULT_LOCALE) -> int:
    """Give every output directory a listing page if it lacks index.html.

    Links to a directory (``…/docs/``, ``…/packs/``) are rewritten to
    ``index.html`` during rendering; this makes those targets real.

    These pages were the site's worst surface: a raw slug as the heading, a flat
    ``<ul>`` of file names, no page gutter, and roughly three hundred of them.
    They are a designed surface now — the page's own measure, a breadcrumb back
    through the path, and one card per entry in the catalog's card language,
    with the entry count taken from the directory rather than asserted.
    """
    created = 0
    # Every output directory — including ones that hold only subdirectories —
    # needs an index; a parent's listing links to <child>/index.html, and a
    # missing one is a broken link the build must not ship.
    dirs = {p for p in out.rglob("*") if p.is_dir()}
    for d in sorted(dirs):
        # Hidden trees (`.github/`, `.nojekyll`'s siblings) are repository
        # internals, not catalog content; publishing them would leak the
        # project's scaffolding into the public site and the sitemap.
        if any(part.startswith(".") for part in d.relative_to(out).parts):
            continue
        index = d / "index.html"
        if index.exists():
            continue
        try:
            entries = sorted(d.iterdir())
        except OSError:
            continue
        cards = []
        for entry in entries:
            if entry.name == "index.html":
                continue
            is_dir = entry.is_dir()
            href = f"{entry.name}/index.html" if is_dir else entry.name
            label, ext = _entry_label(entry.name)
            note = ""
            if is_dir:
                try:
                    n = sum(1 for c in entry.iterdir() if c.name != "index.html")
                except OSError:
                    n = 0
                note = f'<span class="dirnote"{_ia("dir.items" if n != 1 else "dir.items.one", n=n)}>{_t("dir.items" if n != 1 else "dir.items.one", lang, n=n)}</span>'
            elif ext:
                note = f'<span class="dirnote">.{html.escape(ext)}</span>'
            cards.append(
                f'<a class="dircard" href="{html.escape(href)}">'
                f'<span class="diricon">{icon("grid" if is_dir else "book")}</span>'
                f'<span class="dirname">{html.escape(label)}</span>'
                f"{note}</a>"
            )
        if not cards:
            continue
        parts = d.relative_to(out).parts
        rel = d.relative_to(out).as_posix()
        prefix = "../" * len(parts)
        title = _entry_label(parts[-1])[0]
        body = (
            '<div class="wrap">'
            + _path_crumbs(parts, prefix, lang)
            + '<header class="listhead">'
            + f"<h1>{html.escape(title)}</h1>"
            + f'<p class="path">{html.escape(rel)}/</p>'
            + "</header>"
            + f'<div class="dirgrid">{"".join(cards)}</div>'
            + "</div>"
        )
        write(index, page_shell(
            title=f"{title} — Open Solution Atlas",
            description=_t("dir.contents", lang, path=rel),
            prefix=prefix, body=body, body_class="doc",
            lang=lang,
        ))
        created += 1
    return created


def write_sitemap(out: Path, site_url: str) -> None:
    """Emit ``sitemap.xml`` — one <url> per generated HTML page.

    Without this, 299 pages are invisible to crawlers beyond what they can
    reach from the catalog links. The base must be absolute; when the caller
    passes an empty value the file is skipped rather than emitting relative
    loc elements (which sitemaps do not allow).
    """
    base = (site_url or "").strip().rstrip("/")
    if not base:
        print("note: --site-url unset, no sitemap emitted")
        return
    # Generated pages first (they are the canonical entry points). Hidden
    # trees are repository internals and must never reach a sitemap.
    urls = sorted(
        p.relative_to(out).as_posix() for p in out.rglob("*.html")
        if not any(part.startswith(".") for part in p.relative_to(out).parts)
    )
    body = "".join(f"<url><loc>{html.escape(f'{base}/{u}')}</loc></url>" for u in urls)
    write(
        out / "sitemap.xml",
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + body + "</urlset>\n",
    )


def write_robots(out: Path, site_url: str) -> None:
    """Emit ``robots.txt`` — permit everything, point at the sitemap."""
    base = (site_url or "").strip().rstrip("/")
    lines = [
        "User-agent: *",
        "Allow: /",
        # The catalog UI is client-side; the raw index is machine data.
        "Disallow: /search-index.json",
    ]
    if base:
        # URL-join instead of string concat: a trailing "/" in --site-url
        # must not produce "//sitemap.xml".
        lines.append(f"Sitemap: {base}/sitemap.xml")
    write(out / "robots.txt", "\n".join(lines) + "\n")


def write_404(out: Path, site_url: str = "", lang: str = DEFAULT_LOCALE) -> None:
    """Emit a branded ``404.html`` (GitHub Pages serves it on unknown paths)."""
    # `.wrap` carries the gutter and the measure. The catalog's hero — the same
    # panel — sits inside it; this one did not, so its left edge was the viewport
    # edge and the panel spanned the whole window instead of 1180px.
    body = (
        '<div class="wrap">'
        f'<section class="hero"><h1{_ia("notfound.title")}>{_t("notfound.title", lang)}</h1>'
        f'<p class="hero-sub"{_ia("notfound.body")}>{_t("notfound.body", lang)}</p>'
        '<div class="searchwrap">'
        f'<a class="clear" href="index.html"{_ia("notfound.back")}>'
        f'{_t("notfound.back", lang)}</a></div>'
        "</section>"
        "</div>"
    )
    write(
        out / "404.html",
        page_shell(
            title=f'{_t("notfound.title", lang)} — Solution Atlas',
            description=_t("notfound.body", lang),
            prefix="", body=body, body_class="catalog",
            lang=lang, canonical=abs_url(site_url, "404.html"),
        ),
    )


def verify_internal_links(out: Path) -> list[str]:
    """Every relative href/src in the built site must resolve on disk.

    Catches the failure mode that matters most here: a link that survived the
    Markdown -> HTML rewrite but points at a page we never generated.
    """
    broken: list[str] = []
    for page in sorted(out.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        for match in HTML_ATTR_RE.finditer(text):
            target = match.group(1)
            if target.startswith(NON_LOCAL_PREFIX):
                continue
            path = target.split("#", 1)[0].split("?", 1)[0]
            if not path:
                continue
            if not (page.parent / path).exists():
                broken.append(f"{page.relative_to(out).as_posix()} -> {target}")
    return broken


def build_bilingual(out: Path, base_url: str = "/", site_url: str = "") -> int:
    """Build both language trees into one output directory.

    The English tree is the site root and the Chinese tree lives under `zh/`.
    Each tree is a complete site in its own language - chrome and prose agree
    - and the switch between them is a link, because a translation is a
    sibling file and the URL space never changes.
    """
    if build(out, base_url, site_url, "en"):
        return 1
    # The English tree is annotated before the Chinese tree exists: the pass
    # walks the whole output directory, and the two trees must not annotate
    # each other.
    inject_language_links(out, "en", LOCALE_TREE["en"], LOCALE_TREE["zh"], site_url)
    zh_out = out / LOCALE_TREE["zh"].rstrip("/")
    if build(zh_out, base_url, site_url, "zh"):
        return 1
    # The Chinese tree's own crawler artifacts would point at the wrong
    # origin: its pages live under /zh/, and the one sitemap that matters is
    # the root one.
    for artifact in ("robots.txt", "sitemap.xml"):
        (zh_out / artifact).unlink(missing_ok=True)
    inject_language_links(
        zh_out, "zh", LOCALE_TREE["zh"], LOCALE_TREE["en"], site_url
    )
    # The root sitemap was written by the English build, before the Chinese
    # tree existed; rewrite it so it lists both.
    write_sitemap(out, site_url)
    broken = verify_internal_links(out)
    if broken:
        print(f"[ERROR] {len(broken)} broken internal link(s):")
        for path in broken[:20]:
            print(f"  {path}")
        return 1
    pages = sum(1 for _ in out.rglob("*.html"))
    try:
        where = out.relative_to(ROOT).as_posix()
    except ValueError:
        where = out.as_posix()
    print(
        f"built bilingual site: {pages} pages -> {where}/ "
        f"(en at /, zh at /{LOCALE_TREE['zh'].rstrip('/')}/)"
    )
    print("internal links: all resolve")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the static site")
    parser.add_argument("--out", default="_site", help="output directory")
    parser.add_argument(
        "--base-url", default="/",
        help="path the site is served under, for relative links (default: /)",
    )
    parser.add_argument(
        "--site-url",
        default="https://embkit.github.io/open-solution-atlas",
        help="absolute public origin, used for canonical URLs, sitemap.xml "
             "and robots.txt; pass '' for a local-only build with no "
             "crawler artifacts (default: the deployed GitHub Pages origin)",
    )
    parser.add_argument(
        "--lang", default="both",
        help="language(s) to build: 'en', 'zh' or 'both' (default: both). "
             "'both' builds the English site at the output root and the Chinese "
             "site under zh/, each complete in its own language, with a switch "
             "between them that changes the prose and not only the chrome",
    )
    args = parser.parse_args()
    if args.lang not in LOCALES and args.lang != "both":
        parser.error(f"--lang must be one of {', '.join(LOCALES)} or both")
    if args.lang == "both":
        return build_bilingual(ROOT / args.out, args.base_url, args.site_url)
    return build(ROOT / args.out, args.base_url, args.site_url, args.lang)


if __name__ == "__main__":
    sys.exit(main())

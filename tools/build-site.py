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

MATURITY_LABEL = {
    "L1": ("L1 · Brief", "m1"),
    "L2": ("L2 · Blueprint", "m2"),
    "L3": ("L3 · Agent-ready", "m3"),
    "L4": ("L4 · Proven", "m4"),
}
VERIFICATION_LABEL = {
    "unverified": ("unverified", "v0"),
    "source-checked": ("source-checked", "v1"),
    "practitioner-reviewed": ("practitioner-reviewed", "v2"),
    "field-proven": ("field-proven", "v3"),
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


def load_summaries() -> dict[str, str]:
    """Parse packs/README.md's index table into {slug: summary}."""
    index = PACKS_DIR / "README.md"
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
        if "templates" in parts or "tests" in parts:
            continue
        if "site-assets" in parts:  # vendored third-party libs, not content
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
<meta name="theme-color" content="#fbfaf7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121316" media="(prefers-color-scheme: dark)">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='24' font-size='24'>{icon}</text></svg>">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="{prefix}index.html"><span class="brand-mark">◈</span> Solution&nbsp;Atlas</a>
  <details class="navmenu">
    <summary aria-label="Toggle navigation"><span class="navmenu-icon" aria-hidden="true">☰</span>Menu</summary>
    <nav class="topnav" aria-label="Primary">
      <a href="{prefix}index.html">Catalog</a>
      <a href="{prefix}docs/pack-standard.v1.html">Standard</a>
      <a href="{prefix}docs/taxonomy.html">Taxonomy</a>
      <a href="{prefix}docs/roadmap.html">Roadmap</a>
    </nav>
  </details>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="sitefoot">
  <p><strong>Open Solution Atlas</strong> — blueprints for real enterprise systems.
     Content <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>,
     code <a href="https://opensource.org/license/mit">MIT</a>.
     Every pack is <code>llm-drafted</code> and <strong>not field-verified</strong> —
     read its <code>SOURCES.md</code> before trusting a specific claim.</p>
</footer>
{scripts}
</body>
</html>
"""


def page_shell(
    *,
    title: str,
    description: str,
    prefix: str,
    body: str,
    body_class: str = "doc",
    icon: str = "◈",
    scripts: str = "",
    lang: str = "en",
    canonical: str = "",
) -> str:
    head = HEAD.format(
        title=html.escape(title), description=html.escape(description),
        prefix=prefix, body_class=body_class, icon=icon,
        lang=lang, canonical=canonical,
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
    return (
        head
        + body
        + FOOT.format(scripts=scripts)
    )


def breadcrumb(prefix: str, pack: Pack | None) -> str:
    if not pack:
        return ""
    return (
        '<nav class="crumbs">'
        f'<a href="{prefix}index.html">Catalog</a>'
        f'<span>/</span><span>{html.escape(pack.domain)}</span>'
        f'<span>/</span><span class="crumb-cur">{html.escape(pack.slug)}</span>'
        "</nav>"
    )


def pill(label: str, kind: str) -> str:
    return f'<span class="pill {kind}">{html.escape(label)}</span>'


def pack_pills(pack: Pack) -> str:
    m_label, m_kind = MATURITY_LABEL.get(pack.maturity, (pack.maturity, "m1"))
    v_label, v_kind = VERIFICATION_LABEL.get(pack.verification, (pack.verification, "v0"))
    return pill(m_label, m_kind) + pill(v_label, v_kind)


def nav_tree(pack: Pack, current_url: str, prefix: str) -> str:
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
    out = ['<nav class="packnav" aria-label="Pack chapters">']
    for group in sorted(groups):
        label = group or "overview"
        has_active = any(doc.url == current_url for doc in groups[group])
        out.append(
            f'<details class="navgroup"{"" if has_active else " open"}>'
            f'<summary class="navgroup-label">{html.escape(label)}</summary><ul>'
        )
        for doc in sorted(groups[group], key=lambda d: d.rel):
            rel_inside = Path(doc.rel).relative_to(pack.rel_dir).as_posix()
            name = Path(rel_inside).name
            name = "overview" if name == "README.md" else name[:-3]
            active = ' class="active" aria-current="page"' if doc.url == current_url else ""
            href = prefix + doc.url
            out.append(f'<li><a{active} href="{href}">{html.escape(name)}</a></li>')
        out.append("</ul></details>")
    out.append("</nav>")
    return "".join(out)


def render_toc(toc_tokens: list) -> str:
    if not toc_tokens:
        return ""

    def walk(tokens, level=0):
        if level > 2:
            return ""
        items = []
        for tok in tokens:
            items.append(
                f'<li><a href="#{html.escape(tok["id"])}">{html.escape(tok["name"])}</a></li>'
            )
            items.append(walk(tok.get("children", []), level + 1))
        inner = "".join(items)
        return f'<ul>{inner}</ul>' if inner else ""

    return f'<aside class="toc" aria-label="On this page"><span class="toc-label">On this page</span>{walk(toc_tokens)}</aside>'


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #

def build(out: Path, base_url: str, site_url: str = "", lang: str = "en") -> int:
    summaries = load_summaries()
    packs = load_packs(summaries)
    if not packs:
        print("ERROR: no packs found", file=sys.stderr)
        return 1

    # The structured index is extracted once and shared by the renderer and
    # the emitted JSON, so a page and the data file can never disagree.
    pack_index = build_pack_index()
    spec_entries = {p["slug"]: p for p in pack_index["packs"]}

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    # Render every pack document.
    for pack in packs:
        pack_dir = ROOT / pack.rel_dir
        for src in sorted(pack_dir.rglob("*.md")):
            text = src.read_text(encoding="utf-8")
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
                )
            )

    # Render non-pack Markdown (docs/, root files, the packs index).
    other_docs: list[Doc] = []
    for src in discover_markdown():
        rel = src.relative_to(ROOT).as_posix()
        if rel.startswith("packs/") and rel != "packs/README.md":
            continue
        text = src.read_text(encoding="utf-8")
        body_html, plain, toc = render_markdown(text)
        other_docs.append(
            Doc(
                src=src, rel=rel, url=url_for(src),
                title=first_heading(text, Path(src).stem),
                html=body_html, text=plain, toc=toc,
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
    write(out / "index.html", render_catalog(packs, base_url, site_url, lang))
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
        bundles = build_bundles(entry, ROOT / pack.rel_dir)
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
    generated = generate_missing_indexes(out)

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


def _id_chip(id_: str, kind: str, href: str | None = None) -> str:
    """An identifier that links to its own row, or stands alone if uncited."""
    if href:
        return f'<a class="chip idchip" href="{href}" data-id="{_esc(id_)}">{_esc(id_)}</a>'
    return f'<span class="chip idchip" data-id="{_esc(id_)}">{_esc(id_)}</span>'


def _spec_status_badges(entry: dict) -> str:
    """Per-section extraction quality — the honest part of the panel.

    A pack whose rules live in prose gets a visible `prose-only` badge rather
    than an empty table, so the gap is a fact a reader can act on instead of
    an impression the site quietly creates.
    """
    label = {"structured": "可结构化", "prose-only": "仅散文", "absent": "缺失"}
    cells = []
    for key, _title, _cls in SPEC_SECTIONS:
        if key not in entry["sections"]:
            continue
        st = entry["sections"][key]["status"]
        n = entry["sections"][key]["count"]
        cells.append(
            f'<span class="sq {st}" title="{_esc(key)}">{label[st]}'
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


def render_spec_view(entry: dict, prefix: str) -> str:
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
        ("rules", "Business rules", counts["rules"]),
        ("requirements", "Requirements", counts["requirements"]),
        ("nfrs", "NFR targets", counts["nfrs"]),
        ("controls", "Controls", counts["controls"]),
        ("adrs", "ADRs", counts["adrs"]),
        ("constraints", "Integrity constraints", counts["constraints"]),
        ("store_constraints", "of which store-enforced", counts["store_constraints"]),
        ("policy_nfrs", "policy-assumed targets", counts["policy_nfrs"]),
    ]
    tiles = "".join(
        f'<a class="stat" href="#sec-{k}"><b>{v}</b><span>{_esc(lbl)}</span></a>'
        for k, lbl, v in stats if v
    )

    jump = "".join(
        f'<a class="jump" href="#sec-{key}">{_esc(title)} · {counts.get(key, len(entry.get(key, [])))}</a>'
        for key, title, _ in SPEC_SECTIONS if counts.get(key, len(entry.get(key, [])))
    )

    sections: list[str] = []

    # ---- ADRs ------------------------------------------------------------
    if entry["adrs"]:
        rows = "".join(
            f'<tr id="spec-{_esc(a["id"])}"><th><code>{_esc(a["id"])}</code></th>'
            f'<td><b>{_esc(a["name"])}</b>'
            + (f'<p class="dec">{_esc(a["decision"])}</p>' if a["decision"] else "")
            + f'<p class="refs">被引用：{_spec_row_chips(entry, refs.get(a["id"], []), "ref")}</p></td></tr>'
            for a in entry["adrs"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-adr" open><summary>'
            f'Architecture decisions · {len(entry["adrs"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- Business rules ---------------------------------------------------
    if entry["rules"]:
        rows = "".join(
            f'<tr id="spec-{_esc(r["id"])}"><th><code>{_esc(r["id"])}</code></th>'
            f'<td><b>{_esc(r["name"])}</b>'
            + (f'<p class="prop">{_esc(r["proposition"])}</p>' if r["proposition"] else "")
            + f'<p class="refs">强制：{_spec_row_chips(entry, r["enforced_by"] + r["trace_adrs"], "ref")}</p></td></tr>'
            for r in entry["rules"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-rule" open><summary>'
            f'Business rules · {len(entry["rules"])}</summary>'
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
            + f'<p class="refs">追溯：{_spec_row_chips(entry, q["traces"], "ref")}</p></td></tr>'
            for q in entry["requirements"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-req" open><summary>'
            f'Functional requirements · {len(entry["requirements"])}</summary>'
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
            f'Non-functional targets · {len(entry["nfrs"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- Controls ---------------------------------------------------------
    if entry["controls"]:
        rows = "".join(
            f'<tr id="spec-{_esc(c["id"])}"><th><code>{_esc(c["id"])}</code></th>'
            f'<td><b>{_esc(c["name"])}</b>'
            + (f'<p class="inst">{_esc(c["instrument_names"])}</p>' if c["instrument_names"] else "")
            + f'<p class="refs">追溯：{_spec_row_chips(entry, c["requirements"] + c["rules"] + c["capabilities"], "ref")}</p></td></tr>'
            for c in entry["controls"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-ctl"><summary>'
            f'Compliance controls · {len(entry["controls"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    # ---- Data-model constraints ------------------------------------------
    if entry["constraints"]:
        rows = "".join(
            f'<tr id="spec-con-{c["n"]}"><th><code>{c["n"]}</code></th>'
            f'<td>{_esc(c["text"])}'
            + (' <span class="sq structured" title="the data model claims this is enforced in the store">store</span>'
               if c["store"] else "")
            + f'<p class="refs">强制：{_spec_row_chips(entry, c["enforces"], "ref")}</p></td></tr>'
            for c in entry["constraints"]
        )
        sections.append(
            f'<details class="spec-sec" id="sec-con"><summary>'
            f'Integrity constraints · {len(entry["constraints"])} '
            f'(<b>{counts["store_constraints"]}</b> store-enforced)</summary>'
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
            f'Capabilities · {len(entry["capabilities"])}</summary>'
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
            f'Bounded contexts · {len(entry["contexts"])}</summary>'
            f'<table class="spectab"><tbody>{rows}</tbody></table></details>'
        )

    demo = ""
    if entry.get("demo"):
        demo = (
            '<a class="demobtn" href="' + _esc(prefix + entry["demo"]["url"]) + '">'
            '<b>打开交互 demo</b><span>' + _esc(entry["demo"].get("title") or entry["slug"]) + "</span></a>"
        )

    return f"""
<section class="spec" id="spec">
  <div class="spec-head">
    <div>
      <h2>规格面板 · {total_ids} 条已识别标识</h2>
      <p class="spec-note">由 <code>tools/pack_index.py</code> 从本包 Markdown
        <b>抽取</b>而成，不是手写页面：下列数字随包内容变化，与散文同源同版本。</p>
    </div>
    {demo}
  </div>
  <div class="spec-stats">{tiles}</div>
  <div class="spec-qlabel">机器可读性 <span>(标记为「仅散文」的章节含标识但无法结构化，是内容待办而非解析上限)</span></div>
  {_spec_status_badges(entry)}
  <nav class="spec-jump">{jump}</nav>
  <div class="spec-secs">{''.join(sections)}</div>
</section>
"""


def render_prompt_section(entry: dict, prefix: str, pack_dir: Path) -> str:
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
    bundles = build_bundles(entry, pack_dir)
    base = f"{pack_dir.relative_to(ROOT).as_posix()}/prompts/"

    inline = bundles["inline"]["implement"]
    inline_html = (
        '<div class="prm-actions">'
        '<button type="button" class="copybtn" data-copy="prm-implement">复制提示词</button>'
        '<a class="prm-dl" href="' + _esc(prefix + base + "implement.md") + '" download>下载 .md</a>'
        '</div>'
        '<textarea class="prm-text" id="prm-implement" readonly spellcheck="false">'
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
                + _esc(prefix + base + fname) + '">复制</button>'
                + '<a class="prm-dl" href="' + _esc(prefix + base + fname) + '" download>.md</a>'
                + "</span></li>"
            )
        return '<ul class="prm-list">' + "".join(rows) + "</ul>"

    context_size = len(bundles["files"]["context.md"])
    return f"""
<section class="prompts" id="prompts">
  <h3>提示词 · 由本包内容拼装</h3>
  <p class="prompts-note">
    这些不是模板占位。每条都由 <code>tools/prompts.py</code> 在构建期从<i>本包</i>的
    规则、已决决策、强制约束与可测目标拼装而成：带上 <code>BR-05</code> 的语义、
    <code>ADR-0004</code> 的决策和存储级约束，生成的东西才可能具备已定义的保证——
    只说「做一个带审批的工作流引擎」不会，而且再润色也不会。
    每条都写明诚实条件（<code>verification: unverified</code>、不主张符合性、
    <code>(A)</code> 是策略而非测量），因为省略它们的提示词，会让实现方悄悄把那些东西发明出来。
  </p>
  <details class="prm" open>
    <summary><b>按规格实现原型</b><span class="prm-blurb">能力 · 规则 · 已决决策 · 强制约束 · 可测目标</span></summary>
    {inline_html}
  </details>
  <details class="prm">
    <summary><b>实现一条 ADR 的决策</b><span class="prm-blurb">{len(bundles['inline']['adr'])} 条：决策 + 依赖它的需求 + 被否备选项所在文件</span></summary>
    {_list(bundles['inline']['adr'], 'adr')}
  </details>
  <details class="prm">
    <summary><b>为一条规则生成测试</b><span class="prm-blurb">{len(bundles['inline']['test'])} 条：命题 + 强制它的需求 + 测量它的公式</span></summary>
    {_list(bundles['inline']['test'], 'test')}
  </details>
  <details class="prm">
    <summary><b>导出整包上下文</b><span class="prm-blurb">{context_size:,} 字符 · 各章节原文，供需要原文而非摘要的模型</span></summary>
    <div class="prm-actions">
      <button type="button" class="copybtn" data-copy-url="{_esc(prefix + base + 'context.md')}">复制整包</button>
      <a class="prm-dl" href="{_esc(prefix + base + 'context.md')}" download>下载 context.md</a>
    </div>
  </details>
</section>
"""


def render_view_switch(entry: dict | None) -> str:
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
        '<label class="vs-lab" for="vs-doc">文档视图</label>'
        '<input class="vs-in" type="radio" name="vs" id="vs-spec">'
        '<label class="vs-lab" for="vs-spec">结构视图'
        + (f" · {n} IDs" if n else "") + "</label>"
    )


def render_doc_page(
    pack: Pack,
    doc: Doc,
    prefix: str,
    site_url: str = "",
    lang: str = "en",
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
            render_spec_view(spec_entry, prefix)
            + render_prompt_section(spec_entry, prefix, pack_dir)
        )
    spec = extra
    header = ""
    if is_overview:
        header = (
            '<div class="packhead">'
            f'<div class="packhead-titles"><h1>{html.escape(pack.title)}</h1>'
            + (f'<p class="zh" lang="zh-CN">{html.escape(pack.title_zh)}</p>' if pack.title_zh else "")
            + "</div>"
            f'<div class="packhead-meta">{pack_pills(pack)}'
            f'<span class="meta-plain">{html.escape(pack.domain)} / {html.escape(pack.subdomain)}</span>'
            f'<span class="meta-plain">v{html.escape(str(pack.manifest.get("version", "")))}</span>'
            "</div></div>"
        )
    body = (
        breadcrumb(prefix, pack)
        + header
        + render_view_switch(spec_entry if is_overview else None)
        + '<div class="layout">'
        + nav_tree(pack, doc.url, prefix)
        + f'<article class="prose">{annotate_lang(doc.html)}</article>'
        + render_toc(doc.toc)
        + "</div>"
        + spec
    )
    scripts = ""
    if "class=\"mermaid\"" in doc.html:
        scripts = mermaid_script(prefix)
    if is_overview and spec_entry:
        # The copy buttons are an enhancement; the prompts themselves are real
        # .md files, so without JS the action is still a working link.
        scripts += mermaid_script(prefix) if "class=\"mermaid\"" in doc.html else ""
        scripts += '<script src="' + prefix + 'assets/prompt-copy.js" defer></script>'
    return page_shell(
        title=f"{pack.title} · {doc.title}",
        description=pack.manifest.get("_summary", doc.title),
        prefix=prefix, body=body, body_class="pack", scripts=scripts,
        lang=lang, canonical=abs_url(site_url, doc.url),
    )


def render_plain_page(doc: Doc, prefix: str, site_url: str = "", lang: str = "en") -> str:
    body = f'<article class="prose prose-wide">{annotate_lang(doc.html)}</article>'
    scripts = mermaid_script(prefix) if 'class="mermaid"' in doc.html else ""
    return page_shell(
        title=doc.title, description=doc.title,
        prefix=prefix, body=body, body_class="doc", scripts=scripts,
        lang=lang, canonical=abs_url(site_url, doc.url),
    )


def mermaid_script(prefix: str = "") -> str:
    """Load the vendored mermaid build and start it in the current color scheme.

    The script tag carries an integrity hash so a tampered or truncated vendor
    file fails loudly instead of silently rendering nothing; the noscript
    fallback below is what readers see when JS is unavailable.
    """
    return (
        f'<script src="{prefix}assets/vendor/mermaid.min.js" '
        f'integrity="{VENDOR_EXPECTED["mermaid.min.js"]}" crossorigin="anonymous"></script>\n'
        "<script>(function(){var d=window.matchMedia"
        "&&window.matchMedia('(prefers-color-scheme: dark)').matches;"
        "window.mermaid&&window.mermaid.initialize("
        "{startOnLoad:true,theme:d?'dark':'default'});})();</script>"
    )


def render_catalog(packs: list[Pack], base_url: str, site_url: str = "", lang: str = "en") -> str:
    domains = sorted({p.domain for p in packs})
    maturities = ["L1", "L2", "L3", "L4"]
    verifications = ["unverified", "source-checked", "practitioner-reviewed", "field-proven"]

    cards = "".join(render_card(p) for p in sorted(packs, key=lambda p: p.slug))

    def count_for(field_name: str, value: str) -> int:
        return sum(1 for p in packs if str(p.manifest.get(field_name, "")) == value)

    def facet(field_name: str, values: list[str], label_fn) -> str:
        chips = "".join(
            f'<button class="chip" data-facet="{field_name}" data-value="{html.escape(v)}">'
            f'{html.escape(label_fn(v))}<span class="chip-n">{count_for(field_name, v)}</span>'
            "</button>"
            for v in values
        )
        return (
            f'<div class="facet" role="group" aria-label="{field_name}">'
            f'<span class="facet-label">{field_name}</span>{chips}</div>'
        )

    facets = (
        facet("domain", domains, lambda v: v)
        + facet("maturity", maturities, lambda v: v)
        + facet("verification", verifications, lambda v: v)
    )

    body = f"""
<section class="hero">
  <h1>Solution Atlas</h1>
  <p class="hero-sub">Production-grade blueprints for real enterprise systems —
     MES, WMS, IAM, BI and more — written for human architects and AI coding
     agents alike.</p>
  <div class="searchwrap">
    <input id="q" type="search" autocomplete="off" spellcheck="false"
           placeholder="Search {len(packs)} solutions — try “warehouse”, “OEE”, “federated login”, “FEFO”…"
           aria-label="Search solutions" aria-describedby="index-status">
    <kbd class="hint">/</kbd>
    <p id="index-status" class="index-status" role="status" hidden></p>
  </div>
  <p class="trustnote">Every pack is <code>llm-drafted</code>;
     <strong>none has been field-verified</strong>. Maturity measures
     completeness, not correctness — check each pack's <code>SOURCES.md</code>.</p>
</section>

<section class="controls">
  <div class="facets">{facets}</div>
  <button id="clear" class="clear" hidden>Clear filters</button>
</section>

<section id="results">
  <p id="count" class="count" aria-live="polite"></p>
  <div id="cards" class="cards">{cards}</div>
  <div id="hits" class="hits" hidden></div>
</section>
"""
    scripts = (
        f'<script src="assets/vendor/fuse.min.js" '
        f'integrity="{VENDOR_EXPECTED["fuse.min.js"]}" crossorigin="anonymous"></script>\n'
        f'<script src="assets/app.js" defer></script>\n'
        f'<script>window.__BASE__={json.dumps(base_url)};</script>'
    )
    return page_shell(
        title="Solution Atlas — blueprints for real enterprise systems",
        description="Searchable catalog of solution packs for enterprise systems: "
                    "manufacturing, logistics, identity, data & AI and more.",
        prefix="", body=body, body_class="catalog", icon="◈", scripts=scripts,
        lang=lang, canonical=abs_url(site_url, "index.html"),
    )


def render_card(pack: Pack) -> str:
    tags = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in pack.tags[:8])
    summary = str(pack.manifest.get("_summary", ""))
    zh = f'<p class="zh" lang="zh-CN">{html.escape(pack.title_zh)}</p>' if pack.title_zh else ""
    return (
        f'<article class="card" data-slug="{html.escape(pack.slug)}"'
        f' data-domain="{html.escape(pack.domain)}"'
        f' data-maturity="{html.escape(pack.maturity)}"'
        f' data-verification="{html.escape(pack.verification)}">'
        f'<a class="card-link" href="{pack.index_url}">'
        f'<h3>{html.escape(pack.title)}</h3></a>{zh}'
        f'<p class="card-sum">{html.escape(summary)}</p>'
        f'<div class="card-meta">{pack_pills(pack)}'
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


def generate_missing_indexes(out: Path) -> int:
    """Give every output directory a listing page if it lacks index.html.

    Links to a directory (``…/docs/``, ``…/packs/``) are rewritten to
    ``index.html`` during rendering; this makes those targets real.
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
        items = []
        for entry in entries:
            if entry.name == "index.html":
                continue
            if entry.is_dir():
                items.append(
                    f'<li><a href="{entry.name}/index.html">{html.escape(entry.name)}/</a></li>'
                )
            else:
                items.append(f'<li><a href="{entry.name}">{html.escape(entry.name)}</a></li>')
        if not items:
            continue
        rel = d.relative_to(out).as_posix()
        title = rel if rel != "." else "Open Solution Atlas"
        prefix = "../" * len(d.relative_to(out).parts)
        body = f'<h1>{html.escape(title)}</h1><ul class="dirlist">{"".join(items)}</ul>'
        write(index, page_shell(
            title=title, description=title, prefix=prefix, body=body, body_class="doc",
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


def write_404(out: Path, site_url: str = "", lang: str = "en") -> None:
    """Emit a branded ``404.html`` (GitHub Pages serves it on unknown paths)."""
    body = (
        '<section class="hero"><h1>Page not found</h1>'
        '<p class="hero-sub">That page does not exist — it may have been renamed '
        "when a pack was promoted. The catalog is searchable.</p>"
        '<div class="searchwrap">'
        '<a class="clear" href="index.html">← Back to the catalog</a></div>'
        "</section>"
    )
    write(
        out / "404.html",
        page_shell(
            title="Page not found — Solution Atlas",
            description="404 — the requested page does not exist.",
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
        "--lang", default="en",
        help="value of the <html lang> attribute for the site chrome "
             "(default: en); pack prose is language-tagged separately",
    )
    args = parser.parse_args()
    return build(ROOT / args.out, args.base_url, args.site_url, args.lang)


if __name__ == "__main__":
    sys.exit(main())

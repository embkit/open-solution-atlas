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

ROOT = Path(__file__).resolve().parent.parent
PACKS_DIR = ROOT / "packs"
DOCS_DIR = ROOT / "docs"
ASSETS_SRC = Path(__file__).resolve().parent / "site-assets"

FUSE_CDN = "https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js"
MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

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
    non-content trees (``templates/`` is scaffolding, ``_site/`` is output).
    """
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*.md")):
        parts = path.relative_to(ROOT).parts
        if any(part.startswith(".") for part in parts):
            continue
        if "_site" in parts or "templates" in parts or "tests" in parts:
            continue
        files.append(path)
    return files


def url_for(src: Path) -> str:
    """Map a source Markdown path to its site-relative output URL."""
    rel = src.relative_to(ROOT).as_posix()
    if rel.endswith("/README.md"):
        return rel[: -len("README.md")] + "index.html"
    if rel == "README.md":
        return "overview.html"
    return rel[:-3] + ".html"


def load_packs(summaries: dict[str, str]) -> list[Pack]:
    packs: list[Pack] = []
    for manifest_path in sorted(PACKS_DIR.glob("*/*/manifest.yaml")):
        pack_dir = manifest_path.parent
        try:
            data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
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
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{description}">
<title>{title}</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><text y='24' font-size='24'>{icon}</text></svg>">
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body class="{body_class}">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="{prefix}index.html"><span class="brand-mark">◈</span> Solution&nbsp;Atlas</a>
  <nav class="topnav">
    <a href="{prefix}index.html">Catalog</a>
    <a href="{prefix}docs/pack-standard.v1.html">Standard</a>
    <a href="{prefix}docs/taxonomy.html">Taxonomy</a>
    <a href="{prefix}docs/roadmap.html">Roadmap</a>
  </nav>
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
) -> str:
    return (
        HEAD.format(
            title=html.escape(title), description=html.escape(description),
            prefix=prefix, body_class=body_class, icon=icon,
        )
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
    """Sidebar: the pack's files grouped by their chapter directory."""
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
        out.append(f'<div class="navgroup"><span class="navgroup-label">{html.escape(label)}</span><ul>')
        for doc in sorted(groups[group], key=lambda d: d.rel):
            rel_inside = Path(doc.rel).relative_to(pack.rel_dir).as_posix()
            name = Path(rel_inside).name
            if name == "README.md":
                name = "overview"
            else:
                name = name[:-3]
            active = ' class="active"' if doc.url == current_url else ""
            href = prefix + doc.url
            out.append(f'<li><a{active} href="{href}">{html.escape(name)}</a></li>')
        out.append("</ul></div>")
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

def build(out: Path, base_url: str) -> int:
    summaries = load_summaries()
    packs = load_packs(summaries)
    if not packs:
        print("ERROR: no packs found", file=sys.stderr)
        return 1

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
            body = render_doc_page(pack, doc, prefix)
            write(out / doc.url, body)

    # ---- write non-pack pages --------------------------------------------
    for doc in other_docs:
        depth = doc.url.count("/")
        prefix = "../" * depth
        body = render_plain_page(doc, prefix)
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
    write(out / "index.html", render_catalog(packs, base_url))
    write(out / "search-index.json", json.dumps(build_index(packs, other_docs), ensure_ascii=False))

    # ---- assets ------------------------------------------------------------
    assets_out = out / "assets"
    assets_out.mkdir(exist_ok=True)
    for asset in ASSETS_SRC.iterdir():
        shutil.copy2(asset, assets_out / asset.name)

    # Any directory still lacking an index.html gets a generated listing, so
    # links to a directory (…/docs/, …/packs/) resolve.
    generated = generate_missing_indexes(out)

    pages = sum(1 for _ in out.rglob("*.html"))
    print(
        f"built {pages} pages, {len(packs)} packs, "
        f"{copied} linked asset(s), {generated} generated index(es) -> {out.relative_to(ROOT)}/"
    )

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


def render_doc_page(pack: Pack, doc: Doc, prefix: str) -> str:
    rel_inside = Path(doc.rel).relative_to(pack.rel_dir).as_posix()
    is_overview = rel_inside == "README.md"
    header = ""
    if is_overview:
        header = (
            '<div class="packhead">'
            f'<div class="packhead-titles"><h1>{html.escape(pack.title)}</h1>'
            + (f'<p class="zh">{html.escape(pack.title_zh)}</p>' if pack.title_zh else "")
            + "</div>"
            f'<div class="packhead-meta">{pack_pills(pack)}'
            f'<span class="meta-plain">{html.escape(pack.domain)} / {html.escape(pack.subdomain)}</span>'
            f'<span class="meta-plain">v{html.escape(str(pack.manifest.get("version", "")))}</span>'
            "</div></div>"
        )
    body = (
        breadcrumb(prefix, pack)
        + header
        + '<div class="layout">'
        + nav_tree(pack, doc.url, prefix)
        + f'<article class="prose">{doc.html}</article>'
        + render_toc(doc.toc)
        + "</div>"
    )
    scripts = ""
    if "class=\"mermaid\"" in doc.html:
        scripts = mermaid_script(prefix)
    return page_shell(
        title=f"{pack.title} · {doc.title}",
        description=pack.manifest.get("_summary", doc.title),
        prefix=prefix, body=body, body_class="pack", scripts=scripts,
    )


def render_plain_page(doc: Doc, prefix: str) -> str:
    body = f'<article class="prose prose-wide">{doc.html}</article>'
    scripts = mermaid_script(prefix) if 'class="mermaid"' in doc.html else ""
    return page_shell(
        title=doc.title, description=doc.title,
        prefix=prefix, body=body, body_class="doc", scripts=scripts,
    )


def mermaid_script(prefix: str = "") -> str:
    return (
        f'<script src="{MERMAID_CDN}"></script>\n'
        "<script>(function(){var d=window.matchMedia"
        "&&window.matchMedia('(prefers-color-scheme: dark)').matches;"
        "window.mermaid&&window.mermaid.initialize("
        "{startOnLoad:true,theme:d?'dark':'default'});})();</script>"
    )


def render_catalog(packs: list[Pack], base_url: str) -> str:
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
           aria-label="Search solutions">
    <kbd class="hint">/</kbd>
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
        f'<script src="{FUSE_CDN}"></script>\n'
        f'<script src="assets/app.js"></script>\n'
        f'<script>window.__BASE__={json.dumps(base_url)};</script>'
    )
    return page_shell(
        title="Solution Atlas — blueprints for real enterprise systems",
        description="Searchable catalog of solution packs for enterprise systems: "
                    "manufacturing, logistics, identity, data & AI and more.",
        prefix="", body=body, body_class="catalog", icon="◈", scripts=scripts,
    )


def render_card(pack: Pack) -> str:
    tags = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in pack.tags[:8])
    summary = str(pack.manifest.get("_summary", ""))
    zh = f'<p class="zh">{html.escape(pack.title_zh)}</p>' if pack.title_zh else ""
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
        })
        for doc in pack.docs:
            rel_inside = Path(doc.rel).relative_to(pack.rel_dir).as_posix()
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
    dirs = {f.parent for f in out.rglob("*") if f.is_file()}
    for d in sorted(dirs):
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
    parser.add_argument("--base-url", default="/", help="base URL the site is served from")
    args = parser.parse_args()
    return build(ROOT / args.out, args.base_url)


if __name__ == "__main__":
    sys.exit(main())

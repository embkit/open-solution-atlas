"""Tests for the Chinese corpus: it is complete, faithful, and actually used.

Three layers, each with its own failure mode.

1. **The checker** (``tools/check-translations.py``) must catch a missing
   translation, a translation that lost a rule, and a translation that is
   still English. A checker that passes a broken corpus is worse than none.
2. **The extractors** (``tools/pack_index.py``) must read the Chinese labels.
   A Chinese spec panel that silently drops every trace link is not a
   translation, it is a rendering bug with a nicer font.
3. **The build** (``tools/build-site.py``) must render the translation, and
   must say so on the page when a chapter has none.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
LOCALE = "zh-CN"


# --------------------------------------------------------------------------- #
# The checker
# --------------------------------------------------------------------------- #

def _write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_missing_translation_is_reported(check_translations, tmp_path):
    source = _write(tmp_path, "a.md", "# Title\n\nSome prose here.\n")
    translation = _write(tmp_path, "a.zh-CN.md", "# \u6807\u9898\n\n\u8fd9\u91cc\u662f\u4e00\u4e9b\u6bb5\u843d\u3002\n")
    problems = check_translations.compare(source, translation)
    assert problems == []


def test_a_lost_rule_is_caught(check_translations, tmp_path):
    source = _write(tmp_path, "b.md", "# R\n\n- **BR-01** first rule\n- **BR-02** second rule\n")
    translation = _write(
        tmp_path, "b.zh-CN.md",
        "# R\n\n- **BR-01** \u7b2c\u4e00\u6761\u89c4\u5219\n",
    )
    problems = check_translations.compare(source, translation)
    assert any("list items" in p for p in problems), problems
    assert any("BR-02" in p for p in problems), problems


def test_a_lost_identifier_is_caught(check_translations, tmp_path):
    source = _write(tmp_path, "c.md", "# R\n\nTraces: FR-001, BR-02\n")
    translation = _write(tmp_path, "c.zh-CN.md", "# R\n\n\u8ffd\u6eaf\uff1aFR-001\n")
    problems = check_translations.compare(source, translation)
    assert any("BR-02" in p and "lost" in p for p in problems), problems


def test_an_untranslated_line_is_caught(check_translations, tmp_path):
    source = _write(tmp_path, "d.md", "# R\n\nThe system shall enforce this rule.\n")
    translation = _write(tmp_path, "d.zh-CN.md", "# R\n\n\u7cfb\u7edf\u5e94\u5f53\u5f3a\u5236\u6267\u884c\u8be5\u89c4\u5219\u3002\n")
    assert check_translations.compare(source, translation) == []


def test_english_left_in_a_translation_is_caught(check_translations, tmp_path):
    source = _write(tmp_path, "e.md", "# R\n\nThe system shall enforce this rule.\n")
    translation = _write(tmp_path, "e.zh-CN.md", "# R\n\nThe system shall enforce this rule.\n")
    problems = check_translations.compare(source, translation)
    assert any("not translated" in p for p in problems), problems


def test_corrupt_text_is_caught(check_translations, tmp_path):
    source = _write(tmp_path, "f.md", "# R\n\n\u4e2d\u6587\u3002\n")
    translation = _write(tmp_path, "f.zh-CN.md", "# R\n\n\u4e2d\u6587\ufffd\u3002\n")
    problems = check_translations.compare(source, translation)
    assert any("corrupt" in p for p in problems), problems


def test_code_blocks_are_not_mistaken_for_untranslated_prose(check_translations, tmp_path):
    source = _write(tmp_path, "g.md", "# R\n\n```\nconst a = 1;\n```\n")
    translation = _write(tmp_path, "g.zh-CN.md", "# R\n\n```\nconst a = 1;\n```\n")
    assert check_translations.compare(source, translation) == []


def test_a_multiline_html_comment_is_not_prose(check_translations, tmp_path):
    """A comment that spans lines is comment on every line it spans.

    A line-wise pattern cannot see that at all - `.` does not cross a
    newline - so the checker tracks the comment as state, the way it
    already tracks a code fence.
    """
    body = "# R\n\n<!-- This note is kept in English.\nIt spans two lines.\n-->\n\n\u6b63\u6587\u3002\n"
    source = _write(tmp_path, "h.md", body)
    translation = _write(tmp_path, "h.zh-CN.md", body)
    assert check_translations.compare(source, translation) == []


def test_prose_after_a_multiline_comment_is_still_checked(check_translations, tmp_path):
    source = _write(tmp_path, "i.md", "# R\n\n<!-- note\nstill the note\n-->\n\n\u6b63\u6587\u3002\n")
    translation = _write(
        tmp_path, "i.zh-CN.md",
        "# R\n\n<!-- note\nstill the note\n-->\n\nThe system shall enforce this rule.\n",
    )
    problems = check_translations.compare(source, translation)
    assert any("not translated" in p for p in problems), problems


# --------------------------------------------------------------------------- #
# The corpus itself
# --------------------------------------------------------------------------- #

def test_every_pack_file_is_in_the_checkers_inventory(check_translations):
    """No file may be invisible to the checker.

    A file the checker does not know about is a file nobody will ever be
    told is missing a translation, so the inventory has to cover every
    Markdown file in the pack.
    """
    for pack in sorted(p for p in (ROOT / "packs").glob("*/*") if (p / "manifest.yaml").exists()):
        listed = {p.resolve() for p in check_translations.translatable_files(pack)}
        on_disk = {
            p.resolve()
            for p in pack.rglob("*.md")
            if not p.name.endswith(f".{LOCALE}.md")
            and "translations" not in p.relative_to(pack).parts
        }
        assert listed == on_disk, sorted(str(p) for p in on_disk ^ listed)


# --------------------------------------------------------------------------- #
# The extractors read Chinese
# --------------------------------------------------------------------------- #

def test_chinese_requirement_is_parsed_with_its_traces(pack_index):
    index = pack_index.build_index(LOCALE)
    pack = next(p for p in index["packs"] if p["slug"] == "itsm-helpdesk")
    fr = next(r for r in pack["requirements"] if r["id"] == "FR-001")
    assert fr["name"], fr
    assert re.search(r"[\u4e00-\u9fff]", fr["name"]), fr
    assert re.search(r"[\u4e00-\u9fff]", fr["when"]), fr
    assert "BR-11" in fr["traces"], fr


def test_chinese_index_matches_the_english_one_in_shape(pack_index):
    """Same identifiers, same counts. The content differs; the structure does not."""
    en = pack_index.build_index()
    zh = pack_index.build_index(LOCALE)
    en_by = {p["slug"]: p for p in en["packs"]}
    for pack in zh["packs"]:
        source = en_by[pack["slug"]]
        assert pack["counts"] == source["counts"], pack["slug"]
        assert [a["id"] for a in pack["adrs"]] == [a["id"] for a in source["adrs"]], pack["slug"]
        assert [r["id"] for r in pack["rules"]] == [r["id"] for r in source["rules"]], pack["slug"]


def test_the_english_index_is_not_affected_by_the_chinese_one(pack_index):
    """The bilingual parsers must not change what the English build reports."""
    en = pack_index.build_index()
    for slug in ("itsm-helpdesk", "personal-blog", "wms"):
        pack = next(p for p in en["packs"] if p["slug"] == slug)
        assert pack["counts"]["rules"] > 0
        assert pack["counts"]["requirements"] > 0
        assert pack["counts"]["adrs"] > 0


def test_a_translated_adrs_decision_is_read(pack_index):
    index = pack_index.build_index(LOCALE)
    pack = next(p for p in index["packs"] if p["slug"] == "itsm-helpdesk")
    adr = next(a for a in pack["adrs"] if a["id"] == "ADR-0001")
    assert re.search(r"[\u4e00-\u9fff]", adr["name"]), adr
    assert re.search(r"[\u4e00-\u9fff]", adr["decision"]), adr
    assert adr["rejected"], adr


def test_the_store_claim_is_read_from_chinese(pack_index):
    """`Constraints 1, 3 ? are enforced in the store` has a Chinese twin."""
    index = pack_index.build_index(LOCALE)
    pack = next(p for p in index["packs"] if p["slug"] == "itsm-helpdesk")
    stored = sorted(c["n"] for c in pack["constraints"] if c["store"])
    assert stored == [1, 3, 8, 10, 11, 12, 15], stored


# --------------------------------------------------------------------------- #
# The build uses it
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="module")
def zh_site(tmp_path_factory):
    out = tmp_path_factory.mktemp("zh-site")
    result = subprocess.run(
        [sys.executable, "tools/build-site.py", "--lang", "zh", "--out", str(out), "--site-url="],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return out


def test_a_translated_pack_renders_in_chinese(zh_site):
    page = (zh_site / "packs/horizontal/itsm-helpdesk/index.html").read_text(encoding="utf-8")
    assert "transnote" not in page, "a translated pack must not carry the fallback banner"
    assert re.search(r"[\u4e00-\u9fff]{4,}", page)


def _tracked_pages(zh_site, build_site) -> list[Path]:
    """The site pages that come from tracked repository content.

    A working checkout can carry directories that are not project content -
    the ux-ui-agent-skills kit is one - and the build renders whatever
    Markdown it finds on disk. Only the tracked files are the repository's
    own pages, so only they are the repository's business.

    One tracked directory is excluded on purpose: `design-systems/` is
    committed *verbatim* as an external reference and is not part of the
    translated corpus (AGENTS.md says so where it enters the boundary).
    Its pages carry the banner by design - the banner is doing its exact
    job there, telling a Chinese reader that this reference is English.
    """
    out = subprocess.run(
        ["git", "ls-files", "*.md"], cwd=ROOT,
        capture_output=True, text=True, check=True,
    )
    pages = []
    for rel in out.stdout.splitlines():
        if rel.endswith(".zh-CN.md"):
            continue  # a translation is rendered in place of its original
        if rel.startswith("design-systems/"):
            continue  # vendored reference: English, verbatim, untranslated
        page = zh_site / build_site.url_for(ROOT / rel)
        if page.is_file():
            pages.append(page)
    return pages


def test_no_tracked_chapter_carries_the_fallback_banner(zh_site, build_site):
    """The corpus is complete, so no page announces a missing translation.

    The banner exists for a chapter that has no Chinese sibling yet. With
    every chapter translated there is nothing to announce, and a banner left
    behind would tell a Chinese reader that a page they are reading in
    Chinese is not.
    """
    offenders = [
        page.relative_to(zh_site).as_posix()
        for page in _tracked_pages(zh_site, build_site)
        if "transnote" in page.read_text(encoding="utf-8")
    ]
    assert offenders == [], f"pages still carrying the fallback banner: {offenders[:10]}"


def test_the_fallback_banner_still_exists(build_site):
    """A chapter without a translation must announce itself.

    The corpus is complete today, so this cannot be checked against the
    repository; the notice itself is what has to keep working, in the
    reader's language.
    """
    note = build_site.translation_note("zh")
    assert "transnote" in note
    assert re.search(r"[\u4e00-\u9fff]{4,}", note), (
        "the notice must be written in the language of the page"
    )


def test_the_catalogue_is_chinese(zh_site):
    page = (zh_site / "index.html").read_text(encoding="utf-8")
    assert 'lang="zh-CN"' in page
    assert re.search(r"[\u4e00-\u9fff]{4,}", page)

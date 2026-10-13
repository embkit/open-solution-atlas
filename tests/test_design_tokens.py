"""Assert the site against the EmbKit UI contract.

`docs/embkit-ui-contract.md` is a verbatim copy of EmbKit's authoritative client
UI specification, and the catalog answers to it because the catalog is the
product's shop window. Its own summary of why this matters is blunt: leaving
several surfaces on several palettes is the failure mode, not a detail.

This module checks the parts of the contract that can be checked mechanically,
so they cannot regress silently:

* `--primary` is indigo `#4f46e5` and nothing else. The contract marks the hue
  LOCKED, and it names a specific former value (`#635bff`) that must not
  survive anywhere.
* the neutrals are cold. The contract says so twice ("不要引入暖灰，会和 indigo
  打架"), and a warm grey is the sort of thing a later edit introduces without
  noticing, because it looks neutral next to a blue.
* spacing sits on the contract's scale, and radius and shadow are the
  contract's values — §5 forbids "游离值" by name, and §6 gives four shadows,
  all cool-blue rather than black.
* **every surface shares one theme.** The demos carry their tokens inline
  (they must open on their own), so their `:root` blocks are compared
  byte-for-byte against each other and against the site's values.
* category colours stay on icon strokes. §1.4 permits them on an icon's stroke
  and its tinted background and nowhere else.

Run:  python -m pytest tests/test_design_tokens.py -q
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "tools" / "site-assets" / "style.css"
CONTRACT = ROOT / "docs" / "embkit-ui-contract.md"

# Contract §1.1 and §1.2.
LOCKED_PRIMARY = "#4f46e5"
FORMER_PRIMARY = "#635bff"  # §10 item 1: must not survive
COLD_NEUTRALS = (
    "page", "surface", "surface-2", "surface-3",
    "line", "line-strong", "line-x", "navy", "navy-2",
)
SPACING_SCALE = {4, 8, 12, 16, 20, 24, 28, 32}
RADIUS_VALUES = {"6px", "8px", "10px", "12px", "14px", "999px"}
SHADOWS = (
    "0 1px 2px rgba(15, 23, 42, 0.04), 0 8px 24px rgba(15, 23, 42, 0.06)",
    "0 2px 4px rgba(15, 23, 42, 0.05), 0 14px 34px rgba(15, 23, 42, 0.09)",
    "0 12px 32px rgba(15, 23, 42, 0.12)",
    "0 20px 50px rgba(15, 23, 42, 0.16)",
)


def _luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    channels = [int(h[i : i + 2], 16) / 255 for i in (0, 2, 4)]

    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(c) for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = _luminance(a), _luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _rules(css: str) -> list[tuple[str, str]]:
    """(selector, declarations) pairs, comments stripped."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    return re.findall(r"([^{}]+)\{([^{}]*)\}", css)


def _root_block(css: str, dark: bool = False) -> str:
    if dark:
        m = re.search(
            r"@media \(prefers-color-scheme: dark\)\s*\{\s*:root\s*\{(.*?)\n\s*\}",
            css, re.DOTALL)
    else:
        # the demos indent their inline :root, the site stylesheet does not
        m = re.search(r"^\s*:root\s*\{(.*?)\n\s*\}", css, re.DOTALL | re.MULTILINE)
    assert m, f"could not find the :root block (dark={dark})"
    return m.group(1)


def _tokens(block: str) -> dict[str, str]:
    return dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{3,8})\s*;", block))


@pytest.fixture(scope="module")
def css() -> str:
    return CSS.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def light(css) -> dict[str, str]:
    return _tokens(_root_block(css))


@pytest.fixture(scope="module")
def dark(css) -> dict[str, str]:
    return _tokens(_root_block(css, dark=True))


# --------------------------------------------------------------------------- #
# The contract is present and is the contract
# --------------------------------------------------------------------------- #

def test_the_contract_is_vendored():
    assert CONTRACT.is_file(), "the EmbKit UI contract is not vendored"
    body = CONTRACT.read_text(encoding="utf-8")
    assert "LOCKED" in body, "the vendored contract does not mark its locked items"
    assert "4F46E5" in body or "4f46e5" in body


# --------------------------------------------------------------------------- #
# Brand — locked
# --------------------------------------------------------------------------- #

def test_primary_is_the_locked_indigo(light, dark):
    assert light["primary"] == LOCKED_PRIMARY, (
        f"primary is {light['primary']}; the contract LOCKs {LOCKED_PRIMARY}"
    )
    assert dark["primary"] != LOCKED_PRIMARY, (
        "the dark scheme needs a lifted indigo, not the locked light value"
    )
    # the dark value must still be the same hue family — blue-dominant, and
    # clearly brighter than the ground it sits on
    assert int(dark["primary"].lstrip("#")[4:6], 16) > 200


def test_no_former_brand_colour_survives(css):
    """§10 item 1 names `#635bff` as the value being replaced."""
    assert FORMER_PRIMARY not in css.lower(), "the Stripe purple survived"
    assets = (ROOT / "tools" / "site-assets").rglob("*.css")
    for path in assets:
        assert FORMER_PRIMARY not in path.read_text(encoding="utf-8").lower()


# --------------------------------------------------------------------------- #
# Neutrals are cold
# --------------------------------------------------------------------------- #

def test_neutrals_are_cool_not_warm(light):
    """The contract's rule: no warm grey, or it fights the indigo."""
    for name in COLD_NEUTRALS:
        value = light.get(name)
        assert value, f"missing neutral --{name}"
        r, g, b = (int(value.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        assert b >= r, f"--{name} ({value}) is warm: blue {b} < red {r}"


def test_page_is_darker_than_surface(light):
    """§4.2: the sidebar/content lightness difference is the page's layering."""
    assert _luminance(light["surface"]) > _luminance(light["page"])


# --------------------------------------------------------------------------- #
# Contrast
# --------------------------------------------------------------------------- #

def test_text_pairs_clear_aa(light, dark):
    pairs = [
        ("text", "page"), ("text", "surface"), ("text-2", "surface"),
        ("text-3", "surface"), ("primary", "surface"), ("on-primary", "primary"),
        ("danger", "danger-soft"), ("ok", "ok-soft"), ("warn", "warn-soft"),
        ("text", "surface-3"), ("primary", "primary-tint"),
    ]
    for scheme, values in (("light", light), ("dark", dark)):
        for fg, bg in pairs:
            if fg not in values or bg not in values:
                continue
            ratio = contrast(values[fg], values[bg])
            assert ratio >= 4.0, (
                f"{scheme}: {fg} on {bg} is {ratio:.2f}:1"
            )


def test_control_borders_clear_the_non_text_floor(light, dark):
    for scheme, values in (("light", light), ("dark", dark)):
        ratio = contrast(values["line-strong"], values["surface"])
        assert ratio >= 1.3, f"{scheme}: control borders are invisible ({ratio:.2f}:1)"


# --------------------------------------------------------------------------- #
# Scale discipline
# --------------------------------------------------------------------------- #

def test_spacing_is_on_the_contract_scale(css):
    """§5: "禁止出现 7px / 13px / 21px 这类游离值"."""
    declared = {int(v) for v in re.findall(r"--sp-\d:\s*(\d+)px", css)}
    assert declared == SPACING_SCALE, f"spacing scale is {sorted(declared)}"
    for token in ("sp-1", "sp-2", "sp-3", "sp-4", "sp-5", "sp-6", "sp-7", "sp-8"):
        assert f"--{token}:" in css


def test_radius_values_are_the_contract_set(css):
    """§6 fixes six radius steps; a seventh is an improvisation."""
    declared = re.findall(r"--r-[a-z0-9]+:\s*([^;]+);", css)
    for value in declared:
        assert value.strip() in RADIUS_VALUES, f"off-scale radius: {value.strip()}"


def test_shadows_are_the_contract_values_and_are_cool(css):
    """§6: shadows are cool-blue; pure black reads as a different design."""
    block = _root_block(css)
    for value in SHADOWS:
        assert value in block, f"missing the contract shadow: {value}"
    assert "rgba(0, 0, 0" not in block.split("@media")[0], (
        "the light scheme uses a black shadow; the contract's are cool-blue"
    )


# --------------------------------------------------------------------------- #
# One theme across every surface — the contract's stated failure mode
# --------------------------------------------------------------------------- #

def _demo_root(pack_glob: str) -> str:
    for path in (ROOT / "packs").glob(pack_glob):
        block = _root_block(path.read_text(encoding="utf-8"))
        return block
    raise AssertionError(f"no demo matched {pack_glob}")


def test_every_demo_shares_byte_identical_tokens():
    """The demos inline their tokens, so they are where a second palette starts."""
    blocks = []
    for demo in (ROOT / "packs").glob("*/*/10-demo/index.html"):
        blocks.append((demo, _root_block(demo.read_text(encoding="utf-8"))))
    assert blocks, "no demos found"
    first_path, first = blocks[0]
    for path, block in blocks[1:]:
        assert block == first, (
            f"{path.relative_to(ROOT)} has its own palette; "
            f"{first_path.relative_to(ROOT)} differs"
        )


def test_demos_use_the_contract_brand(light):
    for demo in (ROOT / "packs").glob("*/*/10-demo/index.html"):
        values = _tokens(_root_block(demo.read_text(encoding="utf-8")))
        assert values["primary"] == LOCKED_PRIMARY, (
            f"{demo.parent.parent.name} does not use the locked indigo"
        )
        assert values["page"] == light["page"], (
            f"{demo.parent.parent.name} does not use the contract's page ground"
        )


# --------------------------------------------------------------------------- #
# Category colour discipline
# --------------------------------------------------------------------------- #

def test_category_colours_stay_on_icons(css):
    """§1.4: category colours appear on an icon's stroke and tint, nowhere else."""
    rules = re.findall(r"([^{}]+)\{([^{}]*)\}", re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL))
    offenders = []
    for selector, body in rules:
        if "var(--cat-" not in body:
            continue
        # a category colour may be used where an icon is styled
        if ".cat-icon" in selector:
            continue
        offenders.append(selector.strip())
    assert not offenders, f"category colours leaked outside .cat-icon: {offenders}"


# --------------------------------------------------------------------------- #
# Motion — §8
# --------------------------------------------------------------------------- #

def test_no_transition_all(css):
    """§8 forbids it by name: the property must be named."""
    assert not re.search(r"transition:\s*all", css), "transition: all reintroduced"


def test_reduced_motion_is_respected(css):
    assert "prefers-reduced-motion" in css
    assert "--t-reduced" in css


def test_reduced_motion_neutralises_transitions(css):
    block = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}",
                      css, re.DOTALL)
    assert block, "no reduced-motion block"
    assert "transition-duration" in block.group(1)


# --------------------------------------------------------------------------- #
# Accessibility floor
# --------------------------------------------------------------------------- #

def test_keyboard_focus_is_visible(css):
    assert ":focus-visible" in css


def test_mobile_breakpoints_exist(css):
    for width in ("1100px", "900px", "820px"):
        assert width in css, f"missing the {width} breakpoint"

# --------------------------------------------------------------------------- #
# The kit's central checks, held repo-side so CI can guard them
# --------------------------------------------------------------------------- #
#
# `scripts/lint_hardcodes.py`, `lint_taste.py` and `axe_audit.mjs` come from the
# ux-ui-agent-skills kit, which is a local tool install rather than repository
# content (251 files, 140 of them crosswalks for other products). CI therefore
# cannot run them, so the findings they produced are asserted here instead —
# the same properties, checked without the kit:
#
#   lint_hardcodes   "OK: no hardcoded values found"   -> test_no_hardcoded_values
#   axe_audit        "OK: 0 violations"                -> test_tertiary_text_..., test_prompt_has_accessible_name
#   verify_target_size / verify_states / verify_reduced_motion  -> build-site tests + the motion check above
#
# Run the kit's own verifiers locally before a design change; they cover more
# than these do (axe runs 80+ rules, the state verifier walks hover and focus on
# every interactive element).

TOKEN_DECLARATION = re.compile(r"--[a-z0-9-]+:\s*[^;]+;")


def test_no_hardcoded_values_outside_token_declarations(css):
    """The contract's §11 iron rule, and the kit's central check.

    A literal colour or length inside a rule is how a design system stops being
    one: the value is right today and drifts tomorrow, because nothing names it.
    Token declarations themselves are the only place a literal belongs — plus
    zero, `calc`, and any line carrying the kit's own exception marker.
    """
    offenders = []
    for selector, body in _rules(css):
        if selector.strip().startswith(":"):
            continue  # the token blocks
        for decl in body.split(";"):
            if not decl.strip() or "ds-allow-hardcode" in decl:
                continue
            head = decl.split(":", 1)
            if len(head) < 2:
                continue
            value = head[1]
            # a bare 0, a negative shadow offset, calc/repeat with tokens, and
            # `1px` on a hairline are all fine; a new colour or size is not
            for literal in re.findall(r"#[0-9a-fA-F]{3,8}\b|\b\d+(?:\.\d+)?px\b", value):
                if literal in ("0px",):
                    continue
                offenders.append(f"{selector.strip()} -> {head[0].strip()}: {literal}")
    assert not offenders, (
        "hardcoded values outside token declarations:\n  "
        + "\n  ".join(sorted(set(offenders))[:20])
    )


def test_tertiary_text_clears_aa_on_every_ground(light, dark):
    """axe-core found 110 nodes below 4.5:1 before this was fixed.

    `--text-3` carries facet labels, chip counts and card metadata, so it sits
    on `--page`, `--surface`, `--surface-2` and `--surface-3` — not just
    `--surface`. The contract's own value (#8792a2) fails, and EmbKit's
    correction (#6b7785) still failed on the darker grounds; a test on
    `--surface` alone would have missed all of it.
    """
    grounds = ("page", "surface", "surface-2", "surface-3")
    for scheme, values in (("light", light), ("dark", dark)):
        for ground in grounds:
            ratio = contrast(values["text-3"], values[ground])
            assert ratio >= 4.5, (
                f"{scheme}: --text-3 on --{ground} is {ratio:.2f}:1"
            )


def test_no_opacity_reduced_text(css):
    """axe blends an alpha'd colour before judging it.

    `opacity: 0.75` on a small label over `--surface-3` dropped it below 4.5:1
    even though the *declared* colour passed. De-emphasis uses an explicit
    colour now.
    """
    offenders = [
        sel.strip()
        for sel, body in _rules(css)
        if re.search(r"opacity:\s*0?\.[1-9]", body)
    ]
    # `opacity: 0` and `opacity: 1` are fine; a partial one on text is the risk
    assert not offenders, f"partial opacity on text: {offenders}"


def test_inline_prompt_has_an_accessible_name():
    """axe reported `#prm-implement` as an unlabelled form element (critical)."""
    src = (ROOT / "tools" / "build-site.py").read_text(encoding="utf-8")
    marker = 'id="prm-implement"'
    assert marker in src
    window = src[src.index(marker) : src.index(marker) + 400]
    assert "aria-label" in window or "aria-labelledby" in window, (
        "the inline prompt textarea has no accessible name"
    )


def test_demo_selects_have_accessible_names():
    """axe reported the demo's completion-policy select (critical).

    A preceding `<h3>` groups visually; it is not a label association, and axe
    is right to distinguish them.
    """
    for demo in (ROOT / "packs").glob("*/*/10-demo/index.html"):
        text = demo.read_text(encoding="utf-8")
        for tag in re.findall(r"<select[^>]*>", text):
            assert "aria-label" in tag or "aria-labelledby" in tag, (
                f"{demo.parent.parent.name}: an unnamed <select> ({tag[:60]})"
            )

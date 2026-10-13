"""Tests for the site's design tokens and the rules the design is built on.

The stylesheet is a design system with a stated point of view, and this module
checks the parts that can silently regress:

* **contrast** — the token pairs a person actually reads, computed rather than
  eyeballed. The structural rule and the control rule are held to different
  floors, because they do different jobs: a hairline between rows only has to
  be perceivable, while the border of a control must clear WCAG 1.4.11's 3:1.
* **no rounded containers, no elevation** — hierarchy in this design comes
  from line weight and column alignment. A `border-radius` or a `box-shadow`
  reintroduced by a later change is the SaaS-card kit creeping back, and it
  would not be caught by any functional test.
* **no ALL-CAPS labels** — tracked-out caps over every heading is one of the
  commonest tells of a generated page.

Run:  python -m pytest tests/test_design_tokens.py -q
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

CSS = Path(__file__).resolve().parent.parent / "tools" / "site-assets" / "style.css"


# --------------------------------------------------------------------------- #
# Contrast maths, so the floor is computed and not asserted by eye
# --------------------------------------------------------------------------- #

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


@pytest.fixture(scope="module")
def tokens() -> dict[str, dict[str, str]]:
    """Both colour schemes, parsed out of the stylesheet's `:root` blocks."""
    css = CSS.read_text(encoding="utf-8")
    light = re.search(r":root\s*\{(.*?)\n\}", css, re.DOTALL)
    dark = re.search(r"@media \(prefers-color-scheme: dark\)\s*\{\s*:root\s*\{(.*?)\n\s*\}", css, re.DOTALL)
    assert light and dark, "could not find both colour schemes"

    def parse(block: str) -> dict[str, str]:
        return dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{3,8})\s*;", block))

    return {"light": parse(light.group(1)), "dark": parse(dark.group(1))}


# --------------------------------------------------------------------------- #
# The palette
# --------------------------------------------------------------------------- #

def test_one_accent_and_one_warning_colour(tokens):
    """The palette is three neutrals, one accent, one violation colour.

    `-soft` variants are tints of their own hue, not new colours, so they are
    counted as part of the family. What this guards against is a *third* accent
    arriving for a new concept — an ochre for policy targets, a green for
    success — because a palette that grows one colour per concept stops meaning
    anything, and red stops meaning violated.
    """
    for scheme, values in tokens.items():
        families = {name.rsplit("-", 1)[0] for name in values}
        assert "revise" in families, f"{scheme} lost the violation colour"
        assert "draft" in families, f"{scheme} lost the accent"
        others = families - {
            "vellum", "ink", "rule", "draft", "revise", "code"
        }
        assert not others, f"{scheme} grew a new colour family: {sorted(others)}"


def test_text_pairs_clear_aa(tokens):
    """Every pair a person reads, in both schemes."""
    pairs = [
        ("ink", "vellum"),
        ("ink-soft", "vellum"),
        ("draft", "vellum"),
        ("vellum", "draft"),
        ("revise", "vellum"),
        ("revise", "revise-soft"),
        ("ink", "code-bg"),
        ("draft", "draft-soft"),
    ]
    for scheme, values in tokens.items():
        for fg, bg in pairs:
            if fg not in values or bg not in values:
                continue
            ratio = contrast(values[fg], values[bg])
            assert ratio >= 4.5, (
                f"{scheme}: {fg} on {bg} is {ratio:.2f}:1, below AA 4.5:1"
            )


def test_control_borders_clear_the_non_text_floor(tokens):
    """WCAG 1.4.11: 3:1 for anything identifying a control.

    `rule-strong` borders the inputs, chips and buttons. `rule` only separates
    rows, where adjacent content already carries its own leading, so it is held
    to a lower perceivability floor and that split is deliberate.
    """
    for scheme, values in tokens.items():
        assert contrast(values["rule-strong"], values["vellum"]) >= 3.0, (
            f"{scheme}: control borders are {contrast(values['rule-strong'], values['vellum']):.2f}:1"
        )
        assert contrast(values["rule"], values["vellum"]) >= 1.7, (
            f"{scheme}: structural rules barely perceivable"
        )


def test_dark_scheme_is_a_real_dark_scheme(tokens):
    """Not a half-measure: the ground must actually be dark."""
    assert _luminance(tokens["dark"]["vellum"]) < 0.1
    assert _luminance(tokens["light"]["vellum"]) > 0.7


# --------------------------------------------------------------------------
# The principles, checked mechanically
# --------------------------------------------------------------------------

def _rules(css: str) -> list[str]:
    """Selector-declaration pairs, comments stripped."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    return re.findall(r"([^{}]+)\{([^{}]*)\}", css)


def test_no_rounded_containers():
    """`border-radius: 0` is the design's stance; any other value is a card."""
    css = CSS.read_text(encoding="utf-8")
    offenders = []
    for sel, body in _rules(css):
        for value in re.findall(r"border-radius:\s*([^;]+)", body):
            if value.strip() != "0":
                offenders.append(sel.strip())
    assert not offenders, f"rounded containers reintroduced: {sorted(set(offenders))}"


def test_no_elevation():
    """No `box-shadow`: hierarchy comes from line weight, not from shadow."""
    css = CSS.read_text(encoding="utf-8")
    offenders = [
        sel.strip() for sel, body in _rules(css) if "box-shadow" in body
    ]
    assert not offenders, f"shadow reintroduced: {offenders}"


def test_no_all_caps_labels():
    """Tracked-out caps over headings is a tell of a generated page."""
    css = CSS.read_text(encoding="utf-8")
    offenders = [
        sel.strip()
        for sel, body in _rules(css)
        if re.search(r"text-transform:\s*uppercase", body)
    ]
    assert not offenders, f"ALL-CAPS labels reintroduced: {offenders}"


def test_reduced_motion_is_respected():
    css = CSS.read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in css, "reduced motion not honoured"


def test_keyboard_focus_is_visible():
    css = CSS.read_text(encoding="utf-8")
    assert ":focus-visible" in css, "no visible focus style"


def test_mobile_breakpoint_exists():
    css = CSS.read_text(encoding="utf-8")
    assert "max-width: 760px" in css, "no mobile breakpoint"

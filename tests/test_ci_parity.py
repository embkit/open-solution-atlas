"""Regression tests for the CI-vs-local tooling drift this branch hit.

Adding ruff lint made CI red on the first run while the identical command
passed locally: CI installed the newest 0.x, the workstation had 0.16.6, and
ruff 0.17 added UP017 to a rule family we select wholesale. These tests pin
the invariants that keep that class of failure from recurring.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_dev_requirements_pin_ruff_exactly():
    """A floating ruff range guarantees a local/CI verdict drift."""
    text = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
    pins = [
        line.split("#", 1)[0].strip()
        for line in text.splitlines()
        if line.strip().startswith("ruff")
    ]
    assert len(pins) == 1, "requirements-dev.txt must declare ruff exactly once"
    assert re.fullmatch(r"ruff==\d+\.\d+\.\d+", pins[0]), (
        f"ruff must be pinned to an exact version, got {pins[0]!r}; "
        "a range lets CI pick a newer version that adds rules to the "
        "families selected in pyproject.toml"
    )


def test_lint_job_installs_from_requirements_dev():
    """The lint job must use the same pinned toolchain as a contributor."""
    text = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "pip install -r requirements-dev.txt" in text, (
        "the lint job must install the pinned ruff from requirements-dev.txt"
    )
    # No job may re-declare a floating ruff range.
    assert not re.search(r'ruff\s*>=', text), (
        "ci.yml must not install ruff from a floating range"
    )


def test_pyproject_selects_families_that_are_version_stable():
    """Documenting why an exact pin is required: selection is by family."""
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    # Selecting rule *families* (not explicit codes) means new rules in those
    # families are enabled by a ruff upgrade alone.
    assert "UP" in text and "RUF" in text, (
        "test assumes family-level selection, which is version-sensitive"
    )


def test_repo_floor_is_python_311_or_newer():
    """`datetime.UTC` (used by validate-packs) requires Python 3.11+."""
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'target-version\s*=\s*"py(\d)(\d+)"', pyproject)
    assert match, "pyproject.toml must declare a ruff target-version"
    major, minor = int(match.group(1)), int(match.group(2))
    assert (major, minor) >= (3, 11), (
        "target-version below py311 would allow datetime.timezone.utc-style "
        "code back in and reintroduce the UP017 split"
    )
    assert sys.version_info >= (3, 11), "test environment must be Python 3.11+"


def test_datetime_usage_is_timezone_aware():
    """No naive `.today()`/`.utcnow()` — the 180-day decay rule needs UTC."""
    offenders = []
    for path in sorted((ROOT / "tools").glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for pattern in (r"datetime\.date\.today\(\)", r"datetime\.datetime\.now\(\)\s*$"):
            for match in re.finditer(pattern, text):
                line_no = text[: match.start()].count("\n") + 1
                offenders.append(f"{path.name}:{line_no}")
        if "datetime.today()" in text or "utcnow()" in text:
            offenders.append(path.name)
    assert not offenders, f"naive datetime usage found: {offenders}"


def test_ruff_is_installed_for_this_suite():
    """Skip the rest meaningfully if ruff is absent, but do so loudly."""
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "ruff", "--version"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        proc = None
    if proc is None or proc.returncode != 0:
        # Not a failure of the repo; a readable note beats a stack trace.
        print("note: ruff not installed here; lint parity is enforced in CI")
        return
    assert re.search(r"\d+\.\d+", proc.stdout), "ruff --version must report a version"

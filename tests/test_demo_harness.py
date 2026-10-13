"""Run the demo harness for every demo, so a demo that dies on load fails CI.

The harness (`tools/demo-harness/`) loads a demo's inline script against a
minimal DOM and asserts two things that matter more than the layout:

  - **smoke**: it loads, and every control it renders can be clicked.
  - **semantic**: it *fails correctly* — the invariant panel lights up on the
    action the pack's rule is about.

It lives here rather than in a scratch directory because a demo is the
interactive half of a pack and a demo that throws on load is worse than no demo.
It was in a scratch directory while the first three were written, and a demo
reached the published site referencing an element its page never declared: the
browser threw on load, and the harness passed it, because the stub minted a node
for any id asked for. Both halves of that are fixed — the stub returns null for
an unknown id and registers the ids the HTML declares — and the regression is
now impossible to reintroduce silently.

Node is required. It is present on the CI runner and on any machine that builds
the demos, but the check skips rather than fails where it is absent: a missing
runtime is not a demo defect.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
HARNESS = ROOT / "tools" / "demo-harness" / "demo_check.js"
NODE = shutil.which("node")


def _demos() -> list[Path]:
    return sorted(ROOT.glob("packs/*/*/10-demo/index.html"))


pytestmark = pytest.mark.skipif(
    NODE is None, reason="node is not installed; the demo harness needs it"
)


@pytest.mark.parametrize("mode", ["smoke", "semantic"])
@pytest.mark.parametrize("demo", _demos(), ids=lambda p: p.parent.parent.name)
def test_demo(demo: Path, mode: str) -> None:
    result = subprocess.run(
        [NODE, str(HARNESS), str(demo), mode],
        capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    assert result.returncode == 0, (
        f"{demo.parent.parent.name} [{mode}] failed:\n"
        f"{result.stdout}\n{result.stderr}"
    )


def test_the_harness_is_in_the_repository() -> None:
    """It was a scratch-directory script once, which is how a broken demo shipped."""
    assert HARNESS.is_file(), f"missing {HARNESS.relative_to(ROOT)}"
    assert (HARNESS.parent / "demo_stub.js").is_file()
    assert _demos(), "no demo pages found — the glob is wrong or the demos moved"

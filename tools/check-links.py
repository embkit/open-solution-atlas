#!/usr/bin/env python3
"""check-links.py — verify Markdown links.

Two modes:

1. **Relative links (default, blocking)** — every inline link whose target is
   relative must resolve on disk. Exit 1 if any is broken.

2. **External links (`--check-external`, informational)** — probe every
   http(s) URL cited in the repo (SOURCES.md ledgers are the main consumer)
   with a HEAD request. Failures are printed but do NOT fail the run unless
   `--strict-external` is given, because citation sites (standards bodies,
   vendor docs) legitimately rate-limit bots and this project must not go red
   on someone else's maintenance window.

Usage:
    python tools/check-links.py
    python tools/check-links.py --check-external [--timeout 8] [--strict-external]
Exit:
    0 = relative links resolve (and, in strict mode, external probes pass);
    1 = broken relative link, or a failed external probe in --strict-external.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# [text](target) — non-greedy; images included (both checked)
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "tel:", "ftp://")

# Citation hosts that reject bot HEAD requests; probed but never failed in
# --strict-external mode. Keep small and justified.
EXTERNAL_ALLOWLIST = (
    "https://www.iso.org/",
    "https://www.rfc-editor.org/",
)


def _rel(path: Path) -> str:
    """Path relative to the repo root, or absolute if it lies outside (tests)."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def check_file(md: Path) -> list[str]:
    """Return broken *relative* links in one Markdown file."""
    problems: list[str] = []
    try:
        text = md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{md}: not UTF-8"]
    for match in LINK_RE.finditer(text):
        target = match.group(1)
        if target.startswith(SKIP_PREFIXES):
            continue
        if "://" in target:  # any other scheme (computer://, file:// …)
            continue
        path_part = target.split("#", 1)[0]
        if not path_part:
            continue
        resolved = (md.parent / path_part).resolve()
        if not resolved.exists():
            line = text.count("\n", 0, match.start()) + 1
            problems.append(f"{_rel(md)}:{line}: broken link -> {target}")
    return problems


def iter_markdown() -> list[Path]:
    return [
        md
        for md in sorted(ROOT.rglob("*.md"))
        if ".git" not in md.parts and "node_modules" not in md.parts
    ]


def collect_external_urls() -> dict[str, set[str]]:
    """Map external URL -> set of citing files (relative paths)."""
    urls: dict[str, set[str]] = {}
    for md in iter_markdown():
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = _rel(md)
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://")):
                urls.setdefault(target.split("#", 1)[0], set()).add(rel)
    return urls


def _probe(url: str, timeout: float) -> tuple[str, str | None]:
    """HEAD a URL. Returns (url, None) on success or (url, reason) on failure."""
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "open-solution-atlas-linkcheck/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if response.status >= 400:
                return url, f"HTTP {response.status}"
            return url, None
    except urllib.error.HTTPError as exc:
        # 405/403 mean "exists but refuses HEAD" — treat as reachable.
        if exc.code in (403, 405):
            return url, None
        return url, f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001 — network layer, report verbatim
        return url, type(exc).__name__


def check_external(timeout: float, strict: bool) -> list[str]:
    urls = collect_external_urls()
    if not urls:
        return []
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        futures = {pool.submit(_probe, url, timeout): url for url in urls}
        for future in as_completed(futures):
            url, reason = future.result()
            if reason is None:
                continue
            if any(url.startswith(prefix) for prefix in EXTERNAL_ALLOWLIST):
                print(f"[INFO] allowlisted (probe failed: {reason}) {url}")
                continue
            cited = ", ".join(sorted(urls.get(url, [])))
            failures.append(f"{url} -> {reason}  (cited by: {cited})")
    print(f"summary: probed {len(urls)} external URL(s), {len(failures)} unreachable")
    for failure in sorted(failures):
        print(f"[{'ERROR' if strict else 'WARN'}] {failure}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown link checker")
    parser.add_argument(
        "--check-external",
        action="store_true",
        help="also probe cited http(s) URLs (informational by default)",
    )
    parser.add_argument(
        "--strict-external",
        action="store_true",
        help="treat unreachable external URLs as failures (implies --check-external)",
    )
    parser.add_argument(
        "--timeout", type=float, default=10.0, help="per-request timeout in seconds"
    )
    args = parser.parse_args()

    problems: list[str] = []
    for md in iter_markdown():
        problems.extend(check_file(md))
    for problem in problems:
        print(f"[ERROR] {problem}")
    print(f"summary: {len(problems)} broken relative link(s)")

    exit_code = 1 if problems else 0

    if args.check_external or args.strict_external:
        failures = check_external(args.timeout, args.strict_external)
        if args.strict_external and failures:
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

"""Tests for tools/prompts.py — prompts assembled from the pack, not written.

The whole premise is that a prompt carries the pack's *content*: its rule
propositions, the ADR it rested on, the store-enforced constraints, and the
conditions under which the repository is honest about what it does not know. A
prompt that omits those gets an implementation that invents them, which is the
generic-system failure this catalog exists to avoid.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def entry(prompts, pack_index) -> dict:
    return next(
        p for p in pack_index.build_index()["packs"] if p["slug"] == "workflow-bpm"
    )


PACK_DIR = Path(__file__).resolve().parent.parent / "packs" / "horizontal" / "workflow-bpm"


# --------------------------------------------------------------------------- #
# Every template carries the honesty conditions
# --------------------------------------------------------------------------- #

def test_every_prompt_carries_the_repository_conditions(prompts, entry):
    """A prompt without them gets an implementation that invents them."""
    expected = [
        "verification: unverified",
        "no deployment evidence",
        "policy assumptions",
        "conformance",
    ]
    for name, text in (
        ("implement", prompts.implement(entry)),
        ("adr", prompts.adr(entry, "ADR-0004")),
        ("test", prompts.test(entry, "BR-05")),
        ("context", prompts.context_bundle(entry, PACK_DIR)),
    ):
        for phrase in expected:
            assert phrase in text, f"{name} prompt omits: {phrase}"


def test_implement_prompt_carries_the_packs_own_content(prompts, entry):
    text = prompts.implement(entry)
    assert "BR-05" in text and "ADR-0004" in text
    assert "FR-013" in text, "requirements are what the decisions force"
    assert "store-enforced" in text, "constraints must say how they are enforced"
    assert entry["counts"]["rules"] > 0


def test_implement_prompt_names_rule_propositions_not_just_ids(prompts, entry):
    """An ID alone tells a model nothing; the proposition is the content."""
    text = prompts.implement(entry)
    for rule in entry["rules"][:5]:
        assert rule["name"] in text
    assert "Participants resolve by role and business scope" in text


# --------------------------------------------------------------------------- #
# The ADR prompt is the one that most needs the rejected options
# --------------------------------------------------------------------------- #

def test_adr_prompt_lists_what_was_ruled_out(prompts, entry):
    """The winner alone lets a model re-derive the loser."""
    text = prompts.adr(entry, "ADR-0004")
    assert "Ruled out" in text
    assert "Leave the terms to the implementation" in text
    assert "Choose a vendor's definitions" in text


def test_adr_prompt_lists_what_depends_on_the_decision(prompts, entry):
    text = prompts.adr(entry, "ADR-0004")
    for req in ("FR-009", "FR-013", "FR-017"):
        assert req in text, f"{req} traces to ADR-0004 and must appear"


def test_unknown_adr_is_reported_not_fabricated(prompts, entry):
    text = prompts.adr(entry, "ADR-9999")
    assert "No such ADR" in text
    assert "ADR-0004" not in text, "must not substitute another decision"


def test_unknown_rule_is_reported_not_fabricated(prompts, entry):
    text = prompts.test(entry, "BR-9999")
    assert "No such rule" in text


# --------------------------------------------------------------------------- #
# The test prompt must include the SHALL NOT half
# --------------------------------------------------------------------------- #

def test_test_prompt_includes_the_prohibition(prompts, entry):
    """The `SHALL NOT` clause is the half that fails first in a real system."""
    text = prompts.test(entry, "BR-05")
    assert "SHALL NOT" in text
    assert "FR-013" in text, "the requirement that enforces it"


def test_test_prompt_names_the_measure(prompts, entry):
    text = prompts.test(entry, "BR-09")
    assert "NFR-009" in text or "formula" in text.lower()


# --------------------------------------------------------------------------- #
# The context bundle carries chapters and ADR files
# --------------------------------------------------------------------------- #

def test_context_bundle_carries_real_chapters(prompts, entry):
    text = prompts.context_bundle(entry, PACK_DIR)
    assert "AGENTS.md" in text
    assert "01-business/business-rules.md" in text
    assert "04-architecture/adr/" in text
    assert len(text) > 20000, "a summary this small would not be the source"


def test_context_bundle_omits_nothing_that_exists(prompts, entry):
    text = prompts.context_bundle(entry, PACK_DIR)
    for rel in ("README.md", "SOURCES.md", "05-data/data-dictionary.md"):
        assert rel in text, f"{rel} exists in the pack but is not in the bundle"


# --------------------------------------------------------------------------- #
# Emission: the file and the link must agree
# --------------------------------------------------------------------------- #

def test_bundle_filenames_are_not_double_prefixed(prompts):
    """`ADR-0004` already says its kind; `adr-adr-0004.md` says it twice."""
    assert prompts.bundle_filename("adr", "ADR-0004") == "adr-0004.md"
    assert prompts.bundle_filename("test", "BR-05") == "test-br-05.md"


def test_emitted_files_match_the_names_the_page_links_to(prompts, entry):
    bundles = prompts.build_bundles(entry, PACK_DIR)
    written = set(bundles["files"])
    for item in bundles["inline"]["adr"]:
        assert prompts.bundle_filename("adr", item["id"]) in written
    for item in bundles["inline"]["test"]:
        assert prompts.bundle_filename("test", item["id"]) in written
    assert "context.md" in written and "implement.md" in written


def test_prompts_are_json_free_of_nones(prompts, entry):
    """Nothing non-serialisable is written to a page or a file."""
    import json

    bundles = prompts.build_bundles(entry, PACK_DIR)
    json.dumps(bundles, ensure_ascii=False)

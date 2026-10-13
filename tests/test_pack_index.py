"""Tests for tools/pack_index.py — the structured extraction layer.

The extractor is the thing that turns 17 packs of prose into records a page,
a prompt bundle or a code generator can read. Two properties matter more than
any individual parse: it must accept **every** convention the corpus actually
uses (or it reports a pack as having zero rules when it has fifteen), and it
must report *why* it got nothing rather than silently returning an empty list.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# The real corpus: what the extractor must actually cope with
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="module")
def index(pack_index) -> dict:
    return pack_index.build_index()


def _pack(index: dict, slug: str) -> dict:
    return next(p for p in index["packs"] if p["slug"] == slug)


# --------------------------------------------------------------------------- #
# Identifier conventions
# --------------------------------------------------------------------------- #

def test_both_rule_conventions_are_parsed(index):
    """L2 writes `### BR-01 — …`; L3 writes `**BR-01 Name**`; ITSM writes a table.

    All three are in use across the corpus, and a pack with rules in an
    unrecognised shape must not come back as zero.
    """
    for slug in ("workflow-bpm", "iam-platform", "itsm-helpdesk"):
        rules = _pack(index, slug)["rules"]
        assert len(rules) >= 10, f"{slug}: only {len(rules)} rules extracted"
        assert all(r["id"].startswith("BR-") for r in rules)


def test_requirements_parse_in_both_conventions(index):
    for slug in ("workflow-bpm", "wms"):
        reqs = _pack(index, slug)["requirements"]
        assert len(reqs) >= 10, f"{slug}: only {len(reqs)} requirements extracted"
        assert all(r["id"].startswith("FR-") for r in reqs)


def test_sub_id_rules_are_not_dropped(index):
    """`BR-03a` is a sub-rule of `BR-03` in at least one pack."""
    ids = {r["id"] for r in _pack(index, "itsm-helpdesk")["rules"]}
    assert "BR-03" in ids
    assert any(i.startswith("BR-03a") for i in ids), "sub-ID silently dropped"


def test_capabilities_accept_a_bare_number_column(index):
    """Some packs label the ID column `**01**` rather than `**CAP-01**`."""
    for slug, expected in (("workflow-bpm", 10), ("omnichannel-commerce", 10)):
        caps = _pack(index, slug)["capabilities"]
        assert len(caps) == expected, f"{slug}: {len(caps)} capabilities"
        assert all(c["id"].startswith("CAP-") for c in caps), "ID not normalised"


def test_control_matrix_parses_in_both_layouts(index):
    """Five columns (L2) and four columns with a mixed trace column (L3)."""
    for slug in ("workflow-bpm", "iam-platform"):
        ctls = _pack(index, slug)["controls"]
        assert len(ctls) >= 4, f"{slug}: {len(ctls)} controls"
        assert all(c["requirements"] or c["rules"] for c in ctls), "no traces found"


# --------------------------------------------------------------------------- #
# EARS decomposition
# --------------------------------------------------------------------------- #

def test_shall_not_is_split_out_of_shall(pack_index):
    block = """### FR-001 — Stay in the core

- **WHEN** a variant is taken
- **THE SYSTEM SHALL** operate without it, and SHALL NOT require the variant (BR-11)
- Traces: CAP-01, BR-11, ADR-0006
"""
    out = pack_index.parse_requirements(block)
    assert len(out) == 1
    req = out[0]
    assert req["when"] == "a variant is taken"
    assert req["shall_not"] == "require the variant (BR-11)"
    # The prohibition must not appear in both fields.
    assert "SHALL NOT" not in req["shall"]
    assert "SHALL NOT" not in req["shall"]


def test_inline_ears_statement_is_decomposed(pack_index):
    line = "- **FR-001** WHEN a subject is created, THE SYSTEM SHALL enforce a proofing tier"
    out = pack_index.parse_requirements(line)
    assert out[0]["when"] == "a subject is created"
    assert "enforce a proofing tier" in out[0]["shall"]


def test_policy_marker_is_read_from_the_label(pack_index):
    """`(A)` sits on the label — `- **Target (A)**:` — not on its value."""
    text = """## NFR-001 — Some target
- **Target (A)**: ≤ 0.1% of routings fail.
- **Formula**: `a / b`.
"""
    out = pack_index.parse_nfrs(text)
    assert out[0]["is_policy"] is True
    assert "≤ 0.1%" in out[0]["target"]

    plain = pack_index.parse_nfrs("## NFR-001 — Invariant\n- **Target**: 100%.\n")
    assert plain[0]["is_policy"] is False


def test_nfr_table_form_is_parsed(pack_index):
    line = "| NFR-001 | Intake latency | Portal submit → ticket visible `≤ 2 s p95 (A)` |"
    out = pack_index.parse_nfrs(line)
    assert out[0]["id"] == "NFR-001"
    assert out[0]["name"] == "Intake latency"
    assert out[0]["is_policy"] is True


# --------------------------------------------------------------------------- #
# Identifiers must survive cleaning
# --------------------------------------------------------------------------- #

def test_clean_keeps_underscores_in_identifiers(pack_index):
    """`DEFINITION_VERSION.in_flight_treatment` must not lose its underscores."""
    text = "| 2 | `DEFINITION_VERSION.in_flight_treatment` is NOT NULL at publication | BR-03 |"
    out = pack_index.parse_constraints(text)
    assert "DEFINITION_VERSION.in_flight_treatment" in out[0]["text"]


# --------------------------------------------------------------------------- #
# Store enforcement is derived from a claim, including a wrapped one
# --------------------------------------------------------------------------- #

def test_store_enforcement_survives_a_line_wrap(pack_index):
    """The sentence is routinely wrapped mid-phrase by the source's width."""
    text = (
        "| 1 | a | BR-01 |\n| 2 | b | BR-02 |\n\n"
        "> Constraints 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12 and 13 are **enforced in the\n"
        "> store**, not in application code.\n"
    )
    out = pack_index.parse_constraints(text)
    assert [c["store"] for c in out] == [True, True]


def test_store_enforcement_is_absent_without_the_claim(pack_index):
    text = "| 1 | a | BR-01 |\n\nConstraints are listed above.\n"
    assert pack_index.parse_constraints(text)[0]["store"] is False


def test_store_flag_is_only_ever_derived_never_invented(index):
    total = sum(p["counts"]["constraints"] for p in index["packs"])
    store = sum(p["counts"]["store_constraints"] for p in index["packs"])
    assert 0 <= store <= total
    # No pack may claim more store-enforced constraints than it has.
    for p in index["packs"]:
        assert p["counts"]["store_constraints"] <= p["counts"]["constraints"]


# --------------------------------------------------------------------------- #
# Extraction quality: reported, never silently zero
# --------------------------------------------------------------------------- #

def test_unparsable_section_reports_prose_only_not_silent_zero(pack_index):
    """A file with IDs that cannot be decomposed must say so."""
    text = "## Some section\n\nRules like BR-01 and FR-002 are discussed here.\n"
    assert pack_index._status(0, text) == "prose-only"
    assert pack_index._status(0, "no identifiers here\n") == "absent"
    assert pack_index._status(3, text) == "structured"


def test_corpus_gaps_are_visible_in_the_index(index):
    """The packs without a constraint table must be reported, not papered over."""
    gaps = [p["slug"] for p in index["packs"] if p["counts"]["constraints"] == 0]
    assert gaps, "expected the L3 packs to lack a constraint table"
    assert all(
        p["sections"]["constraints"]["count"] == 0 for p in index["packs"] if p["slug"] in gaps
    )


def test_extraction_summary_adds_up_to_the_pack_count(index):
    for key, counts in index["extraction"]["sections"].items():
        assert sum(counts.values()) == index["pack_count"], key


# --------------------------------------------------------------------------- #
# Whole-corpus sanity
# --------------------------------------------------------------------------- #

def test_every_pack_yields_rules_and_requirements(index):
    for p in index["packs"]:
        assert p["counts"]["rules"] >= 10, f"{p['slug']}: {p['counts']['rules']} rules"
        assert p["counts"]["requirements"] >= 10, f"{p['slug']}: {p['counts']['requirements']} FR"
        assert p["counts"]["adrs"] >= 4, f"{p['slug']}: {p['counts']['adrs']} ADRs"


def test_urls_follow_the_site_layout(index):
    for p in index["packs"]:
        assert p["url"].endswith("/index.html")
        assert p["url"].startswith("packs/")
        for a in p["adrs"]:
            assert a["url"].endswith(".html")


def test_doc_url_matches_the_site_mapping(pack_index, build_site):
    """The content model and the renderer must never disagree on a URL."""
    root = Path(__file__).resolve().parent.parent
    for rel in (
        "packs/horizontal/workflow-bpm/README.md",
        "packs/horizontal/workflow-bpm/AGENTS.md",
        "packs/horizontal/workflow-bpm/01-business/business-rules.md",
    ):
        assert pack_index.doc_url(rel) == build_site.url_for(root / rel)


def test_index_is_json_serialisable(index):
    """Emitted verbatim, so a non-serialisable value would fail the build."""
    assert json.loads(json.dumps(index, ensure_ascii=False))["pack_count"] == index["pack_count"]

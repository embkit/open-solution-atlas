# AGENTS.md - Open Solution Atlas

## Project shape

Open Solution Atlas is a content-and-tooling repository, not a production
application. Its primary deliverables are vendor-neutral Solution Packs:
complete specifications for real industry systems, written for both human
readers and spec-driven coding agents. The repository also ships validators,
a pack registry, prompt generators, and a static GitHub Pages site.

English is the primary repository language; Simplified Chinese is a
first-class translation. Do not rewrite correct full-width Chinese punctuation
as ASCII.

## Source boundary

Only tracked repository content is project source. In particular:

- `packs/` - the 17 Solution Packs and all pack-level source material.
- `docs/` - normative pack standard, taxonomy, roadmap, site UI contract, and
  citation audit.
- `schemas/` - editor-facing manifest schema.
- `tools/` - Python validators/builders plus the registry site assets.
- `tests/` - tests for the Python tooling and generated site.
- `templates/` - reusable pack template and scaffolding instructions.
- `.github/` - CI, Pages, CodeQL, and contribution workflow configuration.
- Root `README*`, `CONTRIBUTING.md`, `CHANGELOG.md`, and license files.

The following top-level directories exist only as local ignored tooling or
build output; they are not Open Solution Atlas content and must not be edited
or committed as repository changes:

- `accessibility/`, `components/`, `content/`, `design-systems/`,
  `frameworks/`, `scripts/`, `taste/`, `tokens/`, `workflows/`, `.claude/`
- `_site/`, `_final2/`, `_v2/`, `_v3/`, `_v4/`, and every other `_*` directory
- `package.json`, `package-lock.json`, `node_modules/`

When source versus local-tool ambiguity matters, prefer `git ls-files` and
`.gitignore` over a raw filesystem listing.

## Load order

For any repository-wide task:

1. Read this file.
2. Read the relevant root entry point:
   - Pack content or trust rules: `README.md`, `docs/pack-standard.v1.md`
   - Contribution constraints: `CONTRIBUTING.md`
   - Taxonomy and collection scope: `docs/taxonomy.md`
   - Planned promotion work: `docs/roadmap.md`
   - Site behavior or UI rules: `docs/embkit-ui-contract.md`

For work inside `packs/<domain>/<slug>/`, read that pack's `AGENTS.md`
immediately after this file, then its `manifest.yaml`, `README.md`, and
`SOURCES.md`. Follow the pack's own chapter load order; do not substitute a
generic scan of the pack.

## Hard rules

- `maturity` and `verification` are independent. Maturity measures
  completeness; verification measures external evidence. Never imply one
  proves the other.
- New LLM-drafted content starts `provenance: llm-drafted` and
  `verification: unverified` with the required draft banner. An LLM may draft
  content but may never verify it.
- Stable IDs such as `FR-*`, `NFR-*`, `CTL-*`, `BR-*`, `AC-*`, `ADR-*`,
  `SM-*`, `CAP-*`, and `T-*` are immutable. Add IDs; never renumber them.
- Settled ADRs are constraints. If a requested change appears to reopen one,
  raise the conflict instead of silently reversing the decision.
- Mark unresolved facts explicitly as `> ASSUMPTION:` with the repository's
  established marker style.
- Keep the core vendor-neutral. A technology-specific position belongs in a
  clearly labeled `variants/` overlay.
- Never add confidential, client-derived, credential, or identifiable
  employer/customer material.
- Trace L2/L3 claims to public sources or evidence already recorded in the
  pack. Do not upgrade `verification` without the required evidence.

## Common commands

Run the relevant subset while editing; run the full sequence before declaring
repository-wide work complete.

```powershell
python tools/validate-packs.py
python tools/check-ids.py
python tools/check-links.py
python tools/build-site.py --site-url=
python -m pytest tests/ -q
ruff check .
```

CI parity details are in `.github/workflows/ci.yml`. Runtime dependencies are
pinned in `requirements.txt` and `requirements-dev.txt`; Node is used only by
the local browser verification tooling, not by the published site.

## Completion criteria

A change is complete when its content and generated behavior agree:

- Pack edits satisfy the applicable maturity checklist and trust-banner rules.
- Relative Markdown links resolve.
- Stable IDs referenced across chapters still resolve.
- The static site builds successfully.
- Tooling changes pass pytest and Ruff.
- Generated `_*` output is never committed.

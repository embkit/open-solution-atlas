# Maintainers

Open Solution Atlas uses a **domain-scoped maintainer** model: each taxonomy
domain (see [`docs/taxonomy.md`](docs/taxonomy.md)) is owned by people with
first-hand experience in that domain, so pack reviews are substantive rather
than editorial.

## Current state

| Role | Holder | Notes |
|---|---|---|
| Repository maintainer | [@ebk-slm](https://github.com/ebk-slm) | Owns the standard, tooling, CI, and release tagging. Sole maintainer today. |
| Domain maintainers | _none yet_ | Recruited from the practitioner review queue (see below). Each new appointment is what unlocks `practitioner-reviewed` verification for its domain. |

> This file records actual holders, not intentions. Until a domain maintainer
> accepts their role, the repository maintainer reviews that domain's PRs —
> which is a bottleneck, and the single highest-value contribution available
> right now is filling these rows.

## Roles

- **Repository maintainer** — `docs/pack-standard.v1.md`, `tools/`, CI,
  templates, release tagging. Merge rights on everything.
- **Domain maintainer** — review PRs under `packs/<domain>/**`; runs the
  practitioner-review process (`.github/ISSUE_TEMPLATE/practitioner-review.yml`)
  for that domain; may approve `practitioner-reviewed` promotions together
  with a named domain practitioner (standard §8.3 rule 4: authors may not
  self-approve).
- **Pack author** — anyone per [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Promotion authority (who may raise `verification`)

| Promotion | Who can do it | Machine gate |
|---|---|---|
| `unverified` → `source-checked` | any contributor + green CI | `tools/validate-packs.py` (ledger, evidence, banner) |
| → `practitioner-reviewed` | named practitioner(s) via issue template + domain maintainer merge | `verified_by` non-empty, entries complete |
| → `field-proven` | repository maintainer, with public reference implementation or describable deployment evidence | `deployment`/`case-study` evidence entry |

> **The verification ladder is empty above rung 2.** No pack in this library is
> `practitioner-reviewed` or `field-proven`, because both rungs require named
> humans and real deployments — work that no amount of tooling can substitute
> for. This is stated plainly rather than papered over.

## Becoming a domain maintainer

Open an issue: state your domain, your first-hand experience (generalized —
never employer-confidential), and the packs you are willing to review on an
ongoing basis. Two sustained substantive reviews is the bar we start from.

# Open Solution Atlas

<p align="center">
<i>Talk is cheap. Show me the code.</i> — Linus Torvalds, 2000<br/>
<b><i>Code is cheap. Show me the solution.</i></b>
</p>

<p align="center">
<b>Open, specification-grade blueprints for real-world software systems —
written for human architects and AI coding agents alike.</b><br/>
开放的、规格级的真实软件系统蓝图库 ·
<a href="./README.zh-CN.md">中文</a>
</p>

<p align="center">
<img alt="CI" src="https://github.com/embkit/open-solution-atlas/actions/workflows/ci.yml/badge.svg">
<img alt="License: CC BY-SA 4.0 + MIT" src="https://img.shields.io/badge/license-CC%20BY--SA%204.0%20%2B%20MIT-blue">
<img alt="Pack Standard" src="https://img.shields.io/badge/pack%20standard-v1.0%20draft-orange">
<img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen">
</p>

## Why this exists

Software engineering education is rich at the two ends of the spectrum:

- **Interview & scale tutorials** — design a URL shortener, a feed, a chat app
- **Runnable frameworks** — take a whole opinionated product and adapt it

What is missing in the open world is the middle that the industry actually runs
on: **the solution blueprint for a specific kind of business system** — a
factory's MES, a warehouse management system, a one-stop government service
portal, an enterprise BI stack. That knowledge today lives behind consulting
engagements, vendor whitepapers, and the private experience of individual
architects. It is scattered, unnamed, and almost never written down at a level
of completeness that allows the system to actually be built.

As coding agents absorb routine implementation, the binding constraint on
delivering serious systems shifts upward: from code to **specification**.
Open Solution Atlas is the open content layer for that shift — a library where
each system is documented completely enough to be handed to a spec-driven
development workflow and implemented.

## What a Solution Pack contains

Every pack describes **one system**, from business context to delivery tasks:

```
industry context & regulatory landscape
        │
business capabilities · processes · rules
        │
functional requirements (EARS) · NFRs · compliance controls
        │
domain model · state machines · glossary
        │
architecture & ADRs · data model · API contracts
        │
acceptance criteria · test & DR strategy
        │
milestones · agent-executable task map
```

Every requirement, decision, contract, and test carries a stable ID and traces
to its neighbors. Each pack ships an `AGENTS.md` entry point so coding agents
load it in the correct order. See the full standard in
[`docs/pack-standard.v1.md`](docs/pack-standard.v1.md).

### Maturity levels

| Level | Meaning |
|---|---|
| 🟡 **L1 Brief** | Context, capabilities, stakeholders, regulations |
| 🔵 **L2 Blueprint** | Requirements, domain, architecture, data, compliance |
| 🟢 **L3 Agent-ready** | Contracts, acceptance criteria, task map — buildable by a coding agent |
| ⚫ **L4 Proven** | Validated against a linked reference implementation |

Packs honestly declare their level. A maintained L1 is worth more than a
fabricated L3.

### Trust: two axes, never merged

Maturity measures **completeness**. It says nothing about **trustworthiness**.
Every pack therefore declares a second, independent field — `verification` —
that climbs only by acquiring external evidence
([standard §8](docs/pack-standard.v1.md)):

| Verification | Meaning |
|---|---|
| ⛔ `unverified` | No external evidence. Every specific claim is a hypothesis; a draft banner is mandatory. |
| 📑 `source-checked` | Every load-bearing claim traces to a public source in the pack's `SOURCES.md`; unsourced specifics are marked `⚠️ ASSUMPTION`. |
| 👤 `practitioner-reviewed` | Named domain practitioners reviewed the pack — recorded per-person in `verified_by`. |
| ✅ `field-proven` | Public reference implementation or describable deployment evidence (same bar as L4). |

All content is `provenance: llm-drafted` until proven otherwise, and **no
pack is validated in a real deployment yet**. This is enforced, not just
promised: CI runs [`tools/validate-packs.py`](tools/validate-packs.py) on
every PR — banner rules, ladder honesty, required chapters per level, and
relative-link integrity are machine-checked
([schema](schemas/pack-manifest.schema.json)). An LLM may not review another
LLM's pack into verified status.

## How this differs from existing projects

| | Interview repos (system-design-primer, system-design-101) | Cloud architecture centers | Open-source cores (Fineract etc.) | SDD tools (Spec Kit, BMAD, Kiro) | **Open Solution Atlas** |
|---|---|---|---|---|---|
| Real industry systems with compliance depth | ✗ | partial | one domain each | ✗ | **✓** |
| Vendor-neutral | ✓ | ✗ | ✓ | ✓ | **✓** |
| Complete buildable specification, not code | ✗ | ✗ | code, not specs | empty process | **✓ content** |
| Agent-native packaging (`AGENTS.md`, traceable IDs) | ✗ | ✗ | ✗ | tool only | **✓** |
| Open community library across every vertical | ✓ | ✗ | single product | ✗ | **✓** |

We are the **content layer** that SDD tools need and the **open counterpart**
of what consultancies and cloud vendors keep private.

## Browse online

A generated site renders the whole atlas with **full-text search and filters**
(search "FEFO", "OEE", "federated login" and land on the right chapter):

**https://embkit.github.io/open-solution-atlas/**

Build it locally with `python tools/build-site.py` (writes `_site/`; the build
fails if any internal link is broken). It publishes to GitHub Pages on every
push to `main`.

## Shelf map

The full taxonomy lives in [`docs/taxonomy.md`](docs/taxonomy.md):

- **horizontal** — IAM/SSO, CMS/blog, workflow & BPM/OA, ITSM service desk
- **manufacturing** — MES/MOM, WMS/TMS, ERP, quality/PLM
- **retail-commerce** — omnichannel commerce, marketplace, retail operations
- **government-public** — one-stop services, data exchange, smart city, tax
- **energy-utilities** — power marketing & CIS, grid operations IT, energy data
- **data-ai** — BI, warehouse/lakehouse, growth analytics, MLOps
- **telecom · healthcare**
- **finance** — currently non-bank scope only (insurance, generic fintech);
  banking systems are intentionally not collected for now

Current packs and their status: [`packs/`](./packs/).

## Use a pack

**As a human** — read it like the solution document an experienced delivery
team would wish they had received: business context first, architecture and
trade-offs second.

**With a coding agent** — an L3 pack plugs directly into spec-driven workflows:

```bash
# 1. copy or reference the pack
# 2. point your agent at the pack's AGENTS.md
# 3. let it expand the delivery task map into plan/tasks (Spec Kit, BMAD, Kiro…)
# 4. review at the human gates; the pack defines done via acceptance criteria
```

Compatibility notes per tool: [`docs/`](./docs/) (guides tracked on the
[roadmap](docs/roadmap.md)).

## Contribute

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) — it is short. The essential
bargain: contribute **generalized public knowledge**; never material that
identifies an employer or client. Cite public regulations and sources.
Vendor-neutral is the default; stack opinions live in labeled `variants/`.

A maintained L1 brief about a system you know deeply is a fantastic first PR.

## Governance

This project is honest about a current gap: it has **no named maintainers
yet**. [`MAINTAINERS.md`](MAINTAINERS.md) defines the roles and the promotion
authority for each verification rung; `.github/CODEOWNERS` is a placeholder
until real handles exist, and the security contact in
[`SECURITY.md`](SECURITY.md) is likewise pending publication. Recruiting
domain maintainers — the people who make `practitioner-reviewed` (rung 3)
possible — is the highest-value contribution right now; open a
[maintainer application](./.github/ISSUE_TEMPLATE/maintainer-application.yml)
if that is you.

## License

Content: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Code & templates: [MIT](https://opensource.org/license/mit).
See [`LICENSE`](./LICENSE).

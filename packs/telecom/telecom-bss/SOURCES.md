# SOURCES — Telecom BSS/OSS Suite

> Provenance ledger. Maps load-bearing claims to public, checkable sources.
> **Status: starter ledger — not yet complete to `source-checked`.**
> Provenance: `llm-drafted` · Verification: `unverified`. See
> [`docs/pack-standard.v1.md` §8](../../../docs/pack-standard.v1.md).

## 1. Standards & specifications

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| Component/capability decomposition of a digital telecom operator (BSS vs OSS boundary) | TM Forum | Open Digital Architecture (ODA) — https://www.tmforum.org/oda/ | Exact component list / release to confirm |
| Commercial product catalog model | TM Forum | TMF620 Product Catalog Management API — https://www.tmforum.org/open-apis/ | API version (e.g. v4) to confirm |
| Order capture / decomposition | TM Forum | TMF622 Product Ordering Management API | API version to confirm |
| Billing / invoices | TM Forum | TMF678 Customer Bill Management API | API version to confirm |
| Order-to-activation hand-off (OSS side) | TM Forum | TMF640 Service Activation Management API | API version to confirm |
| Business process vocabulary (order-to-cash) | TM Forum | Business Process Framework (eTOM) — https://www.tmforum.org/ | Mapping to pack capabilities to confirm |
| Telephone number inventory / numbering structure | ITU-T | Recommendation E.164 — https://www.itu.int/rec/T-REC-E.164/ | Number plan structure for number inventory |
| Subscriber personal data (privacy, retention, erasure) | EU | GDPR (EU 2016/679) — https://eur-lex.europa.eu/eli/reg/2016/679/oj | Per-data-class retention/erasure rules to map |
| ITU-T recommendations (general) | ITU | https://www.itu.int/ | Which recommendations bind this pack — to confirm |

## 2. Normative documents (RFC / official specs)

| Topic / claim | Source | Reference | Notes |
|---|---|---|---|
| TMF Open API family as the normative interface language | TM Forum | Open APIs — https://www.tmforum.org/open-apis/ | Which API families are normative in core is a pack decision |
| Provisioning / OSS integration protocols | — | to confirm | 3GPP/other OSS interface specs not yet identified |

## 3. Citable open-source implementations

| System / topic | Project | Link | Notes |
|---|---|---|---|
| Order / process orchestration engine | Camunda | https://camunda.com/ | BPMN engine; candidate for order orchestration boundary |
| Integration / routing | Apache Camel | https://camel.apache.org/ | Channel and mediation patterns |
| Identity for agent/subscriber portals (not BSS core) | Keycloak | https://www.keycloak.org/ | Boundary component only |

## 4. Uncited specifics to resolve

Resolved at L2 (pack design; still need external sourcing for source-checked):

- **BSS/OSS boundary** — ADR-0001 settles it as an integration contract with a
  declared five-aspect interface contract. Still open: the **contract itself**
  as payload shapes and state vocabulary (L3).
- **Two catalogs + specification** — ADR-0002 settles first-class + only
  permitted join. Still open: **specification currency** — a stale
  specification is worse than none because it is trusted.
- **CO/SO/RO traceability** — ADR-0003 settles both-direction links and
  explicit partial-failure cancellation. Still open: the **reverse link** is
  the one that decays in practice (NFR-002 measures it).
- **Charge events / two-way reconciliation** — ADR-0004 settles immutability and
  both directions. Still open: the **retention period** per class, in tension
  with personal-data obligations (deliberately unresolved).
- **Tariff rules** — BR-08 settles versioned + effective-dated + governed
  separately from billing code. Still open: **the tariff rule content itself**,
  deliberately not encoded (see industry-brief.md §11).
- **ODA / TMF vocabulary** — ADR-0005 settles adoption-not-conformance. Still
  open: **which edition**, deliberately unspecified.

Still open:

- **Disconnect guardrail classes** — the classes must exist as enforced state;
  which classes apply is a regulatory input.
- **估抄 method** — rule-bound and labelled is required; the method, period and
  reconciliation against the next actual reading are regulatory inputs.
- **Retention of rules, readings and approval records** — the tension with
  erasure is real; the window is a business decision.
- **Regulatory mapping** — 电力法, MLPS 2.0, GDPR remain **designations only**.
  No clause-level mapping exists, per this repository's scope decision
  (see docs/citation-audit-2026-10.md §4).
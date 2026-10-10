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

- **BSS/OSS boundary ownership** — whether provisioning orchestration lives in this pack or in a dedicated OSS pack. Design choice, no source.
- **TMF Open API conformance depth** — selecting TMF620/622/678/640 as normative (and their versions) is a pack decision, not a cited mandate; versions to confirm.
- **"Currency-agnostic money model"** — architecture assertion with no external source.
- **Resource/number inventory granularity** — logical-only vs physical (ports, cards, sites) is an open question; no source.
- **GDPR retention/erasure "per data class"** — no retention periods are stated; jurisdiction- and data-class-specific, to confirm.
- **ITU-T / 3GPP applicability** — the pack cites ITU-T generically but binds no specific recommendation; to confirm.
- **Rating/billing immutability & reconciliation** — engineering principle asserted in AGENTS.md, no citation.

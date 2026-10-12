# ADR-0006 — The share-type vocabulary is closed at three, and open data is a distinct regime

- Status: Accepted
- Date: 2026-10-12
- Deciders: pack maintainers

## Context

Two statements in `AGENTS.md` look like details and are structural.

The first: share types come from the 国发〔2016〕51号 办法's 第九条 — unconditional,
conditional, not-shareable. The vocabulary is **closed**, and the consequence of
treating it as open is specific. A fourth type — "restricted", "internal", "pending
review" — is a share type with no defined sharing behaviour. It has no rule about
whether it needs a grant, so the platform guesses, and the guess is usually
"treat it like conditional", which quietly converts the policy's default
("share, unless a legal basis says otherwise") into "withhold, unless somebody
negotiates".

The second: open-data metadata follows W3C DCAT, and the 一网通办 portal is a
**consumer via published interfaces**. The pack is the data substrate, not the
service front door. Conflating the two regimes is a control failure, because
publication basis and sharing grant answer different questions:

| | Sharing grant | Open-data publication |
|---|---|---|
| Question | may department X receive resource Y for purpose Z? | may anyone see this dataset? |
| Governing factors | purpose limitation, scope, duration | desensitisation bar, theme, publisher |
| Relationship | — | a dataset can be **not-shareable between departments and publishable publicly**, and the reverse |

Treating one as a subset of the other gets both directions wrong, and the failure is
invisible because both look like "the data went out".

## Options considered

1. **An extensible share-type list** — deployments add what they need, and the
   added types have no defined behaviour. The default inverts.
2. **A closed list of three, with deployment behaviour expressed as rules over the
   three** — the vocabulary stays aligned to the instrument, and deployment
   differences live in rules that are inspectable.
3. **Treat open-data publication as a consequence of being shareable** — simplest,
   and a not-shareable resource becomes unpublishable for no reason, and a
   shareable one becomes publishable without a basis.

## Decision

Option 2 plus, for the second statement, a **separate regime** — enforced by BR-13,
BR-14, FR-025, FR-026, and model constraints 8 and 11.

The share type is constrained to the three values (constraint 11's neighbour in the
data model), and open-data publication carries a **basis recorded separately from
the sharing grant** (FR-026).

## Consequences

- Positive: the policy's default is preserved structurally, because a share type
  that withholds by default cannot be introduced as a convenience.
- Positive: the two regimes cannot be conflated by construction, so a dataset's
  sharing status and its publication status are independently inspectable.
- Negative: a deployment that genuinely needs a fourth concept must express it as
> rules over the three rather than as a new type, which is more work and less
> obvious. The pack's position is that the obvious version is the one that inverts
> the default.
# 04 · Security

> ⚠️ ASSUMPTION — security posture is pack design. Instruments named in
> `02-requirements/compliance.md` are designations; no clause is cited.

## 1. The loop is the control surface, and it must close

The closed loop — authorization → approval → share → lineage — is not a reporting
property. It is the control surface: it is what makes every transfer attributable
to a decision somebody made.

Two things make it close, and the second is the one usually missing:

| | |
|---|---|
| **No transfer without a live, purpose-matching grant** | the forward direction; a grant that exists but does not match the purpose is not a grant for this transfer |
| **Every share walks back to its approval** | the reverse direction; a share that resolves to a grant but not to an approval is half-closed, and half-closed is how unattributable transfers appear |

> The failure is precise: a share trace that stops at the grant tells you *that*
> something was authorised and not *who authorised it or on what basis*. That is
> the difference between an auditable loop and a lawful-looking one.

## 2. Masking is a platform property, not a consumer obligation

Classification-derived masking is applied **by the platform before release**
(BR-04, FR-010). A consumer receives masked data, not raw data and a policy.

The reason is the same as in the sibling packs, and it is measurable: a
classification enforced in a consumer's tool is a classification for that consumer
only. A notebook, a data scientist and an export file are all consumers.

> NFR-005 counts consumer **paths** rather than tool configurations, because the
> failure is a path and not a setting.

## 3. The declared purpose must be structured, or it cannot be checked

第十四条 limits a consumer to the declared purpose. The engineering consequence is
structural rather than documentary: purpose is a **structured grant attribute**
that can be evaluated (FR-013, constraint 6).

> A free-text purpose satisfies the form of the requirement and none of its
> substance — "did the consumer stay within it?" is not an answerable question
> about a sentence. NFR-008 measures the structured share, because it is the field
> that turns an obligation into a capability.

## 4. Revocation is measured by what it removes

A grant is revocable, and revocation's value is the **lead time until access is
actually removed** (BR-07, FR-016, NFR-003).

The named target is access removal, not record-writing. A grant that is recorded
as revoked while the consumer can still read is a revocation in name only, and the
gap between the two is where the control actually lives.

> NFR-003's target is deliberately short because the failure it measures is not
> administrative delay — it is the window in which a revoked consumer still reads.

## 5. A refusal is a control, not a denial

A refusal records its basis (BR-03, FR-005), and a **not-shareable** classification
requires a recorded legal, regulatory, or CPC Central / State Council policy basis
(FR-006, constraint 2).

The engineering consequence is a **field**: the catalog entry must be able to store
and display that basis. A share-type dropdown without a source-and-basis field
cannot satisfy it, and an implementation that records only the type has
implemented the part of the requirement that is easiest.

## 6. Open data is a different regime, and conflating them is a control failure

Open-data publication is governed by different rules from inter-departmental
sharing: the metadata model (DCAT), the consent basis and the desensitisation bar
are all different.

The pack's position is that publication basis is a **different question** from
whether data may be shared, and the two must not be conflated — because a dataset
that is not-shareable between departments is sometimes publishable to the public,
and one that is shareable is sometimes not publishable. Treating one as a subset
of the other produces the wrong answer in both directions.

## 7. Audit evidence

| Artefact | Where it lives | What it answers |
|---|---|---|
| **Share trace** | lineage store | "who authorised this transfer, on what basis, and under which grant?" |
| **Grant with structured purpose** | authorization store | "was this consumer permitted for this purpose, and is that still live?" |
| **Revocation record + completion** | authorization store | "was access actually removed, and how long did it take?" |
| **Classification grade + derived rules** | classification store | "was this dataset controlled by a grade, or by a hand-granted exception?" |
| **Refusal with basis** | catalog store | "why was this refused, and was the refusal permitted?" |
| **Purpose-conformance report** | governance store | "did the consumer stay within the declared purpose?" |

> Each is answerable from the platform's own record. The purpose-conformance
> report is the one most often absent, because it requires the purpose to have
> been structured in the first place — which is why NFR-008 is measured before
> NFR-013.
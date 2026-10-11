# 00-context / Regulatory Landscape

> Every obligation below is stated at the level a reader can act on, with the
> instrument it comes from. Where an article-level mapping is not yet verified,
> it is marked as an open question instead of asserted — per the pack standard
> §5 ("cite or qualify"). This pack is `verification: unverified`; nothing here
> has been confirmed by a practitioner.

## 1. Instruments in scope

| Instrument | Jurisdiction | What it governs here |
|---|---|---|
| **《中华人民共和国电子签名法》** (2004-08-28 通过，2005-04-01 施行；2015-04-24、2019-04-23 两次修正) | CN | Legal effect of electronic signatures and data messages; conditions for a "reliable" signature; when third-party certification is required |
| **GB/T 22239-2019《网络安全等级保护基本要求》** | CN | Graded-protection (等保 / MLPS 2.0) baseline controls for the platform |
| **GB/T 9704-2012《党政机关公文格式》** (2012-06-29 发布，2012-07-01 实施，现行) | CN | Paper-era layout of official documents: paper, elements, pagination, specific formats |
| **GB/T 33476.1-2016《党政机关电子公文格式规范 第1部分：公文结构》** | CN | Electronic official-document structure — the more relevant standard for a digital 公文 flow |
| **ISO/IEC 27001:2022** | Global | ISMS control framework; audit, access control, logging obligations |
| **BPMN 2.0.2** (OMG) | Global (industry) | Notation and interchange for process models |
| **CMIS 1.1** (OASIS) | Global (industry) | Interoperability for the document repository |

> ⚠️ ASSUMPTION: GB/T 33476.1-2016 is included as a **candidate** standard for
> electronic 公文 structure. Its scope and clause numbering have not been
> verified against the standard text; confirm before any conformance claim
> (see `SOURCES.md` §4).

## 2. What the Electronic Signature Law actually requires

The statute is short and its operative conditions are precise. The requirements
a workflow platform must satisfy derive from them:

**Reliability of a signature** — a signature is "reliable" when all four
conditions hold: the signature-creation data is **exclusive** to the signer;
**controlled** by the signer at the time of signing; **any later alteration to
the signature is detectable**; and **any later alteration to the data message
is detectable** (《电子签名法》第十三条).

> Engineering consequence: the platform must be able to *detect* alteration of
> both the signature and the document. That is an integrity property of the
> stored artefact, not a UI feature.

**Legal effect** — a reliable electronic signature has the same legal effect
as a handwritten signature or seal (《电子签名法》第十四条). This is the
sentence that makes seal/signature integration a correctness requirement
rather than a convenience.

**Written form, original form, and retention** — data messages that can be
manifested in tangible form and retrieved at any time are deemed to satisfy
written-form requirements (第四条); and are deemed to satisfy **original-form**
(第五条) and **file-retention** (第六条) requirements when their integrity
from final formation is reliably assured, and sender/recipient/time are
identifiable.

> Engineering consequence: **retrievability and identifiability are legal
> requirements**, not backup policy. "We can restore it from a snapshot" does
> not satisfy "identify the sender, recipient and time".

**Documents excluded from electronic form** — certain instruments (e.g.
marriage/adoption/inheritance-related matters, and other cases prescribed by
law or regulation) may not use electronic documents (第三条). The platform
should not silently offer an electronic path for those.

> ⚠️ ASSUMPTION: article numbers above are quoted from widely reproduced
> official text of the law as amended 2019-04-23. Re-verify against the
> authoritative text before relying on them in a compliance argument.

## 3. What would make this pack `source-checked`

Per pack-standard §8.2, `source-checked` requires every load-bearing claim to
trace to a public source with **no uncited specifics**. The remaining gaps,
in the order they block that promotion:

1. **Article-level mapping** of every obligation above to the authoritative
   statute text (the article numbers are stated but not yet re-verified
   against the official source).
2. **Signature standard** for 电子签章 — the cryptographic/format standard a
   CN e-seal integration is expected to implement. The pack currently names
   none (an earlier draft mentioned a candidate GB/T number; it was removed
   because it was unverified).
3. **GB/T 33476.1-2016 scope and clauses** — confirm what it mandates versus
   recommends.
4. **等保 level mapping** — which GB/T 22239-2019 control set applies at which
   grading level for this system, and who assigns the level.

Until those close, `verification` stays `unverified` and this file's claims
should be read as *framing*, not as compliance advice.

## 4. Regional profiles

This platform is deployed in materially different regimes. The pack keeps the
**core** vendor- and jurisdiction-neutral and puts the specifics here:

| Profile | Distinguishing obligations |
|---|---|
| **CN government / 政务** | 等保 grading; 公文 format & 文号 discipline; 电子签章 with statutory legal effect; archive & retention duties |
| **CN enterprise** | 等保 grading (typically self-assessed); 电子签名法 applies where documents are signed; contractual records |
| **EU / GDPR environments** | data-subject rights, retention limits, processor obligations, records of processing |
| **Other jurisdictions** | to be profiled if a pack is requested |

> The pack does not claim to be a compliance document. A deployment must have
> its obligations determined by a qualified party for its own jurisdiction and
> grading.

# 01-business / Processes

> Process definitions for the one-stop government service platform. Each names its
> trigger, its steps, and the rules that constrain its steps. Rules live in
> `business-rules.md` (BR-xx) and are referenced, never restated.
>
> ⚠️ ASSUMPTION — process decomposition is pack design. 国令第716号 supplies the
> statutory lifecycle vocabulary; it does not supply these processes.

## P-01 — Publish the item

| | |
|---|---|
| **Trigger** | a 事项 is created or revised |
| **Outcome** | a published **事项** — the catalog root |

1. Create the 事项 with its kind: 行政权力事项 or 公共服务事项 (BR-01).
2. Declare the guide's three required elements: 受理条件, 办事材料, 办理流程
   (BR-02).
3. Publish; the guide **is** the public contract (BR-02).

> BR-02: 第六条 makes the three elements mandatory and the guide published. An
> applicant is entitled to rely on what is published, so a guide that changes
> silently is unlawful, not merely inconsistent.

## P-02 — Find & authenticate

| | |
|---|---|
| **Trigger** | an applicant arrives at any channel |
| **Outcome** | an authenticated applicant, identified once |

1. Search the catalogue and read the published guide.
2. Authenticate through the **national unified identity** service — once, and the
   platform holds no competing citizen identity (BR-03).
3. Record the channel, which is a variant and never a fork (BR-04).

> BR-03: 第五条's 一次认证、全网通办 means integrating the national service.
> Re-implementing citizen identity would create a second identity to reconcile,
> and a second one to breach.

## P-03 — Pre-fill & verify

| | |
|---|---|
| **Trigger** | a form is presented |
| **Outcome** | fields that are not demanded where sharing could supply them |

1. Classify every field as **obtainable by sharing** or not (BR-05).
2. Pre-fill and verify from shared data where obtainable.
3. A field obtainable by sharing must not be a **required** input (BR-05).
4. A lookup failure **degrades to a permitted alternative**, never to silently
   re-asking the applicant (BR-05).

> BR-05 is 第七条, and it is the pack's defining constraint. Requiring a document
> is easy; proving it is already available is hard. A platform that defaults to
> asking will look friendlier and be non-compliant.

## P-04 — Submit

| | |
|---|---|
| **Trigger** | the applicant confirms |
| **Outcome** | a 办件, tracked |

1. Collect forms, materials and consent statements.
2. Create the 办件 with its state machine entry (BR-06).
3. Open the first statutory step.

## P-05 — Accept or tell once

| | |
|---|---|
| **Trigger** | a submitted 办件 is reviewed for acceptance |
| **Outcome** | **受理**, or a **一次性告知** listing everything missing, once |

1. If complete, 受理 — which starts the clock and the statutory duties.
2. If incomplete, give 一次性告知: the complete list, once (BR-07).
3. Where a rework is needed after acceptance, that is 补正 — a different step
   from 一次性告知 (BR-07).

> BR-07: the two terms are distinguished because they are different steps, and
> conflating them is how a platform ends up rejecting piecemeal.

## P-06 — Review & decide

| | |
|---|---|
| **Trigger** | an accepted 办件 |
| **Outcome** | a **决定** within 限时办结 |

1. 审查, including any cross-department data call, **consented and audited**
   (BR-08).
2. 决定: approve, refuse, or another disposition defined by the 事项 (BR-06).
3. The clock starts at 受理, not at submission (BR-09).

> BR-08: every cross-department call needs consent plus audit. A call with no
> recorded basis is both a compliance defect and evidence that the platform is
> over-collecting.

## P-07 — Issue, sign & settle

| | |
|---|---|
| **Trigger** | a decision |
| **Outcome** | the result issued, sealed where applicable, fees settled |

1. 出件 — issue the result to the applicant.
2. Apply an electronic seal **through the national unified system** (BR-10).
3. Produce an electronic licence where the result is a 证照, **via the national
   sharing service** (BR-10).
4. Settle administrative fees where the 事项 has them.

> BR-10: these are external platform dependencies, integrated through their
> published standards. Re-implementing a seal or an identity is both non-compliant
> and a security liability.

## P-08 — Rate, archive

| | |
|---|---|
| **Trigger** | a completed 办件 |
| **Outcome** | feedback collected; the electronic file archived |

1. 好差评 — collect the applicant's evaluation.
2. Archive the electronic file **in electronic form** (BR-11).
3. Retain per class (BR-12).

> BR-11: 第十二条 makes electronic archiving the obligation. The platform's data
> model is the archival object, not the department's filing system.

## Rule coverage

| Rule | Processes |
|---|---|
| BR-01 two statutory item kinds | P-01 |
| BR-02 guide is published contract | P-01 |
| BR-03 identity via national service | P-02 |
| BR-04 channels are variants | P-02, P-04 |
| BR-05 anti-double-submission | P-03 |
| BR-06 statutory lifecycle vocabulary | P-04, P-06 |
| BR-07 一次性告知 ≠ 补正 | P-05 |
| BR-08 cross-department calls consented+audited | P-06 |
| BR-09 clock starts at 受理 | P-06 |
| BR-10 seal/licence via national services | P-07 |
| BR-11 electronic archive | P-08 |
| BR-12 retention per class | P-08 |
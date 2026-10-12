# 04 · Integration

> Integration contracts with external services and channels. IDs are stable;
> every flow traces to requirements and rules.
>
> ⚠️ ASSUMPTION — interface selection and protocols are pack design. TM Forum and
> e-licence GB/T 369xx interfaces are consumed as published standards; no API
> version is claimed.

## I. Integration points

| ID | Partner | Direction | Purpose |
|---|---|---|---|
| **I-01** | **National unified identity service** | inbound | 一次认证、全网通办 — the only authentication path |
| **I-02** | **Government data sharing platform** (`data-exchange`) | inbound | the shared data that 第七条 requires the platform to stop asking for |
| **I-03** | **National unified electronic seal system** | outbound | seal application, and a **status query service** the platform consumes |
| **I-04** | **National electronic licence sharing service** | both | licence production and mutual recognition, via published interfaces |
| **I-05** | **Departmental back-office systems** | inbound | approval decisions and status |
| **I-06** | **Payment / treasury** | outbound | administrative fee settlement |
| **I-07** | **Archive management system** | outbound | electronic files and records |
| **I-08** | **Notification gateway** | outbound | progress, 补正 notice, result |
| **I-09** | **好差评 feedback channels** | inbound | ratings and responses |
| **I-10** | **Machine-translation / accessibility services** | outbound | assistive rendering for channels |

## F. Internal flows

### F-01 — Publish the item
1. The item is created with its statutory kind.
2. The guide declares 受理条件, 办事材料, 办理流程 — all three.
3. The guide is published and versioned; changes are dated and attributed.

### F-02 — Authenticate and pre-fill
1. The applicant authenticates through the national service, once.
2. Every form field is resolved against its sharing classification.
3. Obtainable fields are pre-filled or verified, never asked.
4. A failed lookup resolves to a defined permitted alternative.

### F-03 — Submit, accept, decide
1. The application is created and the clock logic is armed but **not started**.
2. 受理 starts the clock and the statutory duties.
3. Incompleteness produces 一次性告知, once and completely.
4. 审查 uses cross-department calls, each consented and audited.
5. 决定 is recorded with its authority and basis.

### F-04 — Issue, seal, settle, archive
1. 出件 delivers the result.
2. A seal is applied through the national system, with validity recorded at
   signing; the status query service is consulted where a validity check is
   required.
3. A licence is produced through the national sharing service where applicable.
4. Fees settle where the item has them.
5. The electronic file is archived and verified complete and retrievable.

### F-05 — Rate
1. The applicant's rating is recorded.
2. A response is recorded where one is given.

## Failure-mode contract

| Integration | Failure mode required |
|---|---|
| **I-01 identity** | an unavailable identity context means **no session**, not a guest session. A guest path is how the platform acquires a citizen identity it should not hold |
| **I-02 sharing platform** | a failed lookup resolves to a **defined permitted alternative** (FR-013) — never to re-asking, and never to a silently empty field. An empty pre-filled field is a demand the applicant cannot see |
| **I-03 seal system** | a failed seal application **blocks** issuance rather than producing an unsealed "issued" document. A result issued without its seal is a document whose legal status is a rendering |
| **I-04 licence service** | a failed licence production blocks the result; a locally defined format is not a fallback (FR-026) |
| **I-05 back-office** | an unavailable back-office leaves the step *unknown*, never auto-approved. Auto-approval on timeout is permitted only by explicit policy, never as a default |
| **I-07 archive** | an archive failure leaves the file retained per class and **recorded**, not silently dropped (FR-028) |
| **I-08 notification** | a failed notice degrades notification, never the statutory step. The 补正 obligation is unaffected by delivery failure |

> The pattern: integration unavailability degrades the external path and is
> recorded as *unknown* — never assumed, never defaulted. Identity, seal and
> licence are the three fail-closed cases, because each of them is a service whose
> re-implementation would create a second thing to secure and reconcile.

## The channel contract (what a channel must declare)

| Aspect | Declared by the channel |
|---|---|
| **Input** | how an application arrives (web session, mini-program, POS device, assisted) |
| **Payment path** | hosted fields available? which POS or marketplace path? |
| **Identity handling** | the national service, once — a channel that authenticates independently is not a variant |
| **Fulfilment sources** | which departments and back-office systems it reaches |
| **Presentation** | which channel-variant attributes to expose |

> An adapter that cannot declare all five is not a variant; it is a fork, and BR-04
> rejects it. The identity aspect is the one that fails hardest: a channel that
> authenticates locally has acquired a citizen identity, which is precisely what
> `AGENTS.md` forbids.